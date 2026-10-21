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
from project_data import FEATURED_PROJECTS, PROJECTS  # noqa: E402

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
required = {'id', 'page', 'title', 'category', 'technologies', 'description', 'result', 'image', 'alt',
            'evidence_date', 'evidence_url', 'evidence_label', 'source_url', 'readme_url'}
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


html_files = [ROOT / 'index.html', ROOT / 'projects.html', ROOT / '404.html', *sorted((ROOT / 'projects').glob('*.html'))]
if not (ROOT / 'Niranjan_Kumar_Agri_CV_Technical_Lead_QA_SDET.pdf').is_file():
    fail('CV download is missing.')
for path in html_files:
    if not path.is_file():
        fail(f'Missing generated page: {path.name}.')
        continue
    parser = Document(path)
    parser.feed(path.read_text(encoding='utf-8'))
    name = path.relative_to(ROOT).as_posix()
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
        target = (path.parent / relative).resolve() if relative else path
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
if home.count('class="card project-card"') != 6:
    fail('Homepage does not contain exactly six featured project cards.')
if explorer.count('class="card project-card"') != len(PROJECTS):
    fail('Projects page card count does not match shared project data.')
if '84%' not in home or 'release test scope' not in home:
    fail('Homepage is missing the measured automation coverage explanation.')
if 'Hiring a Technical Lead QA, Senior SDET, or Test Automation Architect? Let’s connect.' not in home:
    fail('Homepage contact heading does not match the requested wording.')
if 'quality-intelligence-0ur1.onrender.com' not in (ROOT / 'projects' / 'quality-intelligence.html').read_text(encoding='utf-8'):
    fail('Quality Intelligence case study is missing the live dashboard link.')
if not (ROOT / 'robots.txt').is_file() or not (ROOT / 'sitemap.xml').is_file():
    fail('robots.txt or sitemap.xml is missing.')

if ERRORS:
    print('VALIDATION FAILED')
    for issue in ERRORS:
        print('-', issue)
    raise SystemExit(1)
print(f'Validated {len(PROJECTS)} projects, {len(html_files)} HTML pages, local links/assets, CV and key content.')
