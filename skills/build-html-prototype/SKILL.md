---
name: build-html-prototype
description: >
  Use this skill when the user wants to build a clickable HTML prototype from a Prototype Brief
  or hypothesis. Triggers include: "build the prototype", "make it clickable", "build me an HTML
  version", "I want something I can click through", "generate the HTML", or any time the user has
  a Prototype Brief and wants a working artefact they can open in a browser without using Figma.
  Can work from a Prototype Brief file, a pasted build prompt, or directly from a hypothesis if
  no brief exists yet.
---

# Build HTML Prototype

This skill takes a Prototype Brief (or a hypothesis with enough context) and produces a single
self-contained HTML file — embedded CSS and vanilla JS, no dependencies, opens directly in a browser.

The output is a mid-fi clickable prototype for customer testing sessions. It is not production code.
When a Figma design spec exists, the output should look indistinguishable from the real product at
a glance — correct colours, correct font, correct component shapes, correct layout. This is the bar.

---

## Step 0 — Gather source material

### Step 0a — Check for a Figma design spec (run this first, before reading the brief)

Before anything else, check whether a `[company]-figma-spec.md` file exists in the same folder
as the prototype brief:

```bash
ls [company-folder]/*figma-spec*.md 2>/dev/null
```

**If found:** Read it in full. It is the authority on all visual decisions — background colour,
font family, button dimensions, card shadows, nav structure. Extract and note these values before
proceeding:

| What to extract | Where in the spec |
|---|---|
| Background colour (screens) | Section 2b — "Background" role |
| Surface colour (cards, modals) | Section 2b — "Surface elevated" role |
| Primary CTA: background, text colour, height, border-radius | Section 2f — Primary CTA Button |
| Font family + Google Fonts import URL | Section 2c + Section 2i |
| `font-variation-settings` value if noted | Section 2i engineering notes |
| Card border-radius and shadow | Section 2f — Cards |
| Bottom nav: tab count, labels, active/inactive colours | Section 2f — Bottom Navigation |
| Target platform (mobile vs desktop) | Section 2i |
| Primary accent colour | Section 2b — "Primary CTA" hex |
| Text primary + text secondary | Section 2b |
| Border / divider colour | Section 2b |

These extracted values become your CSS. Do not use defaults when the spec is present.
Every value you substitute with a default is a decision the spec already made correctly.

**If not found:** Check for any file named `*design-system*`, `*design*`, or `*branding*`
in the company folder. Use whatever colour or font tokens are present. If nothing exists,
proceed with the generic defaults in Step 2.

---

### Step 0b — Read the prototype brief

**If the user has provided a Prototype Brief file:**
Read it in full. The key sections are:
- **What the Prototype Must Show** — these become your screens
- **What the Prototype Does NOT Need to Do** — hard constraints, respect them exactly
- **Build Prompt** — if present, use it as the primary spec. It was written to be self-contained.

**If the user has provided a hypothesis but no brief:**
Extract the Mechanism section. Infer: the key screen(s), the user and their state, the
intervention the user sees, and the outcome or confirmation state. Ask the user to confirm
your interpretation before building.

**If the user has pasted a build prompt inline:**
Use it directly. Do not ask clarifying questions — the build prompt was written to be
self-contained.

---

## Step 1 — Plan the screens before writing any code

List the screens you intend to build and the click interactions that connect them. Present
this to the user as a simple map:

```
Screen 1: [Name] — [one line description]
  → Click "[element]" → Screen 2

Screen 2: [Name] — [one line description]
  → Click "[element]" → Screen 3

Screen 3: [Name] — [one line description]
  → Click "[element]" → Screen 1 (updated state)
```

Ask:

> "Here's what I'm planning to build. Does this match what you need, or are there screens
> missing or interactions that should work differently?"

Do not write any code until confirmed.

---

## Step 2 — Build the HTML file

### Structure rules

- **Single file.** All CSS in a `<style>` block in `<head>`. All JS in a `<script>` block
  before `</body>`. No external dependencies, no CDN links, no imports — except Google Fonts
  `@import` in the `<style>` block, which is allowed if the figma-spec specifies the font
  is available on Google Fonts.
- **Screen switching via JS.** Each screen is a `<div class="screen" id="screen-N">`.
  Only the active screen has `display: block`. JS shows/hides screens on click.
- **Mobile or desktop:** Determined by the figma-spec (Section 2i) or the build prompt.
  Default: full browser window, 1280px minimum. If the product is a mobile app, use the
  phone frame layout described below.
- **No error states, loading states, or edge cases** unless explicitly in "What the Prototype
  Must Show".

---

### Visual style — when figma-spec is present

Use the exact token values extracted in Step 0a. Rules:

- **Background is never plain white unless the spec says `#FFFFFF`.** Warm cream, off-white,
  light grey — use whatever the spec says. Generic white is the most obvious tell that
  the spec was ignored.
- **Font family must match exactly.** If the spec says DM Sans, use DM Sans — not Inter,
  not system-ui. Import from Google Fonts using the URL format noted in Section 2i of the spec.
  Apply `font-variation-settings` if specified.
- **Button text colour may not be white.** Some designs use dark text on coloured buttons.
  Check the spec's CTA Button section — if it says `#1A1A1A` on an amber button, that is the
  correct output. Do not substitute white.
- **Card shadows must be exact.** Copy the shadow value verbatim from the spec (e.g.
  `0px 14px 44px 0px rgba(79,94,85,0.2)`). Do not simplify to `0 2px 4px rgba(0,0,0,0.1)`.
- **Button dimensions must match.** Use the spec's exact height and border-radius for CTA
  buttons and option buttons. These dimensions are part of what makes the prototype look real.
- **Tab count on bottom nav must match the spec exactly.** If the spec says 4 tabs, build
  4 tabs. If it says 5, build 5. Wrong tab count is immediately visible in testing.

---

### Visual style — fallback (no figma-spec)

If no design spec exists, use this baseline:
- Background: `#ffffff`
- Sidebar / panels: `#f8f9fa`
- Borders: `#e5e7eb`
- Primary action colour: `#2563eb`
- Font: `Inter, -apple-system, BlinkMacSystemFont, sans-serif`
- Border radius: `8px` for cards, `6px` for buttons
- Base font size: `14px`

---

### Mobile phone frame layout

If the figma-spec reports **Target platform: Native mobile** (Section 2i), or the build
prompt specifies a mobile screen width (e.g. "375px wide, mobile browser"), render each
screen inside a centred phone frame:

```css
/* Google Fonts import — use the URL from figma-spec Section 2i */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: #e8eaed;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding: 40px 0;
  font-family: 'DM Sans', sans-serif; /* replace with spec font */
}

.phone-frame {
  width: 390px;            /* use figma-spec screen width from Section 2d */
  background: #FFFAF5;     /* replace with spec background */
  border-radius: 40px;
  overflow: hidden;
  box-shadow: 0 24px 80px rgba(0,0,0,0.25), 0 0 0 1px rgba(0,0,0,0.08);
  position: relative;
}

.screen {
  width: 390px;
  min-height: 844px;
  position: relative;
  overflow: hidden;
  display: none;
}

.screen.active {
  display: block;
}
```

Wrap all screens in a single `.phone-frame` div. JS toggles the `active` class (or
`display` directly) on the `.screen` elements to switch views.

Use the screen dimensions from the figma-spec Section 2d (e.g. 430×932px, 375×812px).
The phone frame width should match the spec's screen width.

---

### Content rules

- Use the **exact copy** from the build prompt or prototype brief — do not paraphrase or
  improve it. The copy is part of what is being tested.
- Use fixed placeholder values for all data (counts, names, dates). Never leave blanks.
- If the brief specifies placeholder names or numbers, use them exactly.

---

### Interaction rules

- Every clickable element must do something. If a nav item is out of scope, keep it
  visually present with a no-op handler — never a dead click with no feedback.
- State changes (e.g. a card going to selected state before transition) must be handled in JS,
  not by duplicating screens.
- Navigation elements (back arrows, bottom nav) should work where the brief requires it,
  and be present but inert elsewhere.
- For mobile prototypes: increase tap target sizes to minimum 44×44px for all interactive
  elements, even if the visual element is smaller.

---

## Step 3 — Save and confirm

Save the file to the same directory as the Prototype Brief. Naming convention:

`[product-slug]-prototype-[hypothesis-slug].html`

Example: `mealtime-prototype-h1-meal-plan-activation.html`

If no source file location is clear, save to the current working directory.

After saving, tell the user:
- The file path
- How many screens it contains
- Which interactions are wired
- Anything left intentionally non-functional and why
- Whether the figma-spec was used (and which company's)

---

## Step 4 — Offer a quick iteration loop

After delivering, ask:

> "Open it in a browser and tell me what needs changing. Common things to adjust:
> - Copy or placeholder data
> - A screen that's missing or needs a different state
> - An interaction that doesn't behave as expected
> - Visual style — colour, spacing, layout
>
> Describe what you want and I'll update the file."

Treat feedback as targeted edits to the existing file — do not rewrite from scratch unless
the screen structure has fundamentally changed.

---

## Quality checklist before delivering

**Structure**
- [ ] Does every screen from "What the Prototype Must Show" exist?
- [ ] Are all click interactions from the screen plan wired up?
- [ ] Does the file open in a browser with no console errors?
- [ ] Is the copy taken verbatim from the brief, not paraphrased?
- [ ] Are all placeholder values filled in — no empty brackets or lorem ipsum?
- [ ] Are items from "What the Prototype Does NOT Need to Do" absent from the build?
- [ ] Is the file fully self-contained — no broken external URLs, no missing assets?

**Design fidelity (when figma-spec exists)**
- [ ] Background colour matches spec — not defaulted to white
- [ ] Font family and Google Fonts import match spec — not defaulted to Inter
- [ ] Primary CTA button: height, border-radius, background, and text colour all match spec
- [ ] Card shadow matches spec exactly — not simplified
- [ ] Bottom nav tab count matches spec exactly
- [ ] Text colour on CTA matches spec (may be dark on a coloured button, not white)
- [ ] Active/inactive colours on bottom nav match spec

**Mobile layout (when applicable)**
- [ ] Screens are inside a phone frame, not full-width browser
- [ ] Phone frame width matches figma-spec screen dimensions
- [ ] Tap targets are at least 44×44px

---

## Common mistakes to avoid

**Ignoring the figma-spec file**
Generic white backgrounds, blue primary buttons, and Inter font are the wrong output when a
`[company]-figma-spec.md` exists in the project folder. The spec exists precisely so that
prototypes look like the real product. A wrong background colour, wrong font, or wrong button
shape makes stakeholders question the design instead of the hypothesis. Read the spec. Use its
values. This is the most impactful change you can make to output quality.

**Using white text on coloured buttons**
Some design systems use dark text on amber, orange, or other coloured CTAs — not white. The
figma-spec's Primary CTA Button section specifies exact text colour. Do not assume white.

**Building too much**
The brief lists what to leave out for a reason. Extra screens, realistic-looking data,
and visual polish beyond what the spec provides add time without adding signal. If it's not in
"What the Prototype Must Show", don't build it.

**Rewriting the copy**
The specific wording on banners, CTAs, and confirmation messages are hypotheses in themselves.
Improving the copy means testing different assumptions than intended.

**Dead-end clicks**
Every tappable element should go somewhere. A non-functional nav item with a no-op handler
is fine. A primary CTA that does nothing will break the customer session.

**Simplifying shadow and spacing values**
`0 2px 4px rgba(0,0,0,0.1)` looks flat and generic next to the real product's card shadow.
Copy shadow values verbatim from the spec. Three extra characters of CSS is worth it.

**Over-engineering the JS**
State management for a 4-screen prototype does not need a framework. A handful of
`getElementById` calls and `classList` toggles is the right level of complexity.
