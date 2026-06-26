# Visual Refresh — Design Spec

## Context

`arvic-realestate-site` is a static landing page (HTML/CSS/vanilla JS) for Arvic Gonzales, a Ray White Manukau real estate agent. The site currently uses a single typeface (Montserrat) throughout, a flat dark/gold palette, and generic gradient placeholders in place of photography. The goal of this pass is a visual/design-only polish — no new features, no content/copy rework, no backend changes — to make the site feel more premium and less templated.

## Goals

- Make the page feel premium and intentional rather than like a generic real-estate template.
- Keep the existing Ray White brand gold (`#f2c200`) as the single accent color.
- Keep the stats block as its own separate dark bar (not merged into the hero).
- No new dependencies beyond a Google Fonts import for the display typeface.
- No changes to JS behavior (filtering, pagination, listings data) — visual/CSS and minor markup only.

## Design Tokens

**Color**
- `--gold: #f2c200` (unchanged — brand accent, used sparingly: CTAs, tags, key numbers, the signature hairline)
- `--gold-dark: #d4a900` (unchanged — hover state)
- `--dark: #15140f` (was `#1a1a1a` — warmer near-black with a subtle gold undertone instead of neutral grey-black)
- `--grey: #6b6b6b` (unchanged — secondary text)
- `--light: #f5f5f5` (unchanged — section backgrounds)

**Type**
- Display (headlines, `h1`/`h2`, hero, section titles): `Fraunces` — a higher-contrast serif that reads editorial/premium, used with restraint (headlines only, not body copy).
- Body/UI (paragraphs, nav, buttons, form fields, listing card text): `Montserrat` (unchanged) — demoted from "everything" to body/UI role only.
- No third "utility" face needed — Montserrat at smaller sizes/letterspacing covers captions and meta text.

**Layout**
- Section vertical rhythm tightened/varied rather than uniform 80px everywhere: hero gets more height and density; content sections keep generous but slightly reduced padding (64–72px) so the hero reads as the clear high point.
- Stats remain a separate full-width dark bar between hero and listings (unchanged structurally from current site — only color/type tokens applied).
- Listing/service cards: refined hover (subtler lift + softer shadow transition, current translateY+shadow approach kept but tuned) and slightly more internal breathing room.
- Placeholder gradients (currently flat grey-to-black `placeholder-1/2/3` and `.about-photo`/`.ig-post`) replaced with warm charcoal-to-gold-edge gradients so the placeholders read as a deliberate stylistic choice rather than missing images.

**Signature element**
- A thin gold hairline rule paired with a small uppercase locale label ("MANUKAU, NZ") positioned near the hero headline. This is the one deliberately memorable detail tying the design to the agent's actual local differentiator. Used once in the hero — not repeated as decoration elsewhere on the page.

## Non-goals

- No copy/content changes.
- No new sections or features.
- No changes to `script.js` logic or `listings-data.js`.
- No restructuring of the listings/filtering/pagination markup beyond what's needed to apply new classes/tokens.
- No palette change beyond the `--dark` adjustment described above (gold accent stays as-is per explicit instruction).

## Implementation notes

- Add Fraunces via Google Fonts `<link>` alongside the existing Montserrat import in `index.html`.
- Token and typography changes live in `styles.css`; only minimal markup changes needed (e.g. adding a locale-label element near the hero `h1`).
- Verify responsive behavior is preserved at the existing breakpoints (900px, 600px).
