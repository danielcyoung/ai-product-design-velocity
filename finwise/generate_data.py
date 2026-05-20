"""
Generates synthetic FinWise product data.
Run once: python3 generate_data.py
Embedded signals:
  H1 — Goal Activation Gap:   no goals_set → 3.4x churn vs goal setters
  H2 — Notification Fatigue:  open rate drops 41% → 18% over 12 months; near-churn users go silent
  H3 — Week-2 Habit Break:    sessions drop steeply days 7-21 for non-activated accounts
"""
import csv, os, random
from datetime import datetime, timedelta

random.seed(42)

SNAPSHOT_DATE = datetime(2026, 3, 1)
N_ACCOUNTS    = 1800
OUT_DIR       = "data"
os.makedirs(OUT_DIR, exist_ok=True)

# ---- Dimensions ----
PLAN_TIERS = ['free', 'pro']
PLAN_W     = [0.62, 0.38]
PLAN_PRICE = {'free': 0.0, 'pro': 9.99}

SEGMENTS = ['anxious_tracker', 'budget_focused', 'savings_motivated', 'mint_refugee', 'new_to_tracking']
SEG_W    = [0.30, 0.25, 0.18, 0.08, 0.19]

PLATFORMS = ['ios', 'android']
PLAT_W    = [0.58, 0.42]

CHANNELS = ['organic', 'paid_social', 'referral', 'mint_refugee', 'other']
CHAN_W   = [0.34, 0.24, 0.20, 0.08, 0.14]

FEATURES  = ['transaction_view','analysis_view','savings_goal','budget_setup',
             'bill_tracking','category_edit','manual_transaction','notification_settings']
FEATURE_W = [0.32, 0.18, 0.10, 0.08, 0.12, 0.06, 0.08, 0.06]
GATED_PRO = {'savings_goal', 'bill_tracking', 'budget_setup'}

TICKET_CATS = ['categorisation','account_sync','billing','feature_request','other']
TICKET_W    = [0.40, 0.20, 0.15, 0.15, 0.10]

ONBOARDING_STEPS = [
    'link_first_account',
    'complete_profile_setup',
    'view_first_spending_summary',
    'link_second_account',
    'set_first_goal',
    'customise_first_category',
]

LAST_NAMES = ['chen','smith','johnson','williams','brown','garcia','miller',
              'davis','wilson','taylor','anderson','thomas','jackson','white',
              'harris','martin','rodriguez','moore','young','allen','walker',
              'hall','lewis','robinson','clark','lee','king','wright','scott',
              'green','baker','adams','nelson','carter','evans','murphy']

def wc(items, weights=None): return random.choices(items, weights)[0]
def clamp(v, lo, hi): return max(lo, min(hi, v))

# ---- Risk groups ----
# Churn and upgrade outcomes are controlled by which group an account falls into.
# This embeds the H1 signal cleanly: goal setters churn at ~3.4x lower rate.
#
#   goal_activated:  goals_set >= 1  +  accounts_linked >= 2  →  6% of all accounts
#   goal_only:       goals_set >= 1  +  accounts_linked = 1   →  6%
#   multi_account:   goals_set = 0   +  accounts_linked >= 2  →  25%
#   single_no_goal:  goals_set = 0   +  accounts_linked = 1   →  63%

GROUPS   = ['goal_activated','goal_only','multi_account','single_no_goal']
GROUP_W  = [0.06, 0.06, 0.25, 0.63]
GROUP_CHURN = {
    'goal_activated': 0.06,
    'goal_only':      0.14,
    'multi_account':  0.22,
    'single_no_goal': 0.42,
}
# Upgrade probability for free-tier accounts only.
# Goal creation is the #1 conversion trigger: hitting the 1-goal free limit.
GROUP_UPGRADE = {
    'goal_activated': 0.28,
    'goal_only':      0.34,   # hit the 1-goal limit → strongest trigger
    'multi_account':  0.05,
    'single_no_goal': 0.01,
}

# --------------------------------------------------
# 1. Accounts
# --------------------------------------------------
print("Generating accounts...")
accounts = []
for i in range(N_ACCOUNTS):
    plan     = wc(PLAN_TIERS, PLAN_W)
    segment  = wc(SEGMENTS, SEG_W)
    platform = wc(PLATFORMS, PLAT_W)
    channel  = wc(CHANNELS, CHAN_W)
    if channel == 'mint_refugee':
        segment = 'mint_refugee'

    age_days = random.randint(14, 730)
    group    = wc(GROUPS, GROUP_W)

    if group == 'goal_activated':
        goals_set       = random.randint(1, 4)
        accounts_linked = random.randint(2, 4)
    elif group == 'goal_only':
        goals_set       = random.randint(1, 3)
        accounts_linked = 1
    elif group == 'multi_account':
        goals_set       = 0
        accounts_linked = random.randint(2, 4)
    else:
        goals_set       = 0
        accounts_linked = 1

    churn   = random.random() < GROUP_CHURN[group]
    upgrade = (plan == 'free') and (random.random() < GROUP_UPGRADE[group])
    # Mint refugees: slightly higher Pro conversion due to category familiarity
    if segment == 'mint_refugee' and plan == 'free':
        upgrade = upgrade or (random.random() < 0.09)

    accounts.append({
        'account_id':          f"fw_acc_{i:05d}",
        'plan_tier':           plan,
        'user_segment':        segment,
        'platform':            platform,
        'acquisition_channel': channel,
        'accounts_linked':     accounts_linked,
        'goals_set':           goals_set,
        'account_age_days':    age_days,
        'monthly_revenue':     PLAN_PRICE[plan],
        'churned_90d':         churn,
        'upgraded_90d':        upgrade,
        '_group':              group,   # internal — stripped before write
    })

FIELDS_ACCOUNTS = ['account_id','plan_tier','user_segment','platform','acquisition_channel',
                   'accounts_linked','goals_set','account_age_days','monthly_revenue',
                   'churned_90d','upgraded_90d']
with open(f"{OUT_DIR}/finwise_accounts.csv", 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS_ACCOUNTS)
    w.writeheader()
    for a in accounts:
        w.writerow({k: a[k] for k in FIELDS_ACCOUNTS})
print(f"  Accounts: {len(accounts)}")

# --------------------------------------------------
# 2. Users — one primary user per account
# --------------------------------------------------
print("Generating users...")
users = []
for a in accounts:
    days_inactive = random.randint(0, 90)
    if a['churned_90d']:
        days_inactive = random.randint(30, 90)
    users.append({
        'user_id':                f"fw_usr_{len(users):07d}",
        'account_id':             a['account_id'],
        'role':                   'primary',
        'country':                'US',
        'platform':               a['platform'],
        'days_since_last_active': days_inactive,
    })

with open(f"{OUT_DIR}/finwise_users.csv", 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['user_id','account_id','role','country','platform','days_since_last_active'])
    w.writeheader()
    w.writerows(users)
print(f"  Users: {len(users)}")

# --------------------------------------------------
# 3. Monthly snapshots
# Notification open rate signal: starts at 41%, declines ~2.5pp/month (H2).
# Single-no-goal accounts show steeper session decay (H3 week-2 break).
# --------------------------------------------------
print("Generating monthly snapshots...")
acc_user = {u['account_id']: u['user_id'] for u in users}

def session_count(group, is_churned, month_idx):
    base = {'goal_activated': 12, 'goal_only': 9, 'multi_account': 7, 'single_no_goal': 4}[group]
    base = random.gauss(base, base * 0.35)
    decay = max(0.35, 1.0 - month_idx * 0.06)
    # Non-activated accounts drop hard after month 1 (week-2 break signal)
    if group == 'single_no_goal' and month_idx >= 1:
        decay *= max(0.18, 1.0 - month_idx * 0.20)
    if is_churned and month_idx >= 2:
        decay *= 0.22
    return clamp(int(base * decay), 0, 60)

snapshots = []
for a in accounts:
    group    = a['_group']
    is_churn = a['churned_90d']
    n_months = min(12, max(1, a['account_age_days'] // 30))

    for m_idx in range(n_months):
        month_date  = (SNAPSHOT_DATE - timedelta(days=30 * (n_months - m_idx))).replace(day=1)
        sessions    = session_count(group, is_churn, m_idx)
        active_days = clamp(int(sessions * random.gauss(1.9, 0.5)), 0, 28)

        # Notification signal: declining open rate over account lifetime
        notif_sent  = clamp(int(sessions * 1.4), 0, 30)
        open_rate   = max(0.13, 0.41 - m_idx * 0.025)
        if group == 'single_no_goal':
            open_rate *= 0.72
        if is_churn and m_idx >= n_months - 2:
            open_rate *= 0.22   # near-churned users go almost silent
        notif_opened = clamp(int(notif_sent * open_rate), 0, notif_sent)

        # Transaction categorisation: disengaged users accumulate uncategorised
        trans_total = clamp(int(random.gauss(45, 15)), 10, 120)
        unc_rate    = random.uniform(0.18, 0.34) if group == 'single_no_goal' else random.uniform(0.04, 0.14)
        trans_unc   = clamp(int(trans_total * unc_rate), 0, trans_total)

        n_tickets = 1 if random.random() < (0.08 if group == 'single_no_goal' else 0.03) else 0

        snapshots.append({
            'account_id':                 a['account_id'],
            'month':                      month_date.strftime('%Y-%m-%d'),
            'active_days':                active_days,
            'sessions':                   sessions,
            'goals_active':               a['goals_set'],
            'transactions_categorised':   trans_total - trans_unc,
            'transactions_uncategorised': trans_unc,
            'notifications_sent':         notif_sent,
            'notifications_opened':       notif_opened,
            'support_tickets':            n_tickets,
            'support_ticket_category':    wc(TICKET_CATS, TICKET_W) if n_tickets else 'none',
        })

FIELDS_SNAP = ['account_id','month','active_days','sessions','goals_active',
               'transactions_categorised','transactions_uncategorised',
               'notifications_sent','notifications_opened',
               'support_tickets','support_ticket_category']
with open(f"{OUT_DIR}/finwise_monthly_snapshots.csv", 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS_SNAP)
    w.writeheader()
    w.writerows(snapshots)
print(f"  Monthly snapshots: {len(snapshots)}")

# --------------------------------------------------
# 4. Feature events
# --------------------------------------------------
print("Generating feature events...")
events = []
ectr = 0

for a in accounts:
    group    = a['_group']
    is_churn = a['churned_90d']
    plan     = a['plan_tier']
    u_id     = acc_user[a['account_id']]
    t0       = SNAPSHOT_DATE - timedelta(days=a['account_age_days'])

    n_base   = {'goal_activated': 140, 'goal_only': 100, 'multi_account': 65, 'single_no_goal': 28}[group]
    n_events = clamp(int(random.gauss(n_base, n_base * 0.3)), 2, n_base * 3)
    if is_churn:
        n_events = clamp(int(n_events * 0.42), 2, n_events)

    for _ in range(n_events):
        feat = wc(FEATURES, FEATURE_W)

        if feat in GATED_PRO and plan == 'free':
            etype = 'blocked'
        elif feat == 'analysis_view':
            # 55% exit within 20 seconds modelled as abandoned
            etype = 'abandoned' if random.random() < 0.55 else 'used'
        elif feat == 'savings_goal' and a['goals_set'] == 0 and plan == 'pro':
            # Pro users who never set a goal: high abandonment on goal setup screen
            etype = 'abandoned' if random.random() < 0.62 else 'used'
        elif feat == 'manual_transaction':
            etype = 'abandoned' if random.random() < 0.39 else 'used'
        else:
            etype = 'used'

        days_off = random.randint(0, a['account_age_days'])
        if is_churn:
            days_off = min(days_off, int(a['account_age_days'] * 0.65))
        ts = t0 + timedelta(days=days_off, hours=random.randint(7, 22), minutes=random.randint(0, 59))

        events.append({
            'event_id':     f"fw_evt_{ectr:08d}",
            'user_id':      u_id,
            'account_id':   a['account_id'],
            'feature_name': feat,
            'event_type':   etype,
            'timestamp':    ts.strftime('%Y-%m-%d %H:%M:%S'),
        })
        ectr += 1

with open(f"{OUT_DIR}/finwise_feature_events.csv", 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['event_id','user_id','account_id','feature_name','event_type','timestamp'])
    w.writeheader()
    w.writerows(events)
print(f"  Feature events: {len(events)}")

# --------------------------------------------------
# 5. Onboarding
# set_first_goal completion = 12% — the key H1 signal.
# --------------------------------------------------
print("Generating onboarding...")
STEP_RATES = {
    'link_first_account':          0.84,
    'complete_profile_setup':      0.91,
    'view_first_spending_summary': 0.61,
    'link_second_account':         0.32,
    'set_first_goal':              0.12,   # THE signal
    'customise_first_category':    0.14,
}

onboarding = []
for a in accounts:
    group   = a['_group']
    t0      = SNAPSHOT_DATE - timedelta(days=a['account_age_days'])
    overrides = {}
    if group in ('goal_activated', 'goal_only'):
        overrides['set_first_goal']      = 1.0
        overrides['link_second_account'] = 0.88 if group == 'goal_activated' else 0.20
    elif group == 'multi_account':
        overrides['link_second_account'] = 0.95

    days_elapsed = 0
    for step in ONBOARDING_STEPS:
        rate = overrides.get(step, STEP_RATES[step])
        if a['churned_90d'] and step not in ('link_first_account', 'complete_profile_setup'):
            rate *= 0.55
        completed    = random.random() < rate
        completed_at = ''
        if completed:
            days_elapsed += random.randint(0, 5)
            completed_at  = (t0 + timedelta(days=days_elapsed)).strftime('%Y-%m-%d')
        onboarding.append({
            'account_id':   a['account_id'],
            'step_name':    step,
            'completed':    completed,
            'completed_at': completed_at,
        })

with open(f"{OUT_DIR}/finwise_onboarding.csv", 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['account_id','step_name','completed','completed_at'])
    w.writeheader()
    w.writerows(onboarding)
print(f"  Onboarding rows: {len(onboarding)}")

# --------------------------------------------------
# Summary
# --------------------------------------------------
n_churn   = sum(1 for a in accounts if a['churned_90d'])
n_upgrade = sum(1 for a in accounts if a['upgraded_90d'])
n_goals   = sum(1 for a in accounts if a['goals_set'] > 0)
print(f"\nDone.")
print(f"  Churned 90d:  {n_churn} ({n_churn / N_ACCOUNTS * 100:.1f}%)")
print(f"  Upgraded 90d: {n_upgrade}")
print(f"  Goal setters: {n_goals} ({n_goals / N_ACCOUNTS * 100:.1f}%)")
