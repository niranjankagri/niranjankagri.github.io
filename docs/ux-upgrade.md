# Portfolio UI/UX upgrade

## What changed

- Added role-focused entry points for Senior SDET, QA Lead, and Automation Architect, tied to named project records and a URL-backed project explorer.
- Refined the shared visual system with neutral section bands, restrained accent colors, a CSS engineering grid and portrait glow, a pointer glow limited to fine-pointer devices, and reduced-motion fallbacks.
- Reworked project cards and filters to make purpose, result, evidence kind, and evidence date easier to scan. Search, category, language, skill, role, sort, and comparison selection are represented in the URL.
- Added accessible project preview and comparison dialogs. Comparisons show catalog facts about test layers, targets, CI, reporting, approach, and limitations; they do not rank projects.
- Standardized generated case studies with contents navigation, an evidence summary, dated evidence, explicit limitations, related projects, and return-to-filtered-results behavior.
- Preserved existing section and image hash anchors while pointing the older contribution, feature, and defect links into the current test-scope or evidence sections.
- Added component-level architecture descriptions for Enterprise TAF and Quality Intelligence, evidence tabs where material exists, and evidence-grounded engineering stories for Enterprise TAF and k6.
- Kept all pages static and GitHub Pages compatible. Project records and case-study pages are generated locally; visitor interactions make no GitHub API or analytics requests.

## Evidence and claim boundaries

Project metadata is maintained in `tools/project_data.py` and consumed by the static generators. The Enterprise TAF architecture SVG summarizes the repository's documented design, and component links point to the corresponding source folders. The Quality Intelligence catalog is synthetic; collected repository and CI result files are described separately. k6 story values come from the same documented demo-shop stress scenario and include its environment and interpretation limits. Screenshots remain identified as static examples, with capture dates stated only when recorded. Dated repository evidence is a check date, not a promise that an older workflow is currently passing.

Comparison metadata describes implementation details documented in the project records and case studies. Empty or general evidence boundaries are preferred over an inferred quality score, severity, root cause, or measured improvement.

## Validation

Run the local generator and structural validator from the repository root:

```bash
python tools/build_site.py
python tools/validate_site.py
node --check projects.js
node --check theme.js
```

The validator checks project counts and required fields, role and comparison references, generated-page metadata and landmarks, accessible names for buttons, image dimensions and alternative text, local paths and anchors, key explorer controls, and case-study evidence and limitations. The browser smoke script exercises the main interactions in Chromium, Firefox and WebKit, plus responsive widths, keyboard flows, reduced motion, copy-email feedback, and the static no-JavaScript project list.

An axe-core 4.10.3 WCAG 2.0, 2.1 and 2.2 A/AA scan found no automated violations across the home page, project explorer, Enterprise and Quality Intelligence case studies in both themes, and the open project preview. Manual review also covered keyboard focus return and dialog containment. The measured foreground token pairs exceed 4.5:1 against the page background in both themes; the lowest measured pair is light-theme teal at 5.68:1.

## Review screenshots

These captures use the local static build and are intended for pull request review. They do not represent hosted production data.

| Page and viewport | Light | Dark |
|---|---|---|
| Home, desktop | ![Home desktop light](../screenshots/enterprise-ux/home-desktop-light.png) | ![Home desktop dark](../screenshots/enterprise-ux/home-desktop-dark.png) |
| Home, mobile | ![Home mobile light](../screenshots/enterprise-ux/home-mobile-light.png) | ![Home mobile dark](../screenshots/enterprise-ux/home-mobile-dark.png) |
| Project explorer, desktop | ![Projects desktop light](../screenshots/enterprise-ux/projects-desktop-light.png) | ![Projects desktop dark](../screenshots/enterprise-ux/projects-desktop-dark.png) |
| Project explorer, mobile | ![Projects mobile light](../screenshots/enterprise-ux/projects-mobile-light.png) | ![Projects mobile dark](../screenshots/enterprise-ux/projects-mobile-dark.png) |

Case-study views: [Enterprise case, desktop light](../screenshots/enterprise-ux/enterprise-case-desktop-light.png), [Enterprise architecture, desktop dark](../screenshots/enterprise-ux/enterprise-architecture-desktop-dark.png), [Enterprise case, mobile dark](../screenshots/enterprise-ux/enterprise-case-mobile-dark.png).
