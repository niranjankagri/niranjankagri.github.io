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
| `style.css`, `theme.js`, `projects.js` | Shared responsive theme, navigation, project filters and interactions |
| `img/` | Portrait, avatar and local project-card report images |
| `Niranjan_Kumar_Agri_CV_Technical_Lead_QA_SDET.pdf` | Downloadable CV |

Workflow badges update when GitHub serves their image. Each project also links to its source and a dated repository or workflow record. The date identifies when the displayed evidence was checked; a past run is not presented as a current run.

The Quality Intelligence dashboard uses collected repository and CI result files. Its requirement catalog is synthetic. AI project CI uses hand-written or replayed examples; it does not claim live model results.

## Build and validate

Project data lives only in `tools/project_data.py`. Generated HTML files should not be edited by hand.

```bash
python tools/build_site.py
python tools/validate_site.py
```

The build uses Python's standard library and keeps the site usable without external services. Update an existing project's evidence URL, date and description in the shared record after checking its source repository and workflow. Keep sample, replayed and historical results labelled. New projects need a unique identifier and page slug, a category, technology tags, a local image with meaningful alternative text, and an evidence date and link.
