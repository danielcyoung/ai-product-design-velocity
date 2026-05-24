---
version: alpha
name: FinWise
description: FinWise Mobile App Design System — light and dark mode color palette with Poppins typography
colors:
  honeydew: "#F1FFF3"
  light-green: "#E1F7F1"
  caribbean-green: "#00CDA8"
  cyprus: "#155E43"
  fence-green: "#0D5540"
  light-blue: "#A7CFFE"
  vivid-blue: "#2299FF"
  ocean-blue: "#0056FF"
  void: "#2C2C2C"
  white: "#FFFFFF"
  black: "#000000"
  
  # Semantic color mapping
  primary: "#00CDA8"
  primary-dark: "#0D5540"
  primary-light: "#E1F7F1"
  secondary: "#2299FF"
  secondary-dark: "#0056FF"
  secondary-light: "#A7CFFE"
  background: "#FFFFFF"
  surface: "#F1FFF3"
  text-primary: "#2C2C2C"
  text-secondary: "#155E43"
  text-tertiary: "#A7CFFE"
  
typography:
  display-bold:
    fontFamily: Poppins
    fontSize: 2rem
    fontWeight: 700
  heading-semibold:
    fontFamily: Poppins
    fontSize: 1.5rem
    fontWeight: 600
  body-medium:
    fontFamily: Poppins
    fontSize: 1rem
    fontWeight: 500
  body-regular:
    fontFamily: Poppins
    fontSize: 1rem
    fontWeight: 400
  label-light:
    fontFamily: Poppins
    fontSize: 0.875rem
    fontWeight: 300
  label-thin:
    fontFamily: Poppins
    fontSize: 0.75rem
    fontWeight: 100

rounded:
  sm: 4px
  md: 8px
  lg: 12px
  xl: 16px
  full: 9999px

spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.white}"
    typography: "{typography.body-medium}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-primary-hover:
    backgroundColor: "{colors.primary-dark}"
    textColor: "{colors.white}"
  button-secondary:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.white}"
    typography: "{typography.body-medium}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-secondary-hover:
    backgroundColor: "{colors.secondary-dark}"
    textColor: "{colors.white}"
  button-tertiary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.body-medium}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-tertiary-hover:
    backgroundColor: "{colors.primary-light}"
    textColor: "{colors.primary-dark}"
  card:
    backgroundColor: "{colors.white}"
    rounded: "{rounded.lg}"
    padding: 16px
  card-hover:
    backgroundColor: "{colors.surface}"
  text-field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.md}"
    padding: 12px 16px
---

## Overview

FinWise is a personal finance mobile app designed to help users track spending, set savings goals, and understand their financial situation. The design system uses a vibrant teal/green primary color palette paired with a cool blue secondary, creating an approachable yet professional identity. The app supports both light and dark modes, with Poppins as the primary typeface for titles, subtitles, and body text.

The visual identity emphasizes clarity, trust, and forward-looking financial wellness. Bright, energetic greens suggest growth and positive financial movement, while cool blues provide a sense of stability and control.

## Colors

The color palette consists of a vibrant teal/green primary range, cool blues for secondary actions, and a neutral dark grey (Void) for text and borders.

**Primary Greens (Growth & Movement):**
- **Caribbean Green (#00CDA8):** Primary brand color for call-to-action buttons, active states, and core interactions. Used for savings goal highlights and positive financial movements.
- **Light Green (#E1F7F1):** Light tint for backgrounds, card highlights, and secondary surfaces. Creates visual hierarchy and highlights important information.
- **Cyprus (#155E43):** Dark green used for text, borders, and emphasis. Provides contrast and visual depth.
- **Fence Green (#0D5540):** Darkest green for dark mode, deep text, and high-contrast borders.

**Secondary Blues (Trust & Stability):**
- **Ocean Blue (#0056FF):** Deep blue for secondary actions, links, and alternative CTAs.
- **Vivid Blue (#2299FF):** Mid-tone blue for notifications, charts, and data visualization.
- **Light Blue (#A7CFFE):** Pale blue for light backgrounds, disabled states, and subtle highlights.

**Neutrals:**
- **Honeydew (#F1FFF3):** Warmest neutral background, soft and approachable.
- **Void (#2C2C2C):** Deep dark grey for primary text and high-contrast elements.
- **White (#FFFFFF):** Card backgrounds and elevated surfaces in light mode.

## Typography

FinWise uses **Poppins** exclusively across all surfaces. Poppins is a clean, geometric sans-serif that conveys approachability and modernity while maintaining excellent readability at all sizes.

**Type Scale:**
- **Display Bold** (32px, 700): Main headlines and hero content. Rare usage, reserved for onboarding or primary page headers.
- **Heading Semibold** (24px, 600): Section headings, goal names, transaction categories.
- **Body Medium** (16px, 500): Button labels, primary interaction text, emphasized body copy.
- **Body Regular** (16px, 400): Standard body text, transaction descriptions, paragraphs.
- **Label Light** (14px, 300): Captions, metadata, secondary information, dates, amounts in secondary positions.
- **Label Thin** (12px, 100): Smallest text, tertiary information, timestamps, help text.

All text benefits from Poppins' built-in spacing and legibility; no custom line-height adjustments required unless otherwise specified.

## Layout

The design system follows an 8px base unit grid system, enabling consistent spacing and alignment across all screens. Mobile-first design (iOS/Android) with safe areas respected.

**Spacing Scale:**
- **XS (4px):** Micro-interactions, tight component spacing.
- **SM (8px):** Tight spacing between related elements, component padding.
- **MD (16px):** Standard spacing between sections, card padding.
- **LG (24px):** Spacing between major sections, large component padding.
- **XL (32px):** Page-level margins, significant vertical separation.

## Elevation & Depth

Light mode uses soft shadows and light backgrounds; dark mode uses subtle elevation with darker cards. No harsh shadows; focus on clean, minimal depth cues.

**Card Elevation:**
- Resting: No shadow; light grey/green background differentiates from page background.
- Hover: Subtle lift with soft shadow or background color change.

**Modal Elevation:**
- Scrim: Semi-transparent overlay (#000000 @ 30% opacity) behind modal.
- Modal card: Rounded 12px, white background in light mode, dark card in dark mode.

## Shapes

Rounded corners are consistent across the design system, creating a friendly, approachable aesthetic.

**Corner Radius Scale:**
- **SM (4px):** Subtle rounding on small components, text fields, slight button rounding.
- **MD (8px):** Standard button and small card rounding.
- **LG (12px):** Primary card rounding, dialog rounding, larger components.
- **XL (16px):** Large modals, full-screen surfaces.
- **Full (9999px):** Pill buttons, circular badges, fully rounded elements.

## Components

### Buttons

**Primary Button** — Caribbean Green background, white text, 12px vertical / 24px horizontal padding, rounded MD. Used for primary actions (Create Goal, Save, Continue).
- *Hover state:* Fence Green background, slight lift shadow.
- *Disabled state:* Light Green background, Cyprus text at 50% opacity.

**Secondary Button** — Ocean Blue background, white text, same padding and rounding. Used for secondary actions (Learn More, View Details, Cancel).
- *Hover state:* Dark Ocean Blue background.
- *Disabled state:* Light Blue background with opacity.

**Tertiary Button** — Light Green background, Caribbean Green text, same padding and rounding. Used for low-priority actions (Skip, Dismiss, Reset).
- *Hover state:* Light Green background becomes Cyprus Green text.

### Cards

**Standard Card** — White background (light mode) / Void + 10% (dark mode), rounded LG, 16px padding on all sides. Used for transactions, goals, accounts.
- *Hover state:* Light Green background tint (light mode) / subtle lift.
- *Selected state:* Caribbean Green left border or shadow.

### Text Fields & Inputs

**Text Input** — Light Green background, Cyprus text, 12px vertical / 16px horizontal padding, rounded MD. Border optional (Cyprus at 20% opacity).
- *Focus state:* Caribbean Green border (2px), Caribbean Green left accent.
- *Error state:* Light red/coral background or red border.
- *Placeholder text:* Cyprus at 40% opacity.

### Icons

Icons use two weights: solid (filled, primary actions) and outline (secondary, informational). Icons are sized at 24px (common actions), 32px (larger buttons/CTAs), 16px (secondary).

## Do's and Don'ts

**Do:**
- Use Caribbean Green for primary CTAs and positive financial moments (savings progress, goal achieved).
- Pair Ocean Blue with Caribbean Green for visual contrast in complex layouts.
- Maintain Poppins throughout; never substitute typefaces.
- Use rounded corners consistently; follow the shape scale.
- Prioritize clarity and legibility; generous whitespace over cramped layouts.

**Don't:**
- Use the primary green for large text areas; reserve it for highlights and action elements.
- Mix multiple typefaces; Poppins is the system font.
- Apply shadows beyond card and modal elevation; keep the design minimal.
- Use harsh colors or high-contrast combinations that create visual fatigue.
- Ignore the 8px grid; all spacing should align to the scale.

---

**Design System Last Updated:** May 23, 2026  
**Figma File:** FinWise Mobile App UI/UX Kit for Budget Tracker — Community Copy  
**Status:** Light mode fully specified; dark mode uses same tokens with background/text color inversions.
