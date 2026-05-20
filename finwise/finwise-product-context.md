# FinWise — Product Context Statement

> This document is provided to AI models analysing FinWise product data. It gives the model the product context needed to interpret data signals as product problems, not just data anomalies. Read this before analysing any FinWise dataset.

---

## What FinWise Is

FinWise is a US-based personal finance app that helps everyday Americans track spending, set savings goals, and understand where their money actually goes. Founded in 2021, Austin TX. Distributed team across Austin, New York, and San Francisco. Series A ($14M, 2024). 62 full-time employees.

**The core job-to-be-done:** reduce the cognitive load and shame of managing money for Americans who earn enough to care about their finances but not enough to afford a financial advisor. The ideal outcome is a user who opens FinWise each week, understands their financial situation in under two minutes, and makes at least one intentional decision as a result.

---

## Who It's For

**Primary user:** Americans aged 25–40. Earns $45K–$120K/year. Financially anxious — knows they should be doing better with money but struggles with consistency. Not bad at money, just overwhelmed by it. Common sign-up triggers: new year resolution, first real job, moving in with a partner, paying off a debt.

**Mint refugee cohort:** approximately 30,000 users acquired after Mint shut down in March 2024. These users are more experienced with personal finance tools, have higher session frequency, and convert to Pro at a higher rate than organic installs. They also churn at higher rates in months 4–6, likely due to unmet expectations around investment account tracking and shared household features that Mint supported.

---

## Core Features

| Feature | What it does | Tier |
|---|---|---|
| `transaction_view` | View and manage all transactions across linked accounts | All |
| `analysis_view` | Charts and breakdowns of spending by category, week, and month | All |
| `category_edit` | Rename categories, reassign transactions, create custom categories | All |
| `manual_transaction` | Manually log a transaction not captured via account sync | All |
| `notification_settings` | Manage spend alert and budget notification preferences | All |
| `savings_goal` | Create and track savings goals with progress visibility | Pro only |
| `budget_setup` | Set monthly budget limits by category with real-time tracking | Pro only |
| `bill_tracking` | Track recurring bills and upcoming payment dates | Pro only |

A `blocked` event in the feature_events table means a free-tier user attempted to use a Pro-gated feature.

A `manual_transaction` event with type `abandoned` means the user started entering a transaction but did not complete it.

---

## Pricing Tiers

| Tier | Monthly price | Key access |
|---|---|---|
| `free` | $0 | All tracking features. Account linking (unlimited). Notifications. Analysis view. 1 savings goal maximum. |
| `pro` | $9.99/month | All free features plus unlimited savings goals, budget automation, bill tracking. |

**Upgrade trigger:** The single strongest conversion moment in the product is when a free-tier user attempts to create a second savings goal and hits the 1-goal limit. 71% of Pro upgrades happen within 14 days of this blocked event.

---

## Business Goals (current)

| Goal | Current | Target | Timeline |
|---|---|---|---|
| Grow engaged user base | 380K registered | 1M registered | End of 2026 |
| Improve month-2 retention | 31% | 50% | Q4 2026 |
| Increase Pro conversion | 4.2% | 8.0% | End of 2026 |
| Reduce support burden | 40% of tickets are categorisation/sync confusion | <15% | Q3 2026 |

**Revenue leverage:** Every 1 percentage point improvement in Pro conversion = approximately $380K additional ARR at current user volume.

---

## What a Healthy, Retained Subscriber Looks Like

A retained Pro subscriber at month 3+ typically has **all** of the following:

- **At least one active savings goal** created within the first 14 days
- **Two or more financial accounts linked** (primary checking + at least one other)
- **Opening the app 3+ times per week** in the first month
- **Notifications engaged with** at least once per week in the first 30 days
- **Fewer than 15% of transactions uncategorised** at the 30-day mark

The single clearest early predictor of churn is an account that links one financial account, views the transaction screen once or twice, and never sets a savings goal. These accounts have no personalised stake in the product. They treat it as a ledger, not a companion.

---

## Interpreting the Data

When a signal appears in the data, ask:

- Is this a **product design problem** (the feature exists but users don't engage with it)?
- Is this a **value visibility problem** (the feature's benefit isn't clear before the user uses it)?
- Is this a **discovery problem** (users don't know the feature exists)?
- Is this a **friction problem** (users attempt the feature but don't complete it)?

These four frames map to four different interventions. Distinguishing them is what separates a specific, defensible mechanism from a generic "improve the experience" recommendation.
