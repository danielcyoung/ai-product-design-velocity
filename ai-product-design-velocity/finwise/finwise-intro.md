# FinWise — Getting Started with This Dataset

## The scenario

You're a product manager at **FinWise**, a US-based personal finance app. FinWise sells direct-to-consumer on a freemium model — users download the app for free, track their spending and set up their accounts at no cost, and upgrade to FinWise Pro at $9.99/month to unlock savings goals, budget automation, and bill tracking.

Like all freemium consumer apps, the two outcomes that drive every product decision are **churn** (losing users before they convert or before they get enough value to stay) and **upgrade** (converting free users to Pro). This dataset gives you 18 months of synthetic but realistic product data to practise the EIM discovery workflow on.

**The core question this data is designed to help you answer:** which user behaviours predict whether an account will churn or upgrade in the next 90 days — and what can product do about it?

---

## What's in the dataset

Five CSV files, all stored in `data/`. They join together via `account_id` and `user_id`.

### `finwise_accounts.csv`
One row per account. Your spine table — every other table joins back to it. Tells you what plan tier each account is on, what user segment they belong to, how many financial accounts they've linked, how many goals they've set, and their 90-day outcome (churned or upgraded).

**What to look for:** `churned_90d` and `upgraded_90d` are your outcome labels. Every hypothesis should point back to one of these.

### `finwise_users.csv`
One row per user. In this dataset, each account has one primary user. Shows platform (iOS or Android), country, and days since last active.

**What to look for:** `days_since_last_active` is a leading churn indicator. Users who go silent for 14+ days are at high risk.

### `finwise_monthly_snapshots.csv`
One row per account per month. Your engagement trend table — shows sessions, active days, goals active, transactions categorised vs uncategorised, notifications sent and opened, and support tickets.

**What to look for:** Two signals are buried here. First: the notification open rate over time — does it hold or drop? Second: the ratio of uncategorised to total transactions — does it grow or stay stable? Both are decay signals.

### `finwise_feature_events.csv`
One row per feature interaction — the highest-volume table. Every time a user touches a feature, an event is logged as `used`, `blocked` (Pro feature hit by free-tier user), or `abandoned` (started but didn't complete). 

**What to look for:** The analysis_view abandonment rate (users who reach the chart screen and leave immediately), the savings_goal blocked rate for free users, and the manual_transaction abandonment rate. Each is a friction signal pointing at a specific mechanism.

### `finwise_onboarding.csv`
One row per account per onboarding step. Six steps: link first account, complete profile setup, view first spending summary, link second account, set first goal, customise first category.

**What to look for:** Which steps have the sharpest drop-off. One step in particular has dramatically lower completion than the others. How that step correlates with 90-day outcomes is the clearest signal in the entire dataset.

---

## Where you'd find this data in your own company

| Dataset | Where to find it in the real world |
|---|---|
| `accounts` | Your billing system (Stripe, RevenueCat, Apple/Google subscriptions) and your app's user database. Churn and upgrade outcomes typically live in billing data or a CRM. |
| `users` | Your auth or identity system, your mobile analytics platform (Mixpanel, Amplitude, Braze), or the user table in your application database. |
| `monthly_snapshots` | Usually built by a data engineer from raw event data. Lives in your data warehouse (Snowflake, BigQuery) as a pre-aggregated reporting table, or surfaces in Looker, Amplitude's charting layer, or a dashboard tool. |
| `feature_events` | Your product event tracking pipeline — Segment, Mixpanel, Amplitude, or PostHog. The analytics platform is usually the query layer. |
| `onboarding` | Often a combination of in-app milestone tracking, analytics funnel definitions, and CRM lifecycle stages. May be in your analytics platform, your CRM, or a custom table in your data warehouse. |

---

## Tips before you start

- **Segment by outcome first.** Split the accounts table into churned vs retained. Look at what's different about each group across every other table before forming hypotheses.
- **Onboarding step completion is your strongest early signal.** The step with the lowest completion rate is not random — it predicts 90-day outcomes more clearly than any other variable in the dataset.
- **Goals and churn are not independent.** The relationship between `goals_set` and `churned_90d` is the most important correlation in this dataset. Investigate it before looking at anything else.
- **Notifications tell a story over time.** Don't just look at open rates as a static number. Look at how they change month-over-month, especially in the 60 days before churned accounts deactivate.
- **Mint refugees are a distinct cohort.** Accounts acquired via the `mint_refugee` channel behave differently from organic installs. Segment them separately when assessing retention.

For full schema details, see [finwise-data-dictionary.md](finwise-data-dictionary.md). For product context that helps you interpret behavioural signals as product problems, see [finwise-product-context.md](finwise-product-context.md).
