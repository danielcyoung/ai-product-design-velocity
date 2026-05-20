---
name: eim-context
description: >
  Run this skill before /eim-product-analyst to establish whether you have enough
  context to produce quality hypotheses. It checks for the right KINDS of information
  (behavioural data, outcome data, product understanding, customer voice) regardless of
  how that information is stored — CSV files, MCP analytics connections, pasted text,
  or documents. It then synthesises everything it finds into a context-base file that
  the EIM analysis reads first. Use when starting a new company analysis, when the data
  source has changed, or when the product context is stale. Triggers include: "set up
  EIM for [company]", "I want to analyse [company] data", "prepare for EIM analysis",
  "check if we have enough to run EIM", or any time /eim-product-analyst is about to
  run on a new company or dataset for the first time.
---

# EIM Context — Readiness Gate and Context Synthesis

This skill runs before `/eim-product-analyst`. Its job is to verify you have the right
**kinds** of information — not specific file names — and to synthesise everything into a
single context document the analysis will read first.

Without this, the EIM skill produces hypotheses that are statistically coherent but
product-irrelevant: signals named incorrectly, mechanisms that don't match how the product
works, or impact estimates attached to segments the team doesn't recognise.

---

## What you're checking for

There are four kinds of information. Two are required. Two improve quality significantly.

| Kind | Required? | What it enables |
|---|---|---|
| **Behavioural data** | Hard stop | Something happened — feature used, step skipped, session started |
| **Outcome data** | Hard stop | Something resulted — churned, upgraded, converted, renewed |
| **Product understanding** | Warn if absent | Interpreting signals as product problems, not data anomalies |
| **Customer voice** | Note gap | Sense-checking findings against what the team already knows |

Data does not have to be a file. It can be an MCP connection to an analytics tool,
a database the user has access to, or data they can describe or paste. What matters
is whether the information exists and is accessible — not the format.

---

## Step 0 — Ask before scanning

Before looking for anything, ask the user:

> "Before I check what we have, tell me:
> 1. **What's the company / product name?** (Used for naming the output file)
> 2. **Where does the data live?** For example:
>    - CSV or JSON files in a folder (tell me the path)
>    - An analytics tool like Amplitude, Mixpanel, PostHog, or Heap (I may be able to connect directly)
>    - A database or data warehouse you can query or export from
>    - Something else — describe it
> 3. **Is there anything written down about the product** — what it does, who it's for, how it's priced? A product brief, a README, a website, a pitch deck — anything.
> 4. **Is there anything from customers** — interview notes, support ticket themes, survey results, sales call notes?"

Wait for the user's answers. Use them to guide the scan in Step 1.

Do not assume the company name, data location, or context document names.

---

## Step 1 — Scan for each kind of information

Work through each of the four kinds in order. For each one, assess: **present**, **partial**, or **absent**.

### 1a. Behavioural data

**What you're looking for:** Any source that records what individual users or accounts did —
event logs, feature usage tables, session data, activity records, onboarding step logs.
Each row should represent an action, a session, or an account-period (e.g. monthly snapshot).

**How to check based on what the user said:**

If they named a **file path:**
```bash
# Scan for data files of any format — do not assume extension or name
ls -lh [path]/**/*.{csv,json,parquet,tsv,xlsx} 2>/dev/null
ls -lh [path]/*.{csv,json,parquet,tsv,xlsx} 2>/dev/null
```
For each file found, inspect enough rows to understand the grain:
- What is one row? (one event, one account, one user-month?)
- Does it contain identifiers (user_id, account_id, session_id)?
- Does it contain behavioural signals (feature names, action types, counts, timestamps)?

If they named an **analytics tool** (Amplitude, Mixpanel, PostHog, Heap, Segment, etc.):
Check whether an MCP connection to that tool is available. If an Amplitude MCP is
available, attempt to authenticate and describe what event data is accessible.
If no MCP is available, ask the user what they can export or describe from it.

If they described **something else:** Ask enough clarifying questions to understand
whether the data contains individual-level behavioural signals. Aggregate reports
(e.g. "we have a dashboard showing DAU") are not sufficient — you need row-level or
account-level data to segment and validate.

**Gate decision:**
- **Present:** At least one source with individual-level behavioural signals exists and is accessible
- **Partial:** Data exists but may be aggregated, incomplete, or inaccessible — flag and describe the limitation
- **Absent:** No behavioural data. **STOP.** Tell the user: *"I need data that shows what individual users or accounts actually did — event logs, feature usage, session records, or activity data at the account or user level. Aggregate reports (total DAU, feature adoption %) are not sufficient on their own. Without this, I can describe aggregate trends but cannot identify which segments or behaviours predict outcomes."*

**Data size gate (run immediately after confirming behavioural data is present):**

For each file source, check size and row count:

```python
import os, pandas as pd

files = [...]  # files found in 1a

for f in files:
    size_mb = os.path.getsize(f) / 1_000_000
    # Read only headers + first chunk to get row count efficiently
    row_count = sum(1 for _ in open(f)) - 1  # subtract header
    print(f"{f}: {row_count:,} rows | {size_mb:.1f} MB")
```

If any file exceeds **200,000 rows** or **100 MB**, generate a stratified sample before the analysis proceeds:

```python
import pandas as pd

df = pd.read_csv(large_file)

# Identify outcome column (the one found in 1b, or the most likely candidate)
outcome_col = '[outcome column]'

# Stratified sample — preserve outcome distribution
sample = df.groupby(outcome_col, group_keys=False).apply(
    lambda x: x.sample(frac=0.2, random_state=42)  # 20% sample, adjust to hit ~50K rows
)

# Cap at 50,000 rows
if len(sample) > 50_000:
    sample = df.groupby(outcome_col, group_keys=False).apply(
        lambda x: x.sample(n=min(len(x), int(50_000 * len(x) / len(df))), random_state=42)
    )

sample_path = f"[company-folder]/[company]-[table]-sample.csv"
sample.to_csv(sample_path, index=False)
print(f"Sample: {len(sample):,} rows (from {len(df):,}) → {sample_path}")
print(f"Outcome distribution preserved: {sample[outcome_col].value_counts(normalize=True).round(3).to_dict()}")
```

Name the sample file: `[company-name]-[table-name]-sample.csv` and save it in the company folder.

Tell the user:
> *"[filename] is [N] rows / [X] MB — too large to analyse efficiently without risking token overflow. I've generated a stratified random sample of [n] rows that preserves the outcome distribution. The analysis will run on the sample. All findings will be noted as 'validated on n=[n] sample (full dataset n=[N])'. The sample is saved at [path]."*

Document sampling in the context-base (see Step 3) with: original row count, sample row count, sampling fraction, outcome distribution before and after, and sample file path.

If the file is under the threshold (< 200K rows and < 100MB), proceed without sampling — note the row count in the context-base for reference.

### 1b. Outcome data

**What you're looking for:** A source that records what happened to those users or accounts
as a business result — churned, upgraded, cancelled, converted, renewed, expanded. This
can be a column in the behavioural data (e.g. `churned_90d = true`), a separate table
joined by account ID, or a status field with values like `active / churned / cancelled`.

**How to check:**
- Inspect the column names and values in the behavioural data sources found in 1a
- Look for: boolean columns (churned, converted, upgraded), date columns implying events
  (`cancelled_at`, `upgraded_at`, `churn_date`), or status fields with categorical values
- If the outcome is not explicit, ask: "Is there a column or table that tells us what
  ultimately happened to each account or user?"

**Gate decision:**
- **Present:** At least one outcome variable is identifiable — either explicit or constructable
- **Partial:** Outcome exists but needs construction (e.g. derive churn from `cancelled_at IS NOT NULL`) — note the construction logic
- **Absent:** No outcome data. **STOP.** Tell the user: *"I need at least one signal that tells me what happened to each account or user — whether they churned, upgraded, converted, or renewed. Without an outcome variable, I can describe behaviour but cannot say which behaviours predict good or bad outcomes."*

### 1c. Product understanding

**What you're looking for:** Enough understanding of the product to interpret a behavioural
signal as a product problem rather than a data anomaly. Specifically:

- What does the product do? (core job-to-be-done)
- Who is it for? (user types, company sizes, verticals)
- How is it priced / tiered? (this matters for interpreting blocked events, upgrade signals)
- What does healthy usage look like? (so you can recognise unhealthy usage)
- What are the known friction points or risk signals? (so you don't rediscover what's known)

**How to check:**
- Scan the company folder for any document mentioning the product — any filename, any format
- Check if the user described the product in their Step 0 answers
- If neither: ask — *"Can you tell me about the product in a few sentences? What does it do,
  who buys it, and what are the main pricing tiers? I can work without a document if you
  describe it."*

Accept any form: a document, a paste, a verbal description captured in notes. Quality of
the hypotheses depends heavily on this — flag explicitly if it is absent.

**Gate decision:**
- **Present:** Enough product understanding exists to interpret signals correctly
- **Partial:** Basic product description exists but pricing/tiers or healthy usage benchmarks are unknown — note the gaps
- **Absent:** No product context. Do not stop, but warn clearly: *"I'll proceed, but without product context the hypotheses will describe statistical patterns rather than product problems. The mechanisms I suggest may not match how your product actually works. I'd recommend adding a brief product description before acting on the output."*

### 1d. Customer voice

**What you're looking for:** Any qualitative signal from customers — interview notes,
support ticket themes, survey verbatims, NPS comments, sales call notes, CX team
summaries. Not required, but it catches hypotheses the data supports that the team
already knows are wrong (or already knows are right and have tried to fix).

**How to check:**
- Scan for any document that looks like research, interviews, or support summaries
- Ask: *"Is there anything from customer calls, support, or sales that I should know
  before I start? Even a few bullet points would help me avoid surfacing things you
  already know."*

**Gate decision:**
- **Present:** Some qualitative signal is available — read it and extract key themes
- **Absent:** Note the gap in the context-base. Do not stop or warn heavily — this is a quality booster, not a requirement.

---

## Step 2 — Present the readiness table

After completing the scan, present a summary table before proceeding:

```
## EIM Context Readiness — [Company Name]

| Kind | Status | Source | Notes |
|---|---|---|---|
| Behavioural data | ✅ Present / ⚠️ Partial / ❌ Absent | [source description] | [grain, row count if known, key tables] |
| Outcome data | ✅ Present / ⚠️ Partial / ❌ Absent | [source description] | [column name or construction logic] |
| Product understanding | ✅ Present / ⚠️ Partial / ❌ Absent | [source description] | [gaps noted] |
| Customer voice | ✅ Present / ➖ Not available | [source or "none found"] | [themes if present] |
```

If any hard stops were triggered in Step 1, stop here and show only the table with the
blocking rows. Do not proceed to Step 3.

If no hard stops: ask — *"Does this look right? Any sources I've missed or context I
should know before I write up the synthesis? Say 'proceed' when ready."*

---

## Step 3 — Synthesise into the context-base document

Read everything available. Produce a structured synthesis that the `/eim-product-analyst`
skill will read as its first step. Write this to:
`[company-folder]/[company-name]-context-base.md`

If no company folder exists, create it. If the company folder path is unclear, save to
the current working directory and tell the user.

### Context-base structure

```markdown
# EIM Context Base — [Company Name]
*Generated: [date]*
*Sources: [list every source read]*

---

## What the Product Does
[2–4 sentences. The core job-to-be-done. Who uses it. What problem it solves.
Written to help interpret a behavioural signal as a product problem.]

## User and Account Types
[Who are the users? Who are the accounts/companies? What roles matter?
What segments exist — by size, vertical, tier, or use case?]

## Pricing and Plan Structure
[What tiers exist? What are the key gates between tiers? What does each tier
include / exclude? This is critical for interpreting blocked events and upgrade signals.]

## What Healthy Usage Looks Like
[What does a retained, expanding account look like in the data? What behaviours
are associated with success? Known benchmarks if available.]

## Known Friction Points and Risk Signals
[What does the team already know causes problems? Where do users drop off?
What support themes recur? Source: product context doc or customer voice.]

## Available Data Sources

### [Table / Source Name]
- **What it is:** [one sentence on the grain — one row = one what?]
- **Key columns:** [the columns that look like behavioural signals or outcome labels]
- **Outcome variable:** [the column(s) that represent business outcomes, or how to construct one]
- **Time range:** [if known]
- **Row count:** [full dataset row count]
- **Sampling:** [If sampled: "Stratified sample of N rows generated from full dataset of M rows (X% sample). Outcome distribution preserved: [outcome col] → [value: %]. Sample file: [path]." If not sampled: "No sampling applied — dataset within size limits."]
- **Gaps / caveats:** [missing data, known quality issues, columns that are ambiguous]

[Repeat for each source]

## Data Dictionary
[If a data dictionary exists, summarise the key column definitions here.
If not, note: "No data dictionary available — column meanings inferred from inspection."]

## Customer Voice Themes
[If qualitative context exists, extract the 3–5 most relevant themes for an EIM analysis.
If not: "No qualitative context available. Recommend validating hypotheses against customer
calls or support data before prioritising."]

## Known Gaps
[What is missing that would improve the analysis? Be specific:
- "No qualitative data — hypotheses should be validated against customer calls before acting"
- "Pricing structure unknown — upgrade signals cannot be quantified accurately"
- "No individual-level event data — only account-level aggregates available"]

---
*Context base ready. Run /eim-product-analyst [company-name] to begin analysis.*
```

---

## Step 4 — Update the eim-product-analyst skill invocation

After saving the context-base file, tell the user:

> "Context base saved to `[path]/[company-name]-context-base.md`.
>
> You're ready to run the analysis. The EIM skill will read this file first before touching the data.
>
> Run: `/eim-product-analyst [company-name]`"

Also note any gaps that could affect hypothesis quality — be specific about what the
hypotheses might miss or get wrong without the missing context.

---

## What this skill does NOT do

- It does not run any analysis or generate hypotheses — that is `/eim-product-analyst`'s job
- It does not require specific file names, specific folder structures, or specific formats
- It does not require a data dictionary — if absent, the analysis will infer and note assumptions
- It does not require all four kinds of information — only behavioural data and outcome data
  are required to proceed

---

## Common failure modes to avoid

**Checking for filenames instead of information kinds**
The gate passes or fails based on whether the right KIND of data exists, not whether
a file named `flowmind_accounts.csv` or `product-context.md` is present. A user with
Amplitude access and a Notion product brief has everything needed even if they have
no local files.

**Treating aggregate dashboards as behavioural data**
A screenshot of a Mixpanel funnel is not behavioural data. A Mixpanel event export
with user_id, event_name, and timestamp is. If the user describes aggregate reports,
ask whether they can access the underlying event data.

**Asking too many questions before scanning**
Step 0 asks four targeted questions. That's enough to start scanning. Do not ask for
more information than you need before beginning — scan what's available, then fill gaps
through targeted follow-up questions.

**Writing a data dictionary when none was provided**
If no data dictionary exists, note the gap and proceed with inference. Do not invent
column meanings. Write what you can infer from column names and value distributions,
and mark inferred meanings clearly as such.
