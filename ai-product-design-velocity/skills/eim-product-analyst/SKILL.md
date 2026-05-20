---
name: eim-product-analyst
description: >
  Use this skill whenever the user wants to analyse product data, customer data, or usage data
  to generate product hypotheses, identify churn signals, find expansion opportunities, or
  understand what's driving retention or growth. Triggers include: "analyse my data", "find
  signals in this data", "what's driving churn", "where should we focus", "generate hypotheses",
  "what does the data say", "find expansion opportunities", "analyse these CSVs", "run EIM on
  this", or any time the user drops data files and wants product insights from them. Also use
  when the user wants to apply the EIM (Evidence → Impact → Mechanism) framework to any dataset.
  Do not wait for the user to say "EIM" explicitly — if they have data and want product insights,
  use this skill. For best results, run /eim-context first to establish product and customer
  context — the analysis reads a context-base file if one exists.
---

# EIM Product Analyst

A skill for turning raw product, customer, or usage data into structured product hypotheses
using the EIM (Evidence → Impact → Mechanism) framework.

The output is not a data analysis report. It is a set of actionable hypotheses — each one
grounded in evidence from the data, quantified by business impact, and paired with a specific
intervention the product team can act on.

---

## Step 0 — Orient before touching data

**First: check for a context-base file**

Before anything else, look for a `[company-name]-context-base.md` file in the company
folder or current directory. This file is produced by `/eim-context` and contains a
pre-synthesised summary of the product, data sources, outcome variables, and known
context gaps.

```bash
ls *-context-base.md 2>/dev/null
```

**If a context-base file exists:** Read it in full. It is your primary orientation document.
Skip steps 1–3 below (data discovery, product context, data dictionary) — the context-base
has already done this work. Proceed directly to Step 1 (data shape inspection), using the
data sources identified in the context-base.

**If no context-base file exists:** Recommend the user run `/eim-context [company-name]`
first to ensure the analysis has the product and customer context it needs to produce
relevant hypotheses. Then proceed through steps 1–3 below, noting any gaps.

---

If proceeding without a context-base, do these three things in order:

**1. Discover what data is available**

Check for files in the current directory and any data subfolder. Do not assume file names,
column names, or table structure. Discover them:

```bash
ls -lh *.csv *.json *.parquet *.xlsx *.tsv 2>/dev/null
ls -lh data/*.csv data/*.json data/*.parquet data/*.xlsx data/*.tsv 2>/dev/null
```

If no files are found, ask the user whether data is available via an analytics tool
connection (Amplitude, Mixpanel, PostHog, etc.) or another source. Do not assume
files are the only option.

If nothing is accessible, tell the user and stop.

**2. Look for product context**

Search for any document that describes the product — what it does, who it's for, how it's
priced. Do not look for specific filenames — look for any document that contains this kind
of content:

```bash
ls *.md *.txt 2>/dev/null
ls use-cases/*/ docs/*/ 2>/dev/null
```

Read any document that looks like product description, context, or positioning.
If none exists, proceed — but note to the user that hypotheses will be less specific
without product context, and that `/eim-context` can help establish this.

**3. Look for a data dictionary**

Search for any document that explains what the data columns mean:

```bash
ls *dict* *schema* *dictionary* *data_dict* 2>/dev/null
```

If found, read it. If not found, proceed — infer column meanings from names and value
distributions, and be explicit about which meanings are inferred vs. documented.

---

## Step 1 — Understand the data shape

For each file discovered, run a quick structural inspection:

```python
import pandas as pd
import glob

files = (glob.glob("*.csv") + glob.glob("data/*.csv") +
         glob.glob("*.tsv") + glob.glob("data/*.tsv") +
         glob.glob("*.json") + glob.glob("data/*.json"))
for f in files:
    df = pd.read_csv(f) if f.endswith(('.csv', '.tsv')) else pd.read_json(f)
    print(f"\n── {f} ──────────────────────")
    print(f"Rows: {len(df):,}  |  Cols: {len(df.columns)}")
    print(df.dtypes.to_string())
    print(df.head(3).to_string())
```

**Ask yourself before proceeding:**
- What is the grain of each table? (one row = one what?)
- Which columns look like outcome labels? (churned, converted, cancelled, upgraded, etc.)
- Which columns look like behavioural signals? (counts, dates, flags, categories)
- How do the tables join? (look for shared ID columns)
- What is the time range of the data?

Do not generate hypotheses yet. Just understand the shape.

---

## Output discipline — follow these rules for every query

Token limits are a real constraint. Every line of Python output enters the context window
and stays there. These rules apply to every script you run throughout the analysis:

**Never print raw rows.** `df.head(3)` is acceptable for initial inspection only. Never
use `df.to_string()`, `print(df)`, or any output that prints more than 5 rows of raw data.

**Only print aggregated results.** Every analytical query should reduce to a summary table —
groupby + agg, value_counts, crosstab, or a scalar. If the output can't fit in ~20 lines,
it's not sufficiently aggregated.

**Cap output per script block.** No single code execution should produce more than
50 lines of printed output. If you need to inspect more dimensions, run separate focused
scripts — one question per run.

**Round and trim.** Use `.round(3)` on floats. When printing a groupby result with many
rows, filter to the most relevant (e.g. `result.head(10)` or `result[result['n'] >= 30]`).

**Name your findings, don't echo raw data.** After running a query, state the finding
in one sentence before moving to the next query. This replaces the need to re-read the
raw output later.

If a context-base file was present and noted that sampling was applied, use the sampled
data files for all analysis — do not load the original raw files.

---

## Step 2 — Identify outcome variables

Find the columns that represent business outcomes. These become the dependent variables
for all analysis. Common patterns:

```python
# Look for boolean/binary columns that suggest outcomes
for col in df.columns:
    if df[col].dtype == bool or df[col].nunique() <= 2:
        print(col, df[col].value_counts().to_dict())

# Look for date columns that imply events (churn_date, cancelled_at, upgraded_at)
date_cols = [c for c in df.columns if any(x in c.lower() for x in
             ['churn', 'cancel', 'upgrade', 'convert', 'renew', 'expire'])]
```

If no explicit outcome column exists, look for one that can be constructed:
- Is there a `status` column with values like `active / churned / cancelled`?
- Is there a date column where null = still active, not-null = churned?
- Can you join to another table to get outcomes?

Be explicit with the user if outcomes are ambiguous or need constructing.

---

## Step 3 — Segment before concluding

**This is the most important analytical discipline.**

Aggregate patterns lie. A 20% churn rate across all accounts is meaningless until you know
whether it is 8% in one segment and 45% in another.

Always slice by every available categorical dimension before forming a hypothesis:

```python
# Template: churn rate by segment
for col in categorical_cols:
    result = df.groupby(col)['outcome_col'].agg(['mean', 'count'])
    result.columns = ['outcome_rate', 'n']
    result = result[result['n'] >= 20]   # minimum sample filter
    result = result.sort_values('outcome_rate', ascending=False)
    print(f"\n── by {col} ──")
    print(result.to_string())
```

Minimum sample sizes before trusting a segment finding: **n ≥ 30** for rates, **n ≥ 50** for
multi-variable interaction effects.

Flag any segment effect that shows **>1.5x difference** from the population base rate.
These are your candidate signals.

---

## Step 4 — Test interaction effects

The strongest signals are usually **intersections**, not single-variable findings.

For each promising single-variable signal, test whether it interacts with other dimensions:

```python
# Template: two-variable interaction
result = df.groupby(['segment_a', 'segment_b'])['outcome_col'].agg(['mean', 'count'])
result.columns = ['outcome_rate', 'n']
result = result[result['n'] >= 20].sort_values('outcome_rate', ascending=False)
```

Look for interactions where:
- The effect is **stronger in one segment than another** (Signal #1 pattern)
- The effect **disappears when you add a third variable** (confound — be careful)
- Two weak signals **compound** into a strong combined signal

---

## Step 4.5 — Retention curves (when date columns are present)

If the dataset contains a date column (e.g. `created_at`, `signup_date`, `first_login`) and an outcome column, generate cohort-based retention curves. This reveals *when* users churn, not just *whether* they do — which often changes which mechanism makes sense.

**Check for date columns first:**

```python
date_cols = [c for c in df.columns if df[c].dtype in ['datetime64[ns]', 'object']
             and any(x in c.lower() for x in ['date', 'created', 'signup', 'start', 'joined'])]
print("Date columns found:", date_cols)
```

If no date column exists, skip this step and note it in the output.

**If a date column is found, generate three curves:**

**Curve 1: Retention by signup cohort (month)**
```python
df['cohort_month'] = pd.to_datetime(df[date_col]).dt.to_period('M')
cohort_retention = df.groupby('cohort_month')['outcome_col'].agg(['mean', 'count'])
cohort_retention.columns = ['churn_rate', 'n']
cohort_retention = cohort_retention[cohort_retention['n'] >= 30]
```
*Reveals: whether churn is improving or worsening across cohorts — a product trajectory signal.*

**Curve 2: Retention by number of features used**
```python
feature_cols = [c for c in df.columns if df[c].dtype == bool or df[c].nunique() == 2]
df['feature_count'] = df[feature_cols].sum(axis=1)
feature_retention = df.groupby('feature_count')['outcome_col'].agg(['mean', 'count'])
feature_retention.columns = ['churn_rate', 'n']
```
*Reveals: whether there's a "magic number" of features that predicts retention — a key activation signal.*

**Curve 3: Retention by individual feature (30-day)**
```python
for col in feature_cols:
    adopted = df[df[col] == True]['outcome_col'].mean()
    not_adopted = df[df[col] == False]['outcome_col'].mean()
    n_adopted = df[col].sum()
    print(f"{col}: adopted={adopted:.1%} (n={n_adopted}), not adopted={not_adopted:.1%}, ratio={adopted/not_adopted:.1f}x")
```
*Reveals: which individual features have the strongest churn-reduction effect.*

Include the key retention curve findings in the Evidence section of any hypothesis they inform. Flag the "magic number" of features if one is found — it is usually a high-value intervention trigger.

---

## Step 5 — Validate against red herrings

High usage ≠ high value. Before including a signal in a hypothesis, validate it:

```python
# Template: does this behavioural signal actually predict the outcome?
signal_heavy = df[df['feature_usage'] >= df['feature_usage'].quantile(0.75)]
signal_light = df[df['feature_usage'] <= df['feature_usage'].quantile(0.25)]

print("Heavy users outcome rate:", signal_heavy['outcome_col'].mean())
print("Light users outcome rate:", signal_light['outcome_col'].mean())
print("Ratio:", signal_heavy['outcome_col'].mean() / signal_light['outcome_col'].mean())
```

A signal is only worth including in a hypothesis if:
1. The outcome rate difference is **>1.5x**
2. The sample size on both sides is **n ≥ 30**
3. The effect **holds when you control for one other variable** (not just raw correlation)

---

## Step 6 — Construct EIM hypotheses

For each validated signal, write a structured EIM hypothesis. Each one has exactly three parts.

Read `references/eim-format.md` for the full format spec and worked examples.

**The three parts:**

**E — Evidence**
What does the data actually show? Be specific. Include the metric, the segment, the magnitude,
and the sample size. No hand-waving.

*Bad:* "Users who don't complete onboarding churn more."
*Good:* "Accounts in the small (20–50 employee) segment that skipped the `connect_second_integration`
onboarding step churned at 40.7% within 90 days, vs 11.1% for those who completed it (n=412 / n=289,
3.7x difference)."

**I — Impact**
What is the business opportunity if this is addressed? Quantify it. Use the data you have —
account count × churn rate × contract value is usually enough for a rough estimate.

*Bad:* "Reducing churn here could be significant."
*Good:* "412 at-risk small accounts × 40.7% churn rate × average ACV of $3,200 = ~$536K ARR at
risk annually. Even a 25% reduction in churn for this segment = ~$134K ARR retained."

**M — Mechanism**
What specific intervention in the product (or adjacent to it) would address this? Name the
feature, the surface, the trigger, and the user. Not a strategy — a thing someone could build.

*Bad:* "Improve the onboarding experience for small accounts."
*Good:* "Trigger an in-app prompt on day 3 for accounts with <2 integrations connected, surfaced
to the admin role only, offering a guided 'connect your second tool' wizard with pre-built templates
for the top 5 integration pairs. Test with a 50/50 holdout."

---
> 🛑 **PAUSE — PM validation before writing the final report**

Present a draft summary of the hypotheses (titles + one-line Evidence summaries only — not the full write-up) and ask:

> "Before I write the full EIM report, I want to check the findings against your experience:
>
> Here are the hypotheses the data is pointing to:
> 1. [Title] — [one-line evidence summary]
> 2. [Title] — [one-line evidence summary]
> 3. [Title] — [one-line evidence summary]
>
> A few questions:
> - Do these signals align with what you're hearing from customers or in support tickets?
> - Is there anything you know from qualitative sources — customer calls, support tickets, sales feedback — that would change the priority order?
> - Any segments we should focus on or exclude?
> - Anything surprising here — or anything you expected to see that's missing?
>
> Say 'proceed' to get the full report, or give me context to adjust before I write it up."

Incorporate any corrections or context into the hypotheses before producing the full output.

---

## Step 7 — Output format

Produce a clean markdown output with this structure:

```
# EIM Hypothesis Report
**Dataset:** [file names used]
**Analysis date:** [today]
**Outcome variable:** [what you're predicting]

---

## Hypothesis 1: [Short descriptive title]

**Evidence**
[2–4 sentences. Specific numbers, segments, sample sizes.]

**Impact**
[2–3 sentences. Quantified ARR / revenue / account count at stake.]

**Mechanism**
[2–4 sentences. Specific intervention. Surface, trigger, user, test approach.]

---

## Hypothesis 2: [Title]
...

---

## What We Ruled Out
[Brief list of signals that looked promising but didn't hold up on validation.
Explain why each was ruled out. This teaches the reader what not to act on.]

---

## Recommended Next Steps
[Rank the hypotheses by confidence × impact. Suggest which to run first and why.]
```

Aim for **3–5 hypotheses** per analysis. More than 5 dilutes focus. Fewer than 3 suggests
the analysis wasn't deep enough.

**Save the report** to the company folder root (the directory containing the `data/` folder
and the data dictionary). Naming convention: `[company-name]-eim-report.md`. Tell the user
the file path after saving.

---

## Step 8 — Sense-check before delivering

Before outputting, ask yourself:

- [ ] If a date column was present, were retention curves generated (by cohort, by feature count, by individual feature)?
- [ ] Is every Evidence claim traceable to a specific query I ran?
- [ ] Does every Impact estimate show its working (the multiplication)?
- [ ] Is every Mechanism specific enough that a PM could write a brief from it?
- [ ] Did I validate each signal against the outcome variable (not just assume correlation)?
- [ ] Did I segment before concluding (no aggregate-only findings)?
- [ ] Did I include a "What We Ruled Out" section?

If any box is unchecked, go back.

---

## Common Pitfalls to Avoid

**Describing the data instead of interpreting it**
The output is hypotheses, not a data summary. "40% of accounts are on the starter tier" is
not a hypothesis. "Starter accounts in the finance vertical upgrade at 3x the rate of other
verticals when they hit a feature block" is a hypothesis.

**Aggregate findings without segment validation**
Always slice. The most important signal in the dataset may only exist in one segment.

**Missing the mechanism**
"Improve onboarding" is not a mechanism. A mechanism names a surface, a trigger, a user role,
and a testable intervention. Push yourself to be specific.

**Ignoring sample size**
A 60% churn rate in a segment of n=12 is noise. Always show n. Always apply the n≥30 filter.

**Confusing activity with value**
High-frequency usage of a feature that has no correlation with retention is a red herring.
Validate every usage signal against an outcome before including it.
