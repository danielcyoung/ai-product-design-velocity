# EIM Hypothesis Report — FinWise
**Dataset:** finwise_accounts.csv, finwise_users.csv, finwise_monthly_snapshots.csv, finwise_feature_events.csv, finwise_onboarding.csv
**Analysis date:** 2026-05-20
**Outcome variable:** churned_90d, upgraded_90d

---

## Hypothesis 1: The Goals Activation Gap

**Evidence**
Accounts that have set 0 goals churn at a rate of 36.0% (n=1581), compared to 14.7% for accounts that have set at least 1 goal (n=75). This is a 2.4x difference in churn rate. Furthermore, the onboarding step `set_first_goal` has a completion rate of only 18.9%.

**Impact**
In this sample of 1800 accounts, 1581 have 0 goals. If we could reduce their churn rate from 36.0% to the 14.7% seen in users with 1 goal, we would retain approximately 337 accounts over 90 days. Scaled across the full user base, the impact would be significant.

**Mechanism**
Introduce a guided goal-setting wizard immediately after the user links their first account during onboarding. The wizard should offer 3 template goals based on the user's segment (e.g., "Build an emergency fund" for `anxious_tracker`) to reduce friction in goal creation.

---

## Hypothesis 2: Multi-Account Retention Boost

**Evidence**
Users who fail to link a second account churn at 45.7% (n=1004), vs 17.2% for those who do (n=796). This is a 2.6x difference. The completion rate for the `link_second_account` onboarding step is 44.2%.

**Impact**
There are 1004 accounts in the sample that did not link a second account. Reducing their churn rate from 45.7% to 17.2% would retain approximately 286 accounts in this sample over 90 days.

**Mechanism**
Surface a "Link a credit card to see the full picture" prompt to users who have only linked a checking account, appearing on the transaction view screen after 3 sessions. The mechanism should highlight the benefit of seeing combined spending.

---

## Hypothesis 3: Mint Refugee Conversion Opportunity

**Evidence**
The `mint_refugee` segment has a 10.6% upgrade rate (n=283), which is more than double the base upgrade rate of 4.4% and significantly higher than the 7.0% rate for free users generally.

**Impact**
While the sample has only 283 Mint refugees, the company acquired ~30,000 Mint refugees. A 10.6% conversion rate on 30,000 users yields ~3,180 Pro upgrades, worth ~$380K ARR (at $9.99/month).

**Mechanism**
Create a dedicated onboarding path for users identified as Mint refugees (via UTM or self-selection) that skips basic educational steps and directly highlights Pro features like budget automation and bill tracking, which they are likely familiar with.

---

## What We Ruled Out
- **Feature Abandonment as Churn Predictor**: We inspected abandonment rates for `analysis_view` and `manual_transaction`. While high (55% and 37% respectively), they did not differ significantly between churned and retained users, suggesting they are baseline friction points rather than active churn drivers.

---

## Recommended Next Steps
1. **Prioritize Hypothesis 1 (The Goals Activation Gap)**: It has the largest volume of at-risk users (1581 accounts) and a strong correlation with retention.
2. **Run Hypothesis 3 (Mint Refugee Conversion)**: It targets a high-intent cohort with a proven higher conversion rate, offering a quick win for revenue.
