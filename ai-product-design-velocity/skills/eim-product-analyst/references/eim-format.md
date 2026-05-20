# EIM Format Reference

The EIM framework structures product hypotheses into three parts that force specificity
at every stage. This reference explains each part and provides worked examples.

---

## The Three Parts

### E — Evidence
**What the data actually shows.**

Requirements:
- One specific metric (a rate, a count, a ratio — not a vague trend)
- The segment or population it applies to
- The comparison group (what does it look like for everyone else?)
- The sample size on both sides (n=X)
- The magnitude of the effect (Xx difference, +X percentage points)

The Evidence should be falsifiable. Someone should be able to run the same query and get
the same number.

---

### I — Impact
**The business opportunity if this signal is acted on.**

Requirements:
- Start from the population affected (how many accounts / users / seats?)
- Apply the outcome rate from the Evidence
- Multiply by a value proxy (ACV, ARR per seat, LTV estimate)
- State a conservative scenario (what if we only improve it by 20%? 25%?)

The Impact should make the opportunity legible to a non-technical stakeholder. Use AUD or
the relevant currency. Round to the nearest thousand. Show your working.

Do not overstate. A 25–30% improvement assumption is usually more defensible than 50%+
unless you have benchmark data from similar interventions.

---

### M — Mechanism
**The specific intervention that would address the signal.**

Requirements:
- Name the product surface (onboarding flow, in-app tooltip, email trigger, dashboard widget)
- Name the trigger condition (what event or state causes this to fire?)
- Name the target user (admin? member? specific role or segment?)
- Describe the intervention itself (what does the user see or experience?)
- Suggest a test approach (A/B holdout? Staged rollout? Which metric is the success signal?)

The Mechanism should be specific enough that a product manager could write a one-page brief
from it without needing to ask clarifying questions.

---

## Worked Examples

---

### Example 1: Onboarding Churn Signal

**Evidence**
Accounts in the small company segment (20–50 employees) that did not complete the
`connect_second_integration` onboarding step churned at 40.7% within 90 days, compared
to 11.1% for small accounts that completed it (n=412 vs n=289). This 3.7x difference
does not appear in mid or large company segments, where churn rates converge regardless
of onboarding completion.

**Impact**
412 small accounts at 40.7% churn × average ACV of $3,200 = approximately $536K ARR at
annual risk. A 25% reduction in churn rate for this segment (i.e., moving from 40.7% to
~30.5%) would retain approximately $134K ARR per year. This is a conservative estimate —
it does not include the downstream expansion value of retained accounts.

**Mechanism**
On day 3 post-signup for any account with company_size = small and integration_count < 2,
trigger an in-app modal surfaced to the admin role. The modal offers a guided "connect your
second tool" wizard with pre-built integration templates for the 5 most common tool pairs in
the small company segment. Dismiss state is stored so it only appears once. Run a 50/50
holdout test with `connect_second_integration_completed` as the primary success metric and
`churned_90d` as the secondary metric. Minimum test duration: 6 weeks.

---

### Example 2: Expansion Signal by Vertical

**Evidence**
Pro-tier accounts in the RevOps vertical with 4 or more connected integrations upgraded to
Enterprise within 90 days at a rate of 70.8% (n=89). This compares to an overall upgrade
rate of 10.2% across all Pro accounts (n=684). The effect is specific to the RevOps vertical
— Pro accounts with 4+ integrations in other verticals upgrade at 18–22%, which is elevated
but not at the same magnitude.

**Impact**
89 accounts currently meet the Pro + RevOps + 4+ integration criteria. At a 70.8% upgrade
rate, approximately 63 are likely to upgrade within 90 days regardless of intervention.
However, there are an estimated 140 Pro + RevOps accounts with 2–3 integrations who have
not yet crossed the 4-integration threshold. Accelerating integration adoption in this group
— even converting 30% of them to 4+ integrations — could unlock ~42 additional upgrade
candidates. At an Enterprise ACV of $24,000 vs Pro ACV of $9,600, each conversion represents
~$14,400 incremental ARR. 42 accounts × $14,400 = approximately $605K incremental ARR
opportunity.

**Mechanism**
For Pro accounts in the RevOps vertical with integration_count between 2 and 3, surface an
in-app "integration milestone" banner visible to the admin role. The banner highlights which
integrations are most commonly used by similar RevOps teams and shows a progress indicator
(e.g., "Teams like yours typically connect 4–6 tools — you're at 2"). Include a one-click
path to the integration catalogue filtered to RevOps-relevant tools. Track `integration_count`
change as the primary metric and `upgraded_90d` as the lagging secondary metric over a 90-day
measurement window. No holdout required for the banner itself — instrument it and measure
lift in integration additions for the target segment vs the prior 90-day baseline.

---

### Example 3: Billing Friction Churn Signal

**Evidence**
Accounts that raised a billing-category support ticket in their first month churned at 32.5%
within 90 days, compared to 14.3% for accounts that raised product or integration tickets in
month 1 (2.3x difference, n=161 billing vs n=408 other). The effect is strongest in accounts
acquired via paid_search (where misaligned expectations are most common) but is present across
all acquisition channels. It is masked in aggregate churn data because billing tickets represent
only 12% of all month-1 tickets.

**Impact**
161 accounts raised billing tickets in month 1 in this dataset period. At 32.5% churn, ~52
accounts churned that would have been retained at the non-billing ticket churn rate of 14.3%.
At average ACV of $4,800 (blended across plan tiers for month-1 billing ticket raisers), this
represents approximately $250K ARR lost annually to billing-friction-driven churn. The mechanism
cost is low — this is a CX and pricing clarity intervention, not a product build.

**Mechanism**
Two-part intervention. First, route any billing-category ticket raised in a customer's first
30 days to a dedicated onboarding success agent (not general support) with a response SLA of
4 hours. Equip this agent with a churn-risk flag in the CRM based on the billing ticket trigger.
Second, review the paid_search ad copy and landing page messaging for plan tier misrepresentation —
the concentration of billing tickets in paid_search cohorts suggests expectation mismatch at
point of acquisition. Track `churned_90d` for billing ticket raisers as the primary metric,
with a 90-day measurement window from ticket creation date.

---

## What Makes a Good EIM Hypothesis

| Quality | Test |
|---|---|
| Specific | Can someone reproduce the Evidence number from the data? |
| Segmented | Does the signal hold in a specific sub-population, not just in aggregate? |
| Quantified | Does the Impact show its working (population × rate × value)? |
| Actionable | Could a PM write a brief from the Mechanism without asking clarifying questions? |
| Testable | Does the Mechanism name a success metric and a measurement window? |
| Honest | Does the "What We Ruled Out" section name signals that didn't hold up? |

---

## Anti-Patterns

**Vague Evidence**
"Users who engage more tend to churn less." This is not Evidence. It is a truism.
Evidence requires a specific metric, a specific segment, a specific comparison, and sample sizes.

**Unstated Impact assumptions**
"This could represent significant ARR." Show the multiplication. State the ACV you used.
State the improvement percentage you assumed. Make it auditable.

**Generic Mechanisms**
"Improve the onboarding experience." This is a strategy, not a mechanism.
A mechanism names a surface, a trigger, a user, an intervention, and a test.

**Missing sample sizes**
A 3x effect in n=8 is noise. Always show n. Always flag if n < 30.

**Correlation without validation**
A feature with high usage that does not predict retention is a red herring.
Always validate behavioural signals against outcome variables before including them.
