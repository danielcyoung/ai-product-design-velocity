# FinWise — Data Dictionary

All five tables join on `account_id`. `finwise_users.csv` also exposes `user_id`, which links to `finwise_feature_events.csv`.

---

## finwise_accounts.csv

One row per account. The spine table. All other tables join back to this.

| Column | Type | Description |
|---|---|---|
| `account_id` | string | Unique account identifier. Format: `fw_acc_XXXXX`. Primary key. |
| `plan_tier` | string | Subscription tier. Values: `free`, `pro`. |
| `user_segment` | string | User intent segment at sign-up. Values: `anxious_tracker`, `budget_focused`, `savings_motivated`, `mint_refugee`, `new_to_tracking`. |
| `platform` | string | Primary device platform. Values: `ios`, `android`. |
| `acquisition_channel` | string | How the account was acquired. Values: `organic`, `paid_social`, `referral`, `mint_refugee`, `other`. |
| `accounts_linked` | integer | Number of financial accounts linked (bank accounts, credit cards). Range: 1–4. |
| `goals_set` | integer | Number of savings goals ever created by this account. Range: 0–4. Free-tier accounts are capped at 1 by the product. |
| `account_age_days` | integer | Days since account creation at snapshot date (2026-03-01). |
| `monthly_revenue` | float | Monthly recurring revenue from this account. `0.0` for free, `9.99` for pro. |
| `churned_90d` | boolean | Whether the account churned within 90 days of the snapshot date. |
| `upgraded_90d` | boolean | Whether a free-tier account upgraded to Pro within 90 days of the snapshot date. Always `False` for pro accounts. |

---

## finwise_users.csv

One row per user. In this dataset, each account has one primary user.

| Column | Type | Description |
|---|---|---|
| `user_id` | string | Unique user identifier. Format: `fw_usr_XXXXXXX`. Primary key. |
| `account_id` | string | Account this user belongs to. Foreign key → `finwise_accounts.account_id`. |
| `role` | string | User role within the account. Value: `primary`. |
| `country` | string | User's country. Value: `US` (all users are US-based). |
| `platform` | string | Device platform. Values: `ios`, `android`. Matches `finwise_accounts.platform`. |
| `days_since_last_active` | integer | Days since this user last opened the app, as of snapshot date. 0 = active today. |

---

## finwise_monthly_snapshots.csv

One row per account per month. Covers up to 12 months of history per account.

| Column | Type | Description |
|---|---|---|
| `account_id` | string | Foreign key → `finwise_accounts.account_id`. |
| `month` | date | First day of the calendar month. Format: `YYYY-MM-DD`. |
| `active_days` | integer | Number of distinct days in the month when the account had at least one session. |
| `sessions` | integer | Total app sessions in the month. |
| `goals_active` | integer | Number of savings goals currently active for this account in this month. |
| `transactions_categorised` | integer | Transactions that have been assigned to a named category. |
| `transactions_uncategorised` | integer | Transactions currently sitting in the default "Other" or uncategorised bucket. |
| `notifications_sent` | integer | Push notifications sent to the account's primary user in this month. |
| `notifications_opened` | integer | Notifications opened (tapped) by the user. Always ≤ `notifications_sent`. |
| `support_tickets` | integer | Support tickets raised by this account in this month. Values: 0 or 1. |
| `support_ticket_category` | string | Category of the support ticket. Values: `categorisation`, `account_sync`, `billing`, `feature_request`, `other`, `none`. |

**Derived signals worth computing:**
- `notifications_opened / notifications_sent` → notification open rate (declining trend over time is the H2 signal)
- `transactions_uncategorised / (transactions_categorised + transactions_uncategorised)` → uncategorised rate (>20% is a friction signal)
- Month-over-month `sessions` change → engagement trajectory (steep drop in months 2–3 is the H3 signal)

---

## finwise_feature_events.csv

One row per feature interaction. Highest-volume table.

| Column | Type | Description |
|---|---|---|
| `event_id` | string | Unique event identifier. Format: `fw_evt_XXXXXXXX`. Primary key. |
| `user_id` | string | User who triggered the event. Foreign key → `finwise_users.user_id`. |
| `account_id` | string | Account associated with the event. Foreign key → `finwise_accounts.account_id`. |
| `feature_name` | string | Feature touched. Values: `transaction_view`, `analysis_view`, `savings_goal`, `budget_setup`, `bill_tracking`, `category_edit`, `manual_transaction`, `notification_settings`. |
| `event_type` | string | Outcome of the interaction. Values: `used` (completed), `blocked` (free-tier limit hit), `abandoned` (started but not completed). |
| `timestamp` | datetime | When the event occurred. Format: `YYYY-MM-DD HH:MM:SS`. |

**Feature-specific notes:**
- `analysis_view` + `abandoned`: user reached the charts/analysis screen and exited within ~20 seconds without interacting. 55% abandonment rate is the expected baseline.
- `savings_goal` + `blocked`: free-tier user attempted to create a second savings goal, hitting the 1-goal limit. This is the primary Pro upgrade trigger.
- `manual_transaction` + `abandoned`: user started entering a manual transaction and did not complete it. ~39% abandonment rate expected.
- `savings_goal` + `abandoned` (Pro users only): Pro user reached the goal creation screen but did not complete goal setup.

---

## finwise_onboarding.csv

One row per account per onboarding step. Six steps total.

| Column | Type | Description |
|---|---|---|
| `account_id` | string | Foreign key → `finwise_accounts.account_id`. |
| `step_name` | string | Onboarding step. See step definitions below. |
| `completed` | boolean | Whether the user completed this step. |
| `completed_at` | date | Date of completion. Empty string if not completed. Format: `YYYY-MM-DD`. |

**Onboarding steps (in order):**

| Step | What it means | Typical completion rate |
|---|---|---|
| `link_first_account` | User linked at least one bank or credit card account | 84% |
| `complete_profile_setup` | User completed basic profile (name, currency, notification preferences) | 91% |
| `view_first_spending_summary` | User viewed the Analysis or category summary screen for the first time | 61% |
| `link_second_account` | User linked a second financial account (checking + credit card, or two banks) | 32% |
| `set_first_goal` | User created at least one savings goal | 12% |
| `customise_first_category` | User renamed or reassigned at least one transaction category | 14% |

**The key signal:** `set_first_goal` has the lowest completion rate (12%) of any onboarding step. It is also the single strongest predictor of 90-day retention. These two facts together define the core product opportunity in this dataset.
