"""Shared page components: header, footer and the project card used on every generated page.

Each generator passes ``prefix`` ('' at the site root, '../' for pages in projects/) so the same
markup works from any folder.
"""
from __future__ import annotations

import hashlib
from datetime import date
import html
from pathlib import Path

e = html.escape
CV = 'Niranjan_Kumar_Agri_CV_Technical_Lead_QA_SDET.pdf'
HOME = 'https://niranjankagri.github.io/'
GITHUB = 'https://github.com/niranjankagri/'
LINKEDIN = 'https://www.linkedin.com/in/niranjan-kumar-agri/'
EMAIL = 'niranjankagri@gmail.com'
ROOT = Path(__file__).resolve().parent.parent
ASSET_VERSION = hashlib.sha256(b''.join((ROOT / name).read_bytes() for name in ('style.css', 'theme.js', 'projects.js'))).hexdigest()[:12]


def stylesheet(prefix: str = '') -> str:
    return f'<link rel="stylesheet" href="{prefix}style.css?v={ASSET_VERSION}">'


def script_asset(name: str, prefix: str = '') -> str:
    return f'<script src="{prefix}{e(name, quote=True)}?v={ASSET_VERSION}" defer></script>'

ICONS = {
    'download': 'M11 3h2v9.6l3.3-3.3 1.4 1.4L12 16.4l-5.7-5.7 1.4-1.4 3.3 3.3zM4 18h16v2H4z',
    'mail': 'M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm9 7.2L4 7.3V17h16V7.3z',
    'github': 'M12 .5a11.5 11.5 0 0 0-3.64 22.4c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.53-1.33-1.28-1.69-1.28-1.69-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.81 1.19 1.84 1.19 3.1 0 4.42-2.7 5.4-5.26 5.68.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5z',
    'linkedin': 'M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.6 8.65 21 11.3 21 14.7V21h-4v-5.6c0-1.33-.03-3.05-1.86-3.05-1.86 0-2.14 1.45-2.14 2.95V21H9z',
    'arrow': 'M13.2 5.3l1.4-1.4L22.7 12l-8.1 8.1-1.4-1.4 5.7-5.7H2v-2h16.9z',
}


def icon(name: str) -> str:
    return f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{ICONS[name]}"/></svg>'


def external(url: str, label: str, css: str = '') -> str:
    cls = f' class="{css}"' if css else ''
    return f'<a{cls} href="{e(url, quote=True)}" target="_blank" rel="noopener">{e(label)}</a>'


def readable_date(iso: str) -> str:
    """'2026-10-21' -> '21 Oct 2026' (the evidence dates are ISO in the shared data)."""
    d = date.fromisoformat(iso)
    return f'{d.day} {d:%b %Y}'


def header(prefix: str, current: str, project_count: int | None = None) -> str:
    """Sticky top bar. ``current`` is 'home', 'projects' or 'case' (a case study counts as Projects)."""
    on_home = current == 'home'
    home_href = './' if prefix == '' else prefix
    section = '#' if on_home else f'{prefix}index.html#'
    count = f' <span class="nav-count">{project_count}</span>' if project_count else ''
    projects_current = ' aria-current="page"' if current in ('projects', 'case') else ''
    home_current = ' aria-current="page"' if on_home else ''
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="nav"><div class="wrap">
  <a class="home" href="{home_href}"{home_current}><span class="brand-mark" aria-hidden="true">NA</span><span>Niranjan Kumar Agri</span></a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav"><span class="menu-icon" aria-hidden="true">☰</span><span class="sr-only">Open navigation</span></button>
  <nav id="primary-nav" aria-label="Primary navigation">
    <a href="{prefix}projects.html"{projects_current}>Projects{count}</a><a href="{section}experience">Experience</a><a href="{section}skills">Skills</a><a href="{section}contact">Contact</a><a class="nav-cv" href="{prefix}{CV}" download>{icon('download')}CV</a>
  </nav>
  <button class="theme" id="theme" type="button" aria-label="Use dark theme" title="Change color theme">◐</button>
</div></header>'''


def footer(prefix: str) -> str:
    home_href = './' if prefix == '' else prefix
    return f'''<footer><div class="wrap footer-layout">
  <div class="footer-brand"><a class="footer-name" href="{home_href}">Niranjan Kumar Agri</a><p>© 2026 · Quality engineering and automation</p></div>
  <nav aria-label="Explore"><h2>Explore</h2><a href="{home_href}#projects">Featured projects</a><a href="{prefix}projects.html">All projects</a><a href="{home_href}#experience">Experience</a></nav>
  <nav aria-label="Evidence"><h2>Evidence</h2><a href="{prefix}projects/playwright-typescript.html#results">Cross-browser execution</a><a href="{prefix}projects/k6-performance.html#results">Performance testing</a><a href="{prefix}projects/quality-intelligence.html#results">Quality intelligence</a></nav>
  <nav aria-label="Connect"><h2>Connect</h2><a href="mailto:{EMAIL}">Email</a><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a><a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a><a href="{prefix}{CV}" download>Download CV</a><a href="{GITHUB}niranjankagri.github.io" target="_blank" rel="noopener">Website source</a></nav>
</div></footer>'''


def ci_status(p: dict) -> str:
    """The live GitHub Actions badge, or a plain note when the project has no workflow."""
    if not p['workflow_url']:
        return '<span class="no-ci">No CI workflow</span>'
    badge = p['workflow_url'] + '/badge.svg'
    return (f'<a class="badge-link" href="{e(p["workflow_url"], quote=True)}" target="_blank" rel="noopener" '
            f'aria-label="Open the {e(p["workflow_name"])} workflow history of {e(p["title"])}">'
            f'<img class="ci" src="{e(badge, quote=True)}" alt="GitHub Actions workflow badge" '
            f'width="150" height="20" loading="lazy"><span class="badge-fallback" hidden>Workflow history</span></a>')


def project_card(p: dict, prefix: str = '', heading: str = 'h3', filters: dict[str, str] | None = None) -> str:
    # One canonical project card, with optional explorer controls and filter metadata.
    page = f'{prefix}projects/{e(p["page"], quote=True)}.html'
    fields = dict(filters or {})
    fields.update({
        'featured': str(p['featured']).lower(),
        'date': p['evidence_date'],
        'roles': ' '.join(p['roles']),
        'purpose': p['short_purpose'],
        'result': p['result'],
        'result-kind': p['result_kind'],
        'languages': ', '.join(language for language, aliases in (('Java', ('Java', 'Java 17', 'Java 21')), ('Python', ('Python',)), ('TypeScript', ('TypeScript',)), ('JavaScript', ('JavaScript',))) if any(tag in aliases for tag in p['technologies'])) or 'See technology tags',
        'layers': p['comparison_layers'],
        'targets': p['comparison_targets'],
        'approach': p['comparison_approach'],
        'report': p['report_label'],
        'limitations': '',
        'comparison-limits': p['comparison_limits'],
        'case': page,
        'report-url': p['report_url'],
        'architecture-image': p['architecture_preview'],
        'architecture-alt': p['architecture_preview_alt'],
        'image': f'{prefix}img/{p["image"]}.jpg',
        'alt': p['alt'],
        'source': p['source_url'],
        'live': p['live_demo'],
        'evidence-url': p['evidence_url'],
        'evidence-label': p['evidence_label'],
        'workflow': p['workflow_url'],
        'workflow-name': p['workflow_name'],
        'focus': ' '.join(p['focuses']),
    })
    data = ''.join(f' data-{key}="{e(value, quote=True)}"' for key, value in fields.items())
    tags = ''.join(f'<li><a class="tag tag-link" href="projects.html?skill={e(tag, quote=True)}">{e(tag)}</a></li>' for tag in p['technologies'])
    live = external(p['live_demo'], 'Live demo', 'live-action') if p['live_demo'] else ''
    explorer_actions = ('<button class="text-action preview-action" type="button" data-preview-project data-js-only aria-haspopup="dialog">Preview</button>'
                        '<button class="text-action compare-action" type="button" data-compare-project data-js-only aria-pressed="false">Compare</button>') if filters else ''
    if p.get('preview_caption'):
        dialog_id = 'featured-image-' + hashlib.sha1(p['id'].encode('utf-8')).hexdigest()[:12]
        preview_type, preview_scope = p['preview_caption']
        image_path = f'{prefix}img/{e(p["image"], quote=True)}.jpg'
        preview = (f'<figure class="featured-preview"><button type="button" data-image-dialog="{dialog_id}" aria-haspopup="dialog" '
                   f'aria-label="Enlarge {e(preview_type.lower(), quote=True)}: {e(p["alt"], quote=True)}">'
                   f'<img src="{image_path}" alt="{e(p["alt"], quote=True)}" width="640" height="400" loading="lazy">'
                   '<span class="sr-only">Enlarge preview</span></button>'
                   f'<figcaption><span class="preview-type">{e(preview_type)}.</span> {e(preview_scope)}</figcaption></figure>'
                   f'<dialog class="image-viewer" id="{dialog_id}" aria-labelledby="{dialog_id}-caption">'
                   '<form method="dialog"><button type="button" data-dialog-close aria-label="Close image viewer">Close</button></form>'
                   f'<img src="{image_path}" alt="{e(p["alt"], quote=True)}" width="640" height="400">'
                   f'<p class="viewer-caption" id="{dialog_id}-caption"><b>{e(preview_type)}.</b> {e(preview_scope)}</p></dialog>')
    else:
        preview = (f'<a class="card-image" href="{page}" tabindex="-1"><img src="{prefix}img/{e(p["image"], quote=True)}.jpg" '
                   f'alt="{e(p["alt"], quote=True)}" width="640" height="400" loading="lazy"></a>')
    return f'''<article class="card project-card" data-project-id="{e(p['id'], quote=True)}"{data}>
      {preview}
      <div class="body">
        <p class="kind">{e(p['project_kind'])} | {e(', '.join(p['category']))}</p>
        <{heading} class="card-title"><a href="{page}">{e(p['title'])}</a></{heading}>
        <p class="desc">{e(p['short_purpose'])}</p>
        <div class="card-result"><p class="fact">{e(p.get('card_result', p['result']))}</p><p class="evidence-kind">{e(p['result_kind'])}</p></div>
        <ul class="tags" aria-label="Technologies">{tags}</ul>
        <div class="card-foot">
          <div class="actions"><a class="go" href="{page}">Case study {icon('arrow')}</a>{external(p['source_url'], 'Source', 'source-action')}{live}{explorer_actions}</div>
          <div class="card-meta"><div class="workflow-meta">{ci_status(p)}</div><p class="evidence" title="{e(p['evidence_label'], quote=True)}">Evidence checked {readable_date(p['evidence_date'])} | {external(p['evidence_url'], p['evidence_label'])}</p></div>
        </div>
      </div>
    </article>'''
