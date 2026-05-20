# Skills: AI-Powered Product Workflow

## What this is

Most AI products fail — not because they were built badly, but because nobody answered three questions before building:

- **What does the data actually show?** (Evidence)
- **What is it worth to fix?** (Impact)
- **What specifically should be built?** (Mechanism)

EIM is the framework that forces those three answers before anything gets built. These skills are the workflows that produce them — from real company data, in a form a product team can act on and defend.

The output is not a data report. It is a defensible product hypothesis: specific numbers, quantified business impact, and a mechanism precise enough that an engineer can scope it, a PM can brief it, and a stakeholder can fund it.

This is the discovery machine you build and use throughout the Velocity course. The skills are yours permanently — they work on any company, any dataset, any product decision.

> **The mindset that makes it work:** Claude finds the patterns. You decide which ones matter. EIM is the thinking. Skills are the execution. Together they're your system.

---

## The workflow at a glance

```
/eim-context                  ← do you have the right context to analyse?
        ↓
/eim-product-analyst          ← analyse data, generate EIM hypotheses
        ↓
      PAUSE                   ← you validate the findings against what you know
        ↓
/hypothesis-to-prd            ← turn one hypothesis into a PRD and/or prototype brief
        ↓
      PAUSE                   ← you confirm E/I/M extraction
        ↓
      PAUSE                   ← explore solution options, pick the right approach
        ↓
      PAUSE                   ← review PRD draft before prototype brief
        ↓
   Output files               ← PRD.md, Prototype Brief.md
        ↓
        ├── /build-html-prototype      ← fast: clickable HTML file, browser-ready
        │
        ├── /figma-prototype-builder   ← build screens directly into a Figma file
        │       recommended first: run /figma-make-spec on your Figma file (see below)
        │       auto-discovers: PRD, Prototype Brief, and Figma spec from the project folder
        │       output: new Figma page per hypothesis, frames + prototype links wired
        │
        └── Figma Make (manual)        ← paste the build prompt from the brief into Figma Make

   Have an existing Figma file to build from?
        ↓
        /figma-make-spec               ← run this first on your source Figma file
                requires: Figma design file URL
                output: [product]-figma-spec.md — design tokens, component inventory,
                        screen specs, engineering notes
                ↓
                feeds into /figma-prototype-builder automatically (picked up in Phase 0)
                — gives much more reliable token + component extraction than live MCP scraping
```

---

## Skill 1: `/eim-context`

**What it does:** Checks whether you have the right *kinds* of information before the analysis starts — and synthesises everything it finds into a context document the analysis reads first.

Quality of hypotheses depends almost entirely on product context. Without it, the analysis produces statistically coherent signals attached to mechanisms that don't match how the product actually works. This skill catches that before it happens.

**When to use it:** Once per company, before running `/eim-product-analyst` for the first time. Re-run it if the product has changed significantly or you're switching to a different data source.

**Trigger phrases:**
- "Set up EIM for [company]"
- "Check if we have enough to run EIM"
- "Prepare for EIM analysis"

**What it needs (by kind, not by filename):**
- Behavioural data — events, feature usage, session records, onboarding steps. Can be files, an analytics tool connection (Amplitude, Mixpanel, PostHog), or a database export
- Outcome data — what happened to those users: churned, upgraded, converted. A column, a joined table, or a status field
- Product understanding — what the product does, who it's for, how it's priced. A document, a paste, or a description
- Customer voice — interview notes, support themes, sales feedback (optional but valuable)

**What it produces:**
- A `[company]-context-base.md` file that `/eim-product-analyst` reads automatically as its first step

**The gate:**
- Hard stop if no behavioural data or outcome variable is accessible
- Warning (but proceeds) if product context is absent
- Note (no block) if customer voice is missing

---

## Skill 2: `/eim-product-analyst`

**What it does:** Analyses product, customer, or usage data and produces a set of EIM hypotheses — each grounded in evidence from the data, quantified by business impact, and paired with a specific intervention.

**When to use it:** You have data files and want to know where to focus. You don't need to frame the question — just drop the data and ask for signals.

**Trigger phrases:**
- "Analyse my data"
- "What's driving churn?"
- "Find expansion opportunities"
- "Run EIM on this"
- "Where should we focus?"

**What it needs:**
- One or more data files (CSV, JSON, TSV, Parquet)
- Optional: a product context document (any `.md` or `.txt` describing the product)
- Optional: a data dictionary

**What it produces:**
- 3–5 EIM hypotheses ranked by confidence × impact
- A "What We Ruled Out" section explaining discarded signals
- Recommended next steps

**Where it pauses for you:**
1. After generating hypothesis titles — before writing the full report, it checks the findings against your qualitative knowledge

---

## Skill 3: `/hypothesis-to-prd`

**What it does:** Takes a single EIM hypothesis and produces a PRD, a Prototype Brief, or both — depending on what you ask for.

**When to use it:** After `/eim-product-analyst`, or any time you have a hypothesis (from any source) and want to move it toward execution or customer testing.

**Trigger phrases:**
- "Turn this into a PRD"
- "Write a PRD for H2"
- "Build a prototype brief"
- "Make this ready for the team"
- "What would we actually build?"

**What it needs:**
- An EIM hypothesis — either from a file, pasted inline, or referenced by number (e.g. "H2")
- Optional: Figma file URLs or design references (used to ground the PRD in existing components)

**What it produces:**
- **PRD** (`[product]-prd-[hypothesis].md`) — problem statement, hypothesis, success metrics, scope, user stories, functional requirements, analytics instrumentation, open questions
- **Prototype Brief** (`[product]-prototype-[hypothesis].md`) — TL;DR, what to test, what to build, fidelity recommendation, build prompt (paste into Claude Code / Figma Make / Lovable), obvious objections, customer conversation guide

**Where it pauses for you:**
1. At the start — asks whether you want a PRD, Prototype Brief, or both
2. After parsing the hypothesis — confirms the E/I/M extraction before writing anything
3. Solution exploration — presents 3–4 distinct ways to address the problem (including the EIM Mechanism as one option), asks you to choose, combine elements across options, or propose something different — before writing a single requirement
4. After the PRD draft — review and correct before the Prototype Brief is produced

---

## Skill 4: `/build-html-prototype`

**What it does:** Takes a Prototype Brief (or a hypothesis with enough context) and builds a single self-contained HTML file — clickable, browser-ready, no dependencies, no Figma required.

**When to use it:** You have a Prototype Brief and want something you can open immediately in a browser and put in front of a customer. Faster than Figma for simple flows, and easier to iterate on in real time during a session.

**Trigger phrases:**
- "Build the prototype"
- "Make it clickable"
- "Build me an HTML version"
- "I want something I can click through"
- "Generate the HTML"

**What it needs:**
- A Prototype Brief file — or a build prompt pasted inline
- Optional: a branding folder with colour tokens or fonts

**What it produces:**
- A single `.html` file saved alongside the Prototype Brief
- All CSS and JS embedded — open it in any browser, share it as a file, no server needed

**Where it pauses for you:**
1. After reading the brief — confirms the screen plan and interactions before writing any code
2. After delivery — offers an iteration loop for copy, layout, or interaction changes

**When to use Figma Make instead:**
If you need high-fidelity mobile frames, device mockups, or output that lives in your design system — use the build prompt from the Prototype Brief in Figma Make. Use this skill when you want something fast and browser-native that you can tweak in plain text.

---

## End-to-end example

```
You:  /eim-product-analyst
      [drops fitbody_churn.csv]

AI:   Analyses data → presents 4 hypothesis titles for your review
      PAUSE: "Do these align with what you're hearing from customers?"

You:  "Yes — H2 and H3 look right. H1 feels like noise, skip it."

AI:   Writes full EIM report with H2, H3, H4
      Saves to: fitbody/fitbody-eim-report.md

---

You:  /hypothesis-to-prd
      "Use H2 from fitbody/fitbody-eim-report.md"

AI:   "Do you want PRD, Prototype Brief, or both?"

You:  "Both"

AI:   Reads H2, extracts E/I/M
      PAUSE: "Here's what I extracted — does this look right?"

You:  "Yes, proceed"

AI:   Writes PRD draft
      PAUSE: "Review the PRD — any corrections before I write the brief?"

You:  "Looks good, proceed"

AI:   Writes Prototype Brief
      Saves to: fitbody/fitbody-prd-h2-[slug].md
                fitbody/fitbody-prototype-h2-[slug].md

---

You:  /build-html-prototype
      "Use fitbody/fitbody-prototype-h2-[slug].md"

AI:   Reads the brief, plans the screens
      PAUSE: "Here are the 3 screens and interactions I'm planning — does this look right?"

You:  "Yes, build it"

AI:   Builds the HTML file
      Saves to: fitbody/fitbody-prototype-h2-[slug].html
      "Open it in a browser. 3 screens, all interactions wired. Let me know what to change."
```

---

## Skill 5: `/figma-make-spec`

**What it does:** Reads a Figma file using the Figma MCP and produces a complete product + engineering specification — covering design tokens, component inventory, screen-by-screen specs, interaction behaviour, accessibility requirements, and engineering notes.

**When to use it:** You have a Figma file and need to hand it off to engineering, or you want a structured spec before writing a PRD.

**Trigger phrases:**
- "Generate a spec from this Figma file"
- "Turn this Figma design into a spec"
- "Document this design system"

**What it needs:**
- A Figma file URL (must be a `/design/` URL, not a team/project browser URL)

**What it produces:**
- A structured Markdown spec covering: brand identity, colour system, typography, design system architecture, interaction & motion, screen-by-screen breakdown, component inventory, accessibility requirements, and engineering notes

---

## Skill 6: `/figma-prototype-builder`

**What it does:** Builds a clickable prototype directly inside Figma using the Figma MCP — creating a new page per hypothesis, importing existing components from the source file, laying out screens, and wiring navigation flows. Auto-discovers the PRD and prototype spec from the project folder.

**When to use it:** After `/hypothesis-to-prd` has produced a PRD and Prototype Brief and you want the prototype built in Figma rather than HTML.

**Trigger phrases:**
- "Build the prototype in Figma"
- "Write the H1 prototype to Figma"
- "Create the Figma screens for H2"

**What it needs:**
- A Figma file URL (must be a file you own — not a community/read-only file)
- Optional: hypothesis number (e.g. "H1") — if omitted, lists available hypotheses and asks

**What it produces:**
- A new Figma page named after the hypothesis (e.g. "H1 – Solo Admin Trap")
- Frames for each screen defined in the Prototype Brief, positioned in labelled sections
- Prototype connections wired between screens per the navigation flow
- A build summary: screens created, components used, gaps flagged

**Important:** The source Figma file must be a duplicate you own. Community files are read-only — the skill will stop and ask you to duplicate before proceeding.

---

## Tips

**Running just the prototype brief:** If you already have a PRD or a clear hypothesis and just need something to test with customers, choose option B at the first pause. The skill skips straight to the brief.

**Pointing to a specific hypothesis:** Say "H2" or quote the title. If you don't specify, the skill lists the available hypotheses and asks you to choose.

**Using Figma files:** If you have Figma URLs in the conversation or linked from a product context doc, the skill will pull design context before writing the PRD. This makes the functional requirements significantly more accurate.

**Saving outputs:** All files are saved to the same directory as your source EIM report. If there's no source file, they're saved to the current working directory.

**Building the HTML prototype without a brief:** You can skip straight to `/build-html-prototype` and paste a hypothesis or describe the screens you want. The skill will infer the structure and confirm it with you before building.
