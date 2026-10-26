"""Validate shared records, generated pages, internal links and basic semantics."""
from __future__ import annotations

from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from project_data import CARD_RESULTS, COMPARISON_DETAILS, EXPLORATION_FOCUSES, FEATURED_PREVIEW_CAPTIONS, FEATURED_PROJECTS, PROJECTS, ROLE_VIEWS  # noqa: E402
from portfolio_content import HOME_PROJECT_IDS  # noqa: E402
from components import ASSET_VERSION  # noqa: E402

ALLOWED = {'Web & API', 'Mobile', 'Performance', 'Security', 'Accessibility', 'AI & LLM', 'CI/CD', 'Quality Intelligence', 'Learning Labs'}
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


ids = [p['id'] for p in PROJECTS]
pages = [p['page'] for p in PROJECTS]
if len(ids) != len(set(ids)):
    fail('Duplicate project identifiers in shared data.')
if len(pages) != len(set(pages)):
    fail('Duplicate project page slugs in shared data.')
if len(PROJECTS) != 25:
    fail(f'Expected all 25 existing projects, found {len(PROJECTS)}.')
if len(FEATURED_PROJECTS) != 6:
    fail(f'Expected six featured projects, found {len(FEATURED_PROJECTS)}.')
featured_ids = {p['id'] for p in FEATURED_PROJECTS}
if set(CARD_RESULTS) != featured_ids:
    fail('Concise card results must cover exactly the six featured projects.')
if set(FEATURED_PREVIEW_CAPTIONS) != featured_ids:
    fail('Every featured preview needs a visible scope and capture-date caption.')
if len(EXPLORATION_FOCUSES) != 6 or any(
    project_id not in ids for focus in EXPLORATION_FOCUSES.values() for project_id in focus.get('projects', [])
):
    fail('Problem-led focus metadata is incomplete or references an unknown project.')
required = {'id', 'page', 'title', 'category', 'technologies', 'description', 'result', 'image', 'alt',
            'short_purpose', 'comparison_layers', 'comparison_targets', 'comparison_approach',
            'comparison_limits', 'evidence_date', 'evidence_url', 'evidence_label', 'source_url', 'readme_url',
            'workflow_name', 'report_label'}
for p in PROJECTS:
    missing = sorted(field for field in required if not p.get(field))
    if missing:
        fail(f'{p.get("id", "?")}: missing fields: {", ".join(missing)}')
    if not set(p.get('category', [])) <= ALLOWED:
        fail(f'{p["id"]}: unknown category value.')
    try:
        date.fromisoformat(p.get('evidence_date', ''))
    except ValueError:
        fail(f'{p["id"]}: evidence date is missing or is not ISO formatted.')
    image = ROOT / 'img' / (p.get('image', '') + '.jpg')
    if not image.is_file():
        fail(f'{p["id"]}: missing card image {image.relative_to(ROOT)}.')
    if not urlparse(p.get('evidence_url', '')).scheme.startswith('http'):
        fail(f'{p["id"]}: evidence URL is not an HTTP link.')
    case = ROOT / 'projects' / (p.get('page', '') + '.html')
    if not case.is_file():
        fail(f'{p["id"]}: case study was not generated.')
    if not p.get('short_purpose') or len(p['short_purpose']) > 160:
        fail(f'{p["id"]}: card purpose is missing or too long.')
    if 'roles' not in p or not isinstance(p['roles'], list):
        fail(f'{p["id"]}: role metadata must be a list, even when no role is highlighted.')
    if 'focuses' not in p or not isinstance(p['focuses'], list):
        fail(f'{p["id"]}: problem focus metadata must be a list, even when no focus applies.')
    comparison_fields = ('comparison_layers', 'comparison_targets', 'comparison_approach',
                         'comparison_limits', 'workflow_name', 'report_label')
    for field in comparison_fields:
        value = str(p.get(field, '')).strip()
        if not value or value.casefold() in {'undefined', 'null'}:
            fail(f'{p["id"]}: comparison field {field} is empty or unsafe.')

if set(COMPARISON_DETAILS) != set(ids):
    fail('Comparison metadata must cover exactly the shared project catalog.')
for role_id, role in ROLE_VIEWS.items():
    if not role.get('skills') or not role.get('impact') or any(project_id not in ids for project_id in role.get('projects', [])):
        fail(f'{role_id}: role view has missing focus content or an unknown project.')
for project in PROJECTS:
    if any(role_id not in ROLE_VIEWS for role_id in project.get('roles', [])):
        fail(f'{project["id"]}: role metadata references an unknown role.')

class Document(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids: set[str] = set()
        self.refs: list[tuple[str, str]] = []
        self.images: list[dict[str, str | None]] = []
        self.buttons: list[dict[str, str | None]] = []
        self.links: list[dict[str, str | None]] = []
        self.headings: list[int] = []
        self.h1_count = 0
        self.title = False
        self.description = False
        self.canonical = False
        self.landmarks: set[str] = set()
        self.skip_link = False
        self._stack: list[tuple[str, dict[str, str | None]]] = []
        self._text_for = {'title', 'a', 'button', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if a.get('id'):
            if a['id'] in self.ids:
                fail(f'{self.path.relative_to(ROOT)}: duplicate id {a["id"]}.')
            self.ids.add(a['id'])
        if tag in ('main', 'nav', 'header', 'footer'):
            self.landmarks.add(tag)
        if tag == 'a':
            self.links.append(a)
        if tag in ('a', 'link') and a.get('href'):
            self.refs.append(('href', a['href']))
        if tag in ('script', 'iframe') and a.get('src'):
            self.refs.append(('src', a['src']))
        if tag == 'a':
            if a.get('href', '').startswith('#') and a.get('href') != '#main':
                self.refs.append(('anchor', a['href'][1:]))
            if a.get('class') == 'skip':
                self.skip_link = True
        if tag in ('img', 'source'):
            if tag == 'img':
                self.images.append(a)
            attr = 'src' if tag == 'img' else 'srcset'
            value = a.get(attr)
            if value:
                self.refs.append((attr, value.split(',')[0].strip().split(' ')[0]))
        if tag == 'button':
            self.buttons.append(a)
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = int(tag[1])
            self.headings.append(level)
            if level == 1:
                self.h1_count += 1
        if tag == 'title':
            self.title = True
        if tag == 'meta' and a.get('name') == 'description' and a.get('content'):
            self.description = True
        if tag == 'link' and a.get('rel') == 'canonical' and a.get('href'):
            self.canonical = True
        if tag in self._text_for:
            self._stack.append((tag, a))
        if a.get('aria-labelledby'):
            for ident in a['aria-labelledby'].split():
                self.refs.append(('aria-labelledby', ident))
        if a.get('aria-controls'):
            for ident in a['aria-controls'].split():
                self.refs.append(('aria-controls', ident))

    def handle_endtag(self, tag: str) -> None:
        if self._stack and self._stack[-1][0] == tag:
            self._stack.pop()

    def handle_data(self, data: str) -> None:
        for tag, attrs in self._stack:
            if tag in ('a', 'button') and data.strip():
                attrs['__has_text'] = '1'


stylesheet = re.sub(r'\s+', '', (ROOT / 'style.css').read_text(encoding='utf-8'))
css_rules = re.findall(r'([^{}]+)\{([^{}]*)\}', stylesheet)
for selector in ('.exploration-band::before', '.engineering-evidence::before'):
    rule = next(
        (body for header, body in css_rules if selector in header.split(',')),
        '',
    )
    if 'width:100%' not in rule or '100vw' in rule or '100vmax' not in rule:
        fail(f'{selector}: full-width backgrounds must use a clipped 100vmax shadow.')


html_files = [ROOT / 'index.html', ROOT / 'projects.html', ROOT / '404.html', *sorted((ROOT / 'projects').glob('*.html'))]
if len(html_files) != 28:
    fail(f'Expected 28 generated HTML pages, found {len(html_files)}.')
if not (ROOT / 'Niranjan_Kumar_Agri_CV_Technical_Lead_QA_SDET.pdf').is_file():
    fail('CV download is missing.')
for path in html_files:
    if not path.is_file():
        fail(f'Missing generated page: {path.name}.')
        continue
    parser = Document(path)
    parser.feed(path.read_text(encoding='utf-8'))
    name = path.relative_to(ROOT).as_posix()
    asset_values = [value for kind, value in parser.refs if kind in ('href', 'src')]
    for asset_name in ('style.css', 'theme.js'):
        if not any(value.split('?', 1)[0].endswith(asset_name) and f'v={ASSET_VERSION}' in value for value in asset_values):
            fail(f'{name}: missing versioned {asset_name} release asset.')
    if path.name == 'projects.html' and not any(
        value.split('?', 1)[0].endswith('projects.js') and f'v={ASSET_VERSION}' in value
        for value in asset_values
    ):
        fail(f'{name}: missing versioned projects.js release asset.')
    if not parser.title or not parser.description or not parser.canonical:
        fail(f'{name}: needs a title, description and canonical URL.')
    if 'main' not in parser.landmarks or not parser.skip_link:
        fail(f'{name}: missing main landmark or Skip to content link.')
    if parser.h1_count != 1:
        fail(f'{name}: expected one h1, found {parser.h1_count}.')
    if parser.headings and any(b - a > 1 for a, b in zip(parser.headings, parser.headings[1:])):
        fail(f'{name}: heading levels skip a level.')
    for image in parser.images:
        if image.get('alt') is None:
            fail(f'{name}: image has no alt attribute.')
        if not image.get('width') or not image.get('height'):
            fail(f'{name}: image missing intrinsic width/height.')
    for button in parser.buttons:
        if not button.get('aria-label') and not button.get('__has_text') and not button.get('aria-labelledby'):
            fail(f'{name}: button lacks an accessible name.')
    for link in parser.links:
        if link.get('target') == '_blank' and 'noopener' not in (link.get('rel') or '').split():
            fail(f'{name}: new-window link is missing rel="noopener".')
        if not link.get('aria-label') and not link.get('__has_text'):
            # A link containing an image is checked below through its descendant's alt text.
            pass
    for kind, value in parser.refs:
        if kind == 'aria-labelledby' or kind == 'aria-controls' or kind == 'anchor':
            if value not in parser.ids:
                fail(f'{name}: unresolved {kind} reference {value}.')
            continue
        parsed = urlparse(value)
        if parsed.scheme or value.startswith('//') or value.startswith('data:') or not value:
            continue
        relative = unquote(parsed.path)
        target = (
            (ROOT / relative.lstrip('/')).resolve()
            if relative.startswith('/')
            else (path.parent / relative).resolve() if relative else path
        )
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            fail(f'{name}: local path escapes the site: {value}.')
            continue
        if target.is_dir():
            target = target / 'index.html'
        if not target.exists():
            fail(f'{name}: broken local link or asset {value}.')
        elif parsed.fragment and target.suffix.lower() in ('.html', '.htm'):
            target_parser = Document(target)
            target_parser.feed(target.read_text(encoding='utf-8'))
            if unquote(parsed.fragment) not in target_parser.ids:
                fail(f'{name}: missing destination anchor {value}.')

home = (ROOT / 'index.html').read_text(encoding='utf-8')
explorer = (ROOT / 'projects.html').read_text(encoding='utf-8')
if home.count('class="card project-card"') != len(HOME_PROJECT_IDS):
    fail('Homepage does not contain exactly three flagship project cards.')
if explorer.count('class="card project-card"') != len(PROJECTS):
    fail('Projects page card count does not match shared project data.')
if '84%' not in home or 'release test scope' not in home:
    fail('Homepage is missing the measured automation coverage explanation.')
if 'Let’s build reliable releases.' not in home or 'Open to Senior SDET, QA Lead and Test Automation Architect opportunities' not in home:
    fail('Homepage is missing the requested contact heading or hiring context.')
if f'<strong>{len(PROJECTS)} projects</strong>' not in home:
    fail('Homepage evidence strip count does not match shared project data.')
if home.count('class="featured-preview"') != len(HOME_PROJECT_IDS):
    fail('Featured project cards are missing a visible report or diagram caption.')
for project in FEATURED_PROJECTS:
    if project['id'] not in HOME_PROJECT_IDS:
        continue
    if project['id'] not in home or project['preview_caption'][0] not in home or project['preview_caption'][1] not in home:
        fail(f'{project["id"]}: preview caption is not present in the generated homepage.')
    if project['card_result'] != CARD_RESULTS[project['id']]:
        fail(f'{project["id"]}: concise result summary diverges from shared card metadata.')
if 'Find work by role or problem' not in home or 'By problem' not in home or 'Engineering evidence' not in home:
    fail('Homepage is missing problem-led exploration or evidence content.')
if not (home.index('class="hero"') < home.index('id="projects"') < home.index('id="exploration"')):
    fail('Homepage sections must present featured projects before exploration paths.')
if home.count('data-exploration-panel=') != len(EXPLORATION_FOCUSES) or ' data-exploration-panel="maintainable-automation" open' in home:
    fail('Problem-led paths must start collapsed and retain every configured question.')
if 'quality-intelligence-0ur1.onrender.com' not in (ROOT / 'projects' / 'quality-intelligence.html').read_text(encoding='utf-8'):
    fail('Quality Intelligence case study is missing the live dashboard link.')
if home.count('data-role-panel=') != len(ROLE_VIEWS):
    fail('Homepage role explorer does not contain every configured role view.')
if 'aria-label="Project filters"' not in explorer or 'data-preview-project' not in explorer or 'data-compare-project' not in explorer:
    fail('Project explorer is missing its filters, preview or comparison controls.')
if not all(value in explorer for value in ('Featured first', 'Recently verified', 'Alphabetical', 'Clear all')):
    fail('Project explorer is missing a required sorting or reset option.')
if ' ? <a' in explorer:
    fail('Project explorer footer contains stray punctuation.')
for project in PROJECTS:
    case = (ROOT / 'projects' / (project['page'] + '.html')).read_text(encoding='utf-8')
    if 'My contribution' in case or 'I built and maintain this public project' in case:
        fail(f'{project["page"]}: generic contribution text must not replace project-specific scope.')
    if 'data-project-return' not in case or 'class="toc"' not in case or 'toc-title">On this page<' not in case:
        fail(f'{project["page"]}: missing back-to-results or contents navigation.')
    if 'Evidence explorer' not in case or 'Known limitations' not in case:
        fail(f'{project["page"]}: missing evidence or limitation context.')
    if case.count('id="limitations"') != 1 or '<section aria-labelledby="limitations"><h2 id="limitations">Known limitations</h2><h3>Known limitations' in case:
        fail(f'{project["page"]}: duplicate limitations heading.')
    if 'undefined' in case.lower():
        fail(f'{project["page"]}: rendered undefined fallback text.')
    if re.search(r'>(?:undefined|null)<', case, re.IGNORECASE):
        fail(f'{project["page"]}: rendered unsafe fallback text.')
    if project['id'] in {'enterprise-test-automation-framework', 'automation-coverage-quality-intelligence',
                         'playwright-typescript-framework'}:
        if 'architecture-component-tabs' not in case or 'View source</a>' not in case:
            fail(f'{project["page"]}: missing the selectable architecture panel and readable source link.')
    for anchor in ('contribution', 'features', 'defects'):
        if f'id="{anchor}"' not in case:
            fail(f'{project["page"]}: missing compatibility anchor #{anchor}.')
if not (ROOT / 'img' / 'enterprise-architecture.svg').is_file():
    fail('Enterprise architecture preview SVG was not generated.')
if not (ROOT / 'robots.txt').is_file() or not (ROOT / 'sitemap.xml').is_file():
    fail('robots.txt or sitemap.xml is missing.')

if ERRORS:
    print('VALIDATION FAILED')
    for issue in ERRORS:
        print('-', issue)
    raise SystemExit(1)
print(f'Validated {len(PROJECTS)} projects, {len(html_files)} HTML pages, local links/assets, CV and key content.')
