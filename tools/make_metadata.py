"""Generate static hosting metadata and the not-found page."""
from datetime import date
import html
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(__file__))
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

not_found = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found · Niranjan Kumar Agri</title><meta name="description" content="The requested page could not be found. Browse the portfolio projects or return to the home page.">
<link rel="canonical" href="https://niranjankagri.github.io/404.html"><link rel="stylesheet" href="style.css">
<script>try{var t=localStorage.getItem('na-theme');if(t)document.documentElement.dataset.theme=t}catch(e){}</script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="nav"><div class="wrap">
<a class="home" href="./"><picture><source srcset="img/avatar-2026-10c.webp" type="image/webp"><img class="avatar" src="img/avatar-2026-10c.jpg" alt="" width="40" height="40"></picture>Niranjan Kumar Agri</a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav"><span aria-hidden="true">☰</span><span class="sr-only">Open navigation</span></button>
<nav id="primary-nav" aria-label="Primary navigation"><a href="projects.html">Projects</a><a href="index.html#experience">Experience</a><a href="index.html#skills">Skills</a><a href="index.html#contact">Contact</a><a href="Niranjan_Kumar_Agri_CV_Technical_Lead_QA_SDET.pdf" download>Download CV</a></nav><button class="theme" id="theme" type="button" aria-label="Use dark theme">◐</button></div></header>
<main id="main" class="wrap"><section class="hero"><p class="eyebrow">404 · Page not found</p><h1>This page isn’t here.</h1><p class="lead">The link may have changed. You can return home or browse the project collection.</p><div class="btns"><a class="btn primary" href="projects.html">Browse all projects</a><a class="btn" href="./">Portfolio home</a></div></section></main>
<footer>© 2026 Niranjan Kumar Agri · <a href="projects.html">Projects</a></footer><script src="theme.js" defer></script></body></html>'''
with open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(not_found)
print(f'hosting metadata written ({len(urls)} sitemap locations)')
