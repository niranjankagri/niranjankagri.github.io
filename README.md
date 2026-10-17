# niranjankagri.github.io

Portfolio site of Niranjan Kumar Agri (Technical Lead QA | Senior SDET | Test Automation Architect):
https://niranjankagri.github.io

Static pages served by GitHub Pages, no build step:

| File | What |
|---|---|
| `index.html` | home page: summary, work results with how they were measured, sixteen featured projects, more projects, experience, skills, contact |
| `projects/*.html` | one page per featured project: purpose, stack, architecture, decisions, features, how to run, results, CI, limitations |
| `style.css`, `theme.js` | shared styles; light/dark toggle |
| `img/` | crops of each framework's own test report |
| `Niranjan_Kumar_Agri_CV_Technical_Lead_QA_SDET.pdf` | CV (website version: no phone number) |

Every project claim is taken from the project's own README; CI badges are the live GitHub Actions status.

## Updating the site

The pages are generated; edit the data in the scripts, not the HTML:

```bash
python tools/make_index.py    # index.html: hero, facts, featured and more projects, experience, skills
python tools/make_pages.py    # projects/*.html: one page per featured project
```

To add a new project: add a card to `FEATURED` or `MORE` in `tools/make_index.py` (and, for a featured one,
a page entry in `tools/make_pages.py`), crop its report screenshot to `img/<name>.jpg` (640x400), run both
scripts, check the result in a browser, then commit and push. Replaced images get a new file name, because
GitHub Pages lets browsers cache images for 10 minutes.
