"""Generate the accessible static project explorer from shared project records."""
from __future__ import annotations

import html
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(__file__))
from components import HOME, footer, header, project_card, stylesheet, script_asset  # noqa: E402
from project_data import EXPLORATION_FOCUSES, PROJECTS  # noqa: E402


e = html.escape
CATEGORIES = ['Web & API', 'Mobile', 'Performance', 'Security', 'Accessibility', 'AI & LLM',
              'CI/CD', 'Quality Intelligence', 'Learning Labs']
LANGUAGES = ['Java', 'Python', 'TypeScript']


def matches_language(project: dict, language: str) -> bool:
    aliases = {
        'Java': {'java', 'java 17', 'java 21'},
        'Python': {'python'},
        'TypeScript': {'typescript'},
    }
    return any(value.casefold() in aliases[language] for value in project['technologies'])


def filters_of(project: dict) -> dict[str, str]:
    """Prepare the URL-backed search values for one project card."""
    search_values = [project['title'], project.get('text', ''), project['description'], project['result'],
                     project['result_kind'], project['evidence_label'], *project['technologies']]
    return {
        'category': '|'.join(value.casefold() for value in project['category']),
        'tech': ' '.join(value.casefold() for value in LANGUAGES if matches_language(project, value)),
        'focus': ' '.join(project['focuses']),
        'search': ' '.join(search_values).casefold(),
    }


def chips(name: str, values: list[str], counts: dict[str, int]) -> str:
    """Render labeled native checkboxes with category counts from the full catalog."""
    return ''.join(
        f'<label class="check"><input type="checkbox" name="{name}" value="{e(value, quote=True)}">'
        f'<span>{e(value)}</span><span class="check-count" aria-label="{counts[value]} {"project" if counts[value] == 1 else "projects"}">{counts[value]}</span></label>'
        for value in values
    )


category_counts = {category: sum(category in project['category'] for project in PROJECTS) for category in CATEGORIES}
language_counts = {language: sum(matches_language(project, language) for project in PROJECTS) for language in LANGUAGES}
cards = ''.join(project_card(project, heading='h2', filters=filters_of(project)) for project in PROJECTS)

html_doc = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Projects | Niranjan Kumar Agri</title>
<meta name="description" content="Explore all {len(PROJECTS)} automation and quality engineering projects by purpose, evidence, language and category.">
<link rel="canonical" href="{HOME}projects.html">
<meta property="og:title" content="Projects | Niranjan Kumar Agri"><meta property="og:description" content="Search {len(PROJECTS)} automation and quality engineering projects, each with a case study and dated evidence."><meta property="og:type" content="website"><meta property="og:url" content="{HOME}projects.html"><meta property="og:image" content="{HOME}img/profile-2026-10b.jpg"><meta name="twitter:card" content="summary_large_image">
{stylesheet()}
<script>try{{var t=localStorage.getItem('na-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head><body>
{header('', 'projects', len(PROJECTS))}
<main id="main" class="wrap projects-page">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="./">Home</a> / <span aria-current="page">Projects</span></nav>
  <header class="projects-intro"><p class="eyebrow">Project collection</p><h1>Explore the work</h1><p class="lead">All {len(PROJECTS)} projects remain listed here. Search purpose and tools, combine categories and languages, then open a preview or compare up to three projects.</p></header>
  <form id="project-filters" class="filters" role="search" aria-label="Project filters">
    <details class="filter-details" id="filter-details" open><summary>Search and filters</summary><div class="filter-controls">
      <div class="search-row"><label for="project-search" class="sr-only">Search projects</label><input id="project-search" name="q" type="search" autocomplete="off" placeholder="Search title, purpose, decisions or technology"><button class="btn" id="clear-filters" type="button">Clear all</button></div>
      <p class="filter-help">Within Category and Language, selected values match any selection. Search, skill, problem focus and category/language groups all apply together; role highlights do not hide other projects. Counts use the full project list, and a project may appear in more than one category.</p>
      <fieldset><legend>Category</legend><div class="check-list">{chips('category', CATEGORIES, category_counts)}</div></fieldset>
      <fieldset><legend>Language</legend><div class="check-list">{chips('tech', LANGUAGES, language_counts)}</div></fieldset>
      <label class="role-filter" for="role-focus">Explore by role <select id="role-focus" name="role"><option value="">All roles</option><option value="senior-sdet">Senior SDET</option><option value="qa-lead">QA Lead</option><option value="automation-architect">Automation Architect</option></select></label>
      <label class="focus-filter" for="project-focus">Explore by problem <select id="project-focus" name="focus"><option value="">Any focus</option>{''.join(f'<option value="{e(focus_id, quote=True)}">{e(focus["label"])}</option>' for focus_id, focus in EXPLORATION_FOCUSES.items())}</select></label>
      <label class="skill-filter" for="skill-search">Skill or technology <input id="skill-search" name="skill" type="search" placeholder="e.g. Playwright" autocomplete="off"></label>
    </div></details>
  </form>
  <section class="results" aria-labelledby="results-title"><div class="results-heading"><div><h2 id="results-title">Project collection</h2><p id="result-count" role="status" aria-live="polite" aria-atomic="true">Showing {len(PROJECTS)} of {len(PROJECTS)} projects</p></div>
    <label class="sort-control" for="project-sort">Sort by <select id="project-sort" name="sort"><option value="featured">Featured first</option><option value="recent">Recently verified</option><option value="alpha">Alphabetical</option></select></label>
    <ul id="active-filters" class="active-filters" aria-label="Active filters"></ul></div>
    <div id="role-context" class="role-context" hidden></div>
    <div id="project-grid" class="grid project-grid">{cards}</div>
    <p id="empty-results" class="empty-results" hidden>No projects match this combination. Remove one filter, broaden the search, or use Clear all.</p>
  </section>
  <section class="no-script-help"><h2>Browse without scripts</h2><p>Search, sorting, previews and comparison need JavaScript. The complete collection of {len(PROJECTS)} project links and their evidence remain available above.</p></section>
</main>
<div class="compare-tray" id="compare-tray" hidden><p><strong id="compare-count">0 projects selected</strong><span id="compare-announcement" class="sr-only" role="status" aria-live="polite"></span></p><div><button class="btn primary" type="button" id="open-comparison">Compare selected</button><button class="btn" type="button" id="clear-comparison">Clear</button></div></div>
<dialog class="project-drawer" id="project-preview" aria-labelledby="preview-title"><div class="drawer-head"><p class="eyebrow">Project preview</p><button class="btn" type="button" data-dialog-close aria-label="Close project preview">Close</button></div><h2 id="preview-title">Project preview</h2><div id="preview-content"></div></dialog>
<dialog class="comparison-dialog" id="comparison-dialog" aria-labelledby="comparison-title"><div class="drawer-head"><div><p class="eyebrow">Side-by-side review</p><h2 id="comparison-title">Project comparison</h2></div><button class="btn" type="button" data-dialog-close aria-label="Close project comparison">Close</button></div><p class="sub">Descriptions below come from shared project records and linked case studies. No project score is calculated.</p><div class="comparison-content" id="comparison-content"></div></dialog>
{footer('')}
{script_asset('theme.js')}{script_asset('projects.js')}</body></html>
"""

with open(os.path.join(ROOT, 'projects.html'), 'w', encoding='utf-8', newline='\n') as stream:
    stream.write(html_doc)
print(f'projects page written with {len(PROJECTS)} projects')
