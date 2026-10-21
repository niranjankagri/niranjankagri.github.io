"""Generate the portfolio home page from the shared project catalogue."""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(__file__))
from components import CV, EMAIL, GITHUB, HOME, LINKEDIN, footer, header, icon, project_card  # noqa: E402
from project_data import FEATURED_PROJECTS, PROJECTS  # noqa: E402


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
<meta property="og:image" content="{HOME}img/profile-2026-10b.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%234f43d6'/%3E%3Ctext x='32' y='42' font-family='Segoe UI,Arial' font-size='28' font-weight='700' fill='white' text-anchor='middle'%3ENA%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="style.css">
<script>try{{var t=localStorage.getItem('na-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
<body>
{header('', 'home', len(PROJECTS))}
<main id="main" class="wrap">
  <section class="hero" aria-labelledby="hero-title"><div class="hero-grid">
    <div class="hero-text">
      <p class="eyebrow">Technical Lead QA · Senior SDET · Test Automation Architect</p>
      <h1 id="hero-title">I build automation frameworks and quality strategies that accelerate reliable releases.</h1>
      <p class="lead">I combine hands-on framework engineering with QA leadership, from test strategy and traceability to CI pipelines and release decisions. My work spans regulated software, web and API automation, mobile, performance, and AI-assisted testing.</p>
      <p class="where"><span>Based in Haldwani, Uttarakhand, India</span><span>Open to European relocation</span></p>
      <div class="btns primary-actions"><a class="btn primary" href="projects.html">Explore projects {icon('arrow')}</a><a class="btn" href="{CV}" download>{icon('download')}Download CV</a></div>
      <div class="btns secondary-actions"><a class="text-action" href="{GITHUB}" target="_blank" rel="noopener">{icon('github')}GitHub</a><a class="text-action" href="{LINKEDIN}" target="_blank" rel="noopener">{icon('linkedin')}LinkedIn</a><a class="text-action" href="mailto:{EMAIL}">{icon('mail')}Email</a></div>
    </div>
    <picture class="portrait"><source srcset="img/profile-2026-10b.webp" type="image/webp"><img src="img/profile-2026-10b.jpg" alt="Portrait of Niranjan Kumar Agri in a dark navy suit and white shirt" width="560" height="700" decoding="async" fetchpriority="high"></picture>
  </div></section>

  <section class="impact" aria-labelledby="impact-title"><h2 id="impact-title" class="sr-only">Professional impact</h2>
    <div class="stats">
      <article class="stat"><strong>12+ years</strong><span>in software engineering and quality assurance, from Java development to QA leadership</span></article>
      <article class="stat"><strong>84%</strong><span>of one regulated product release test scope automated</span></article>
      <article class="stat"><strong>4 engineers</strong><span>led and mentored, with ownership of test strategy, traceability, defect triage and release sign-off</span></article>
    </div>
    <p class="stat-note"><b>84%</b> is measured as the share of test cases in the release scope that were automated and ready to run, including all multi-user performance and upgrade suites. This describes automation coverage, not product quality.</p>
  </section>

  <section id="projects" aria-labelledby="projects-title"><div class="section-heading"><div><p class="eyebrow">Selected work</p><h2 id="projects-title">Featured projects</h2><p class="sub">Six projects selected for engineering depth, range and evidence. Every card links to its case study and source.</p></div><a class="btn" href="projects.html">View all {len(PROJECTS)} projects</a></div>
    <div class="grid featured-grid">{''.join(project_card(p) for p in FEATURED_PROJECTS)}</div>
  </section>

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

  <section id="skills" aria-labelledby="skills-title"><p class="eyebrow">Strengths and tools</p><h2 id="skills-title">Skills</h2><p class="sub">Professional experience is separated from tools and approaches demonstrated in portfolio projects.</p>
    <div class="skills">
      <article class="skill"><h3>QA leadership · Professional</h3><p>Test strategy, test planning, RTM, release sign-off, defect triage and management, mentoring, offshore team coordination.</p></article>
      <article class="skill"><h3>Automation · Professional</h3><p>Selenium WebDriver, Robot Framework, Java, Python, API testing, CI/CD integration.</p><a href="projects.html?category=Web+%26+API">Supporting projects</a></article>
      <article class="skill"><h3>Automation · Portfolio experience</h3><p>Playwright, Cypress, Appium, TestNG, JUnit, Cucumber, Pact, TypeScript, JavaScript.</p><a href="projects.html?tech=TypeScript">Supporting projects</a></article>
      <article class="skill"><h3>API and integration testing</h3><p>REST Assured, Postman, contract testing, database checks, Kafka and Testcontainers.</p><a href="projects.html?q=API">Supporting projects</a></article>
      <article class="skill"><h3>Performance · Professional</h3><p>rfswarm, multi-user browser testing and release to release response-time baselines.</p><a href="projects.html?category=Performance">Related projects</a></article>
      <article class="skill"><h3>Performance · Portfolio experience</h3><p>k6 scenarios, SLO thresholds, load, stress, spike and soak testing.</p><a href="projects/k6-performance.html">k6 case study</a></article>
      <article class="skill"><h3>Framework design</h3><p>Page Object Model, data-driven testing, keyword-driven testing, BDD, parallel execution, test data isolation.</p><a href="projects.html?q=framework">Supporting projects</a></article>
      <article class="skill"><h3>CI/CD and tools</h3><p>Jenkins, Azure DevOps, Git, GitHub, Jira, TestRail. Portfolio: GitHub Actions, CircleCI, Docker, Selenium Grid, Allure, Maven.</p><a href="projects.html?category=CI%2FCD">Supporting projects</a></article>
      <article class="skill"><h3>Regulated environments</h3><p>GxP, ICH-GCP clinical software quality assurance.</p></article>
      <article class="skill"><h3>AI-assisted testing</h3><p>Test design and test data suggestions with human review; portfolio projects document sample and replay runs separately from live model outputs.</p><a href="projects.html?category=AI+%26+LLM">Supporting projects</a></article>
    </div>
    <div class="two credentials"><article class="box"><h3>Education</h3><p><b>M.Tech, Computer Science and Engineering</b><br><span class="org">Galgotias University · 2012–2014</span></p><p><b>B.Tech, Information Technology</b><br><span class="org">Graphic Era University, Dehradun · 2008–2012</span></p></article>
      <article class="box"><h3>Languages and work authorization</h3><p>Hindi (native) · English (professional working proficiency)</p><p>Based in India. My earlier work in Germany does not give me a current right to work there or elsewhere in Europe. I would need a work permit for the destination country and am open to relocating.</p></article></div>
  </section>

  <section id="contact" aria-labelledby="contact-title"><div class="contact"><p class="eyebrow">Get in touch</p><h2 id="contact-title">Hiring a Technical Lead QA, Senior SDET, or Test Automation Architect? Let’s connect.</h2>
    <div class="btns"><a class="btn primary" href="mailto:{EMAIL}">{icon('mail')}Email me</a><button class="btn" type="button" data-copy-email="{EMAIL}">Copy email</button><a class="btn" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a><a class="btn" href="{GITHUB}" target="_blank" rel="noopener">GitHub</a><a class="btn" href="{CV}" download>Download CV</a></div><p class="copy-status" role="status" aria-live="polite"></p><p class="sub">{EMAIL}</p>
  </div></section>
</main>
{footer('')}
<script src="theme.js" defer></script>
</body></html>
'''

with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(HTML)
print(f'index written with {len(PROJECTS)} projects ({len(FEATURED_PROJECTS)} featured)')
