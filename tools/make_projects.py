"""Generate the project collection (searchable with JavaScript, a full list without) from shared records."""
from __future__ import annotations

import html
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(__file__))
from components import CV, HOME, footer, header, project_card  # noqa: E402
from project_data import PROJECTS  # noqa: E402

e = html.escape
CATEGORIES = ['Web & API', 'Mobile', 'Performance', 'Security', 'Accessibility', 'AI & LLM',
              'CI/CD', 'Quality Intelligence', 'Learning Labs']
TECHNOLOGIES = ['Java', 'Python', 'TypeScript']


def filters_of(p: dict) -> dict[str, str]:
    """The data-* values projects.js matches against: categories, languages and free text."""
    return {
        'category': '|'.join(x.lower() for x in p['category']),
        'tech': ' '.join(t.lower() for t in TECHNOLOGIES if any(t.lower() in x.lower() for x in p['technologies'])),
        'search': ' '.join([p['title'], p['description'], *p['technologies']]).lower(),
    }


def chips(name: str, values: list[str]) -> str:
    # A real checkbox inside each chip: keyboard, screen readers and the URL state keep working
    return ''.join(f'<label class="check"><input type="checkbox" name="{name}" value="{e(v, quote=True)}"><span>{e(v)}</span></label>'
                   for v in values)


cards = ''.join(project_card(p, heading='h2', filters=filters_of(p)) for p in PROJECTS)
html_doc = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Projects · Niranjan Kumar Agri</title>
<meta name="description" content="Explore all {len(PROJECTS)} portfolio projects across web and API automation, mobile, performance, security, accessibility, AI and CI/CD. Search technologies and review dated evidence.">
<link rel="canonical" href="{HOME}projects.html">
<meta property="og:title" content="Projects · Niranjan Kumar Agri"><meta property="og:description" content="Search {len(PROJECTS)} automation and quality engineering projects, each with case study and evidence links."><meta property="og:type" content="website"><meta property="og:url" content="{HOME}projects.html"><meta property="og:image" content="{HOME}img/profile-2026-10b.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="style.css">
<script>try{{var t=localStorage.getItem('na-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head><body>
{header('', 'projects', len(PROJECTS))}
<main id="main" class="wrap projects-page">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="./">Home</a> / <span aria-current="page">Projects</span></nav>
  <header class="projects-intro"><p class="eyebrow">Project collection</p><h1>Projects</h1><p class="lead">Search the full collection of {len(PROJECTS)} automation and quality engineering projects. Each project has source code, context and the available evidence; older frameworks and learning labs are labelled.</p></header>
  <form id="project-filters" class="filters" role="search" aria-label="Project filters">
    <div class="search-row"><label for="project-search" class="sr-only">Search projects</label><input id="project-search" name="q" type="search" autocomplete="off" placeholder="Search title, purpose or tool"><button class="btn" id="clear-filters" type="button">Clear filters</button></div>
    <fieldset><legend>Category</legend><div class="check-list">{chips('category', CATEGORIES)}</div></fieldset>
    <fieldset><legend>Language</legend><div class="check-list">{chips('tech', TECHNOLOGIES)}</div></fieldset>
  </form>
  <section class="results" aria-labelledby="results-title"><div class="results-heading"><h2 id="results-title" class="sr-only">All projects</h2><p id="result-count" role="status" aria-live="polite" aria-atomic="true">Showing {len(PROJECTS)} of {len(PROJECTS)} projects</p><ul id="active-filters" class="active-filters" aria-label="Active filters"></ul></div>
    <div id="project-grid" class="grid project-grid">{cards}</div>
    <p id="empty-results" class="empty-results" hidden>No projects match these search terms and filters. Clear filters or try a broader search.</p>
  </section>
</main>
{footer('', f' · <a href="{CV}" download>Download CV</a>')}
<script src="theme.js" defer></script><script src="projects.js" defer></script></body></html>
'''

with open(os.path.join(ROOT, 'projects.html'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(html_doc)
print(f'projects page written with {len(PROJECTS)} projects')
