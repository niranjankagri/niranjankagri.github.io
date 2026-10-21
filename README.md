# niranjankagri.github.io

Portfolio site of Niranjan Kumar Agri (Technical Lead QA, Senior SDET and Test Automation Architect):
<https://niranjankagri.github.io>

The site is static and hosted by GitHub Pages. It does not call GitHub APIs or third-party analytics when a visitor opens a page.

## Pages and data

| File | Purpose |
|---|---|
| `index.html` | Concise home page, professional impact, six featured projects, experience, skills and contact |
| `projects.html` | Searchable collection of all 25 projects; cards remain available without JavaScript |
| `projects/*.html` | One case study per project, with setup, architecture, dated evidence and limitations |
| `tools/project_data.py` | Shared project records, category and technology tags, evidence links and featured selection |
| `tools/make_*.py` | Static page and hosting metadata generators |
| `tools/validate_site.py` | Data, page, link, image, metadata and semantic structure checks |
| `tools/browser_smoke.py` | Optional Playwright checks for role views, filters, dialogs, case-study controls and responsive layouts |
| `style.css`, `theme.js`, `projects.js` | Shared responsive theme, navigation, project filters and interactions |
| `img/` | Portrait, avatar and local project-card report images |
| `Niranjan_Kumar_Agri_CV_Technical_Lead_QA_SDET.pdf` | Downloadable CV |

Workflow badges update when GitHub serves their image. Each project also links to its source and a dated repository or workflow record. The date identifies when the displayed evidence was checked; a past run is not presented as a current run.

The Quality Intelligence dashboard uses collected repository and CI result files. Its requirement catalog is synthetic. AI project CI uses hand-written or replayed examples; it does not claim live model results.

## Project discovery and case studies

The homepage has focused role views for Senior SDET, QA Lead, and Automation Architect. These views point into the same 25-project catalog and do not hide the rest of the site. The collection supports URL-backed search, category and language filters, skill matching, role focus, three sort orders, previews, and comparison of up to three projects. Search and skill terms combine with category and language groups; selections within each category or language group use OR matching.

Explorer links can include `q`, repeated `category` and `tech` parameters, `skill`, `role`, `sort`, and repeated `compare` parameters. Case-study links retain the filtered results URL and scroll position for the Back to Projects action within the same browser tab. The explorer remains a static list when JavaScript is unavailable; previews, sorting, filters, and comparison require JavaScript.

Case studies share a generated layout with a contents list, evidence summary, limitations, related projects, and supporting links. Featured case studies add component details for the architecture maps, evidence tabs, and engineering stories. These interactions present existing project data and artifacts; they do not calculate project ratings or make unsupported performance claims. A static image is identified as a screenshot, and sample, replayed, synthetic, or historical evidence is labeled where it appears.

For implementation details and review screenshots, see [the portfolio UX upgrade notes](docs/ux-upgrade.md).

## Build and validate

Project data lives only in `tools/project_data.py`. Generated HTML files should not be edited by hand.

```bash
python tools/build_site.py
python tools/validate_site.py
```

For interactive browser checks, install Playwright for Python and its browser binaries, then serve the generated site and run the smoke script:

```bash
python -m pip install playwright
python -m playwright install chromium firefox webkit
# Terminal 1
python -m http.server 8765
# Terminal 2
python tools/browser_smoke.py --base-url http://127.0.0.1:8765
```

The build uses Python's standard library and keeps the site usable without external services. Update an existing project's evidence URL, date and description in the shared record after checking its source repository and workflow. Keep sample, replayed and historical results labelled. New projects need a unique identifier and page slug, a category, technology tags, a local image with meaningful alternative text, and an evidence date and link.
