"""Generate the no-JavaScript project collection from shared records."""
from __future__ import annotations

import html
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(__file__))
from project_data import PROJECTS  # noqa: E402

e = html.escape
HOME = 'https://niranjankagri.github.io/'
GITHUB = 'https://github.com/niranjankagri/'
EMAIL = 'niranjankagri@gmail.com'
CATEGORIES = ['Web & API', 'Mobile', 'Performance', 'Security', 'Accessibility', 'AI & LLM',
              'CI/CD', 'Quality Intelligence', 'Learning Labs']
TECHNOLOGIES = ['Java', 'Python', 'TypeScript']


def card(p: dict) -> str:
    cats = '|'.join(x.lower() for x in p['category'])
    tech_keys = ' '.join(t.lower() for t in TECHNOLOGIES if any(t.lower() in x.lower() for x in p['technologies']))
    searchable = ' '.join([p['title'], p['description'], *p['technologies']]).lower()
    tags = ''.join(f'<li class="tag">{e(t)}</li>' for t in p['technologies'])
    workflow_status = ''
    if p['workflow_url']:
        badge_url = p['workflow_url'] + '/badge.svg'
        workflow_status = f'''<div class="workflow-row"><span class="badge">Workflow configured</span>
        <a class="badge-link" href="{e(p['workflow_url'], quote=True)}" target="_blank" rel="noopener" aria-label="Open workflow history for {e(p['title'])}">
        <img class="ci" src="{e(badge_url, quote=True)}" alt="GitHub Actions workflow status badge; workflow history remains available if the image does not load" width="150" height="20" loading="lazy"><span class="badge-fallback" hidden>Workflow badge unavailable · open history</span></a></div>'''
    else:
        workflow_status = '<span class="badge">No automated workflow</span>'
    live = f'<a href="{e(p["live_demo"], quote=True)}" target="_blank" rel="noopener">Live demo</a>' if p['live_demo'] else ''
    return f'''<article class="card project-card" data-project-id="{e(p['id'], quote=True)}" data-category="{e(cats, quote=True)}" data-tech="{e(tech_keys, quote=True)}" data-search="{e(searchable, quote=True)}">
      <img src="img/{e(p['image'], quote=True)}.jpg" alt="{e(p['alt'], quote=True)}" width="640" height="400" loading="lazy">
      <div class="body"><span class="kind">{e(p['project_kind'])} · {e(', '.join(p['category']))}</span>
        <h2><a href="projects/{e(p['page'], quote=True)}.html">{e(p['title'])}</a></h2>
        <p>{e(p['description'])}</p><p class="fact">{e(p['result'])}</p>
        <ul class="tags" aria-label="Technologies">{tags}</ul>{workflow_status}
        <p class="evidence">{e(p['result_kind'])} · evidence {e(p['evidence_date'])} · <a href="{e(p['evidence_url'], quote=True)}" target="_blank" rel="noopener">{e(p['evidence_label'])}</a></p>
        <div class="actions"><a href="projects/{e(p['page'], quote=True)}.html">View case study</a><a href="{e(p['source_url'], quote=True)}" target="_blank" rel="noopener">Source code</a>{live}</div>
      </div></article>'''


cats = ''.join(f'<label class="check"><input type="checkbox" name="category" value="{e(c, quote=True)}"><span>{e(c)}</span></label>' for c in CATEGORIES)
techs = ''.join(f'<label class="check"><input type="checkbox" name="tech" value="{e(t, quote=True)}"><span>{e(t)}</span></label>' for t in TECHNOLOGIES)
cards = ''.join(card(p) for p in PROJECTS)
html_doc = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Projects · Niranjan Kumar Agri</title>
<meta name="description" content="Explore all {len(PROJECTS)} portfolio projects across web and API automation, mobile, performance, security, accessibility, AI and CI/CD. Search technologies and review dated evidence.">
<link rel="canonical" href="{HOME}projects.html">
<meta property="og:title" content="Projects · Niranjan Kumar Agri"><meta property="og:description" content="Search {len(PROJECTS)} automation and quality engineering projects, each with case study and evidence links."><meta property="og:type" content="website"><meta property="og:url" content="{HOME}projects.html"><meta property="og:image" content="{HOME}img/profile-2026-10b.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="style.css">
<script>try{{var t=localStorage.getItem('na-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head><body><a class="skip" href="#main">Skip to content</a>
<header class="nav"><div class="wrap"><a class="home" href="./"><picture><source srcset="img/avatar-2026-10c.webp" type="image/webp"><img class="avatar" src="img/avatar-2026-10c.jpg" alt="" width="40" height="40"></picture>Niranjan Kumar Agri</a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav"><span class="menu-icon" aria-hidden="true">☰</span><span class="sr-only">Open navigation</span></button>
  <nav id="primary-nav" aria-label="Primary navigation"><a href="projects.html" aria-current="page">Projects <span class="nav-count">{len(PROJECTS)}</span></a><a href="index.html#experience">Experience</a><a href="index.html#skills">Skills</a><a href="index.html#contact">Contact</a><a href="Niranjan_Kumar_Agri_CV_Technical_Lead_QA_SDET.pdf" download>Download CV</a></nav>
  <button class="theme" id="theme" type="button" aria-label="Use dark theme" title="Change color theme">◐</button></div></header>
<main id="main" class="wrap projects-page"><p class="crumbs"><a href="./">Home</a> / Projects</p>
  <header class="projects-intro"><p class="eyebrow">Project collection</p><h1>Projects</h1><p class="lead">Search the full collection of {len(PROJECTS)} automation and quality engineering projects. Each project has source code, context and the available evidence; older frameworks and learning labs are labelled.</p></header>
  <div class="project-layout"><aside class="filters" aria-label="Project filters"><form id="project-filters" role="search">
    <div class="search-row"><label for="project-search">Search projects</label><input id="project-search" name="q" type="search" autocomplete="off" placeholder="Title, purpose, technology"></div>
    <fieldset><legend>Category</legend><div class="check-list">{cats}</div></fieldset>
    <fieldset><legend>Technology</legend><div class="check-list">{techs}</div></fieldset>
    <button class="btn" id="clear-filters" type="button">Clear filters</button>
  </form></aside>
  <section class="results" aria-labelledby="results-title"><div class="results-heading"><h2 id="results-title">All projects</h2><p id="result-count" role="status" aria-live="polite" aria-atomic="true">Showing {len(PROJECTS)} of {len(PROJECTS)} projects</p></div>
    <ul id="active-filters" class="active-filters" aria-label="Active filters"></ul>
    <div id="project-grid" class="grid project-grid">{cards}</div>
    <p id="empty-results" class="empty-results" hidden>No projects match these search terms and filters. Clear filters or try a broader search.</p>
  </section></div>
</main>
<footer>© 2026 Niranjan Kumar Agri · <a href="./">Portfolio home</a> · <a href="{GITHUB}niranjankagri.github.io">Website source</a></footer>
<script src="theme.js" defer></script><script src="projects.js" defer></script></body></html>
'''

with open(os.path.join(ROOT, 'projects.html'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(html_doc)
print(f'projects page written with {len(PROJECTS)} projects')
