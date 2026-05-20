---
name: figma-prototype-builder
description: >
  Use this skill when the user wants to build a prototype directly inside Figma using the Figma
  MCP tools. Triggers include: "build the prototype in Figma", "create it in Figma", "add it to
  the Figma file", "write the prototype to Figma", "use Figma Make to build this", or any time
  the user has a Prototype Brief (and optionally a Figma URL) and wants the output to live in
  Figma rather than as an HTML file. Requires the user to own (not just view) the target Figma
  file. Auto-discovers [product]-figma-spec.md if /figma-make-spec was run first — the user
  does not need to re-supply the Figma URL in that case.
---

# Figma Prototype Builder

This skill takes a Prototype Brief (and optionally a PRD) and builds a clickable prototype
directly inside a Figma file using the Figma MCP Plugin API. It creates a new Figma page per
hypothesis — never writes to the cover page or existing design pages.

---

## Phase 0 — Locate source material

**Auto-discover in the product folder:**

1. Look for `[product]-figma-spec.md` — produced by `/figma-make-spec`. If found, read it.
   This replaces any need to re-query Figma for design tokens. Skip Phase 1 scraping.
2. Look for `[product]-prototype-[hypothesis].md` — the Prototype Brief. Read it.
   Key sections: **What the Prototype Must Show**, **What the Prototype Does NOT Need to Do**,
   **Build Prompt**.
3. Look for `[product]-prd-[hypothesis].md` — the PRD. Read it for metric and scope context.

**If no figma-spec.md exists:**
Ask the user for the Figma file URL, then run the scraping steps in Phase 1 before building.

**If no Prototype Brief exists:**
Ask the user which hypothesis to build and what screens it needs to show. Confirm before
building.

**Figma file URL:**
- If figma-spec.md was found, the fileKey is recorded in the spec — use it.
- If not, ask the user for the Figma URL and extract the fileKey from it.
- The user must own the file (not a community/view-only copy). If in doubt, ask.

---

## Phase 1 — Extract design tokens (only if no figma-spec.md)

If no spec file was found, read design tokens from Figma before building:

1. Call `get_metadata` with the fileKey to discover screen frame IDs
2. Call `get_design_context` on 3–5 representative frames (home screen, onboarding screen,
   a modal or sheet if present)
3. Extract: background colours, primary CTA colour, font family, button heights/radius,
   card styles, bottom nav structure, progress indicator style
4. Note all tokens — they inform the plugin code in Phase 3

---

## Phase 2 — Plan the prototype screens

From the Prototype Brief's "What the Prototype Must Show" section, list:
- Each screen by name
- The click interactions between them
- Which elements are interactive vs inert

Present this plan to the user:

```
Screen 1: [Name] — [one line description]
  → Click "[element]" → Screen 2

Screen 2: [Name] — [one line description]
  → Click "[element]" → Screen 3
```

Ask: "Does this match what you need before I build?" Do not proceed until confirmed.

---

## Phase 3 — Build in Figma via Plugin API

Use `use_figma` to run Plugin API code. Follow these rules:

**Page creation — always create a new page:**
```js
const page = figma.createPage();
page.name = '[Hypothesis name] Prototype';
await figma.setCurrentPageAsync(page);
```
Never write to the cover page or any existing page. Always create a new page.

**Frame per screen:**
Create one top-level Frame per screen at standard mobile dimensions (390 × 844):
```js
const frame = figma.createFrame();
frame.name = 'Screen 1 — [Name]';
frame.resize(390, 844);
frame.x = screenIndex * 440; // space screens horizontally
```

**Design tokens:**
Use the exact values from the figma-spec.md (or Phase 1 extraction):
- Background fills, text colours, button colours taken verbatim from spec
- Font family loaded via `figma.loadFontAsync({ family: '[font]', style: '[weight]' })`

**Interactivity — prototype links:**
After creating all frames, wire interactions using Figma prototype links:
```js
const reaction = {
  trigger: { type: 'ON_CLICK' },
  action: { type: 'NODE', destinationId: targetFrame.id, transition: null }
};
sourceNode.reactions = [reaction];
```

**Content rules:**
- Use exact copy from the Build Prompt — do not paraphrase
- Use placeholder rectangles for images (coloured fills, no external URLs)
- Use fixed placeholder data (name "Alex", plan "Premium") as specified in the brief
- Inert elements: keep them visually present but do not wire prototype links to them

**Scope discipline:**
Build only what is in "What the Prototype Must Show". Do not add extra screens, states,
or interactions not described in the brief.

---

## Phase 4 — Confirm and hand off

After the plugin code executes, tell the user:
- The page name created in Figma
- How many screens were built
- Which interactions are wired
- Anything left intentionally inert and why
- How to enter Prototype mode in Figma to test it (Shift+E or the Present button)

If the plugin code failed (Figma returned an error), diagnose before retrying:
- "Can't call X in read-only mode" → the file is not owned by the user; they need to
  duplicate it to their own account
- Font not found → check the exact font family name in the spec and retry with
  `figma.loadFontAsync` using the corrected name
- Node not found → the target frame ID may be stale; re-read metadata to get current IDs

---

## What this skill does NOT do

- Build HTML prototypes — use `/build-html-prototype` for that
- Read community/view-only Figma files for writing — the user must own the file
- Auto-publish or share the Figma file — the user controls sharing
- Write to the cover page or existing design pages — always creates a new page

---

## Common mistakes to avoid

**Writing to the cover/existing page**
Always call `figma.createPage()` first. Never assume `figma.currentPage` is the right place.

**Using community file for writing**
Community files are read-only. If `use_figma` returns a read-only error, tell the user to
duplicate the file to their own account (File → Duplicate to your drafts) and provide the
new URL.

**Building without confirming the screen plan**
The Phase 2 screen plan confirmation is mandatory. Building the wrong screens wastes time
and confuses customer sessions.

**Loading fonts without awaiting**
Always `await figma.loadFontAsync(...)` before creating text nodes. Missing this causes
silent failures where text appears as empty boxes.
