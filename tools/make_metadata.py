"""Generate static hosting metadata and the not-found page."""
from datetime import date
import html
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(__file__))
from components import footer, header, stylesheet, script_asset  # noqa: E402
from project_data import PROJECTS  # noqa: E402

HOME = 'https://niranjankagri.github.io/'
e = html.escape

with open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('User-agent: *\nAllow: /\nSitemap: ' + HOME + 'sitemap.xml\n')

urls = [HOME, HOME + 'projects.html'] + [HOME + 'projects/' + p['page'] + '.html' for p in PROJECTS]
url_items = ''.join(f'<url><loc>{e(url)}</loc><lastmod>{date.today().isoformat()}</lastmod></url>' for url in urls)
with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + url_items + '</urlset>\n')

not_found = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found · Niranjan Kumar Agri</title><meta name="description" content="The requested page could not be found. Browse the portfolio projects or return to the home page.">
<link rel="canonical" href="https://niranjankagri.github.io/404.html">{stylesheet()}
<script>try{{var t=localStorage.getItem('na-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script></head>
<body>
{header('', 'other')}
<main id="main" class="wrap"><section class="not-found"><p class="eyebrow">404 · Page not found</p><h1>This page isn’t here.</h1><p class="lead">The link may have changed. You can return home or browse the project collection.</p><div class="btns"><a class="btn primary" href="projects.html">Browse all projects</a><a class="btn" href="./">Portfolio home</a></div></section></main>
{footer('')}{script_asset('theme.js')}</body></html>'''
with open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(not_found)
print(f'hosting metadata written ({len(urls)} sitemap locations)')
