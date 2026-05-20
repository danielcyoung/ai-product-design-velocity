# EIM Context Base — FinWise
*Generated: 2026-05-20*
*Sources: finwise/data/, finwise-product-context.md, finwise-intro.md, finwise-data-dictionary.md*

---

## What the Product Does
FinWise is a US-based personal finance app that helps everyday Americans track spending, set savings goals, and understand where their money actually goes. The core job-to-be-done is to reduce the cognitive load and shame of managing money. The ideal outcome is a user who opens the app each week, understands their financial situation in under two minutes, and makes at least one intentional decision.

## User and Account Types
- **Primary User**: Americans aged 25–40, earning $45K–$120K/year. Financially anxious but not bad at money, just overwhelmed.
- **Mint Refugee Cohort**: ~30,000 users acquired after Mint shut down in March 2024. More experienced, higher session frequency, higher conversion to Pro, but also higher churn in months 4–6 due to unmet expectations around investment account tracking and shared household features.
- **Segments**: `anxious_tracker`, `budget_focused`, `savings_motivated`, `mint_refugee`, `new_to_tracking`.

## Pricing and Plan Structure
- **Free**: $0/month. Unlimited account linking, analysis view, max 1 savings goal.
- **Pro**: $9.99/month. Unlimited savings goals, budget automation, bill tracking.
- **Key Gate**: Attempting to create a second savings goal (primary Pro upgrade trigger).

## What Healthy Usage Looks Like
A retained Pro subscriber at month 3+ typically has:
- At least one active savings goal created within the first 14 days.
- Two or more financial accounts linked.
- Opening the app 3+ times per week in the first month.
- Notifications engaged with at least once per week in the first 30 days.
- Fewer than 15% of transactions uncategorised at the 30-day mark.

## Known Friction Points and Risk Signals
- **Onboarding Drop-off**: `set_first_goal` has the lowest completion rate (12%) but is the strongest predictor of 90-day retention.
- **Value Visibility/Friction**: `analysis_view` has a 55% abandonment rate. `manual_transaction` has a 39% abandonment rate.
- **Churn Predictor**: Linking only one financial account, viewing transaction screen once or twice, and never setting a savings goal.
- **Decay Signals**: Notification open rate declining over time; ratio of uncategorised transactions growing.

## Available Data Sources

### finwise_accounts.csv
- **What it is:** Spine table, one row per account.
- **Key columns:** `plan_tier`, `user_segment`, `accounts_linked`, `goals_set`.
- **Outcome variable:** `churned_90d`, `upgraded_90d`.
- **Row count:** 1,800
- **Sampling:** No sampling applied — dataset within size limits.

### finwise_users.csv
- **What it is:** One row per user (one user per account in this dataset).
- **Key columns:** `platform`, `days_since_last_active`.
- **Row count:** 1,800
- **Sampling:** No sampling applied.

### finwise_monthly_snapshots.csv
- **What it is:** One row per account per month.
- **Key columns:** `active_days`, `sessions`, `goals_active`, `transactions_categorised`, `transactions_uncategorised`, `notifications_sent`, `notifications_opened`.
- **Row count:** 16,448
- **Sampling:** No sampling applied.

### finwise_feature_events.csv
- **What it is:** One row per feature interaction.
- **Key columns:** `feature_name`, `event_type`.
- **Row count:** 74,171
- **Sampling:** No sampling applied.

### finwise_onboarding.csv
- **What it is:** One row per account per onboarding step.
- **Key columns:** `step_name`, `completed`.
- **Row count:** 10,800
- **Sampling:** No sampling applied.

## Data Dictionary
Summarized in `finwise-data-dictionary.md`. Key derived signals include notification open rate, uncategorised transaction rate, and month-over-month sessions change.

## Customer Voice Themes
No qualitative context available. Recommend validating hypotheses against customer calls or support data before prioritising.

## Known Gaps
- **No qualitative data**: Hypotheses should be validated against customer calls before acting.
