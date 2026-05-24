# PRD: Goal-Setting Activation — FinWise

**Hypothesis:** We believe that prompting users to set a savings goal on day 1 (with a day 3–4 reminder), followed by a targeted email on day 5 if no goal is created, will increase goal-setter rate from 18.9% to 28–30%, resulting in 135+ additional retained accounts annually.

**Because:** Only 18.9% of accounts ever set a goal, yet goal-setters churn at 14.4% vs. 37.5% for non-setters (2.60x difference). This is an activation bottleneck, not a feature quality problem.

**We'll know it worked when:** Goal-setter rate reaches 28%+ within 30 days of feature launch, and 30-day retention lift is +2–4 percentage points for prompted cohorts vs. control.

---

## 1. Problem Statement

A user signs up for FinWise to understand their finances better. They link their first bank account and see their transactions. But they haven't set a savings goal. Without a goal tied to their spending, the app feels like a ledger—something to view but not act on. By day 3–4, many of these users are disengaging because they don't see how FinWise helps them *do* something, not just *see* something. By day 30, 37.5% of these goal-less accounts have churned.

---

## 2. Hypothesis

**We believe** that prompting users to create a savings goal on day 1 (after account linking), repeating the prompt on day 3–4 if dismissed, and sending a reassurance email on day 5 (if still no goal) **will increase goal creation rate from 18.9% to 28–30%**, resulting in significant retention lift.

**Because** goal-setting is the single strongest predictor of retention in the data (2.60x churn difference), and currently 81% of accounts never create a goal — indicating a discovery/activation problem, not a feature problem. Users don't know goals exist or don't know where to start.

**We'll know it worked when:**
- Goal-setter rate increases to 28%+ within 30 days of feature launch (measured by `set_first_goal` completion rate)
- 30-day retention improves by +2–4 percentage points for accounts exposed to the prompt vs. control group
- Email follow-up achieves ≥20% click-through rate on the "Set Your First Goal" CTA
- Time-to-goal decreases (accounts reach goal-setting faster)

---

## 3. Success Metrics

### Primary Metric (Leading)
**Goal-Setting Completion Rate Within 7 Days**
- *What it is:* % of accounts that create ≥1 goal within 7 days of signup
- *Baseline:* ~5% (inferred from current 18.9% total goal-setter rate across all account ages; very few set goals in first 7 days)
- *Target:* 15%+ within 7 days
- *Why leading:* Directly caused by the intervention; measurable within 1 week
- *Measurement:* Track `set_first_goal` event timestamp, calculate % with timestamp ≤7 days from account creation

### Primary Metric (Leading) — Phase 2
**Email Follow-Up Click-Through Rate (Day 5+ non-goal-setters)**
- *What it is:* % of users who receive the day 5 email and click the "Set Your First Goal" CTA
- *Baseline:* Unknown (no comparable email send today)
- *Target:* ≥20% CTR
- *Measurement:* Track email delivery, click events on authenticated goal-creation link

### Secondary Metric (Lagging)
**30-Day Retention Rate (Cohort)**
- *What it is:* % of accounts that are not churned at day 30
- *Baseline:* ~66% (derived from 33.1% overall churn; varies by segment)
- *Target:* 68–70% for prompted cohort vs. control (2–4 percentage point lift)
- *Measurement:* Compare churned_90d rate for day 1 signup cohort in treatment vs. control after 30 days
- *Note:* 90-day churn is the definitive metric, but 30-day lift suggests the intervention is working

### Guardrail Metric
**Dismissal Rate on Day 1 Prompt**
- *What it is:* % of accounts that see the day 1 goal-setting prompt and click "Maybe Later" without creating a goal
- *Baseline:* Unknown (no prompt exists today)
- *Target:* ≤65% (we expect some dismissal; if >65%, the prompt copy or timing is wrong)
- *Why guardrail:* High dismissal rate signals the benefit messaging is weak or the timing is off

### Guardrail Metric
**Support Tickets Related to Goal-Setting or Prompt Confusion**
- *What it is:* Count of support tickets mentioning confusion about goals, how to set them, or modal appearing unexpectedly
- *Baseline:* Unknown (currently no goal-setting activation feature)
- *Target:* <5 tickets per 1,000 accounts exposed to prompt in first 30 days
- *Measurement:* Tag support tickets with [goal-prompt-confusion] and track volume

---

## 4. Scope

### In Scope

**UI/UX Components:**
- **Day 1 Goal-Setting Modal Prompt** (non-dismissible, appears after `link_first_account` completion)
  - Headline: "Set your first goal"
  - Subheading: "Users who set a goal are 2.6x more likely to stay on track with their finances."
  - Four CTA buttons: [Emergency Fund] [Vacation Fund] [Debt Payoff] [Custom Goal]
  - Secondary CTA: [Maybe Later] (or [Dismiss]) — user must click one to proceed
  - Upon creation, goal appears on dashboard with edit affordance visible
  - Modal is non-dismissible on background click (required UX)

- **Day 3–4 Re-Prompt Modal** (if goal not created)
  - Identical copy and CTAs as day 1
  - Appears after account opens the app on day 3, 4, or 5 (whichever is first after day 1 dismissal)
  - Same non-dismissible behavior
  - Only shows once (not every day until goal is created)

- **Email: Day 5 Goal-Setting Nudge** (if goal still not created)
  - Subject: "The #1 thing successful FinWise users do"
  - Body copy (required): "Users who set goals within the first week report feeling 78% more secure about their finances 3 weeks later. It takes just 30 seconds; we'll help you every step of the way."
  - Primary CTA: [Set Your First Goal] — links to authenticated goal-creation surface (token-based auth, pre-populating user context)
  - Email templates: [Emergency Fund] [Vacation Fund] [Debt Payoff] [Or Create Custom]
  - Secondary CTA or note: "We're here to help every step" or similar reassurance messaging

**Trigger Logic & State Management:**
- Trigger: `link_first_account` completion flag is true AND `set_first_goal` completion flag is false
- Day 1 Modal: Show on first app open after day 1 of signup
- Day 3–4 Re-Prompt: Show on first app open after day 3 of signup (if goal still not set)
- Email (Day 5): Send if goal still not set by end of day 5; email_sent_flag = true (no resend)
- Account-level flags:
  - `goal_setting_modal_shown_day1` (boolean, timestamp)
  - `goal_setting_modal_shown_day3` (boolean, timestamp)
  - `goal_setting_email_sent_day5` (boolean, timestamp)

**Analytics Instrumentation** (detailed in Section 7):
- Modal impression events (day 1, day 3–4)
- Modal interaction events (goal created, "Maybe Later" clicked, dismissed)
- Email delivery, open, and click events
- Goal creation timestamp and method (from modal vs. email link)

**Integration Requirements:**
- Feature flag: `goal_setting_activation_v1` (for A/B testing, rollout control)
- A/B test setup: Randomize at signup; 50/50 treatment vs. control
- Onboarding state machine: integrate day 1 and day 3–4 prompts into existing onboarding flow
- Email service integration: ensure day 5 email is triggered via email automation system (e.g., Klaviyo, Segment)
- Goal-creation backend: must handle pre-populated template creation from email CTA (authenticated link)

### Out of Scope

- **Goal-editing functionality enhancements:** This PRD does not include changes to how goals are edited or managed post-creation (e.g., renaming, progress UI). Edit affordance is surfaced in the prompt, but feature improvements to editing are separate.
- **Goal-sharing or social features:** No social sharing, referral incentives, or friend-based motivation in Phase 1.
- **Personalization by user segment:** The prompt, email copy, and templates are uniform across all segments (anxious_tracker, budget_focused, etc.). Segment-specific messaging is a Phase 2 opportunity.
- **Mobile vs. web optimization:** The PRD assumes mobile-first (primary platform is iOS/Android). Web goal-setting prompts are not included.
- **Goal recommendation engine:** No ML-based goal suggestions based on spending patterns. Templates are static.
- **Pro tier upsell from goals:** Goals do not trigger Pro conversion messaging. That is handled by separate H3 hypothesis (savings goal blocked event).

### Assumptions & Dependencies

1. **Assumption:** Users have email addresses captured at signup and have not opted out of product emails.
   - *Dependency:* Verify email list health and confirm suppression rules for opt-out accounts before sending day 5 email.

2. **Assumption:** The goal-creation backend can accept pre-populated template selections (e.g., "Emergency Fund") and create goals without additional user input.
   - *Dependency:* Backend API supports template-based goal creation via authenticated links from emails.

3. **Assumption:** Onboarding state (account_age_days, link_first_account completion) is reliably tracked in the database.
   - *Dependency:* Onboarding event log must be queryable in real-time to trigger day 3–4 re-prompt.

4. **Assumption:** The app has a feature flag system capable of 50/50 randomization at signup.
   - *Dependency:* Feature flag service (e.g., LaunchDarkly) is integrated and accessible to mobile and web clients.

5. **Assumption:** Non-goal-setting users (treatment group) will not cancel signup or unsubscribe due to the non-dismissible day 1 prompt.
   - *Dependency:* Monitor churn rate for prompted cohorts during rollout. If Day 1 churn increases >1%, re-evaluate prompt UX (e.g., add easier dismiss option, soften copy).

---

## 5. User Stories

### Story 1: User Creates Goal from Day 1 Prompt
> As a new FinWise user who has just linked my first bank account, I want to set a savings goal with a single tap so that I feel like I'm taking action on my finances.

**Acceptance Criteria:**
- Modal prompt appears on first app open after account linking (day 1 or later)
- I can see four goal options: Emergency Fund, Vacation Fund, Debt Payoff, Custom Goal
- Tapping any template creates the goal immediately without additional input
- Goal appears on my dashboard with an edit affordance visible
- Modal dismisses; dashboard is shown

---

### Story 2: User Dismisses Day 1 Prompt and Sees Day 3–4 Re-Prompt
> As a new user who dismissed the goal-setting prompt on day 1, I want to see the same prompt again on day 3–4 so that I have another chance to set a goal without having to search for it.

**Acceptance Criteria:**
- Day 1 prompt shows when I open the app after account linking
- I click "Maybe Later" to dismiss it
- On day 3, when I next open the app, the same prompt appears again (no dismissal from day 1 persists)
- If I dismiss this one, the prompt does not appear again (no further re-prompts)
- Goal completion flag is tracked separately from dismissal count

---

### Story 3: User Receives Day 5 Email and Creates Goal from Email Link
> As a user who didn't set a goal in the app, I want to receive an encouraging email with a direct link to goal templates so that I can set a goal without opening the app.

**Acceptance Criteria:**
- Email is sent on day 5 (end of day 5) if goal still not created
- Subject line is: "The #1 thing successful FinWise users do"
- Email body includes the copy: "Users who set goals within the first week report feeling 78% more secure about their finances 3 weeks later. It takes just 30 seconds; we'll help you every step of the way."
- Email contains a [Set Your First Goal] CTA that links to an authenticated goal-creation page (no login required; token-based auth)
- Clicking the link shows goal templates and allows me to create one in <30 seconds
- Goal creation from email is tracked separately (via `goal_source` = "email")

---

### Story 4: New Signup Gets Randomized to Control (No Prompt)
> As a new user who is part of the control group, I want the experience to be unchanged so that we can measure the impact of the goal-setting prompt.

**Acceptance Criteria:**
- Control group users (50% of signups) do not see the day 1 or day 3–4 goal-setting prompts
- Control group users do not receive the day 5 email
- All other onboarding steps remain identical
- Control group is tracked via feature flag randomization at signup

---

### Story 5: PM / Analyst Monitors Goal-Setting Activation Metrics
> As a PM, I want to see real-time dashboards of goal-setting completion rate, email CTR, and retention lift so that I can assess whether the intervention is working and make rapid adjustments.

**Acceptance Criteria:**
- Dashboard shows: goal-setter % by day (cumulative), daily unique goal-setters, treatment vs. control retention curves
- Email metrics dashboard shows: send count, open rate, CTR on each CTA
- Modal dismissal rate is tracked and alerted if >65%
- Data is available within 1 hour of event (near real-time)

---

## 6. Functional Requirements

### Trigger & State Management

**FR-01:** When an account completes `link_first_account` onboarding step, set internal flag `link_first_account_complete` to true and `link_first_account_timestamp` to current time.  
*Priority: Must*

**FR-02:** When an account completes `set_first_goal` onboarding step, set flag `set_first_goal_complete` to true, `goal_setting_timestamp` to current time, and `goal_source` to one of: [modal_day1, modal_day3, email_day5, other].  
*Priority: Must*

**FR-03:** Randomize new signups into treatment vs. control at account creation time using feature flag `goal_setting_activation_v1` with 50/50 split. Store assignment in `treatment_group` field (values: treatment, control).  
*Priority: Must*

### Day 1 Modal Prompt

**FR-04:** On first app open after `link_first_account_complete` flag is set, AND `set_first_goal_complete` is false, AND `treatment_group` is treatment, AND feature flag is enabled, display the goal-setting modal.  
*Priority: Must*

**FR-05:** Modal must not be dismissible by tapping the background or using a close button. User must either (a) tap a goal template, (b) tap "Maybe Later", or (c) tap custom goal to proceed.  
*Priority: Must*

**FR-06:** Modal headline must be "Set your first goal" and subheading must be "Users who set a goal are 2.6x more likely to stay on track with their finances."  
*Priority: Must*

**FR-07:** Modal must present four options: [Emergency Fund] [Vacation Fund] [Debt Payoff] [Custom Goal] as tappable buttons.  
*Priority: Must*

**FR-08:** When user taps a template option (e.g., Emergency Fund), create a goal with the selected name and default parameters (e.g., no target amount, no deadline). Goal must appear on dashboard immediately.  
*Priority: Must*

**FR-09:** When user taps [Custom Goal], show a secondary screen/modal allowing user to enter goal name and (optional) target amount. Goal creation must complete with one additional tap.  
*Priority: Should*

**FR-10:** Set flag `goal_setting_modal_shown_day1` to true and `goal_setting_modal_shown_day1_timestamp` to current time when modal is displayed.  
*Priority: Must*

**FR-11:** If user taps "Maybe Later" on day 1 prompt, modal dismisses and does not appear again until day 3 (re-prompt logic handles future display).  
*Priority: Must*

### Day 3–4 Re-Prompt

**FR-12:** On app open after day 3 of account creation (not day 1, not day 2), if `set_first_goal_complete` is false AND `goal_setting_modal_shown_day3` is false AND `treatment_group` is treatment, display the goal-setting modal with identical copy and CTAs as day 1.  
*Priority: Must*

**FR-13:** Day 3–4 modal must only show once (not daily). After display, set `goal_setting_modal_shown_day3` to true and `goal_setting_modal_shown_day3_timestamp` to current time.  
*Priority: Must*

**FR-14:** Day 3–4 modal has identical non-dismissibility and button behavior as day 1 modal.  
*Priority: Must*

### Email: Day 5 Nudge

**FR-15:** On end-of-day 5 (UTC), trigger batch query: SELECT all accounts WHERE account_created_date = 5 days ago AND set_first_goal_complete = false AND treatment_group = treatment AND email_opted_in = true AND email_suppressed = false.  
*Priority: Must*

**FR-16:** For each account in the batch, send email with:
- Subject: "The #1 thing successful FinWise users do"
- Body must include exact copy: "Users who set goals within the first week report feeling 78% more secure about their finances 3 weeks later. It takes just 30 seconds; we'll help you every step of the way."
- Primary CTA: [Set Your First Goal] → links to authenticated goal-creation page (see FR-17)
- Email must include reassurance messaging (e.g., "We're here to help every step")  
*Priority: Must*

**FR-17:** Email CTA link must authenticate user via one-time token (valid for 24 hours) and bypass login, landing user directly on goal-creation template selection screen. Token must encode user_id and timestamp.  
*Priority: Must*

**FR-18:** Set flag `goal_setting_email_sent_day5` to true and `goal_setting_email_sent_day5_timestamp` to current time for each account in the email send batch.  
*Priority: Must*

**FR-19:** Email must not resend if goal is created between the batch query (day 5 00:00 UTC) and email send time. Query must be re-run immediately before send; exclude accounts that completed goal-setting in the interim.  
*Priority: Should*

### Analytics & Tracking

**FR-20:** Log event `goal_setting_modal_impression` when day 1 modal is displayed. Properties: account_id, timestamp, treatment_group, day (1 or 3).  
*Priority: Must*

**FR-21:** Log event `goal_setting_modal_interaction` when user taps any CTA on day 1 or day 3 modal. Properties: account_id, timestamp, action (goal_created | maybe_later), goal_template (if goal_created), time_spent_on_modal_ms.  
*Priority: Must*

**FR-22:** Log event `goal_created` with additional property `source` = one of [modal_day1, modal_day3, email_day5, other]. Use this to track which channel drove goal creation.  
*Priority: Must*

**FR-23:** Log email send event `goal_setting_email_sent` when day 5 email is delivered. Properties: account_id, timestamp, email_address.  
*Priority: Must*

**FR-24:** Log email engagement events `goal_setting_email_opened`, `goal_setting_email_cta_clicked`, `goal_setting_email_cta_bounced`. Properties: account_id, timestamp, cta_name (if clicked).  
*Priority: Must*

### Safety & Rollout

**FR-25:** Feature flag `goal_setting_activation_v1` must support gradual rollout (0%, 10%, 50%, 100% of new signups). Default: 0% (off). Product team manually increases rollout after monitoring initial cohorts.  
*Priority: Must*

**FR-26:** Create alert: if dismissal rate (maybe_later_clicks / modal_impressions) exceeds 65% for 100+ accounts, send Slack alert to #product-alerts.  
*Priority: Should*

**FR-27:** Create alert: if churn rate for day 1 treatment cohort exceeds control cohort by >1 percentage point (measured at day 7), escalate to PM for investigation.  
*Priority: Should*

---

## 7. Analytics Instrumentation

### Event: goal_setting_modal_impression
- **When it fires:** Modal is displayed (day 1 or day 3)
- **Properties:**
  - `account_id` (string)
  - `user_id` (string)
  - `timestamp` (ISO 8601)
  - `modal_day` (integer: 1 or 3)
  - `treatment_group` (string: treatment or control)
  - `source` (string: first_app_open, later_app_open, etc.)
- **Notes:** Should fire exactly once per modal display (not per swipe or scroll)

### Event: goal_setting_modal_interaction
- **When it fires:** User taps a button on the modal (goal template, custom, or "Maybe Later")
- **Properties:**
  - `account_id` (string)
  - `user_id` (string)
  - `timestamp` (ISO 8601)
  - `action` (string: goal_created or dismissed)
  - `goal_template` (string: emergency_fund, vacation_fund, debt_payoff, custom; null if dismissed)
  - `time_on_modal_ms` (integer: milliseconds from impression to interaction)
  - `modal_day` (integer: 1 or 3)
- **Notes:** Fires only once per modal (user makes one choice)

### Event: goal_created
- **When it fires:** Goal record is saved to database
- **Properties:**
  - `account_id` (string)
  - `user_id` (string)
  - `goal_id` (string: unique goal identifier)
  - `timestamp` (ISO 8601)
  - `goal_name` (string: e.g., "Emergency Fund")
  - `source` (string: modal_day1, modal_day3, email_day5, other)
  - `target_amount` (float or null)
  - `target_date` (ISO 8601 or null)
- **Notes:** This event fires regardless of how the goal was created. Source distinguishes which channel drove creation.

### Event: goal_setting_email_sent
- **When it fires:** Email is delivered to mailbox
- **Properties:**
  - `account_id` (string)
  - `user_id` (string)
  - `timestamp` (ISO 8601)
  - `email_address` (string, hashed for privacy)
  - `email_campaign_id` (string: identifier for this cohort send)
- **Notes:** Captured from email service provider (e.g., Klaviyo, Segment)

### Event: goal_setting_email_opened
- **When it fires:** User opens email
- **Properties:**
  - `account_id` (string)
  - `user_id` (string)
  - `timestamp` (ISO 8601)
  - `email_campaign_id` (string)
- **Notes:** Captured from email service provider

### Event: goal_setting_email_cta_clicked
- **When it fires:** User clicks [Set Your First Goal] CTA in email
- **Properties:**
  - `account_id` (string)
  - `user_id` (string)
  - `timestamp` (ISO 8601)
  - `cta_name` (string: set_first_goal)
  - `email_campaign_id` (string)
  - `token_valid` (boolean: true if auth token was valid)
- **Notes:** Captured from authenticated link redirect. If token is expired/invalid, still log as click but mark token_valid = false.

### Derived Metrics (Calculated from Events)

| Metric | Calculation | Refresh |
|---|---|---|
| Goal-setter rate (%) | COUNT(goal_created) / COUNT(account_created) * 100, by day | Daily |
| Goal-setter rate by day of creation | COUNT(goal_created with timestamp ≤ N days from signup) / COUNT(account_created at same time) | Daily |
| Modal dismissal rate (%) | COUNT(dismissed) / COUNT(goal_setting_modal_impression) * 100 | Daily |
| Email send rate (%) | COUNT(goal_setting_email_sent) / COUNT(eligible accounts on day 5) * 100 | Daily |
| Email open rate (%) | COUNT(goal_setting_email_opened) / COUNT(goal_setting_email_sent) * 100 | Daily |
| Email CTA CTR (%) | COUNT(goal_setting_email_cta_clicked) / COUNT(goal_setting_email_opened) * 100 | Daily |
| Goal creation by source (%) | COUNT(goal_created with source = X) / COUNT(goal_created) * 100, by source | Daily |
| Time-to-goal (median days) | MEDIAN(timestamp - account_created_date) for all goal_created events | Daily |
| 30-day retention (treatment vs. control) | % of treatment cohort not churned at day 30 vs. control cohort | Weekly |

### Success Metric Measurement Plan

| Success Metric | Event(s) | Query / Calculation |
|---|---|---|
| Goal-setter rate within 7 days (target: 15%+) | goal_created | `SELECT COUNT(DISTINCT account_id) WHERE source IN (modal_day1, modal_day3, email_day5) AND (timestamp - account_created_date) <= 7 days / COUNT(DISTINCT account_id created in same cohort) * 100` |
| Email CTR (target: ≥20%) | goal_setting_email_sent, goal_setting_email_cta_clicked | `COUNT(goal_setting_email_cta_clicked) / COUNT(goal_setting_email_opened) * 100` |
| 30-day retention (target: +2–4pp vs. control) | goal_created (for attribution), churn events | Compare retention curves for treatment vs. control cohorts at day 30 |
| Modal dismissal rate (guardrail: <65%) | goal_setting_modal_interaction | `COUNT(dismissed) / COUNT(goal_setting_modal_impression) * 100` |

---

## 8. Open Questions

1. **What is the target number of daily active signups used for rollout planning?**
   - *Owner:* Growth / Analytics
   - *Default assumption:* Assume 100–200 daily new signups; rollout control allows gradual testing with smaller cohorts
   - *Resolved by:* Confirm with Growth team; adjust feature flag rollout schedule accordingly

2. **Can the email service send authenticated links that auto-login users without email verification loop?**
   - *Owner:* Backend / Email Infrastructure
   - *Default assumption:* Use one-time token in email link; token is valid for 24 hours; user lands directly on goal-creation template screen
   - *Resolved by:* Technical spike on email link authentication pattern

3. **What is the current email suppression list scope (opt-outs, invalid addresses, bounced accounts)?**
   - *Owner:* Data / Compliance
   - *Default assumption:* Standard email suppression rules apply (unsubscribed, hard bounces, etc.). Day 5 email batch excludes these accounts
   - *Resolved by:* Confirm suppression rules before scheduling day 5 email batch

4. **Should the "Custom Goal" option allow users to set a target amount and deadline on first creation, or keep it minimal?**
   - *Owner:* Product
   - *Default assumption:* Custom goal creation is two-step: (1) name only, (2) optional: add target + deadline. Minimize friction for day 1.
   - *Resolved by:* Prototype testing with users; refine based on feedback

5. **If a user creates a goal from the email link but then later opens the app, should they see the day 3–4 re-prompt again?**
   - *Owner:* Product / Engineering
   - *Default assumption:* No. Once `set_first_goal_complete` = true, neither day 1 nor day 3–4 re-prompt fires again, regardless of channel
   - *Resolved by:* Confirm logic in implementation

6. **What reassurance messaging specifically should appear in the day 5 email (beyond the provided copy)?**
   - *Owner:* Product / Marketing / Content
   - *Default assumption:* Email includes "We're here to help every step of the way" and a support link. Validate messaging resonates in user testing.
   - *Resolved by:* Content review and user research after prototype validation

7. **Should we test the benefit messaging ("2.6x more likely to stay on track", "78% more secure") via A/B testing, or are these primary copy?**
   - *Owner:* Product
   - *Default assumption:* These are primary copy for Phase 1. A/B test variants (different benefit angles) in Phase 2 if engagement is suboptimal.
   - *Resolved by:* Phase 1 launch; assess dismissal rates; adjust if needed

---

## Appendix: Hypothesis vs. EIM Mechanism

**EIM Mechanism (Original):** In-app onboarding prompt on day 2–3, targeting accounts with one linked account but no goal. Pre-populated templates. 50/50 holdout. Expected outcome: 19% → 28–30% goal-setter rate.

**Modified Mechanism (This PRD):** Hybrid approach combining in-app (day 1 + day 3–4 re-prompt) + email (day 5). Day 1 show adds urgency (sooner intervention). Day 3–4 re-prompt handles dismissals. Day 5 email catches accounts who avoid in-app interaction entirely. Different benefit messaging (in-app: "stay on track"; email: "feel more secure") tests assumption variation.

**Rationale for Changes:** User feedback requested earlier intervention (day 1 vs. day 2–3), safety-focused messaging in email, and fallback email for users who don't open the app. These changes increase activation leverage without adding complexity to Phase 1 engineering.

---

*PRD complete. Ready for review and Prototype Brief generation.*
