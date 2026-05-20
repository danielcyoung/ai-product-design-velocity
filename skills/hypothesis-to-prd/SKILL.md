---
name: hypothesis-to-prd
description: >
  Use this skill when the user wants to turn an EIM hypothesis into a Product Requirements
  Document (PRD) and/or a prototype brief. Triggers include: "turn this into a PRD",
  "write a PRD for this hypothesis", "build a prototype brief", "make this ready for
  the dev team", "create requirements for this", "what would we actually build", or
  any time the user references a specific EIM hypothesis and wants to move it toward
  execution. Works from a hypothesis pasted directly into the conversation, from a
  selected EIM report, or from a file path. If the user specifies a hypothesis number
  (e.g. "H2") or title, target that hypothesis. If unspecified, ask which one.
---

# Hypothesis to PRD

This skill takes a single EIM hypothesis — Evidence, Impact, Mechanism — and produces
two outputs:

1. **A Product Requirements Document (PRD)** — structured for a development team to scope,
   estimate, and build the intervention described in the Mechanism.

2. **A Prototype Brief** — a focused spec for building a lightweight prototype (lo-fi or
   clickable) that can be shown to customers to validate the hypothesis before full build.

The outputs are distinct documents with different audiences. The PRD is for engineers and
designers. The Prototype Brief is for whoever is building the test artefact and for
the customer conversation itself.

---

## Step 0 — Establish what the user needs

Before reading any files, ask:

> "What do you need from this?
> - **A** — PRD only (for scoping and build)
> - **B** — Prototype Brief only (for customer testing)
> - **C** — Both
>
> If you're not sure, go with C."

Carry the choice forward. If A: skip Step 3 entirely. If B: skip Step 2 entirely (go straight from Step 1 PAUSE to Step 3). If C: run all steps in sequence.

---

## Step 0.5 — Locate and read the hypothesis

**If the user has provided a file path or selected text:**
Read it directly. Extract the full E, I, M content for the target hypothesis.

**If the user has referenced an EIM report file:**
Read the full report and extract the target hypothesis. If no specific hypothesis is named,
list the hypothesis titles and ask the user to confirm which one to use.

**If the hypothesis is pasted inline:**
Use it as-is. Check whether E, I, and M sections are all present. If any part is missing
or vague, note it — do not invent content to fill gaps.

**Also look for:**
- A product context document (anything named `*product-context*`, `*context*`, `README*`)
- A data dictionary (anything named `*dictionary*`, `*schema*`)

If a product context exists, read it. It tells you what features, plan tiers, and user
roles exist — essential for writing accurate requirements.

---

## Step 1 — Parse the hypothesis into its components

Before writing anything, extract and restate these elements clearly:

**From Evidence:**
- The specific behavioural signal (what behaviour? which users? what rate?)
- The comparison group
- The outcome it predicts (churn? upgrade? activation?)
- The segment where the effect is strongest

**From Impact:**
- The population at risk / opportunity size (n=?)
- The ARR at risk or incremental ARR opportunity
- The improvement assumption used (25%? 30%? what scenario?)

**From Mechanism:**
- The product surface (where does the intervention appear?)
- The trigger condition (what causes it to fire?)
- The target user (role, segment, state)
- The intervention itself (what does the user see or experience?)
- The success metric and test approach

If any of these is unclear or missing from the hypothesis, flag it before proceeding.
Do not invent mechanism details — surface the gap and note it as an open question.

---

---
> 🛑 **PAUSE — Confirm hypothesis parsing before writing anything**

Present the extracted E, I, M components to the user in a concise summary. Ask:

> "Here's what I've extracted from the hypothesis. Does this accurately capture the signal, the opportunity, and the intervention before I start writing?
> - **Evidence:** [summary]
> - **Impact:** [summary]
> - **Mechanism:** [summary]
>
> Any corrections or additions before I proceed to the PRD?"

Do not proceed until the user confirms or corrects.

---

## Step 1.5 — Explore solution options before writing the PRD

The Mechanism in an EIM hypothesis is a starting point, not a final answer. It is the
most obvious solution suggested by the data — not necessarily the right one to build.
Before writing a single requirement, explore the solution space with the user.

**Generate 3–4 distinct options** for how the Evidence/Impact problem could be addressed.
Always include the EIM Mechanism as one of the options (usually Option A), but treat it
as a candidate, not the default. The other options should vary meaningfully — not just
surface-level rewordings of the same idea.

Vary the options along dimensions that matter:

- **Where the intervention lives** — in-product, in-email, in a CS workflow, in onboarding
- **Who initiates it** — the product surfaces it proactively, the user discovers it, a human reaches out
- **When it fires** — at the moment of friction, before friction occurs, after the damage is done
- **What it asks the user to do** — zero-effort (automatic), low-effort (one click), effortful (guided flow)
- **What it bets on** — different options test different assumptions about why the problem exists

**Format each option as:**

---
**Option [A/B/C/D]: [Short name]**

*What it is:* One sentence. The intervention in plain language.

*What the user experiences:* What they see, when they see it, what they do.

*Bets on:* The core assumption this option makes about why the problem exists. If this assumption is wrong, the option won't work.

*Build effort:* Low / Medium / High — and one sentence on why.

*Best if:* The condition under which this is the right choice.

*Trade-off:* What you give up by choosing this over the alternatives.

---

After presenting all options, ask:

> "These are the main ways to address this problem. A few things to consider before choosing:
>
> - Which assumption feels most likely to be true based on what you know from customers?
> - Which option would you be most confident defending to your team?
> - Is there a constraint — time, engineering capacity, existing infrastructure — that rules any out?
>
> You can pick one, combine elements from multiple options, or describe something different.
> What direction do you want to go?"

**Wait for the user's response before writing anything.** Incorporate their choice — including
any modifications or combinations they describe — into the PRD. The chosen solution becomes
the Mechanism the PRD is written around.

If the user picks an option that is significantly different from the EIM Mechanism, note this
in the PRD's Hypothesis section: "Note: the EIM Mechanism suggested [X]. After solution
exploration, the team chose [Y] because [reason given]."

---

## Step 2 — Design context review (if Figma files or design references are available)

Before writing the PRD, check whether any of the following exist:
- A Figma file URL in the conversation or linked from the product context document
- A design system reference or branding folder
- An existing codebase with UI components

**If Figma files are available:** Use the Figma MCP (`get_design_context`, `get_variable_defs`, `get_metadata`) to extract:
- Relevant existing components and their names
- Design tokens (colours, spacing, typography)
- Existing analytics events already instrumented in similar flows

Summarise findings in a table:

| Element | Current Implementation | Relevance to This Intervention |
|---|---|---|
| [Component name] | [Where it exists] | [How it could be reused] |

**If no design references exist:** Note this and proceed. The PRD scope section should flag that design context is not yet available.

This step prevents the PRD from specifying UI that ignores what already exists in the product. Reference the design context table when writing the Scope and Functional Requirements sections.

---

## Step 3 — Produce the PRD

Read `references/prd-format.md` for the full format spec.

The PRD has the following sections. Follow them in order. Do not skip sections.

### 1. Problem Statement
One paragraph. Written from the perspective of the user experiencing the problem, not
the company experiencing the churn. What is the user trying to do? Where are they failing?
What is the cost of that failure to them?

Ground this in the Evidence. Use the specific signal (e.g. "42% of admins who publish
a course never connect a directory source") as the problem definition — not the business
metric (churn rate).

### 2. Hypothesis
Restate the full EIM hypothesis in condensed form:
- **We believe** [the mechanism] **will** [the outcome]
- **Because** [the evidence]
- **We'll know it worked when** [the success metric]

This is the single-sentence (or three-line) version that the team can keep visible during
build. It must be falsifiable.

### 3. Success Metrics
Two tiers:

**Primary metric (leading):** The behavioural metric that changes fastest and is directly
caused by the intervention. Should be measurable within days or weeks of launch.

**Secondary metric (lagging):** The business outcome from the EIM impact section
(`churned_90d`, `upgraded_90d`, etc.). Measured over 60–90 days.

**Guardrail metric:** What must not get worse. Usually a support ticket rate, error rate,
or engagement metric adjacent to the intervention.

For each metric, specify: what it is, how it is measured, the baseline value (from the
EIM evidence), and the target. Set targets based on what would justify the build cost in
a roadmap review — use the EIM impact estimates as the anchor.

### 4. Scope

**In scope:** List the specific features, surfaces, and behaviours the intervention requires.
Be specific — name the UI surface, the trigger logic, the email or notification system,
the user role, any feature flag or experiment tooling required.

**Out of scope:** Explicitly name things that could be confused with this feature but
are not being built in this iteration. This prevents scope creep.

**Assumptions and dependencies:** What must be true for this to work? (e.g. "requires
that HRIS connection status is available as an account attribute at runtime")

### 5. User Stories
Write 3–6 user stories. Format:

> As a [role], I want to [action] so that [outcome].
> **Acceptance criteria:**
> - [specific, testable condition]
> - [specific, testable condition]

Stories should cover: the happy path, the primary edge case, and the admin/operator view
(if relevant). Do not write more than 6 — if there are more, the scope is too wide.

### 6. Functional Requirements
Numbered list of specific, testable requirements. Each one should be answerable with
"pass" or "fail" by a QA engineer. Group by area (trigger logic, UI, email/notification,
analytics instrumentation).

Format:
> **FR-01:** [Requirement statement]
> *Priority: Must / Should / Could*

Must = the intervention doesn't work without it.
Should = significantly reduces effectiveness if missing.
Could = nice to have, defer if time-constrained.

### 7. Analytics Instrumentation
List the specific events that must be tracked for the success metrics to be measurable.
For each event:
- Event name
- When it fires
- Properties captured (user_id, account_id, segment, variant if A/B)

This section must be written before build starts — instrumentation added as an afterthought
is usually wrong.

### 8. Open Questions
A numbered list of unresolved decisions that the team needs to answer before or during
build. Include: the question, who owns the answer, and what the default assumption is
if it is not resolved before build begins.

---
> 🛑 **PAUSE — Review PRD draft before producing the prototype brief**

Present the PRD to the user and ask:

> "PRD draft is complete. Before I move on to the prototype brief:
> - Does the scope accurately reflect what you want to build?
> - Are the success metric targets right?
> - Any functional requirements missing or wrongly prioritised?
> - Open questions — are there any you can resolve now?
>
> Say 'proceed' when ready, or give me corrections first."

Do not produce the prototype brief until the user confirms.

---

## Step 4 — Produce the Prototype Brief

The Prototype Brief is a separate, shorter document. Its audience is whoever is building
the test artefact (designer, no-code builder, or engineer building a throwaway UI), and
the person running the customer conversation.

Read `references/prd-format.md` for the prototype brief format.

### 0. TL;DR
2–4 sentences in plain language. What is being shown to the user, what behaviour it's intended to drive, and why the team believes the mechanism will work. No jargon. Should be readable by someone who hasn't seen the EIM report. Write this first — if you can't summarise it clearly in 4 sentences, the hypothesis isn't sharp enough yet.

### 1. What We're Testing
One sentence. The specific hypothesis being tested — not the feature, the assumption.

> "We believe that surfacing the gap between manually-assigned learners and total employee
> count will motivate admins to connect their HRIS within 7 days."

This is distinct from the PRD problem statement. The PRD describes what to build. The
prototype brief describes what assumption to test.

### 2. What the Prototype Must Show
A list of the specific moments, flows, or states the prototype needs to demonstrate.
Keep it minimal — a prototype that demonstrates 3 things tests 3 things. More than that
and you can't isolate the signal.

Each item should be:
- A specific screen, state, or interaction
- Described in terms of what the customer will see and do — not what the system does

### 3. What the Prototype Does NOT Need to Do
Explicit list of what to leave out. This is the most important section for keeping the
prototype lean. Real data, real integrations, complete edge case handling — all of these
are usually out of scope for a prototype.

### 4. Fidelity Recommendation
One of: **Lo-fi (static slides / Figma frames)**, **Mid-fi (clickable prototype, no real
data)**, or **Hi-fi (working feature, real data)**. With a one-paragraph justification.

For most hypothesis tests, lo-fi or mid-fi is correct. Hi-fi prototypes are appropriate
only when the hypothesis is about a specific interaction quality that cannot be tested
without real behaviour (e.g. a real-time notification, an AI-generated suggestion).

### 6. Build Prompt
A self-contained prompt that can be pasted directly into any prototype-building tool —
Claude Code (HTML/CSS/JS), Lovable, Figma Make, or similar — to generate a working or
static prototype without further explanation.

The prompt must be fully standalone: someone should be able to copy it into a fresh
session with no prior context and get a usable prototype out. It should include:

- **What to build:** The specific screens and states from "What the Prototype Must Show",
  described as UI instructions (layout, components, copy) not as product requirements
- **Placeholder data:** Exact copy and numbers to use (don't leave blanks the tool has
  to guess)
- **Interactions:** Which elements are clickable and what happens when clicked — even in
  a lo-fi prototype, name the transitions
- **What to leave out:** Explicitly name what not to build so the tool doesn't add scope
- **Style guidance:** Minimal — clean, professional SaaS UI is sufficient unless the
  product has a strong existing visual identity to match

Write the build prompt in a fenced code block so it can be copied cleanly.

### 7. Obvious Objections
The most likely critiques when this hypothesis is presented as a roadmap candidate. Aim for 4–6 objections. Cover the obvious angles: data validity (is the benchmark real?), user experience risk (will this annoy users?), revenue linkage (how does this connect to money?), segment justification (why this segment?), size of prize vs. build cost (is it worth it?), and cannibalisation (does this conflict with existing flows?).

For each objection: state it plainly, then give the honest answer and what evidence would close it.

### 8. Customer Conversation Guide
This is used in the session where the prototype is shown to customers.

**Setup (tell the customer):** One paragraph. What context to give before showing anything.
No leading language — do not tell them what the feature is supposed to do.

**Tasks (ask the customer to do):** 2–4 tasks, written as natural prompts. Not "click the
banner" — instead "imagine you've just published your first course. What would you do next?"

**Questions to ask after each task:**
- What did you expect to happen?
- What was confusing, if anything?
- Would you do this? Why or why not?

**Hypothesis-specific questions:** 2–3 questions targeted at the core assumption being
tested. These should reveal whether the mechanism would work, not just whether the UI is
clear.

**What a successful session looks like:** One paragraph. Describe the customer behaviour
that would validate the hypothesis, and the behaviour that would falsify it. Be specific —
not "they liked it" but "they completed the task without prompting and said they would do
this in their own account."

---

## Step 5 — Output format

Produce two separate files. Do not combine them into one response or one file.

**File 1 — PRD:**
Name: `[product-slug]-prd-[hypothesis-slug].md`
Example: `flowmind-prd-h2-revops-integration-milestone.md`

**File 2 — Prototype Brief:**
Name: `[product-slug]-prototype-[hypothesis-slug].md`
Example: `flowmind-prototype-h2-revops-integration-milestone.md`

Save both files to the same directory as the source EIM report. If the source report
is in `flowmind/`, save both files to `flowmind/`. If no source file location is clear,
save to the current working directory and tell the user where they were saved.

Both files should be written in plain markdown, ready to be copied into Notion,
Linear, or a shared doc without reformatting. After saving, confirm the two file paths
to the user.

---

## Step 6 — Sense-check before delivering

- [ ] Is the PRD Problem Statement written from the user's perspective, not the company's?
- [ ] Is the Hypothesis section falsifiable (does it name a metric that can prove it wrong)?
- [ ] Does every Success Metric have a baseline value and a target?
- [ ] Are Out of Scope items explicitly named?
- [ ] Does each user story have testable acceptance criteria?
- [ ] Are FR priorities (Must/Should/Could) assigned?
- [ ] Is the analytics instrumentation section complete enough that a PM could QA it?
- [ ] Is the TL;DR readable in plain language by someone who hasn't seen the EIM report?
- [ ] Does the Obvious Objections section cover data validity, UX risk, revenue linkage, segment justification, size of prize, and cannibalisation?
- [ ] Is the Prototype Brief's "What We're Testing" different from the PRD's problem statement?
- [ ] Is the prototype fidelity justified?
- [ ] Are the customer conversation tasks written as natural prompts (not "click X")?

If any box is unchecked, fix it before outputting.

---

## Common Pitfalls

**PRD that is just the Mechanism restated**
The Mechanism in an EIM hypothesis is a starting point, not a requirement. The PRD must
translate it into testable acceptance criteria, edge cases, and instrumentation. If the
PRD just rephrases the Mechanism in bullet points, it hasn't added value.

**Prototype brief that is a mini-PRD**
The prototype brief tests an assumption, not a feature. If it lists functional requirements,
it has become a PRD. Strip it back to: what will customers see, what will you learn, and
how will you know if the assumption is right or wrong.

**Success metrics without baselines**
"Increase HRIS sync rate" is not a metric. "Increase HRIS sync rate from 58% to 75% within
30 days of account creation (baseline: 58% from EIM analysis, n=347)" is a metric.

**User stories that aren't stories**
"The system sends an email" is not a user story. "As an admin who hasn't synced my directory,
I want to receive a reminder that shows how many employees are missing from my course
assignments, so I can understand the impact of the gap before deciding whether to sync" is
a user story.

**Open questions left empty**
Every PRD has open questions. If none are listed, the author hasn't looked hard enough.
Common ones: "Who owns the email send? What's the suppression logic if the user has opted
out of product emails? What happens if the account is in a trial period?"
