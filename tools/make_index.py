"""Generate the portfolio home page from the shared project catalogue."""
from __future__ import annotations

import html
import os
import sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(__file__))
from components import PORTFOLIO_VERSION, CV, EMAIL, GITHUB, HOME, LINKEDIN, footer, header, icon, project_card, readable_date, stylesheet, script_asset  # noqa: E402
from portfolio_content import HOME_PROJECT_IDS, FLAGSHIP_STORIES  # noqa: E402
from project_data import EXPLORATION_FOCUSES, FEATURED_PROJECTS, PROJECTS, PROJECT_BY_ID, ROLE_VIEWS  # noqa: E402


def skill_link(term: str, label: str) -> str:
    """Link a skill to its matching projects and show the full-catalog match count."""
    query = term.casefold()
    count = sum(query in ' '.join([p['title'], p.get('text', ''), p['description'], p['result'], p['result_kind'], p['evidence_label'], *p['technologies']]).casefold()
                for p in PROJECTS)
    noun = 'project' if count == 1 else 'projects'
    return f'<a href="projects.html?skill={quote(term, safe="")}">{html.escape(label)} <span class="skill-count">{count} {noun}</span></a>'


def role_explorer() -> str:
    """Render all role views as native disclosures, retaining a no-script path."""
    panels = []
    for role_id, role in ROLE_VIEWS.items():
        skills = ''.join(f'<li><a class="tag tag-link" href="projects.html?skill={quote(skill, safe="")}">{html.escape(skill)}</a></li>'
                         for skill in role['skills'])
        projects = ''.join(f'<li><a href="projects/{html.escape(PROJECT_BY_ID[project_id]["page"])}.html">{html.escape(PROJECT_BY_ID[project_id]["title"])}</a></li>'
                           for project_id in role['projects'])
        panels.append(f'<details class="role-panel" data-role-panel="{role_id}"><summary><span class="role-title">{html.escape(role["label"])}</span><span class="role-prompt">Show matching skills and projects</span></summary>'
                      f'<div class="role-panel-body"><p>{html.escape(role["summary"])}</p><h3>Relevant skills</h3><ul class="tags role-skills">{skills}</ul>'
                      f'<h3>Related project work</h3><ul class="role-projects">{projects}</ul><p class="role-impact">{html.escape(role["impact"])}</p>'
                      f'<a class="btn" href="projects.html?role={role_id}">View these projects in the explorer</a></div></details>')
    return ('<section class="role-explorer" id="role-explorer" aria-labelledby="role-explorer-title">'
            '<div class="section-heading"><div><p class="eyebrow">By role</p><h3 id="role-explorer-title">Choose a role</h3>'
            '<p class="sub">Each path connects relevant skills, experience and project evidence.</p></div>'
            '<div class="role-actions"><a class="text-action" href="#role-explorer" data-role-reset>Reset role focus</a></div></div>'
            '<p id="role-selection-status" class="role-selection-status" role="status" aria-live="polite">Choose a role to see a focused set of skills and project links.</p>'
            '<div class="role-options">' + ''.join(panels) + '</div></section>')


def problem_explorer() -> str:
    """Render project and experience paths as native, URL-shareable disclosures."""
    panels = []
    for focus_id, focus in EXPLORATION_FOCUSES.items():
        projects = ''.join(
            f'<li><a href="projects/{html.escape(PROJECT_BY_ID[project_id]["page"])}.html">'
            f'{html.escape(PROJECT_BY_ID[project_id]["title"])}</a></li>'
            for project_id in focus['projects']
        )
        panels.append(
            f'<details class="focus-panel" data-exploration-panel="{html.escape(focus_id)}">'
            f'<summary><span class="focus-title">{html.escape(focus["label"])}</span><span class="focus-prompt">Open project path</span></summary>'
            f'<div class="focus-panel-body"><p>{html.escape(focus["summary"])}</p>'
            f'<p class="focus-experience"><b>Supporting experience:</b> {html.escape(focus["experience"])}</p>'
            f'<h3>Relevant projects</h3><ul class="focus-projects">{projects}</ul>'
            f'<a class="btn" href="projects.html?focus={quote(focus_id, safe="")}">Browse matching projects</a></div></details>'
        )
    return (
        '<section class="problem-explorer" id="focus-explorer" aria-labelledby="focus-explorer-title">'
        '<div class="section-heading"><div><p class="eyebrow">By problem</p>'
        '<h3 id="focus-explorer-title">Choose a question</h3>'
        '<p class="sub">Project links open a shareable filtered collection.</p>'
        '</div><div class="role-actions"><a class="text-action" href="#focus-explorer" data-focus-reset>Reset focus</a></div></div>'
        '<p id="focus-selection-status" class="focus-selection-status" role="status" aria-live="polite">'
        'Choose a question to open a focused project path; all six remain available.</p>'
        '<div class="focus-options">' + ''.join(panels) + '</div></section>'
    )


CAPABILITIES = (
    ('Automation Engineering', 'Build reusable UI, API and mobile checks with clear seams for parallel execution and failure evidence.',
     'maintainable-automation', ['enterprise-test-automation-framework', 'playwright-typescript-framework', 'appium-framework']),
    ('Quality Strategy and Leadership', 'Connect requirements, risk, execution evidence and team decisions for a reviewable release.',
     'qa-strategy', ['automation-coverage-quality-intelligence', 'enterprise-test-automation-framework', 'robot-framework-automation']),
    ('Quality Intelligence and AI Testing', 'Inspect traceability and deterministic evaluation harnesses while keeping synthetic, replayed and live evidence distinct.',
     'ai-testing', ['automation-coverage-quality-intelligence', 'ai-assisted-test-automation', 'llm-feature-testing']),
)


def capability_showcase() -> str:
    cards = []
    for title, statement, focus_id, project_ids in CAPABILITIES:
        links = ''.join(
            f'<li><a href="projects/{html.escape(PROJECT_BY_ID[project_id]["page"])}.html">'
            f'{html.escape(PROJECT_BY_ID[project_id]["title"])}</a></li>'
            for project_id in project_ids
        )
        cards.append(
            f'<article class="capability"><h3>{html.escape(title)}</h3><p>{html.escape(statement)}</p>'
            f'<ul>{links}</ul><a class="text-action" href="projects.html?focus={quote(focus_id, safe="")}">'
            'Explore this capability</a></article>'
        )
    return (
        '<section class="capabilities" id="capabilities" aria-labelledby="capabilities-title">'
        '<div class="section-heading"><div><p class="eyebrow">How I contribute</p>'
        '<h2 id="capabilities-title">Capabilities grounded in project work</h2></div></div>'
        '<div class="capability-grid">' + ''.join(cards) + '</div></section>'
    )


APPROACH_STEPS = (
    ('Understand risk', 'Translate requirements and observed execution into explicit coverage gaps.',
     'automation-coverage-quality-intelligence', 'architecture', 'The sample requirement catalog is synthetic; collected CI evidence is identified separately.'),
    ('Design checks', 'Separate API, UI, database and integration responsibilities so each check has a clear boundary.',
     'enterprise-test-automation-framework', 'architecture', 'The Enterprise application is a demo system with an in-memory database.'),
    ('Automate', 'Compose browser and API checks with owned test data, typed contracts and cross-browser execution.',
     'playwright-typescript-framework', 'architecture', 'The suite depends on a public demo shop; two form-login checks are skipped in CI when its bot check blocks them.'),
    ('Inspect evidence', 'Compare the same documented workload before and after a targeted change.',
     'k6-performance-testing', 'story', 'The measured result applies to the demo shop and linked stress-test profile.'),
)


def engineering_approach() -> str:
    steps = []
    for index, (title, summary, project_id, anchor, limitation) in enumerate(APPROACH_STEPS, 1):
        project = PROJECT_BY_ID[project_id]
        href = f'projects/{project["page"]}.html#{anchor}'
        steps.append(
            f'<details class="approach-step"><summary><span class="step-number">{index:02}</span>'
            f'<span><b>{html.escape(title)}</b><small>{html.escape(summary)}</small></span></summary>'
            f'<div><p><b>Example:</b> <a href="{href}">{html.escape(project["title"])}</a></p>'
            f'<p class="evidence">Evidence checked {html.escape(readable_date(project["evidence_date"]))} · '
            f'<a href="{html.escape(project["evidence_url"], quote=True)}" target="_blank" rel="noopener">'
            f'{html.escape(project["evidence_label"])}</a></p>'
            f'<p class="scope-note"><b>Scope:</b> {html.escape(limitation)}</p></div></details>'
        )
    return (
        '<section class="engineering-approach" id="engineering-approach" aria-labelledby="approach-title">'
        '<div class="section-heading"><div><p class="eyebrow">Working method</p>'
        '<h2 id="approach-title">From risk to evidence</h2>'
        '<p class="sub">Open a step for a concrete case study and its dated source. These examples remain readable as ordinary page content.</p>'
        '</div></div><div class="approach-steps">' + ''.join(steps) + '</div></section>'
    )


EVIDENCE_EXAMPLES = (
    ('Cross-browser execution', 'playwright-typescript-framework', None),
    ('Defect caught and retained as a regression check', 'appium-framework', None),
    ('Performance before and after', 'k6-performance-testing', None),
    ('Quality-gate decision', 'automation-coverage-quality-intelligence',
     'A TaskBoard run had 114 of 114 reported results pass, but its cancelled Firefox job made the release gate incomplete.'),
)


def evidence_showcase() -> str:
    cards = []
    for label, project_id, claim in EVIDENCE_EXAMPLES:
        project = PROJECT_BY_ID[project_id]
        evidence_url = project['readme_url'] if claim else project['evidence_url']
        evidence_label = 'Case study and source notes' if claim else project['evidence_label']
        evidence_target = '#evidence' if claim else '#results'
        cards.append(
            f'<article class="evidence-card"><p class="eyebrow">{html.escape(label)}</p>'
            f'<h3><a href="projects/{project["page"]}.html{evidence_target}">{html.escape(project["title"])}</a></h3>'
            f'<p>{html.escape(claim or project["result"])}</p>'
            f'<p class="evidence">Checked {html.escape(readable_date(project["evidence_date"]))} · '
            f'<a href="{html.escape(evidence_url, quote=True)}" target="_blank" rel="noopener">'
            f'{html.escape(evidence_label)}</a></p>'
            f'<p class="scope-note"><b>Evidence scope:</b> {html.escape(project["comparison_limits"])}</p>'
            '</article>'
        )
    return (
        '<section class="engineering-evidence" id="engineering-evidence" aria-labelledby="evidence-title">'
        '<div class="section-heading"><div><p class="eyebrow">Evidence first</p>'
        '<h2 id="evidence-title">Engineering evidence</h2>'
        '<p class="sub">Dated records describe the linked run or repository material. Limits stay beside the claim; no endorsement or live-status promise is implied.</p>'
        '</div></div><div class="evidence-grid">' + ''.join(cards) + '</div></section>'
    )


def dashboard_showcase() -> str:
    """Present the existing dated dashboard preview as a direct path to the live product."""
    project = PROJECT_BY_ID['automation-coverage-quality-intelligence']
    preview_type, preview_scope = project['preview_caption']
    image = 'img/' + project['image'] + '.jpg'
    return f'''<section class="dashboard-showcase" id="quality-intelligence" aria-labelledby="dashboard-showcase-title">
      <div class="showcase-copy"><p class="eyebrow">Built to bring the evidence together</p>
      <h2 id="dashboard-showcase-title">Quality Intelligence.<br>One place to explore.</h2>
      <p class="sub">{html.escape(project['short_purpose'])}</p>
      <ul class="showcase-features" aria-label="Dashboard capabilities"><li>Repository filters</li><li>Execution trends</li><li>Release gates</li></ul>
      <div class="btns"><a class="btn primary" href="{html.escape(project['live_demo'], quote=True)}" target="_blank" rel="noopener">Open live dashboard {icon('arrow')}</a>
      <a class="text-action" href="projects/{html.escape(project['page'])}.html">Read the case study {icon('arrow')}</a></div>
      <p class="showcase-note">{html.escape(preview_type)}. {html.escape(preview_scope)}</p></div>
      <div class="showcase-preview"><span class="preview-window" aria-hidden="true"><i></i><i></i><i></i><span>Quality Intelligence / Overview</span></span>
      <a href="projects/{html.escape(project['page'])}.html" aria-label="Explore the Quality Intelligence case study"><img src="{image}" alt="{html.escape(project['alt'], quote=True)}" width="640" height="400" loading="lazy"></a></div>
    </section>'''


def flagship_card(project_id):
    project = dict(PROJECT_BY_ID[project_id])
    if not project.get('preview_caption'):
        project['preview_caption'] = ('Architecture illustration', 'Repository pipeline illustration; not a live model result.')
    card = project_card(project)
    story = FLAGSHIP_STORIES[project_id]
    brief = ('<dl class="flagship-brief"><dt>Problem</dt><dd>' + html.escape(story['problem']) + '</dd>'
             '<dt>Approach</dt><dd>' + html.escape(story['decision']) + '</dd></dl>')
    card = card.replace('<div class="card-result">', brief + '<div class="card-result">')
    return card.replace('<div class="actions">', '<div class="actions"><a class="text-action" href="projects/' + project['page'] + '.html#story">Engineering story</a>')


def dashboard_walkthrough():
    return '''<section class="dashboard-tour" aria-labelledby="tour-title" id="dashboard-tour">
      <div><p class="eyebrow">Try the navigation</p><h2 id="tour-title">From repository to results.</h2>
      <p class="sub">Choose a path, then open that scope in the live dashboard. This guide makes no live requests and displays no execution totals.</p></div>
      <form data-dashboard-tour aria-label="Dashboard walkthrough">
        <div class="tour-fields"><label>1. Repository<select name="repository"><option value="enterprise-test-automation-framework">Enterprise Test Automation</option><option value="playwright-typescript-framework">Playwright TypeScript</option><option value="cypress-typescript-framework">Cypress TypeScript</option></select></label>
        <label>2. Test type<select name="kind"><option value="ui">UI</option><option value="api">API</option></select></label>
        <label>3. Browser<select name="browser"><option value="">All browsers</option></select></label></div>
        <p class="tour-status" role="status" aria-live="polite" data-tour-status>Open the live dashboard to explore collected execution evidence. Filters can return no results.</p>
        <div class="btns"><a class="btn primary" data-tour-link href="https://quality-intelligence-0ur1.onrender.com/" target="_blank" rel="noopener">Open selected dashboard ↗</a><button class="btn" type="reset">Reset selection</button></div>
        <noscript><p>The guided selection needs JavaScript. Use the dashboard link above to choose filters directly.</p></noscript>
      </form>
    </section>'''


HTML = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Niranjan Kumar Agri · Technical Lead QA | Senior SDET</title>
<meta name="description" content="Technical Lead QA, Senior SDET and Test Automation Architect with 12+ years in software engineering and QA. Explore verified automation projects, dated CI evidence and case studies. Open to European relocation.">
<link rel="canonical" href="{HOME}">
<meta property="og:title" content="Niranjan Kumar Agri · Technical Lead QA | Senior SDET | Test Automation Architect">
<meta property="og:description" content="A portfolio of {len(PROJECTS)} automation and quality engineering projects, with dated evidence and case studies.">
<meta property="og:type" content="website">
<meta property="og:url" content="{HOME}">
<meta property="og:image" content="{HOME}img/social/portfolio.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Niranjan Kumar Agri — quality engineering portfolio">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%2308665e'/%3E%3Ctext x='32' y='42' font-family='Segoe UI,Arial' font-size='28' font-weight='700' fill='white' text-anchor='middle'%3ENA%3C/text%3E%3C/svg%3E">
{stylesheet()}
<script>try{{var t=localStorage.getItem('na-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
<body>
{header('', 'home', len(PROJECTS))}
<main id="main" class="wrap">
  <section class="hero" aria-labelledby="hero-title"><div class="hero-grid">
    <div class="hero-text">
      <p class="hero-intro">Niranjan Kumar Agri / Quality Engineering</p>
      <p class="eyebrow">Technical Lead QA · Senior SDET · Test Automation Architect</p>
      <h1 id="hero-title">I build automation and quality strategies for reliable releases.</h1>
      <p class="lead">I design test platforms, lead QA strategy and make release evidence easier to inspect—from requirements traceability to browser, API and performance checks.</p>
      <p class="where"><span>Based in Haldwani, Uttarakhand, India</span><span>Open to European relocation</span></p>
      <div class="btns primary-actions"><a class="btn primary" href="projects.html">Explore projects {icon('arrow')}</a><a class="btn" href="{CV}" download>{icon('download')}Download CV</a></div>
      <ul class="hero-evidence-strip" aria-label="Portfolio overview"><li><strong>12+ years</strong><span>engineering and quality</span></li><li><strong>{len(PROJECTS)} projects</strong><span>with case studies</span></li><li><strong>QA leadership</strong><span>led and mentored four engineers</span></li></ul>
      <div class="btns secondary-actions"><a class="text-action" href="{GITHUB}" target="_blank" rel="noopener">{icon('github')}GitHub</a><a class="text-action" href="{LINKEDIN}" target="_blank" rel="noopener">{icon('linkedin')}LinkedIn</a><a class="text-action" href="mailto:{EMAIL}">{icon('mail')}Email</a></div>
    </div>
    <picture class="portrait"><source srcset="img/profile-2026-10b.webp" type="image/webp"><img src="img/profile-2026-10b.jpg" alt="Portrait of Niranjan Kumar Agri in a dark navy suit and white shirt" width="560" height="700" decoding="async" fetchpriority="high"></picture>
  </div></section>

  <section class="impact" aria-labelledby="impact-title"><div class="impact-proof">
    <p class="eyebrow">One regulated product release scope</p><h2 id="impact-title"><strong>84%</strong> automated and ready to run</h2>
    <p class="stat-note">Measured as the share of test cases in that release scope that were automated and ready to run, including all multi-user performance and upgrade suites. This describes automation coverage, not product quality.</p>
  </div>
  </section>


  <section id="projects" aria-labelledby="projects-title"><div class="section-heading"><div><p class="eyebrow">Selected work</p><h2 id="projects-title">Featured projects</h2><p class="sub">Three flagship stories: framework engineering, quality intelligence and reviewed AI-assisted testing. Results link to dated evidence.</p></div><a class="btn" href="projects.html">View all {len(PROJECTS)} projects</a></div>
    <div class="grid featured-grid">{''.join(flagship_card(project_id) for project_id in HOME_PROJECT_IDS)}</div>
  </section>

  {dashboard_showcase()}
  {dashboard_walkthrough()}
  <aside class="recruiter-summary" aria-labelledby="recruiter-title"><div><p class="eyebrow">At a glance</p><h2 id="recruiter-title">Quality engineering, from strategy to execution.</h2><p>Technical Lead QA · Senior SDET · Test Automation Architect</p><p class="sub">Haldwani, India · Open to European relocation. A destination-country work permit would be required.</p></div><div class="btns"><a class="btn primary" href="{CV}" download>Download CV</a><a class="btn" href="mailto:{EMAIL}">Get in touch</a></div></aside>

  <section id="experience" aria-labelledby="experience-title"><p class="eyebrow">Career history</p><h2 id="experience-title">Experience</h2><p class="sub">Employers, titles and dates as recorded on my CV. Key outcomes are visible first; supporting responsibilities expand below.</p>
    <ol class="timeline">
      <li><div class="timeline-head"><div><h3 class="role">Technical Lead QA</h3><p class="org">Sycamore Informatics Inc. · Bengaluru, India</p></div><time datetime="2025-03">Mar 2025–present</time></div>
        <p class="timeline-summary">Lead a four person QA team and own test strategy, requirements traceability and release sign-off for a GxP and ICH-GCP clinical metadata product.</p>
        <details><summary>More responsibilities and outcomes</summary><ul><li>Built the Robot Framework and Python MDR automation suite, covering 84% of the release test scope, including all multi-user performance and upgrade suites.</li><li>Designed rfswarm benchmarks with real browser sessions, ramping to 135 concurrent users across 1,400+ seeded accounts and flagging release response-time drift of 10% or more.</li><li>Use Claude for test design and data suggestions; review generated output before use.</li><li>Received the Sycamore Informatics Platinum Star Award in 2026.</li><li>Own defect triage and quality evidence for release decisions.</li></ul></details>
      </li>
      <li><div class="timeline-head"><div><h3 class="role">Technical Lead QA</h3><p class="org">Ephicacy · Bengaluru, India · client engagement: Sycamore Informatics</p></div><time datetime="2024-06">Jun 2024–Feb 2025</time></div>
        <p class="timeline-summary">Led QA for Sycamore’s MDR product as an Ephicacy consultant; joined Sycamore as an in-house employee in Mar 2025.</p>
        <details><summary>More responsibilities and outcomes</summary><ul><li>Started the Robot Framework and Python automation suite and the requirements traceability process that continued after the move in-house.</li><li>Worked with the client team on test strategy, defect triage and release readiness.</li></ul></details>
      </li>
      <li><div class="timeline-head"><div><h3 class="role">Java Developer / Test Automation Engineer</h3><p class="org">MIVO Mitarbeitervorteile GmbH · Frankfurt, Germany</p></div><time datetime="2022-05">May 2022–Oct 2023</time></div>
        <p class="timeline-summary">Developed Java features for an employee benefits platform and contributed to automated checks and release quality.</p>
        <details><summary>More responsibilities and outcomes</summary><ul><li>Handled functional analysis, front-end and back-end development through release.</li><li>Wrote unit tests and automated checks and reviewed code for quality and coding standards.</li><li>Designed database schemas and queries, tuned database performance and fixed security vulnerabilities.</li><li>Documented work and shared knowledge with a German team through internal training.</li></ul><p class="note-line">Dates reflect the respective company records. The overlap with bebo employment occurred during my transition to a role in Germany.</p></details>
      </li>
      <li><div class="timeline-head"><div><h3 class="role">Software Engineer → Associate Software Architect</h3><p class="org">bebo Technologies Pvt. Ltd. · Chandigarh, India</p></div><time datetime="2017-03">Mar 2017–Sep 2023</time></div>
        <p class="timeline-summary">Progressed through four engineering roles while building web, service and API automation and coordinating test work.</p>
        <details><summary>Role progression and responsibilities</summary><p>Software Engineer (Mar 2017–Mar 2019) · Senior Software Engineer (Mar 2019–Mar 2021) · Principal Software Engineer (Mar 2021–Mar 2023) · Associate Software Architect (Mar 2023–Sep 2023).</p><ul><li>Built a hybrid Selenium WebDriver framework using page objects, data-driven and keyword-driven approaches, and integrated suites into CI/CD.</li><li>Wrote test strategies, estimates and TestRail plans; directed offshore teams on UI and API testing.</li></ul></details>
      </li>
      <li><div class="timeline-head"><div><h3 class="role">Java Developer</h3><p class="org">Simplified Fintech Pvt Ltd · Panchkula, India</p></div><time datetime="2016-04">Apr 2016–Feb 2017</time></div>
        <p class="timeline-summary">Developed Java web applications for a fintech product.</p><details><summary>More responsibilities</summary><ul><li>Worked with the QA team to set up test scripts, test cases and automation.</li></ul></details>
      </li>
      <li><div class="timeline-head"><div><h3 class="role">Java Developer</h3><p class="org">SSV Technologies and Consultancy Services · Indore, India</p></div><time datetime="2014-11">Nov 2014–Feb 2016</time></div>
        <p class="timeline-summary">Built Java web applications, including e-commerce features.</p><details><summary>More responsibilities</summary><ul><li>Added unit and integration tests with JUnit and TestNG.</li></ul></details>
      </li>
      <li><div class="timeline-head"><div><h3 class="role">Trainee Software Developer</h3><p class="org">Ypsilon IT Solutions Pvt Ltd · Indore, India</p></div><time datetime="2014-05">May 2014–Oct 2014</time></div>
        <p class="timeline-summary">Maintained Java applications and contributed to an internal integration platform.</p>
      </li>
    </ol>
  </section>

  <section class="exploration-band" id="exploration" aria-labelledby="exploration-title">
    <div class="section-heading"><div><p class="eyebrow">Explore</p><h2 id="exploration-title">Find work by role or problem</h2><p class="sub">Open any path to see related project evidence and professional experience.</p></div></div>
    {role_explorer()}
    {problem_explorer()}
  </section>



  <div class="supporting-work"><details><summary>Capabilities and working method</summary>{capability_showcase()}{engineering_approach()}</details><details><summary>Inspect engineering evidence</summary>{evidence_showcase()}</details></div>

  <details class="supporting-work" data-skills-disclosure><summary>Skills, education and work authorization</summary>
  <section id="skills" aria-labelledby="skills-title"><p class="eyebrow">Strengths and tools</p><h2 id="skills-title">Skills</h2><p class="sub">Professional experience is separated from tools and approaches demonstrated in portfolio projects.</p>
    <div class="skills">
      <article class="skill"><h3>QA leadership · Professional</h3><p>Test strategy, test planning, RTM, release sign-off, defect triage and management, mentoring, offshore team coordination.</p></article>
      <article class="skill"><h3>Automation · Professional</h3><p>Selenium WebDriver, Robot Framework, Java, Python, API testing, CI/CD integration.</p>{skill_link("Selenium", "Explore supporting projects")}</article>
      <article class="skill"><h3>Automation · Portfolio experience</h3><p>Playwright, Cypress, Appium, TestNG, JUnit, Cucumber, Pact, TypeScript, JavaScript.</p>{skill_link("Playwright", "Explore supporting projects")}</article>
      <article class="skill"><h3>API and integration testing</h3><p>REST Assured, Postman, contract testing, database checks, Kafka and Testcontainers.</p>{skill_link("API", "Explore supporting projects")}</article>
      <article class="skill"><h3>Performance · Professional</h3><p>rfswarm, multi-user browser testing and release to release response-time baselines.</p>{skill_link("performance", "Explore related projects")}</article>
      <article class="skill"><h3>Performance · Portfolio experience</h3><p>k6 scenarios, SLO thresholds, load, stress, spike and soak testing.</p><a href="projects/k6-performance.html">k6 case study</a></article>
      <article class="skill"><h3>Framework design</h3><p>Page Object Model, data-driven testing, keyword-driven testing, BDD, parallel execution, test data isolation.</p>{skill_link("framework", "Explore supporting projects")}</article>
      <article class="skill"><h3>CI/CD and tools</h3><p>Jenkins, Azure DevOps, Git, GitHub, Jira, TestRail. Portfolio: GitHub Actions, CircleCI, Docker, Selenium Grid, Allure, Maven.</p>{skill_link("GitHub Actions", "Explore supporting projects")}</article>
      <article class="skill"><h3>Regulated environments</h3><p>GxP, ICH-GCP clinical software quality assurance.</p></article>
      <article class="skill"><h3>AI-assisted testing</h3><p>Test design and test data suggestions with human review; portfolio projects document sample and replay runs separately from live model outputs.</p>{skill_link("Claude", "Explore supporting projects")}</article>
    </div>
    <div class="two credentials"><article class="box"><h3>Education</h3><p><b>M.Tech, Computer Science and Engineering</b><br><span class="org">Galgotias University · 2012–2014</span></p><p><b>B.Tech, Information Technology</b><br><span class="org">Graphic Era University, Dehradun · 2008–2012</span></p></article>
      <article class="box"><h3>Languages and work authorization</h3><p>Hindi (native) · English (professional working proficiency)</p><p>Based in India. My earlier work in Germany does not give me a current right to work there or elsewhere in Europe. I would need a work permit for the destination country and am open to relocating.</p></article></div>
  </section>

  </details>

  <section id="coming-next" aria-labelledby="coming-next-title"><p class="eyebrow">Portfolio v{PORTFOLIO_VERSION} · UI phase complete</p><h2 id="coming-next-title">Coming next</h2><p>WebdriverIO + TypeScript is in active development and is not counted as a completed project. Portfolio promotion waits for verified Chrome and Firefox execution evidence.</p>
    <div class="grid"><article class="box"><h3>In progress: WebdriverIO + TypeScript</h3><p><a href="https://github.com/niranjankagri/webdriverio-typescript-framework">Framework repository</a>: local demo shop, isolated test data, smoke and regression categories, network and console assertions, failure evidence, JUnit XML, and a Quality Intelligence catalog. Browser execution evidence is still pending; this repository has no CI workflow.</p></article><article class="box"><h3>Enhancement: mutation testing</h3><p>Extend an existing project with repeatable mutation reports and a CI gate that checks whether assertions detect introduced defects.</p></article><article class="box"><h3>Optional: Karate API testing</h3><p>Authentication, schema validation, data-driven and negative scenarios, mocks, and parallel CI. This is a candidate after WebdriverIO, not a delivery commitment.</p></article></div>
  </section>
  <section id="contact" aria-labelledby="contact-title"><div class="contact"><p class="eyebrow">Open to Senior SDET, QA Lead and Test Automation Architect opportunities</p><h2 id="contact-title">Let’s build reliable releases.</h2><p class="contact-context">Based in Haldwani, India · Open to European relocation</p>
    <div class="btns"><a class="btn primary" href="mailto:{EMAIL}">{icon('mail')}Email me</a><a class="btn" href="{CV}" download>{icon('download')}Download CV</a><button class="btn" type="button" data-copy-email="{EMAIL}">Copy email</button><a class="btn" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a><a class="btn" href="{GITHUB}" target="_blank" rel="noopener">GitHub</a></div><p class="copy-status" role="status" aria-live="polite"></p><p class="sub">{EMAIL}</p>
  </div></section>
</main>
{footer('')}
{script_asset('theme.js')}
</body></html>
'''

with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(HTML)
print(f'index written with {len(PROJECTS)} projects ({len(FEATURED_PROJECTS)} featured)')
