# PRD Format Reference

Complete format templates and worked examples for both outputs produced by the
hypothesis-to-prd skill.

---

## PRD Template

```markdown
# PRD: [Hypothesis title]

**Hypothesis source:** [EIM report filename] — Hypothesis [N]
**Author:** [name or "generated"]
**Date:** [date]
**Status:** Draft

---

## Problem Statement

[One paragraph. Written from the user's perspective. What are they trying to do?
Where does the current product leave them stranded? What does that cost them?
Ground the problem in the specific signal from the Evidence section — not the
business outcome.]

---

## Hypothesis

**We believe** [the specific mechanism — the intervention and who it targets]
**will** [the behavioural change or outcome]
**because** [the evidence — the signal and its magnitude].
**We'll know it worked when** [the primary success metric] reaches [target]
within [measurement window].

---

## Success Metrics

| Metric | Type | Baseline | Target | Measurement window |
|---|---|---|---|---|
| [Primary leading metric] | Primary | [value from EIM] | [target] | [days/weeks] |
| [Secondary lagging metric] | Secondary | [value from EIM] | [target] | 90 days |
| [Guardrail metric] | Guardrail | [current value] | Must not decrease | Ongoing |

---

## Scope

### In Scope
- [Specific surface, feature, or behaviour — numbered list]

### Out of Scope
- [Things that could be confused with this but are NOT being built]

### Assumptions and Dependencies
- [What must be true / available for this intervention to work]

---

## User Stories

**Story 1: [Name the scenario]**
As a [role], I want to [action] so that [outcome].

**Acceptance criteria:**
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

[Repeat for 3–6 stories total]

---

## Functional Requirements

### Trigger Logic
- **FR-01:** [Requirement] — *Must*
- **FR-02:** [Requirement] — *Must*

### UI / Surface
- **FR-03:** [Requirement] — *Must*
- **FR-04:** [Requirement] — *Should*

### Email / Notification (if applicable)
- **FR-05:** [Requirement] — *Should*

### Experiment / Feature Flag
- **FR-06:** [Requirement] — *Must*

---

## Analytics Instrumentation

| Event name | When it fires | Key properties |
|---|---|---|
| [event_name] | [trigger condition] | user_id, account_id, [segment fields], [variant] |

---

## Open Questions

1. **[Question]** — Owner: [team/person] | Default if unresolved: [assumption]
2. **[Question]** — Owner: [team/person] | Default if unresolved: [assumption]
```

---

## Prototype Brief Template

```markdown
# Prototype Brief: [Hypothesis title]

**Hypothesis source:** [EIM report filename] — Hypothesis [N]
**Date:** [date]
**Fidelity:** [Lo-fi / Mid-fi / Hi-fi]
**Owner:** [who is building and running this]

---

## TL;DR

[2–4 sentences. Explain the idea in plain language — what is being shown to the user, what behaviour it's intended to drive, and why the team believes this mechanism will work. No jargon. Should be readable by someone who hasn't seen the EIM report.]

---

## What We're Testing

[One sentence. The specific assumption — not the feature. Start with "We believe that..."]

---

## What the Prototype Must Show

1. [Specific screen or state — described from the customer's perspective]
2. [Specific interaction or moment]
3. [Specific outcome or confirmation state]

[3–5 items maximum. Each one should be something a customer can react to.]

---

## What the Prototype Does NOT Need to Do

- [Real data / live integrations]
- [Complete edge case handling]
- [Any feature outside the core test scenario]

---

## Fidelity Recommendation

**[Lo-fi / Mid-fi / Hi-fi]**

[One paragraph justifying the choice. Reference the type of assumption being tested.
If the hypothesis is about whether users notice a gap in their data, static frames
are sufficient. If the hypothesis is about whether a specific CTA drives action,
a clickable prototype is needed. Hi-fi is only needed when real-time behaviour
is the thing being tested.]

---

## Obvious Objections

The most likely critiques when this hypothesis is presented as a roadmap candidate. Each objection is paired with the honest answer and what evidence would close it.

---

**1. [Objection title]**

[The objection stated plainly. Why would a sceptic push back on this?]

*What closes it:* [What data, research, or validation would resolve this objection.]

---

**2. [Objection title]**

[Repeat for each major objection. Aim for 4–6. Cover: data validity, user experience risk, revenue linkage, segment justification, size of prize vs. build cost, and cannibalisation of existing flows.]

*What closes it:* [Resolution.]

---

## Customer Conversation Guide

### Setup (read to the customer before showing anything)

"[Context-setting script. Neutral — does not reveal what the feature does or what
you hope they will do. Sets up the scenario naturally.]"

### Tasks

**Task 1:** "[Natural prompt — not 'click the banner', but 'walk me through what
you'd do after publishing your first course']"

**Task 2:** "[Natural prompt]"

**Task 3 (optional):** "[Natural prompt]"

### Questions to ask after each task

- What did you expect to happen there?
- Was anything confusing or surprising?
- Would you do this in your own account? Why or why not?

### Hypothesis-specific questions

1. [Question targeting the core assumption — the thing that would prove or disprove
   the mechanism]
2. [Question about the value framing — does the user understand why this matters to them?]
3. [Question about the trigger or timing — would they encounter this at the right moment?]

### What a successful session looks like

**Validates the hypothesis:** [Specific customer behaviour or quote that would confirm
the mechanism would work. Not "they liked it" — what would they do?]

**Falsifies the hypothesis:** [Specific customer behaviour or response that would tell
you the mechanism is wrong. What would they say or do if the assumption is incorrect?]
```

---

## Worked Example: Directory Sync Banner (Clearpath H2)

### PRD

```markdown
# PRD: Employee Directory Sync — Day-7 Onboarding Banner

**Hypothesis source:** clearpath-eim-report.md — Hypothesis 2
**Date:** 2026-04-09
**Status:** Draft

---

## Problem Statement

HR and compliance admins who publish training courses in Clearpath often manage their
employee lists manually — adding learners one at a time, or relying on an import they
did at signup that immediately goes stale as the company hires or offboards people.
They don't realise their course assignment data is incomplete until someone asks why a
new hire never received mandatory training. By that point, the trust in the platform has
already eroded. The problem is not that admins don't want to sync their directory — it's
that the gap is invisible to them. There is no moment in the product that shows them how
many employees are unaccounted for.

---

## Hypothesis

**We believe** surfacing the gap between manually-assigned learners and total employee
count to admins who have not synced a directory, triggered on day 7 post-signup,
**will** increase the rate of HRIS connection or CSV employee upload within 14 days of
account creation
**because** 253 accounts that never completed `sync_employee_directory` churned at 28.1%
vs 7.2% for synced accounts (3.9x difference, n=253/n=347), and qualitative signals
suggest the skip is driven by deferred intent rather than active rejection of the feature.
**We'll know it worked when** the 14-day directory sync rate for new accounts increases
from 58% to 72% within 60 days of launch.

---

## Success Metrics

| Metric | Type | Baseline | Target | Measurement window |
|---|---|---|---|---|
| % of new accounts syncing directory within 14 days | Primary | 58% | 72% | 60 days |
| 90-day churn rate for accounts that saw the banner | Secondary | 28.1% (unsynced) | <18% | 90 days |
| Support tickets: "where do I add employees" | Guardrail | [current baseline] | Must not increase | 30 days |

---

## Scope

### In Scope
- In-app banner displayed on the Clearpath admin home screen
- Banner trigger logic: account has completed `publish_first_course`, has not completed
  `sync_employee_directory`, account age = 7 days (±1 day)
- Banner content: shows count of manually-assigned learners vs estimated total employees
  (from company_size field) to surface the gap
- Two CTAs: "Connect HRIS" (opens HRIS connector wizard) and "Upload employee CSV"
  (opens CSV import modal)
- Banner dismissal: only dismissed when sync is completed — not on close/ignore
- Analytics instrumentation for all banner interactions

### Out of Scope
- Changes to the HRIS connector or CSV import flows themselves (existing flows are used)
- A/B test of banner copy variants (single copy in v1)
- Any email or push notification version (in-app only in v1)
- Surfacing the banner to manager or learner roles

### Assumptions and Dependencies
- `company_size` field is populated at account creation and is accessible at runtime
  to compute estimated total employees
- `publish_first_course` completion is available as a real-time account attribute
- Existing HRIS connector and CSV import flows are functional and do not require changes
- Feature flag tooling is available to enable staged rollout

---

## User Stories

**Story 1: Admin sees the banner on day 7**
As an admin who has published a course but not connected my directory, I want to see a
clear signal on my home screen that my employee list may be incomplete, so that I
understand the risk before someone asks why a learner was missed.

**Acceptance criteria:**
- [ ] Banner appears on the home screen for qualifying accounts on day 7 (±1 day)
- [ ] Banner shows the count of learners currently assigned vs estimated employee count
- [ ] Banner is not shown to manager or learner roles
- [ ] Banner does not appear if `sync_employee_directory` is already completed

**Story 2: Admin connects via HRIS**
As an admin who wants to sync my directory, I want to click directly into the HRIS
connector wizard from the banner, so that I don't have to navigate there manually.

**Acceptance criteria:**
- [ ] "Connect HRIS" CTA opens the existing HRIS connector wizard in a modal or new page
- [ ] On successful HRIS connection, the banner is permanently dismissed
- [ ] An analytics event fires on CTA click with account_id and variant

**Story 3: Admin uploads a CSV instead**
As an admin whose company doesn't use a supported HRIS, I want to upload an employee
CSV as an alternative, so that I'm not blocked by the absence of a native integration.

**Acceptance criteria:**
- [ ] "Upload CSV" CTA opens the existing CSV import modal
- [ ] On successful CSV upload, the banner is permanently dismissed

**Story 4: Banner persists until action is taken**
As a product team, we want the banner to remain visible until the sync is complete, so
that admins who ignore it on day 7 continue to see it on subsequent visits.

**Acceptance criteria:**
- [ ] Banner is not closeable via a dismiss/X button
- [ ] Banner reappears on every home screen visit until sync is completed
- [ ] Banner does not reappear after sync is completed, even on return visits

---

## Functional Requirements

### Trigger Logic
- **FR-01:** Banner is displayed when: `publish_first_course = true` AND
  `sync_employee_directory = false` AND `account_age_days >= 7` — *Must*
- **FR-02:** Banner is suppressed once `sync_employee_directory = true` — *Must*
- **FR-03:** Banner is shown to admin role only — *Must*

### UI / Surface
- **FR-04:** Banner appears in the top section of the admin home screen, above the
  main content area — *Must*
- **FR-05:** Banner displays: assigned learner count, estimated employee count
  (derived from company_size), and gap — *Must*
- **FR-06:** Banner includes two CTAs: "Connect HRIS" and "Upload employee CSV" — *Must*
- **FR-07:** Banner has no close/dismiss button — *Must*
- **FR-08:** Banner copy references the specific course published (by name) — *Should*

### Analytics Instrumentation
- **FR-09:** `banner_shown` event fires when banner is rendered — *Must*
- **FR-10:** `banner_cta_clicked` event fires on each CTA click, with `cta_type`
  property (`hris` or `csv`) — *Must*
- **FR-11:** `directory_sync_completed` event fires on successful sync, with
  `source` property (`hris` or `csv`) and `days_since_account_creation` — *Must*

### Experiment
- **FR-12:** Feature flag required for staged rollout (start at 20% of qualifying
  accounts, ramp to 100% over 2 weeks) — *Must*

---

## Analytics Instrumentation

| Event name | When it fires | Key properties |
|---|---|---|
| `banner_shown` | Banner renders on home screen | account_id, account_age_days, learner_count, employee_estimate |
| `banner_cta_clicked` | Admin clicks either CTA | account_id, cta_type (hris/csv) |
| `directory_sync_completed` | HRIS or CSV sync completes | account_id, source, days_since_account_creation, days_since_banner_first_shown |

---

## Open Questions

1. **What is the estimated employee count source?** We plan to use `company_size` bucket
   midpoints. Is a more precise employee count available from the signup form?
   Owner: Product / Data | Default: use company_size midpoints (small=35, mid=150, large=1000)

2. **What is the suppression logic for trial accounts?** Should the banner appear for
   trial accounts, or only paid/converted accounts?
   Owner: Growth | Default: show to all account types in v1, suppress in v2 if needed

3. **Who owns the HRIS connector and CSV import flows?** Confirming no changes are
   needed to those flows before this ships.
   Owner: Engineering | Default: treat both as dependencies with no changes required
```

---

### Prototype Brief

```markdown
# Prototype Brief: Employee Directory Sync Banner

**Hypothesis source:** clearpath-eim-report.md — Hypothesis 2
**Date:** 2026-04-09
**Fidelity:** Mid-fi (clickable Figma prototype, no real data)
**Owner:** [designer / PM running the session]

---

## What We're Testing

We believe that showing admins the gap between their current learner count and their
estimated total employee count will create enough urgency for them to connect their
HRIS or upload a CSV within the same session — without needing to explain why it matters.

---

## What the Prototype Must Show

1. The admin home screen after a first course has been published, with the directory
   gap banner visible in the top section
2. The banner content: assigned learner count, estimated employee count, and the gap
   presented as a number (not a percentage)
3. Both CTA options ("Connect HRIS" and "Upload employee CSV") and what happens when
   each is clicked (opening the respective flow)
4. A confirmation state after a successful sync: banner gone, replaced with a
   completion indicator

---

## What the Prototype Does NOT Need to Do

- Show real account data — use fixed placeholder numbers (e.g. "12 learners assigned,
  ~85 employees in your company")
- Demonstrate the full HRIS connector or CSV import flow — a single "connecting..."
  loading screen leading to a success state is sufficient
- Handle edge cases (e.g. company_size not set, HRIS auth failure)
- Be responsive / mobile-optimised

---

## Fidelity Recommendation

**Mid-fi (clickable Figma prototype)**

The assumption being tested is whether the gap framing creates urgency — not whether
the UI is pixel-perfect. Static frames cannot test whether the CTA is compelling;
the user needs to be able to click through to the sync flow to understand the full
moment. A clickable Figma prototype gives us that without requiring any engineering
time. Real data is not needed because the insight is about the framing, not the accuracy
of the numbers.

---

## Customer Conversation Guide

### Setup

"I'm going to show you an early version of something we're working on in Clearpath.
It's not finished and some things won't work — that's fine, we're not testing you,
we're testing the design. I'll ask you to think out loud as you go. There are no wrong
answers. The most helpful thing you can do is tell me when something is confusing or
when you'd do something differently."

### Tasks

**Task 1:** "You've just published your first training course in Clearpath. Take a
look at your home screen and tell me what you notice."

**Task 2:** "Based on what you're seeing, what would you do next?"

**Task 3:** "Go ahead and do that — walk me through your thinking as you go."

### Questions to ask after each task

- What did you expect to see when you landed on this screen?
- Was there anything that surprised you or that you weren't sure about?
- Would you take this action in your actual account? What would make you more or less
  likely to?

### Hypothesis-specific questions

1. "When you saw the numbers on that banner — [X] learners assigned, ~[Y] total employees
   — what did that tell you? Was it useful information?"
2. "If you saw that banner and you were in the middle of other work, would you deal with
   it now or come back to it? What would make you come back?"
3. "Is connecting your HRIS or uploading a CSV something you'd feel comfortable doing
   yourself, or would you need someone else involved? Who?"

### What a successful session looks like

**Validates the hypothesis:** The customer notices the gap number unprompted, expresses
concern about it ("wait, that means people aren't getting assigned"), and clicks through
to the HRIS or CSV option without being prompted. They say they would do this in their
own account.

**Falsifies the hypothesis:** The customer notices the banner but doesn't understand
why the gap matters ("I'll just add people manually as they need training"), or they
understand it but say connecting the HRIS is something IT handles and they couldn't do
it themselves. Either response suggests the mechanism won't drive the behaviour we expect.
```
