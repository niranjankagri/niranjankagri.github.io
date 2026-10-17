# Generates the portfolio home page (index.html). Run from anywhere: python tools/make_index.py
# Every fact here was checked against the repositories, their CI runs or the user's own records
# (12 Oct 2026). Never put internal employer figures here: CV-level wording only.
import os

# Repository root (this file lives in tools/)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GH = 'https://github.com/niranjankagri/'
CV = 'Niranjan_Kumar_Agri_CV_Technical_Lead_QA_SDET.pdf'

ICON = {
 'cv': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M11 3h2v9.6l3.3-3.3 1.4 1.4L12 16.4l-5.7-5.7 1.4-1.4 3.3 3.3zM4 18h16v2H4z"/></svg>',
 'gh': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 .5a11.5 11.5 0 0 0-3.64 22.4c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.53-1.33-1.28-1.69-1.28-1.69-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.81 1.19 1.84 1.19 3.1 0 4.42-2.7 5.4-5.26 5.68.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5z"/></svg>',
 'in': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.6 8.65 21 11.3 21 14.7V21h-4v-5.6c0-1.33-.03-3.05-1.86-3.05-1.86 0-2.14 1.45-2.14 2.95V21H9z"/></svg>',
 'mail': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm9 7.2L4 7.3V17h16V7.3z"/></svg>',
}

FEATURED = [
 dict(n=1, badge='Flagship', title='Enterprise Test Automation Framework', repo='enterprise-test-automation-framework', wf='nightly.yml',
      wfname='Nightly regression', img='enterprise', alt='Allure report of the Enterprise framework: pass rate, suites and environment',
      page='enterprise', report='docs/images/report-overview.png', arch=True,
      fact='169 TestNG test executions from 124 test methods, all passing in the scheduled nightly run of 12 Oct 2026: API 57, UI 48, database 13, integration 9, end-to-end 2, framework unit tests 40.',
      text='UI, API and database checks of one demo shop kept in the repository; parallel execution, infrastructure-only retries, Allure evidence, Docker + Selenium Grid, nightly CI on Chrome, Firefox and Edge.',
      tags=['Java 17', 'Selenium 4', 'REST Assured', 'JDBC', 'Allure', 'Docker']),
 dict(n=2, badge='Web + API', title='Playwright + TypeScript Framework', repo='playwright-typescript-framework', wf='ci.yml', wfname='CI',
      img='playwright-ts', alt='Playwright HTML report listing API tests with their tags', page='playwright-typescript', report='docs/images/report-overview.png',
      fact='47 tests, 95 test executions per full run: 23 API tests once, plus 24 UI tests on each of Chromium, Firefox and WebKit.',
      text='Page objects with a header component, typed API clients with zod contracts, login through the API, network mocking; CI runs lint and type checks first, then four parallel jobs.',
      tags=['Playwright Test', 'TypeScript', 'zod', 'ESLint', 'GitHub Actions']),
 dict(n=3, badge='Web + API', title='Playwright for Java Framework', repo='playwright-framework', wf='tests.yml', wfname='Tests',
      img='playwright-java', alt='Playwright for Java HTML report with summary and test groups', page='playwright-java', report='docs/images/html-report.png',
      fact='57 UI, API and network tests, run in CI on Chromium, Firefox and WebKit (one job per browser engine).',
      text='Annotation-based page factory, a browser per thread and a context per test, API tests with their own data clean-up, and a trace, video and screenshot kept for every failed UI test.',
      tags=['Playwright', 'Java 17', 'TestNG', 'Jackson', 'GitHub Actions']),
 dict(n=4, badge='Mobile', title='Appium Android Framework', repo='appium-framework', wf='tests.yml', wfname='Tests',
      img='appium', alt='Appium framework report: 40 of 40 tests passed on an Android 15 emulator', page='appium', report='docs/images/report-overview.png',
      fact='40 tests on an Android 15 emulator, locally and in GitHub Actions; found 3 real bugs in the demo app, each kept as a test.',
      text='Screen objects with built-in waits, device tests, a screenshot and screen recording for every failure, retries only on Android "not responding" dialogs.',
      tags=['Appium 3', 'Java 17', 'TestNG', 'UiAutomator2']),
 dict(n=5, badge='Keyword-driven', title='Robot Framework UI + API', repo='robot-framework-automation', wf='ci.yml', wfname='CI',
      img='robot', alt='Robot Framework report: 30 tests passed', page='robot-framework', report='docs/images/report-overview.png',
      fact='30 tests (15 UI, 15 API) in about 70 seconds with 4 parallel pabot processes.',
      text='Page objects as resource files, API service objects, Python only where Robot syntax is awkward; CI lints first, then runs on Chrome and Firefox, plus a scheduled nightly run.',
      tags=['Robot Framework 7', 'Python', 'SeleniumLibrary', 'RequestsLibrary', 'pabot']),
 # Facts checked 13 Oct 2026: 46 tests locally (-n 4, about 1 m 46 s) and CI green on all three browser jobs.
 dict(n=6, badge='API + UI', title='Python pytest + Playwright Framework', repo='python-pytest-framework', wf='ci.yml', wfname='CI',
      img='pytest', alt='pytest-html report of the Python framework: 46 tests passed', page='python-pytest',
      report='docs/images/report-all-passed.png',
      fact='46 tests (32 API, 9 UI, 5 hybrid API + UI) in about 1 m 45 s with 4 parallel workers; in CI the UI and hybrid tests run on Chromium, Firefox and WebKit.',
      text='A requests API client with pydantic contracts, Playwright page objects, login through the API by token injection, a throwaway user per test, and a screenshot in the HTML report for every failed UI test.',
      tags=['Python', 'pytest', 'Playwright', 'requests', 'pydantic', 'GitHub Actions']),
 # Facts checked 13 Oct 2026: local ci-profile runs (stress before/after the fix) and CI green (lint, smoke, load, stress, spike).
 dict(n=7, badge='Performance', title='k6 Performance Testing', repo='k6-performance-testing', wf='perf.yml', wfname='Performance',
      img='k6', alt='k6 web dashboard of a load test: request rate, response times and virtual users over time', page='k6-performance',
      report='docs/images/load-dashboard.png',
      fact='The stress test found the limit of the demo shop: past about 90 orders/s checkout queued without bound (p95 over 3 s). After adding load shedding, the same test stays under 650 ms.',
      text='Smoke, load, stress, spike and soak tests of a shop API kept in the repository; SLOs per endpoint as k6 thresholds that fail the CI job, open and closed workload models, and an HTML dashboard per run.',
      tags=['k6', 'JavaScript', 'Node.js', 'SLOs', 'GitHub Actions']),
 # Facts checked 16 Oct 2026: 64/64 e2e locally (retries off) and 17/17 component; CI green (checks, API, UI on Chrome/Firefox/Edge, component).
 dict(n=8, badge='E2E + API + Component', title='Cypress + TypeScript Framework', repo='cypress-typescript-framework', wf='ci.yml', wfname='CI',
      img='cypress', alt='Mochawesome report of the Cypress framework: 64 of 64 end-to-end and API tests passed', page='cypress-typescript',
      report='docs/images/report-all-passed.png',
      fact='81 Cypress tests: 31 API, 33 UI and 17 component tests; in CI the UI tests run on Chrome, Firefox and Edge.',
      text='A React + Node task app kept in the repository, tested three ways: cy.request with zod contracts, page objects with cy.intercept and cy.clock for errors, slow answers and dates, and React components mounted alone.',
      tags=['Cypress 16', 'TypeScript', 'React', 'zod', 'GitHub Actions']),
 # Facts checked 16 Oct 2026: npm run contract + demo:breaking locally on a fresh broker; CI green (consumer, provider, broker workflow).
 dict(n=9, badge='Contract testing', title='Pact Contract Testing', repo='pact-contract-testing', wf='contract.yml', wfname='Contract tests',
      img='pact', alt='Pact Broker matrix: the main version verified and deployed, a feature-branch version failed', page='pact-contract',
      report='docs/images/broker-matrix.png',
      fact='A TypeScript consumer and a Java Spring Boot provider, 6 interactions verified through a self-hosted Pact Broker; can-i-deploy blocks a breaking consumer change while the provider build stays green.',
      text='Consumer-driven contracts with Pact V4: matchers and provider states with parameters on the consumer side, JUnit 5 verification of the real Spring Boot app with pending and WIP pacts, and publish, can-i-deploy and record-deployment in GitHub Actions.',
      tags=['Pact', 'TypeScript', 'Java 17', 'Spring Boot', 'Docker', 'GitHub Actions']),
 # Facts checked 16 Oct 2026: local Jenkins builds #2-#7 (first 2 min 13 s with cluster creation, then about 30 s); CI green on all 3 jobs.
 dict(n=10, badge='CI/CD + Kubernetes', title='Jenkins + Kubernetes Test Pipeline', repo='jenkins-kubernetes-pipeline', wf='ci.yml', wfname='CI',
      img='jenkins', alt='Jenkins stage graph: checks, image build, kind cluster, deploy, in-cluster smoke, parallel API tests, quality gate', page='jenkins-kubernetes',
      report='docs/images/jenkins-stages.png',
      fact='Jenkins configured entirely as code builds a service, deploys it to a kind Kubernetes cluster and runs 21 tests against it in about 30 seconds; GitHub Actions starts a real Jenkins on every push and requires the pipeline to pass.',
      text='A declarative Jenkinsfile with parallel stages, parameters, a quality gate and masked credentials; a namespace per build, readiness probes, a smoke Job inside the cluster and API tests through port-forward, all in scripts that CI shares.',
      tags=['Jenkins', 'Kubernetes', 'Docker', 'JCasC', 'pytest', 'GitHub Actions']),

 # Facts checked 17 Oct 2026: 48 unit/tooling tests and the UI suite green locally and in CI (Chromium, Firefox, WebKit).
 # Not claimed yet: AI-generated test counts or triage results (the first live recording run is still to do).
 dict(n=11, badge='AI-assisted testing', title='AI-Assisted Test Automation (Claude)', repo='ai-assisted-test-automation', wf='ci.yml', wfname='CI',
      img='ai-testing', alt='Pipeline: a test case goes to Claude, then a quality gate, then human review; failed runs go to AI triage', page='ai-assisted-testing',
      report='docs/images/pipeline.png',
      fact='Claude drafts Playwright tests from plain-language test cases; a three-stage gate (rules, compile, three runs) decides what a person reviews, and nothing is merged without a named reviewer.',
      text='All Java: a demo app in the repository, the Anthropic Java SDK with typed structured outputs, repair rounds fed by the gate, an approve step that marks AI-written tests, and AI failure triage into product bug, test bug, environment or flaky. Answers are recorded, so CI replays them without an API key.',
      tags=['Java 21', 'Claude API', 'Playwright', 'TestNG', 'GitHub Actions']),

 # Facts checked 17 Oct 2026: 86 harness tests green locally (no model calls). Not claimed yet: eval pass rates
 # (the first live recording run is still to do).
 dict(n=12, badge='LLM evals', title='Testing an LLM Feature (Claude)', repo='llm-feature-testing', wf='ci.yml', wfname='CI',
      img='llm-evals', alt='Eval flow: golden set, assistant, deterministic checks, calibrated LLM judge, pass rate per tag', page='llm-feature-testing',
      report='docs/images/eval-flow.png',
      fact='32 hand-written eval cases in six areas, each run three times; prompt-injection and data-leak areas must pass 100%, and the LLM judge is only trusted after it agrees with hand-labelled answers.',
      text='An HR policy assistant on Claude and the harness that decides whether it can ship: structured replies, deterministic checks for facts, citations, a canary and colleagues\' data, a calibrated groundedness judge, pass rates per area, and 86 tests of the harness itself.',
      tags=['Java 21', 'Claude API', 'LLM evals', 'TestNG', 'GitHub Actions']),
]

MORE = [
 # No CI: the app under test (Google Calculator) cannot be redistributed, so a CI machine has no APK.
 # Facts checked 13 Oct 2026: Android suite 1/1 on an Android 15 emulator with Appium 3.8; iOS not run (needs a Mac).
 dict(title='Mobile Framework (2021, upgraded for Android + iOS)', repo='mobile-test-automation-framework',
      report='docs/images/report-dashboard.png',
      text='My 2021 Appium + TestNG framework, upgraded in 2026 to Appium 3, Java client 11 and Selenium 4 without changing its design: '
           'one set of tests for Android and iOS through a platform layer, capabilities per platform in properties files, '
           'and a custom HTML report with failure screenshots. Runs green on an Android 15 emulator; the iOS side is ready but not yet run.'),
 # No CI: tests run against the shared public OrangeHRM demo. Facts checked 13 Oct 2026: 4/4 on visible Chrome
 # and headless Chrome, Edge and Firefox; the logout test had failed since 2024 because of a missing @ in its XPath.
 dict(title='Selenium Page Object Framework (2024, upgraded)', repo='java-selenium-testng-pom-framework',
      report='docs/images/extent-tests.png',
      text='My January 2024 Selenium + TestNG page object framework for OrangeHRM, upgraded step by step in 2026: '
           'explicit waits instead of fixed sleeps, browser and headless mode from a config file, and an Extent report '
           'with a screenshot on every failure. The upgrade also fixed a locator bug that had failed the logout test since 2024.'),
 # No CI: tests run against public practice sites. Facts checked 13 Oct 2026 (after the layer split, commit 5bc9fb8): 5/5 scenarios on visible Chrome and
 # headless Chrome, Edge and Firefox; the 2022 build no longer compiled (Java 1.7 target, mixed Cucumber versions).
 dict(title='Cucumber BDD Demo (2022, upgraded)', repo='cucumber-bdd-demo',
      report='docs/images/report-passing.png',
      text='My first Cucumber project from 2022, which no longer built, brought to Java 17, Cucumber 8 (JUnit Platform '
           'runners) and Selenium 4 step by step, then split into layers: runners, step definitions, page objects, hooks '
           'and utils. Hooks attach a screenshot on failure, and a Scenario Outline that used to pass without checking '
           'anything now asserts each row.'),
 dict(title='Selenium Java Interview Lab', repo='selenium-java-framework', wf='tests.yml', report='docs/images/html-report.png',
      text='148 runnable tests, one per Selenium, TestNG and framework-design topic, plus a PDF of 100+ interview questions.'),
 dict(title='Cucumber BDD Framework', repo='cucumber-java-framework', wf='tests.yml', report='docs/images/html-report.png',
      text='8 BDD scenarios with Cucumber, Selenium 4 and JUnit, and a custom self-contained HTML report.'),
 dict(title='REST API Automation', repo='api-automation', wf='tests.yml', report='docs/images/html-report.png', page='rest-api',
      text='A layered REST Assured framework (one manager per API resource) with one end-to-end scenario and a custom HTML report.'),
 dict(title='API Framework (2024 version)', repo='api-automation-framework', wf='tests.yml', report='docs/images/allure-report.png',
      text='An earlier REST Assured framework with Extent, Allure and custom TestNG reports on the same suite.'),
 dict(title='JSONPlaceholder API Tests', repo='jsonplaceholder-auto', wf='tests.yml', report='docs/images/extent-report.png',
      text='The original version of the API framework, kept to show how it evolved; Hamcrest matchers and an Extent report.'),
]


def ext(href, label):
    return f'<a href="{href}" target="_blank" rel="noopener">{label}</a>'


def badge(repo, wf, name):
    return (f'<a href="{GH}{repo}/actions/workflows/{wf}" aria-label="Live status of the {name} workflow of {repo}">'
            f'<img class="ci" width="150" height="20" src="{GH}{repo}/actions/workflows/{wf}/badge.svg" alt="{name} workflow status" loading="lazy"></a>')


def featured(p):
    repo = p['repo']
    acts = [f'<a href="projects/{p["page"]}.html">Project details</a>', ext(GH + repo, 'View source code'),
            ext(f'{GH}{repo}#readme', 'View README'), ext(f'{GH}{repo}/actions/workflows/{p["wf"]}', 'View latest CI runs'),
            ext(f'{GH}{repo}/blob/main/{p["report"]}', 'View test report')]
    if p.get('arch'):
        acts.append(f'<a href="projects/{p["page"]}.html#architecture">View architecture diagram</a>')
    tags = ''.join(f'<li class="tag">{t}</li>' for t in p['tags'])
    return f'''      <article class="card">
        <img src="img/{p['img']}.jpg" alt="{p['alt']}" loading="lazy" width="640" height="400">
        <div class="body">
          <span class="badge">{p['n']} · {p['badge']}</span>
          <h3>{p['title']}</h3>
          {badge(repo, p['wf'], p['wfname'])}
          <p class="fact">{p['fact']}</p>
          <p>{p['text']}</p>
          <ul class="tags" aria-label="Technologies">{tags}</ul>
          <div class="actions">{''.join(acts)}</div>
        </div>
      </article>
'''


def more(p):
    repo = p['repo']
    # A project without a CI workflow ('wf') gets no status badge and no CI link
    ci = [ext(f'{GH}{repo}/actions/workflows/{p["wf"]}', 'View latest CI runs')] if p.get('wf') else []
    acts = ([f'<a href="projects/{p["page"]}.html">Project details</a>'] if p.get('page') else []) + [
        ext(GH + repo, 'View source code')] + ci + [ext(f'{GH}{repo}/blob/main/{p["report"]}', 'View test report')]
    status = badge(repo, p['wf'], 'Tests') if p.get('wf') else ''
    return f'''      <article class="card"><div class="body">
        <h3>{p['title']}</h3>
        {status}
        <p>{p['text']}</p>
        <div class="actions">{''.join(acts)}</div>
      </div></article>
'''


HTML = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Niranjan Kumar Agri · Technical Lead QA | Senior SDET</title>
<meta name="description" content="Technical Lead QA, Senior SDET and Test Automation Architect with 12+ years in software engineering and QA. Java, Selenium, Playwright, Appium, Robot Framework, API automation, performance testing, CI/CD. Open to European relocation.">
<meta property="og:title" content="Niranjan Kumar Agri · Technical Lead QA | Senior SDET | Test Automation Architect">
<meta property="og:description" content="Test automation portfolio: twelve flagship projects for web, API, mobile, contracts, CI/CD, performance and AI-assisted testing, each with CI, documentation and test reports.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://niranjankagri.github.io/">
<meta property="og:image" content="https://niranjankagri.github.io/img/profile-2026-10b.jpg">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%234f43d6'/%3E%3Ctext x='32' y='42' font-family='Segoe UI,Arial' font-size='28' font-weight='700' fill='white' text-anchor='middle'%3ENA%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="style.css">
<script>try{{var t=localStorage.getItem('na-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="nav">
  <div class="wrap">
    <a class="home" href="./"><picture><source srcset="img/avatar-2026-10c.webp" type="image/webp"><img class="avatar" src="img/avatar-2026-10c.jpg" alt="" width="40" height="40"></picture>Niranjan Kumar Agri</a>
    <nav aria-label="Sections">
      <a href="#projects">Projects</a><a href="#experience">Experience</a><a href="#skills">Skills</a><a href="#contact">Contact</a>
    </nav>
    <button class="theme" id="theme" type="button" aria-label="Switch between light and dark mode">◐</button>
  </div>
</header>

<main id="main" class="wrap">
  <div class="hero">
    <div class="hero-grid">
      <div class="hero-text">
        <p class="eyebrow">Technical Lead QA | Senior SDET | Test Automation Architect</p>
        <h1>I build reliable automation frameworks and quality engineering strategies that <span class="accent">accelerate software delivery.</span></h1>
        <p class="lead">12+ years of experience in software engineering and quality assurance, combining hands-on automation
          engineering with QA leadership. Experienced in Java, Selenium, Playwright, Appium, Robot Framework, API automation,
          performance testing, and CI/CD, including quality assurance for GxP-regulated clinical software.</p>
        <p class="where"><span>Based in India</span> <span>Previously worked in Germany</span> <span>Open to European relocation</span></p>
        <div class="btns">
          <a class="btn primary" href="{CV}" download>{ICON['cv']}Download CV (PDF)</a>
          <a class="btn" href="#projects">Explore featured projects</a>
          <a class="btn" href="{GH}" target="_blank" rel="noopener">{ICON['gh']}View GitHub</a>
          <a class="btn" href="https://www.linkedin.com/in/niranjan-kumar-agri/" target="_blank" rel="noopener">{ICON['in']}Connect on LinkedIn</a>
          <a class="btn" href="#contact">Contact me</a>
        </div>
      </div>
      <picture class="portrait">
        <source srcset="img/profile-2026-10b.webp" type="image/webp">
        <img src="img/profile-2026-10b.jpg" alt="Portrait of Niranjan Kumar Agri in a dark navy suit and white shirt against a light grey background" width="560" height="700" decoding="async" fetchpriority="high">
      </picture>
    </div>

    <div class="facts">
      <h2>At work</h2>
      <div class="stats">
        <div class="stat"><b>12+ years</b><span> in software engineering and QA, from Java developer to Technical Lead QA</span></div>
        <div class="stat"><b>84%</b><span> of the release test scope of a GxP-regulated clinical data product automated</span>
          <small>How measured: the share of test cases in a release's test scope that were automated and ready to run, including
            all multi-user performance and upgrade suites. It is automation coverage of the release test scope, not a measure of
            product quality.</small></div>
        <div class="stat"><b>4 engineers</b><span> in the QA team I lead and mentor; I own test strategy, traceability and release sign-off</span></div>
      </div>
      <h2>In my public portfolio</h2>
      <div class="stats">
        <div class="stat"><b>17 frameworks</b><span> on GitHub with GitHub Actions CI; every card shows the live status of its workflow</span>
          <small><a href="#projects">See them below</a></small></div>
        <div class="stat"><b>3 real bugs</b><span> found in a public demo app by my Appium framework, each kept as a test</span>
          <small><a href="projects/appium.html#bugs">What they are</a></small></div>
      </div>
    </div>
  </div>

  <section id="projects" aria-labelledby="projects-h">
    <h2 id="projects-h">Featured projects</h2>
    <p class="sub">Portfolio projects I built and maintain on GitHub, not company code. Each has CI, a README with setup instructions and a test report; every badge is the live status of the project's workflow.</p>
    <div class="grid">
{''.join(featured(p) for p in FEATURED)}    </div>

    <h2 style="margin-top:46px">More projects &amp; learning labs</h2>
    <p class="sub">Earlier or overlapping frameworks, kept public to show other tools and how my approach evolved.</p>
    <div class="grid small-grid">
{''.join(more(p) for p in MORE)}    </div>
  </section>

  <section id="experience" aria-labelledby="experience-h">
    <h2 id="experience-h">Experience</h2>
    <p class="sub">Employers, titles and dates as on my CV and LinkedIn.</p>
    <ol class="timeline">
      <li>
        <h3 class="role">Technical Lead QA</h3>
        <p class="org">Sycamore Informatics Inc. (employer) · Bengaluru, India · Mar 2025 – present</p>
        <p class="kind">Leadership</p>
        <ul>
          <li>Lead and mentor a team of 4 QA engineers on MDR, a clinical metadata product used by global pharma companies (GxP / ICH-GCP)</li>
          <li>Own test strategy, requirements traceability (RTM), defect triage and release sign-off</li>
          <li>Received the Platinum Star Award from Sycamore Informatics (2026)</li>
        </ul>
        <p class="kind">Hands-on engineering</p>
        <ul>
          <li>Built the MDR test automation suite in Robot Framework and Python, automating 84% of a release's test scope, including all multi-user performance and upgrade suites</li>
          <li>Designed performance benchmarks in rfswarm (Robot Framework Swarm) in which every virtual user drives a real browser session: a gradual ramp-up to 135 concurrent users across 1,400+ seeded accounts, with each release's response times compared against the previous release and drift of 10% or more flagged</li>
          <li>Use Claude for AI-assisted test design (keywords, test cases, test data), with all generated code reviewed</li>
        </ul>
      </li>
      <li>
        <h3 class="role">Technical Lead QA</h3>
        <p class="org">Ephicacy (employer) · Bengaluru, India · Jun 2024 – Feb 2025 · client engagement: Sycamore Informatics</p>
        <ul>
          <li>Led QA for Sycamore Informatics' MDR product as an Ephicacy consultant; moved in-house to Sycamore in Mar 2025</li>
          <li>Started the Robot Framework and Python automation suite and the RTM process later continued at Sycamore</li>
        </ul>
      </li>
      <li>
        <h3 class="role">Java Developer / Test Automation Engineer</h3>
        <p class="org">MIVO Mitarbeitervorteile GmbH · Frankfurt, Germany · May 2022 – October 2023</p>
        <ul>
          <li>Developed front-end and back-end features in Java for an employee benefits platform, from functional analysis to release</li>
          <li>Wrote unit tests and automated checks, and reviewed code for quality and coding standards</li>
          <li>Designed database schemas and queries, tuned database performance, and fixed security vulnerabilities</li>
          <li>Worked with a German team; shared knowledge through documentation and internal training</li>
        </ul>
        <p class="note-line"><em>Note: Employment dates reflect the respective company records. The overlapping period occurred during my transition to a role in Germany.</em></p>
      </li>
      <li>
        <h3 class="role">Software Engineer → Associate Software Architect</h3>
        <p class="org">bebo Technologies Pvt. Ltd. · Chandigarh, India · March 2017 – September 2023</p>
        <p class="note-line">Associate Software Architect (Mar 2023 – Sep 2023) · Principal Software Engineer (Mar 2021 – Mar 2023) · Senior Software Engineer (Mar 2019 – Mar 2021) · Software Engineer (Mar 2017 – Mar 2019)</p>
        <ul>
          <li>Built a hybrid Selenium WebDriver framework (Page Object, data-driven and keyword-driven) for web applications, services and APIs, and integrated the automated suites into CI/CD pipelines</li>
          <li>Wrote test strategies, estimates and test plans in TestRail; directed offshore teams on UI and API testing</li>
        </ul>
      </li>
      <li>
        <h3 class="role">Java Developer</h3>
        <p class="org">Simplified Fintech Pvt Ltd · Panchkula, India · Apr 2016 – Feb 2017</p>
        <ul>
          <li>Developed Java web applications for a fintech product and set up test scripts, test cases and automation with the QA team</li>
        </ul>
      </li>
      <li>
        <h3 class="role">Java Developer</h3>
        <p class="org">SSV Technologies and Consultancy Services · Indore, India · Nov 2014 – Feb 2016</p>
        <ul>
          <li>Built Java web applications, including e-commerce features, with unit and integration tests in JUnit and TestNG</li>
        </ul>
      </li>
      <li>
        <h3 class="role">Trainee Software Developer</h3>
        <p class="org">Ypsilon IT Solutions Pvt Ltd · Indore, India · May 2014 – Oct 2014</p>
        <ul>
          <li>Maintained and built Java applications, and contributed to an internal integration platform</li>
        </ul>
      </li>
    </ol>
  </section>

  <section id="skills" aria-labelledby="skills-h">
    <h2 id="skills-h">Skills</h2>
    <p class="sub">The same list as on my CV.</p>
    <div class="skills">
      <div class="skill"><h3>Test automation</h3><p>Selenium WebDriver, Playwright, Robot Framework, Cypress, Appium, TestNG, JUnit, Cucumber (BDD)</p></div>
      <div class="skill"><h3>Programming</h3><p>Java, Python, JavaScript, TypeScript, SQL</p></div>
      <div class="skill"><h3>API testing</h3><p>REST Assured, Postman</p></div>
      <div class="skill"><h3>Performance testing</h3><p>rfswarm, load and multi-user performance testing, release-to-release response-time baselines</p></div>
      <div class="skill"><h3>Framework design</h3><p>Page Object Model, data-driven testing, keyword-driven testing, BDD, parallel execution</p></div>
      <div class="skill"><h3>CI/CD and tools</h3><p>Jenkins, Azure DevOps, Git, GitHub, Jira, TestRail; in portfolio projects also GitHub Actions, CircleCI, Docker, Selenium Grid, Allure, Maven</p></div>
      <div class="skill"><h3>QA leadership</h3><p>Test strategy, test planning, RTM, release sign-off, defect triage and management, mentoring, offshore team coordination</p></div>
      <div class="skill"><h3>Regulated environments</h3><p>GxP, ICH-GCP</p></div>
      <div class="skill"><h3>AI-assisted testing</h3><p>Claude for test design, script generation and test data, with human review of all output</p></div>
    </div>
  </section>

  <section aria-label="Education and languages">
    <div class="two">
      <div class="box">
        <h3>Education</h3>
        <p><b>M.Tech, Computer Science and Engineering</b><br><span class="org">Galgotias University · 2012 – 2014</span></p>
        <p><b>B.Tech, Information Technology</b><br><span class="org">Graphic Era University, Dehradun · 2008 – 2012</span></p>
      </div>
      <div class="box">
        <h3>Languages and work authorization</h3>
        <p>Hindi (native) · English (professional working proficiency)</p>
        <p>Based in India. My earlier work in Germany does not give me a current right to work there or elsewhere in Europe: I would need a work permit for the destination country, and I am open to relocating.</p>
      </div>
    </div>
  </section>

  <section id="contact" aria-labelledby="contact-h">
    <div class="contact">
      <h2 id="contact-h">Looking for a Technical Lead QA, Senior SDET, or Test Automation Architect opportunity in Europe? Let’s connect.</h2>
      <div class="btns">
        <a class="btn primary" href="mailto:niranjankagri@gmail.com">{ICON['mail']}Email me</a>
        <a class="btn" href="https://www.linkedin.com/in/niranjan-kumar-agri/" target="_blank" rel="noopener">{ICON['in']}LinkedIn</a>
        <a class="btn" href="{GH}" target="_blank" rel="noopener">{ICON['gh']}GitHub</a>
        <a class="btn" href="{CV}" download>{ICON['cv']}Download CV</a>
      </div>
      <p class="sub" style="margin:16px 0 0">niranjankagri@gmail.com</p>
    </div>
  </section>
</main>

<footer>© 2026 Niranjan Kumar Agri · Hosted on GitHub Pages · <a href="{GH}niranjankagri.github.io">Source of this site</a></footer>
<script src="theme.js"></script>
</body>
</html>
'''

open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8', newline='\n').write(HTML)
print('index written')
