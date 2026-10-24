# niranjankagri.github.io

Portfolio site of Niranjan Kumar Agri (Technical Lead QA, Senior SDET and Test Automation Architect):
<https://niranjankagri.github.io>

The site is static and hosted by GitHub Pages. It does not call GitHub APIs or third-party analytics when a visitor opens a page.

## Pages and data

| File | Purpose |
|---|---|
| `index.html` | Home page, professional impact, live dashboard showcase, six featured projects, experience, skills and contact |
| `projects.html` | Searchable collection of all 25 projects; cards remain available without JavaScript |
| `projects/*.html` | One case study per project, with setup, architecture, dated evidence and limitations |
| `tools/project_data.py` | Shared project records, category and technology tags, evidence links and featured selection |
| `tools/make_*.py` | Static page and hosting metadata generators |
| `tools/validate_site.py` | Data, page, link, image, metadata and semantic structure checks |
| `tools/browser_smoke.py` | Playwright checks for routes, role cards, filters, dialogs, comparison, architecture and responsive layouts |
| `tools/stage_site.py` | Creates a clean `_site` deploy directory with the commit id and asset version |
| `tools/run_browser_smoke.py` | Serves the staged build locally, runs the browser matrix and captures review screenshots |
| `tools/serve_site.py` | Local static server with GitHub Pages-style 404 handling, used by the browser smoke |
| `tools/compare_visual_baselines.py` | Compares the review screenshots with reviewed baselines and writes expected, actual and difference images |
| `tools/wait_for_deployment.py` | Confirms Pages serves the expected commit and versioned assets |
| `.github/workflows/portfolio-validation.yml` | PR validation, gated Pages deployment and post-deploy smoke |
| `style.css`, `theme.js`, `projects.js` | Shared responsive theme, navigation, project filters and interactions |
| `img/` | Portrait, avatar and local project-card report images |
| `Niranjan_Kumar_Agri_CV_Technical_Lead_QA_SDET.pdf` | Downloadable CV |

Workflow badges update when GitHub serves their image. Each project also links to its source and a dated repository or workflow record. The date identifies when the displayed evidence was checked; a past run is not presented as a current run.

The Quality Intelligence dashboard uses collected repository and CI result files. Its requirement catalog is synthetic. AI project CI uses hand-written or replayed examples; it does not claim live model results.

## Project discovery and case studies

The homepage has focused role views for Senior SDET, QA Lead, and Automation Architect. These views point into the same 25-project catalog and do not hide the rest of the site. The collection supports URL-backed search, category and language filters, skill matching, role focus, three sort orders, previews, and comparison of up to three projects. Search and skill terms combine with category and language groups; selections within each category or language group use OR matching.

Explorer links can include `q`, repeated `category` and `tech` parameters, `skill`, `role`, `sort`, and repeated `compare` parameters. Case-study links retain the filtered results URL and scroll position for the Back to Projects action within the same browser tab. The explorer remains a static list when JavaScript is unavailable; previews, sorting, filters, and comparison require JavaScript.

Case studies share a generated layout with a contents list, evidence summary, limitations, related projects, and supporting links. Featured case studies add component details for the architecture maps, evidence tabs, and engineering stories. These interactions present existing project data and artifacts; they do not calculate project ratings or make unsupported performance claims. A static image is identified as a screenshot, and sample, replayed, synthetic, or historical evidence is labeled where it appears.

The architecture maps use a keyboard-operable component selector and detail panel on desktop, with a native single-column accordion on narrow screens. Featured report thumbnails retain their proportions, show a scope/date caption, and open in the existing image viewer. Enterprise's thumbnail is identified as a historical local report separate from the linked nightly run.

For implementation details and review screenshots, see [the portfolio UX upgrade notes](docs/ux-upgrade.md).

## Build and validate

Project data lives only in `tools/project_data.py`. Generated HTML files should not be edited by hand.

```bash
python tools/build_site.py
python tools/validate_site.py
```

For the full local browser check, install the pinned dependencies and run the staged-site smoke command. The script starts and stops its own static server, tests Chromium, Firefox and WebKit, checks the 28 routes and CV, and captures screenshots and traces on failure. axe-core runs WCAG 2.0, 2.1 and 2.2 A/AA checks.

```bash
python -m pip install playwright==1.63.0 ruff==0.17.1 Pillow==11.3.0
python -m playwright install chromium firefox webkit
npm install --prefix artifacts/a11y --no-save --no-package-lock axe-core@4.10.3
python tools/build_site.py
python tools/validate_site.py
python tools/stage_site.py --build-id local-review
ASSET_VERSION=$(python -c 'import json; print(json.load(open("_site/release.json", encoding="utf-8"))["asset_version"])')
python tools/run_browser_smoke.py --directory _site --build-id local-review --asset-version "$ASSET_VERSION" --axe-script artifacts/a11y/node_modules/axe-core/axe.min.js --browser all --capture-review artifacts/visual-review/actual
python tools/compare_visual_baselines.py --baselines screenshots/portfolio-ux-review/baselines --actual artifacts/visual-review/actual --failures artifacts/visual-review/failures
```

CI runs the same comparison and fails on any visual difference; how to review and accept an intended change is in [the visual regression workflow](docs/visual-regression.md).

Pull requests validate but do not deploy. Pushes to `main` and manual workflow runs on `main` deploy the validated artifact; a separate job waits for the deployed build id and runs browser smoke against the public site. `Portfolio validation and local browser smoke` is configured as a required check on `main`.

The site build uses Python's standard library and remains usable without external services; browser validation installs Playwright and axe-core in CI. Update an existing project's evidence URL, date and description in the shared record after checking its source repository and workflow. Keep sample, replayed and historical results labelled. New projects need a unique identifier and page slug, a category, technology tags, a local image with meaningful alternative text, and an evidence date and link.
