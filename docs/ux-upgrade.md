# Portfolio UI/UX upgrade

## What changed

- Added role-focused entry points for Senior SDET, QA Lead, and Automation Architect, tied to named project records and a URL-backed project explorer.
- Refined the shared visual system with neutral section bands, restrained accent colors, a CSS engineering grid and portrait glow, a pointer glow limited to fine-pointer devices, and reduced-motion fallbacks.
- Reworked project cards and filters to make purpose, result, evidence kind, and evidence date easier to scan. Search, category, language, skill, role, sort, and comparison selection are represented in the URL.
- Added accessible project preview and comparison dialogs. Comparisons show catalog facts about test layers, targets, CI, reporting, approach, and limitations; they do not rank projects.
- Standardized generated case studies with contents navigation, an evidence summary, dated evidence, explicit limitations, related projects, and return-to-filtered-results behavior.
- Preserved existing section and image hash anchors while pointing the older contribution, feature, and defect links into the current test-scope or evidence sections.
- Added source-linked architecture explorers for Enterprise TAF, Quality Intelligence, and Playwright + TypeScript, with evidence-grounded engineering stories for Enterprise TAF, Playwright + TypeScript, and k6.
- Improved wrapping for related-project summaries and narrow-screen architecture/code diagrams so long text remains readable without widening or clipping the page.
- Aligned role cards at desktop widths, kept each expansion independent, and stacked the cards before narrow layouts become cramped.
- Added dated scope captions to featured report images, concise result summaries, enlargement dialogs, and a historical/separate-run label for Enterprise evidence.
- Rebuilt the desktop architecture explorer as a padded selector/detail layout and retained a native mobile disclosure list with a no-script fallback.
- Added release metadata, versioned CSS/JavaScript assets, browser smoke automation, visual review captures, and a gated GitHub Pages deployment workflow.
- Kept all pages static and GitHub Pages compatible. Project records and case-study pages are generated locally; visitor interactions make no GitHub API or analytics requests.

## Evidence and claim boundaries

Project metadata is maintained in `tools/project_data.py` and consumed by the static generators. The Enterprise TAF architecture SVG summarizes the repository's documented design, and component links point to corresponding source paths. Playwright + TypeScript details cite its test, fixture, page-object, API, and CI structure; its story describes documented shared-demo data changes and the project’s mitigation, while retaining the CI bot-check limitation. The Quality Intelligence catalog is synthetic; collected repository and CI result files are described separately. k6 story values come from the same documented demo-shop stress scenario and include its environment and interpretation limits. Screenshots remain identified as static examples, with capture dates stated only when recorded. Dated repository evidence is a check date, not a promise that an older workflow is currently passing.

Comparison metadata describes implementation details documented in the project records and case studies. Empty or general evidence boundaries are preferred over an inferred quality score, severity, root cause, or measured improvement.

## Validation

Run the local generator and structural validator from the repository root:

```bash
python tools/build_site.py
python tools/validate_site.py
node --check projects.js
node --check theme.js
```

The validator checks all 25 project records and 28 generated pages, comparison fields, human-readable workflow/report labels, page landmarks, local links and assets, the CV PDF, captions, architecture metadata, and required case-study content. Browser smoke covers Chromium, Firefox and WebKit, all case-study footers, role and filter history, preview and comparison dialogs, evidence tabs, architecture components, reduced motion, no-JavaScript fallbacks, and responsive widths from 320 to 1440 CSS pixels. The 720 CSS pixel reflow check approximates a 1440 CSS pixel viewport at 200% zoom.

axe-core 4.10.3 scans the 28 pages in Chromium and checks the home page, project explorer, three architecture case studies, 404 page, and open dialogs in both themes. The key text, muted-text, link, and primary-button color pairs measure at least 6.26:1 in light mode and 10.17:1 in dark mode. Dialog focus restoration, keyboard navigation, and touch layouts are included in browser smoke.

## Review screenshots

The earlier captures show the merge-base design. The new captures show this branch’s local static build for pull request review; neither set represents hosted production data.

| Section and viewport | Earlier light | Earlier dark | Refined light | Refined dark |
|---|---|---|---|---|
| Home hero, desktop | ![Earlier home desktop light](../screenshots/enterprise-ux/home-desktop-light.png) | ![Earlier home desktop dark](../screenshots/enterprise-ux/home-desktop-dark.png) | ![Refined hero desktop light](../screenshots/portfolio-ux-review/hero-desktop-light.png) | ![Refined hero desktop dark](../screenshots/portfolio-ux-review/hero-desktop-dark.png) |
| Home hero, mobile | ![Earlier home mobile light](../screenshots/enterprise-ux/home-mobile-light.png) | ![Earlier home mobile dark](../screenshots/enterprise-ux/home-mobile-dark.png) | ![Refined hero mobile light](../screenshots/portfolio-ux-review/hero-mobile-light.png) | ![Refined hero mobile dark](../screenshots/portfolio-ux-review/hero-mobile-dark.png) |
| Project collection, desktop | ![Earlier collection desktop light](../screenshots/enterprise-ux/projects-desktop-light.png) | ![Earlier collection desktop dark](../screenshots/enterprise-ux/projects-desktop-dark.png) | ![Refined collection desktop light](../screenshots/portfolio-ux-review/collection-desktop-light.png) | ![Refined collection desktop dark](../screenshots/portfolio-ux-review/collection-desktop-dark.png) |
| Project collection, mobile | ![Earlier collection mobile light](../screenshots/enterprise-ux/projects-mobile-light.png) | ![Earlier collection mobile dark](../screenshots/enterprise-ux/projects-mobile-dark.png) | ![Refined collection mobile light](../screenshots/portfolio-ux-review/collection-mobile-light.png) | ![Refined collection mobile dark](../screenshots/portfolio-ux-review/collection-mobile-dark.png) |
| Role explorer, desktop | — | — | ![Refined role explorer light](../screenshots/portfolio-ux-review/role-desktop-light.png) | ![Refined role explorer dark](../screenshots/portfolio-ux-review/role-desktop-dark.png) |
| Featured projects, desktop | — | — | ![Refined featured projects light](../screenshots/portfolio-ux-review/featured-desktop-light.png) | ![Refined featured projects dark](../screenshots/portfolio-ux-review/featured-desktop-dark.png) |
| Featured projects, tablet | — | — | ![Refined featured projects tablet light](../screenshots/portfolio-ux-review/featured-tablet-light.png) | ![Refined featured projects tablet dark](../screenshots/portfolio-ux-review/featured-tablet-dark.png) |
| Featured projects, mobile | — | — | ![Refined featured projects mobile light](../screenshots/portfolio-ux-review/featured-mobile-light.png) | ![Refined featured projects mobile dark](../screenshots/portfolio-ux-review/featured-mobile-dark.png) |

Expanded architecture views: [Enterprise desktop light](../screenshots/portfolio-ux-review/architecture-enterprise-desktop-light.png), [Enterprise desktop dark](../screenshots/portfolio-ux-review/architecture-enterprise-desktop-dark.png), [Enterprise mobile expanded](../screenshots/portfolio-ux-review/architecture-enterprise-mobile-expanded-dark.png), [Quality Intelligence desktop light](../screenshots/portfolio-ux-review/architecture-quality-intelligence-desktop-light.png), [Quality Intelligence mobile expanded](../screenshots/portfolio-ux-review/architecture-quality-intelligence-mobile-expanded-dark.png), [Playwright + TypeScript desktop light](../screenshots/portfolio-ux-review/architecture-playwright-typescript-desktop-light.png), and [Playwright + TypeScript mobile expanded](../screenshots/portfolio-ux-review/architecture-playwright-typescript-mobile-expanded-dark.png).

Earlier case-study captures: [Playwright + TypeScript architecture, desktop](../screenshots/enterprise-ux/playwright-ts-architecture-desktop-light.png), [architecture, mobile](../screenshots/enterprise-ux/playwright-ts-architecture-mobile-dark.png), [engineering story](../screenshots/enterprise-ux/playwright-ts-story-desktop-dark.png), and [related-projects and next-project navigation](../screenshots/enterprise-ux/playwright-ts-related-desktop-light.png).

Footer and comparison captures: [Playwright + TypeScript case-study footer](../screenshots/portfolio-ux-review/case-footer-playwright-typescript.png), [Enterprise case-study footer](../screenshots/portfolio-ux-review/case-footer-enterprise.png), and [three-project comparison](../screenshots/portfolio-ux-review/comparison-desktop-light.png).

Contact section captures: [desktop light](../screenshots/portfolio-ux-review/contact-desktop-light.png), [desktop dark](../screenshots/portfolio-ux-review/contact-desktop-dark.png), [mobile light](../screenshots/portfolio-ux-review/contact-mobile-light.png), and [mobile dark](../screenshots/portfolio-ux-review/contact-mobile-dark.png).

Expanded role states: [Senior SDET desktop](../screenshots/portfolio-ux-review/role-expanded-senior-sdet-desktop-light.png) and [mobile](../screenshots/portfolio-ux-review/role-expanded-senior-sdet-mobile-dark.png), [QA Lead desktop](../screenshots/portfolio-ux-review/role-expanded-qa-lead-desktop-light.png) and [mobile](../screenshots/portfolio-ux-review/role-expanded-qa-lead-mobile-dark.png), [Automation Architect desktop](../screenshots/portfolio-ux-review/role-expanded-automation-architect-desktop-light.png) and [mobile](../screenshots/portfolio-ux-review/role-expanded-automation-architect-mobile-dark.png).

## Portfolio and dashboard visual alignment — 24 October 2026

The shared theme uses black headings, white/slate surfaces and blue interaction accents, with
teal reserved for the NA monogram. Dark mode uses the same structure with light text. The hero
keeps the existing portrait and professional copy, with a calmer text/portrait balance and a
light frame. Experience disclosures, project filters, image viewers and reduced-motion handling
remain available.

A homepage Quality Intelligence showcase reuses its canonical project record and dated local
screenshot. Its direct live-dashboard action and case-study path are distinct. The screenshot's
capture date and synthetic-catalog limitation remain beside it; it is not a live status widget.
The six featured cards keep their source links, dated evidence and report captions, with cleaner
spacing and aligned descriptions. Career facts, project results and the CV are unchanged.

Browser smoke exercises the showcase's case-study return path and preserves the existing
navigation/filter/preview/comparison checks. Visual captures include the showcase at desktop and
phone widths in both themes, alongside the existing component baselines.

## Recruiter-first follow-up (26 October 2026)

The home page now leads with three flagship projects (Enterprise, Quality Intelligence and AI-assisted testing). The full 25-project catalogue, six featured records, role/problem paths, architecture explorers and comparison controls remain available. Career history precedes the exploration paths. Capabilities, working method, evidence and skills use native disclosures to reduce the initial page length; `#skills` opens its disclosure, including on initial navigation.

Flagship briefs and case-study stories share `tools/portfolio_content.py`. Results, dates, preview captions and evidence URLs still come from the existing catalogue. The AI story explicitly distinguishes hand-written samples/replays from live model performance; no customer impact, new measurements or availability claims were introduced.

The dashboard walkthrough is a local scope builder, not an embedded dashboard or a data feed. Changing repository resets the browser; API selections disable it. A reset restores the default repository and removes any browser scope. The outgoing link opens the live report's results route with repository/kind/browser query parameters. Choices are curated navigation examples, not a promise that a matching execution exists. Without JavaScript, the link opens the dashboard home page and explains how to select scope there.

Home, catalogue and all 25 case studies have dedicated 1200×630 JPEG sharing cards. Regenerate with `python tools/make_social_previews.py` after installing Pillow 11.3 and DejaVu Sans. These are text-and-shape graphics, not result screenshots. They are checked in; normal site builds do not require graphics regeneration. No CV, career fact or relocation/permit claim was changed.

Browser smoke covers dependent scope resets, API/browser exclusion, keyboard reset, deep-linked skills disclosure and three flagship cards. The existing three-browser, accessibility, strict visual comparison and post-deployment checks remain enabled. Four walkthrough screenshots extend the existing visual matrix to 54 comparisons.
