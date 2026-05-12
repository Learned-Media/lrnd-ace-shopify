# Ace Party & Tent Rental - Shopify Migration

> **Repository:** lrnd-ace-shopify
> **Purpose:** Shopify theme development for WooCommerce to Shopify migration
> **Last Updated:** 2026-05-12

---

## Project Overview

> **Client:** Ace Party & Tent Rental / Gandel family
> **Account:** LRND (Learned Media) - direct client (NOT via Liger)
> **Project Type:** WooCommerce (WordPress/Divi) to Shopify migration
> **Status:** Phase 2 - Homepage Section Builds (next)
> **Budget:** 200-280 hours
> **Timeline:** 10-12 weeks
> **Asana Project GID:** 1209399682946958
> **Harvest Project ID:** 43710972
> **Developer Brief:** `planning/developer-brief.md` (START HERE for new devs)

Ace Party is a B2B event rental company (tents, chairs, tables, linens, catering equipment) based in Port Washington, NY. Their current site runs WordPress/WooCommerce with a Divi child theme on WPEngine. The catalog is quote-based: 93% of products show "Request Pricing" instead of a fixed price.

New Figma designs exist for 6 content/marketing page templates. Product catalog pages (PDP, PLP, cart) will use Shopify defaults styled to match the brand.

---

## Current Phase Status

### Phase 1: Foundation - COMPLETE
- [x] Shopify dev store provisioned (acepartyrental.myshopify.com)
- [x] Shopify CLI installed and authenticated
- [x] Horizon v3.4.0 installed as live theme; dev sandbox "Ace Party [Dev]" (id: 155978104932)
- [x] Design tokens extracted from Figma, CSS custom properties defined
- [x] Zodiak font loading from Fontshare CDN (Geoform uses Montserrat fallback)
- [x] Header styled (promo bar, nav, dropdowns, mobile drawer, sticky) - ported to Horizon classes
- [x] Footer styled (gradient bg, newsletter, links, social, mobile) - ported to Horizon block structure
- [x] 23 Asana tickets written across 6 phases
- [x] Content reference, nav menu structure, and icon inventory documented
- [x] Developer brief written
- [x] 60 smart collections created (13 top-level + 47 sub-collections including tent types)
- [x] 689 products imported (draft status)
- [x] URL redirects imported
- [x] Nav menus built (build_nav.py ready to run)

### Phase 2: Homepage Sections - NEXT
7 custom Shopify sections to build:
- [ ] #04 Hero Carousel (blob mask, auto-advance, overlay CTAs)
- [ ] #05 Logo Grid ("Trusted by the Best", crossfade animation)
- [ ] #06 Two-Up Services (blob masks, overlaid buttons)
- [ ] #07 Event Cards (4-card grid, frosted-glass icon badges)
- [ ] #08 Tabbed Content ("40+ Years", sidebar tabs + image panels)
- [ ] #09 Testimonials + CTA (100px headline, 3-card carousel)
- [ ] #10 Feature/Blog Card (horizontal card with image + content)
- [ ] #11 Homepage Assembly + QA

---

## Repository Structure

```
lrnd-ace-shopify/
  CLAUDE.md                         # This file
  .gitignore
  planning/
    developer-brief.md              # START HERE - single dev entry point
    design-tokens-spec.md           # Figma design tokens (AUTHORITATIVE, 428 lines)
    extraction-summary.md           # WordPress data extraction (COMPLETE)
    content-reference.md            # Homepage content from current site
    nav-menu-structure.md           # Full navigation tree
    icon-inventory.md               # Icons and assets needed
    data-migration/                 # Product/content migration scripts (future)
    tickets/asana/                  # 23 Asana ticket specs
      00-README.md                  # Ticket index with phases
      01-23 individual tickets      # Full specs with Figma data
    qa/                             # QA reports (future)
  theme/                            # Shopify Horizon theme (v3.4.0) - migrated from Dawn 2026-05-12
    assets/
      ace-brand.css                 # Brand tokens + typography (274 lines)
      ace-header.css                # Header + promo bar overrides (161 lines)
      ace-footer.css                # Footer gradient + layout (217 lines)
    snippets/
      ace-fonts.liquid              # Zodiak CDN + Geoform placeholder
      stylesheets.liquid            # Modified: loads ace-brand/header/footer CSS
    layout/
      theme.liquid                  # Modified: renders ace-fonts snippet
  scripts/                          # Migration scripts (future)
```

---

## Architecture Pattern

All customization is additive - no Horizon core file edits:

1. Custom `ace-*.css` files layered after Horizon's base.css (via stylesheets.liquid)
2. Custom `ace-*.liquid` sections for new components
3. Custom `ace-*.js` files for interactive behavior
4. Horizon uses a block-based architecture (blocks/ directory) for header/footer composition

**Conventions:**
- CSS: `ace-{component}.css`, registered in `snippets/stylesheets.liquid`
- Sections: `ace-{component}.liquid`
- Snippets: `ace-{component}.liquid` for reusable partials
- Variables: `--ace-` prefix (defined in ace-brand.css)
- Commits: Conventional commits (`feat:`, `fix:`, `docs:`, `style:`)

**Horizon vs Dawn differences to know:**
- Nav links: `.menu-list__link` (not `.header__inline-menu .list-menu__item--link`)
- Logo: `.header-logo` (not `.header__heading-logo-wrapper`)
- Header actions: `.header-actions__action` (not `.header__icon`)
- Mega menu: `.mega-menu__link` (same in both)
- Mobile drawer: `.menu-drawer__menu-item` (same in both)
- Footer: block-based via `.footer-content` (not `.footer__content-top` / `.footer__blocks-wrapper`)
- No `mask-blobs.css` in Horizon - implement clip-path directly if needed

---

## Figma

**File key:** Mr6M1UwQ0i45tEOMHSHe6G

### Page Templates (6)

| Template | Node ID | Shopify Template |
|----------|---------|------------------|
| Homepage (Desktop) | 904:382 | templates/index.json |
| Blog Landing Page | 904:442 | templates/blog.json |
| Blog Detail | 904:467 | templates/article.json |
| Event Type Landing | 912:2416 | templates/page.event-type-landing.json |
| Event Detail | 912:2448 | templates/page.event-detail.json |
| Homepage (Mobile) | 904:1040 | (responsive version of index) |

### Homepage Sections

| Section | Node ID | Ticket |
|---------|---------|--------|
| Hero Carousel | 904:429 | #04 |
| Logo Grid | 904:755 | #05 |
| Two-Up Services | 904:425 | #06 |
| Event Cards | 904:411 | #07 |
| 40+ Years Tabbed | 904:406 | #08 |
| Testimonials + CTA | 904:384 | #09 |
| Feature/Blog Card | 904:418 | #10 |

### Key Components

| Component | Node ID |
|-----------|---------|
| Navigation | 904:688 |
| Footer (Desktop) | 904:359 |
| Footer (Mobile) | 904:1291 |
| Promo Bar | 904:532 |
| Buttons | 904:746 |
| Email Field | 904:1008 |

---

## Design Tokens (Quick Reference)

Full spec: `planning/design-tokens-spec.md` (AUTHORITATIVE)

| Token | Value | Notes |
|-------|-------|-------|
| Primary Blue | #005cba | Nav text, headings, links |
| Secondary Red | #ff595a | Primary button fill, accents |
| Text Blue | #063666 | Body text on light backgrounds |
| Background Taupe | #fdfcf8 | Alternating section bg |
| Footer Gradient | #0c6bcd to #387fd7 | linear-gradient(to right) |
| Heading Font | Geoform Medium 500 | All uppercase, 0.04em tracking |
| Body Font | Zodiak Regular 400 | Sentence case, 15px, 1.5 line height |
| Button Radius | 8px | Also cards and form fields |
| Image Radius | 24px | Carousel and hero images |
| Button Height | 40px | 12px/20px padding |

---

## Source Data

### WordPress Site

- **Production:** acepartyrental.com (WPEngine: acepartyandten)
- **Local copy:** ~/Local Sites/acepartyrental/app/public/
- **Local MySQL:** Port 10014, socket zpIcHGqUx, DB: local, user: root/root
- **Product CSV:** wp-content/webtoffee_export/product_export_2024-10-10-05-07-49.csv (may need re-export)

### Content Inventory

| Content | Count | Notes |
|---------|-------|-------|
| Products | 6,677 published | 93% quote-only, 12% have images |
| Pages | 30 published | All Divi Builder, 12 event type detail pages |
| Blog Posts | 20 published | All have Yoast SEO metadata |
| Contact Forms | 2 (CF7) | Contact page + Careers |
| Navigation Menus | 2 | Main Nav (product mega menu) + Secondary |
| Redirects | 14 active | Plus ~7,000 URL pattern changes |
| Media | ~21,025 files (1.6GB) | ~1.4GB after excluding form uploads/logs |
| Quote Requests | 2,281 | Confirms quote workflow is critical |
| Testimonials | 4 | Google Reviews |

---

## Quote/Estimate Workflow

93% of products are quote-only. Shopify implementation uses tag-based conditional logic:

```liquid
{% if product.tags contains 'quote-only' %}
  <!-- Quote app button: "Add to Estimate" -->
  <span class="price--request">Request Pricing</span>
{% else %}
  <!-- Standard Shopify add-to-cart -->
  {{ product.price | money }}
{% endif %}
```

Quote app (Quotify, SA Request a Quote) selection is pending.

---

## Open Blockers

| Blocker | Impact | Status |
|---------|--------|--------|
| Geoform font files (.woff2) | Visual fidelity | Using Montserrat fallback |
| Quote app selection | Core commerce feature | Evaluate for Phase 4 |
| Product CSV freshness | Oct 2024 export may be stale | Check before Phase 5 |
| Shopify plan tier | Feature availability | Confirm before checkout customization |
| DNS access | Required for launch | Unknown |

---

## Dev Environment

- **Live theme:** Horizon v3.4.0 (id: 153877020772) - production
- **Dev theme:** Ace Party [Dev] (id: 155978104932) - Horizon v3.4.0, unpublished sandbox
- **Preview URL:** https://acepartyrental.myshopify.com?preview_theme_id=155978104932
- **Theme editor:** https://acepartyrental.myshopify.com/admin/themes/155978104932/editor

```bash
# Live dev server (hot reload against dev theme)
cd /Users/mlovascio/GitHub/lrnd-ace-shopify/theme
SHOPIFY_CLI_THEME_TOKEN=$(op item get "Ace Shopify Admin API" --vault Engineering --fields label=credential --reveal) \
  shopify theme dev --store acepartyrental.myshopify.com --theme 155978104932
# Runs at http://127.0.0.1:9292

# Push specific files to dev theme
SHOPIFY_CLI_THEME_TOKEN=$(op item get "Ace Shopify Admin API" --vault Engineering --fields label=credential --reveal) \
  shopify theme push --store acepartyrental.myshopify.com --theme 155978104932 --only "assets/ace-brand.css"
```

Git push does NOT deploy to Shopify. Push separately via CLI.

---

## Time Tracking

Track all work to Harvest, ad-hoc project for Ace Party.
Notes format: "Ace + [activity]" (e.g., "Ace + Homepage template build")

---

## Key Reference Files

| File | Purpose |
|------|---------|
| `planning/developer-brief.md` | START HERE - single entry point for devs |
| `planning/design-tokens-spec.md` | AUTHORITATIVE design tokens (428 lines) |
| `planning/content-reference.md` | Homepage content from current site |
| `planning/nav-menu-structure.md` | Full navigation tree |
| `planning/icon-inventory.md` | Icons and assets checklist |
| `planning/extraction-summary.md` | WordPress data extraction overview |
| `planning/tickets/asana/00-README.md` | 23 tickets across 6 phases |

---

## Agent Guidelines

### Working on Theme Development

1. Read `planning/developer-brief.md` first
2. Read `planning/design-tokens-spec.md` before styling
3. Work in `theme/` directory
4. Use CSS custom properties from ace-brand.css
5. Never edit Horizon core files - override with CSS, add new sections
6. All Geoform text must be uppercase
7. For blob/organic shapes: use CSS clip-path directly (Horizon has no built-in mask-blobs.css)
8. Vanilla JS only, no frameworks or build tools

### Working on Data Migration

1. Read `planning/extraction-summary.md` for source data details
2. Product migration scripts go in `scripts/`
3. Tag products `quote-only` or `has-price` based on price data
4. Non-linen products first (~600), linens consolidated later

### Working on Content Pages

1. Check the Figma node ID (listed in Homepage Sections table above)
2. Use `mcp__claude_ai_Figma__get_design_context` with file key and node ID
3. Read the corresponding ticket in `planning/tickets/asana/`
4. Read `planning/content-reference.md` for real content to populate
5. Follow Horizon's block-based patterns for section structure (see blocks/ directory)

---

## Status Log

| Date | Event |
|------|-------|
| 2026-03-02 | Repository created, Dawn v15.4.1 cloned |
| 2026-03-02 | WordPress/WooCommerce extraction complete |
| 2026-03-02 | Design tokens extracted from Figma |
| 2026-03-02 | Phase 1 Foundation complete: tokens, header, footer, promo bar |
| 2026-03-02 | 23 Asana tickets written across 6 phases |
| 2026-03-03 | Pre-build docs complete: developer brief, content reference, nav structure, icon inventory |
