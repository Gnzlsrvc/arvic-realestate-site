# Visual Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply a CSS/markup-only premium visual polish pass to the existing static real-estate landing page, per `docs/superpowers/specs/2026-06-26-visual-refresh-design.md`.

**Architecture:** This is a 3-file static site (`index.html`, `styles.css`, `script.js` + `listings-data.js`, untouched). There is no test framework or build step — verification is manual: open `index.html` directly in a browser (or a simple static server) after each task and visually confirm the change, checking both desktop width and the existing 900px/600px breakpoints.

**Tech Stack:** Plain HTML/CSS/vanilla JS. One new external dependency: Google Fonts `Fraunces` import (display typeface).

## Global Constraints

- Keep `--gold: #f2c200` and `--gold-dark: #d4a900` unchanged — single accent color, do not introduce a second accent.
- Keep the stats block (`.stats` section in `index.html:46-53`) as its own separate full-width dark bar — do not merge it into the hero.
- No new dependencies beyond the Fraunces Google Fonts `<link>`.
- No changes to `script.js` or `listings-data.js` logic — JS-driven behavior (filtering, pagination, reveal-on-scroll) must work identically after this pass.
- No copy/content changes, no new sections, no restructuring of listings/filtering/pagination markup beyond adding classes needed for styling.
- Preserve responsive behavior at the existing breakpoints: `@media (max-width: 900px)` and `@media (max-width: 600px)` in `styles.css:392-401`.

---

### Task 1: Add Fraunces font and update color/type tokens

**Files:**
- Modify: `index.html:8` (font import line)
- Modify: `styles.css:1-17` (`:root` tokens and base `body`/heading rules)

**Interfaces:**
- Produces: `--dark: #15140f` (replaces `#1a1a1a`, used by every section that currently references `var(--dark)` — no signature change, same variable name).
- Produces: a `--font-display: 'Fraunces', serif` custom property and applies it to `h1, h2, h3` (replacing the current bare `h1, h2, h3 { font-weight: 700; }` rule, which currently inherits Montserrat from `body`).

- [ ] **Step 1: Add the Fraunces font import to `index.html`**

In `index.html`, change line 8 from:

```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

to two lines (combined Google Fonts request, one HTTP call):

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

- [ ] **Step 2: Update color and type tokens in `styles.css`**

Change `styles.css:1-17` from:

```css
:root {
  --red: #f2c200;
  --red-dark: #d4a900;
  --dark: #1a1a1a;
  --grey: #6b6b6b;
  --light: #f5f5f5;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  font-family: 'Montserrat', sans-serif;
  color: var(--dark);
  line-height: 1.6;
}
```

to:

```css
:root {
  --red: #f2c200;
  --red-dark: #d4a900;
  --dark: #15140f;
  --grey: #6b6b6b;
  --light: #f5f5f5;
  --font-display: 'Fraunces', serif;
  --font-body: 'Montserrat', sans-serif;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  font-family: var(--font-body);
  color: var(--dark);
  line-height: 1.6;
}
```

Then change `styles.css:44` from:

```css
h1, h2, h3 { font-weight: 700; }
```

to:

```css
h1, h2, h3 { font-family: var(--font-display); font-weight: 600; }
```

(Note: the existing variable name `--red`/`--red-dark` is kept as-is — it's the existing gold accent variable, just named `--red` historically. Do not rename it; other rules throughout `styles.css` already reference `var(--red)`.)

- [ ] **Step 3: Manually verify**

Open `index.html` in a browser (e.g. `open index.html` from the project directory on macOS, or any local static server). Confirm:
- All headings (`Selling Manukau Homes...`, `Featured Listings`, `Recently Sold`, etc.) now render in the Fraunces serif, not Montserrat.
- Body text, nav, and buttons still render in Montserrat.
- The dark sections (header overlay, stats bar, reviews, contact, footer) show the new warmer near-black (`#15140f`) instead of the old neutral `#1a1a1a` — these will look very close; check via browser inspector that `--dark` resolves to `#15140f`.

- [ ] **Step 4: Commit**

```bash
git add index.html styles.css
git commit -m "Add Fraunces display typeface and warm the dark token"
```

---

### Task 2: Add hero signature element (hairline + locale label)

**Files:**
- Modify: `index.html:28-44` (hero section markup)
- Modify: `styles.css:94-142` (`.hero` rules)

**Interfaces:**
- Produces: `.hero-eyebrow` class (gold hairline + uppercase locale label), placed directly above the `<h1>` inside `.hero-content`. No other task depends on this class name, but it must not collide with any existing class — confirmed no `.hero-eyebrow` exists in current `styles.css`.

- [ ] **Step 1: Add the eyebrow markup to the hero section**

In `index.html`, change lines 30-32 from:

```html
  <div class="container hero-content">
    <h1>Selling Manukau Homes<br>With Local Expertise</h1>
    <p>Arvic Gonzales — your trusted Ray White Manukau real estate agent</p>
```

to:

```html
  <div class="container hero-content">
    <div class="hero-eyebrow"><span class="hero-eyebrow-rule"></span>Manukau, NZ</div>
    <h1>Selling Manukau Homes<br>With Local Expertise</h1>
    <p>Arvic Gonzales — your trusted Ray White Manukau real estate agent</p>
```

- [ ] **Step 2: Style the eyebrow in `styles.css`**

In `styles.css`, after the existing `.hero-content` rule (currently `styles.css:109-113`):

```css
.hero-content {
  position: relative;
  z-index: 2;
  margin: 0 auto;
}
```

add a new rule directly after it:

```css
.hero-eyebrow {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: var(--red);
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 18px;
}
.hero-eyebrow-rule {
  display: inline-block;
  width: 36px;
  height: 2px;
  background: var(--red);
}
```

- [ ] **Step 3: Manually verify**

Reload `index.html` in the browser. Confirm a small gold "— MANUKAU, NZ" label with a short gold hairline appears centered above the "Selling Manukau Homes" headline, and that it does not appear anywhere else on the page. Check at 900px and 600px widths (browser dev tools responsive mode) that it stays centered and doesn't wrap awkwardly.

- [ ] **Step 4: Commit**

```bash
git add index.html styles.css
git commit -m "Add hero locale signature element"
```

---

### Task 3: Tighten section rhythm and refine card hover/placeholder gradients

**Files:**
- Modify: `styles.css:155-158` (generic section padding)
- Modify: `styles.css:167-176` (`.listing-card` hover)
- Modify: `styles.css:185-187` (`placeholder-1/2/3` gradients)
- Modify: `styles.css:248-251` (`.about-photo` gradient)
- Modify: `styles.css:265-277` (`.service-card` hover)

**Interfaces:**
- No new classes introduced; existing class names (`.listing-card`, `.service-card`, `.placeholder-1/2/3`, `.about-photo`) keep identical names and HTML hooks — only the CSS rule bodies change.

- [ ] **Step 1: Reduce generic section padding**

In `styles.css`, change line 156 from:

```css
section { padding: 80px 0; }
```

to:

```css
section { padding: 68px 0; }
```

- [ ] **Step 2: Increase hero height/density so it remains the visual high point**

In `styles.css`, change line 97 from:

```css
  min-height: 600px;
```

to:

```css
  min-height: 680px;
```

(within the existing `.hero` rule block at `styles.css:95-103`).

- [ ] **Step 3: Refine listing card hover transition**

Change `styles.css:173-176` from:

```css
.listing-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.12);
}
```

to:

```css
.listing-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 30px rgba(0,0,0,0.1);
}
```

And increase card body breathing room — change `styles.css:198` from:

```css
.listing-body { padding: 20px; }
```

to:

```css
.listing-body { padding: 24px; }
```

- [ ] **Step 4: Replace flat grey placeholder gradients with warm charcoal-to-gold-edge gradients**

Change `styles.css:185-187` from:

```css
.placeholder-1 { background: linear-gradient(135deg, #3a3a3a, #111); }
.placeholder-2 { background: linear-gradient(135deg, #555, #1a1a1a); }
.placeholder-3 { background: linear-gradient(135deg, #2b2b2b, #000); }
```

to:

```css
.placeholder-1 { background: linear-gradient(135deg, #3a3326, #15140f 70%, #f2c200 140%); }
.placeholder-2 { background: linear-gradient(135deg, #4a4030, #15140f 70%, #f2c200 140%); }
.placeholder-3 { background: linear-gradient(135deg, #2b2620, #000 70%, #f2c200 140%); }
```

(The gold stop at `140%` falls outside the visible gradient area, producing a subtle warm edge glow rather than an obvious yellow patch — this matches the spec's "gold-edge" description without overpowering the gold accent's restraint rule.)

- [ ] **Step 5: Apply the same warm gradient treatment to `.about-photo`**

Change `styles.css:248-251` from:

```css
.about-photo {
  height: 400px;
  border-radius: 6px;
  background: linear-gradient(135deg, #444, #1a1a1a);
}
```

to:

```css
.about-photo {
  height: 400px;
  border-radius: 6px;
  background: linear-gradient(135deg, #4a4030, #15140f 70%, #f2c200 140%);
}
```

- [ ] **Step 6: Refine service card hover to match the listing card tuning**

Change `styles.css:274-277` from:

```css
.service-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.1);
}
```

to:

```css
.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 30px rgba(0,0,0,0.1);
}
```

- [ ] **Step 7: Manually verify**

Reload `index.html`. Confirm:
- Section spacing feels tighter/more varied than before, with the hero still clearly the tallest/densest section.
- Hovering a listing card or service card shows a subtler lift with a softer, larger-radius shadow.
- The Instagram placeholder tiles, "About" photo placeholder, and listing placeholder images show a warm charcoal gradient with a faint gold glow at one edge, not a flat grey-to-black gradient.
- At 600px width, sections still stack correctly and nothing overflows horizontally (check `.about-inner`, `.instagram-grid`, `.listing-grid` collapse to single/double column per the existing media queries at `styles.css:392-401`).

- [ ] **Step 8: Commit**

```bash
git add styles.css
git commit -m "Tighten section rhythm and warm placeholder gradients"
```

---

### Task 4: Full-page visual regression pass

**Files:**
- None (verification-only task, no code changes expected unless an issue is found)

**Interfaces:**
- N/A

- [ ] **Step 1: Walk the full page at desktop width (~1440px)**

Open `index.html` and scroll through every section top to bottom: header, hero, stats, listings, sold, office listings, about, services, reviews, instagram, contact, footer. Confirm:
- No layout breakage (overlapping text, broken grids, illegible contrast — gold text on the new `#15140f` dark should still pass basic legibility).
- Fraunces only appears on headings, never on body copy, nav, or buttons.
- The stats bar (`.stats`) is still visually a separate full-width dark block sitting between hero and listings — not merged into the hero.

- [ ] **Step 2: Walk the full page at 900px and 600px widths**

Using browser dev tools responsive mode, set width to 900px then 600px and repeat the scroll-through. Confirm the existing breakpoint rules (`styles.css:392-401`) still collapse the nav, grids, and hero search bar as before — this plan did not touch those media query rules, so behavior should be unchanged, but confirm nothing in Tasks 1-3 broke them (e.g. the new hero min-height or eyebrow element doesn't overflow on mobile).

- [ ] **Step 3: Confirm JS-driven behavior is unaffected**

Click the office-listings filter pills (All / For Sale / Sold) and the pagination buttons; confirm filtering/pagination still works exactly as before (no JS was touched, but this confirms no CSS change broke a JS-dependent visual state like `.is-hidden` or `.filter-btn.active`).

- [ ] **Step 4: Fix any issues found, otherwise commit a final no-op marker is unnecessary — if no issues, this task ends without a commit**

If issues were found and fixed in this task, commit:

```bash
git add index.html styles.css
git commit -m "Fix visual regressions from refresh pass"
```

If no issues were found, no commit is needed — the plan is complete.
