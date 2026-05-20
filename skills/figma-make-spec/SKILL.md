---
name: figma-make-spec
description: >
  Use this skill when the user wants to extract design tokens, component patterns, and a full
  product + engineering spec from a Figma file. Triggers include: "read the Figma design system",
  "extract the design tokens from Figma", "pull the brand from the Figma file", "generate a Figma
  spec", "read the Figma file before building", "create a spec from the Figma file", or any time
  the user provides a Figma URL and wants the visual style, components, and screen patterns
  captured. The output is a [product]-figma-spec.md file that can be consumed by
  /figma-prototype-builder or /build-html-prototype without re-reading the Figma file.
---

# Figma Make Spec

You are acting as a **Senior Product Designer + Staff Frontend Engineer** working together.
Your goal is to convert a Figma design into a **clear, implementation-ready product + engineering
specification** using the Figma MCP tools. The output is saved as a markdown file that prototype-
building skills can consume without re-querying Figma.

---

## Step 0 — Get the Figma URL and product context

**Required from the user:**
- A Figma file URL (figma.com/design/...)
- The product name and the folder to save the spec into

**Extract from the URL:**
- `fileKey` — the alphanumeric segment after `/design/`
- `nodeId` — from `?node-id=X-Y`, convert hyphens to colons (`1-2` → `1:2`)

If no nodeId is in the URL, start from the root (`0:1`) and discover screens from the metadata.

---

## Step 1 — Get file metadata and discover screens

Call `get_metadata` with the fileKey to retrieve the full node tree. Identify:
- Names and IDs of key app screens (Frame nodes under each page/section)
- The page structure and section groupings
- Section labels that indicate screen groups (Onboarding, Home, Settings, etc.)

Select 4–6 screens that together cover the full range of UI patterns:
- A home or dashboard screen
- An onboarding or setup screen
- A modal, bottom sheet, or overlay
- A list or content-heavy screen
- Any screen with a distinct pattern (paywall, empty state, error)

**Critical:** Section header nodes (labels) return only their label text. Always target the
actual Frame nodes inside each section, not the section labels themselves. Use the metadata
node tree to find real frame IDs.

Also call `get_variable_defs` if available to extract named design tokens. If it fails or
returns nothing useful, rely on `get_design_context` CSS output instead.

---

## Step 2 — Extract design context and screenshots

For each selected screen frame, call `get_design_context` with the fileKey and nodeId.

Also call `get_screenshot` on:
- The home/dashboard screen
- One onboarding screen
- Any screen with a distinctive component pattern (e.g. a paywall or modal)

From the CSS and component data returned, extract all of the following:

---

### 2a. Brand Identity

- Brand personality (e.g. warm, playful, enterprise, serious, clean)
- Brand tone (formal / informal / aspirational)
- Logo presence and placement
- Iconography style (outlined, filled, mixed)
- Illustration or imagery style if present
- Motion philosophy (subtle / expressive / functional) — infer from transitions if visible

Flag assumptions explicitly where you are inferring rather than reading directly.

---

### 2b. Colour System

Extract and document:

| Role | Hex | Usage |
|---|---|---|
| Background | | Screen backgrounds |
| Surface elevated | | Cards, modals, inputs |
| Primary CTA | | Buttons, active states |
| Secondary / accent | | Highlights, badges |
| Text primary | | Headings, primary labels |
| Text secondary | | Captions, metadata |
| Text disabled | | Inactive elements |
| Border / divider | | Card borders, separators |
| Success | | Confirmation, completion |
| Warning | | Alerts, caution states |
| Error / destructive | | Errors, delete actions |
| Info | | Informational elements |

Include all colours observed. If a colour appears frequently but has no obvious semantic
role, document it under "Other" with a usage note.

---

### 2c. Typography System

| Role | Font family | Size | Weight | Line height |
|---|---|---|---|---|
| Display / hero | | | | |
| Heading 1 | | | | |
| Heading 2 | | | | |
| Body | | | | |
| Caption | | | | |
| Label / button | | | | |
| Badge | | | | |

Also note: letter-spacing values, italic usage, and any role-specific colour overrides.

---

### 2d. Spacing & Sizing

- Screen horizontal padding (left/right margin)
- Vertical section spacing
- Card border radius
- Button height and border radius
- Input field height and border radius
- Icon sizes used
- Card shadow values
- Gap between list items

---

### 2e. Design System Architecture

- Maturity: ad-hoc / component library / full design system
- Atomic structure observed: foundations → components → patterns → templates
- Naming conventions (if readable from node names in metadata)
- Variant strategy (are components using Figma variants?)
- Token usage consistency (are colours and type scales applied consistently?)

---

### 2f. Component Patterns

Document each major component with its visual spec and interactive states:

**Primary CTA Button**
- Full-width vs contained
- Height, border radius, colour, font size, font weight
- Disabled state (colour, opacity)

**Cards**
- Background colour, border (colour, width, style), shadow, border radius, padding

**Input Fields**
- Height, border colour (default / focus / error), border radius, label position, placeholder style

**Bottom Navigation** (mobile)
- Tab count and labels
- Active state: icon colour, label colour, indicator style
- Inactive state: icon colour, label colour

**Progress Indicators**
- Style: dots / horizontal pills / step numbers / progress bar
- Active colour, inactive colour, dimensions

**Option / Selection Buttons**
- Unselected: border colour, background
- Selected: border colour, background, any icon or checkmark

**Modals / Bottom Sheets**
- Background colour, border radius (top corners), overlay colour/opacity, drag handle style

**Badges / Pills / Tags**
- Background, text colour, border radius, padding, font size

**Empty States**
- Layout: icon + headline + body + CTA
- Dashed border style (if used for placeholder slots)

---

### 2g. Interaction & Motion

- Navigation rules (tab-based, stack-based, modal)
- Click / tap interactions visible from prototype links
- Transitions and animations (spring, fade, slide — and direction)
- Motion timing and easing if inferable

---

### 2h. Screen Inventory

| Screen | Node ID | Description | Key patterns present |
|---|---|---|---|
| [Name] | [ID] | [What this screen does] | [Component patterns visible] |

---

### 2i. Engineering Notes

- Target platform: Web / Mobile web / Native iOS / Native Android / Desktop
- Responsiveness model: Fixed / Responsive / Adaptive
- Input model: Touch / Mouse+keyboard / Hybrid
- Font availability: is the font available via Google Fonts, system fonts, or requires a license?
- Component boundaries: which UI patterns are self-contained vs tightly coupled
- Performance considerations: image-heavy screens, animation complexity

---

### 2j. Open Questions & Risks

- Ambiguities in the design (missing states, unclear interactions)
- Components that appear inconsistent across screens
- Anything that needs clarification before building

---

## Step 3 — Write the spec file

Save as `[product-name]-figma-spec.md` in the product folder (same directory as any existing
EIM report, PRD, or prototype brief for that product).

Use the section structure from Step 2 as the document structure. Add a header block:

```markdown
# [Product Name] — Figma Design Spec
*Extracted from Figma file: [fileKey]*
*Date: [today]*
*Screens sampled: [list of screen names and node IDs]*
*Tool: /figma-make-spec*

---
```

Then include each section from 2a–2j in order. Do not invent UI that is not present in
the Figma file. Clearly mark any assumption or inference.

End with a **Build Notes** section — a plain-English summary of the 3–5 most important
things a prototype builder must know, e.g.:
- "Font is DM Sans — import from Google Fonts"
- "Background is #FFFAF5 warm cream, not white"
- "Bottom nav has 4 tabs, not 5"
- "Primary button is always full-width with 57px height"
- "Progress indicator uses horizontal green pills, not dots"

---

## Step 4 — Confirm and hand off

After saving, tell the user:
- The file path
- The colour palette (a 3–5 token summary: background, primary, text)
- The font family
- Whether screenshots were captured
- That `/build-html-prototype` and `/figma-prototype-builder` will auto-discover this file

> "Spec saved to `[path]`. Run `/build-html-prototype` or `/figma-prototype-builder` and it
> will read this file automatically — no need to provide the Figma URL again."

---

## Common mistakes to avoid

**Reading section header nodes instead of screen frames**
Section nodes return only their label text. Always find actual Frame node IDs from the metadata
node tree before calling `get_design_context`.

**Stopping at one screen**
One screen rarely shows all component states. Sample at least 4 screens to get the full range:
populated, empty, onboarding, modal/sheet.

**Guessing or rounding token values**
Use exact hex values, border-radius, and font sizes as returned by `get_design_context` CSS.
Do not adjust to "rounder" numbers.

**Skipping screenshots**
Screenshots are the fastest way for a prototype builder to sense-check the output. Always
capture at least the home screen and one onboarding screen.

**Only documenting selected states**
Always document both selected and unselected states for interactive components — the contrast
between them is often the key design decision being tested.
