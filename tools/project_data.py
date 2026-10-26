# Canonical project records shared by the home page, project explorer, and case studies.
from datetime import date

FEATURED = [
 dict(n=1, badge='Flagship', title='Enterprise Test Automation Framework', repo='enterprise-test-automation-framework', wf='nightly.yml',
      wfname='Nightly regression', img='enterprise', alt='Allure report of the Enterprise framework: pass rate, suites and environment',
      page='enterprise', report='docs/images/report-overview.png', arch=True,
      fact='As of 12 Oct 2026: 169 TestNG executions across 124 test methods passed in the scheduled nightly run (API 57, UI 48, database 13, integration 9, end-to-end 2, framework unit 40).',
      text='UI, API and database checks of one demo shop kept in the repository; parallel execution, infrastructure-only retries, Allure evidence, Docker + Selenium Grid, nightly CI on Chrome, Firefox and Edge.',
      tags=['Java 17', 'Selenium 4', 'REST Assured', 'JDBC', 'Allure', 'Docker']),
 dict(n=2, badge='Web + API', title='Playwright + TypeScript Framework', repo='playwright-typescript-framework', wf='ci.yml', wfname='CI',
      img='playwright-ts', alt='Playwright HTML report listing API tests with their tags', page='playwright-typescript', report='docs/images/report-overview.png',
      fact='47 unique tests; 95 test executions per full run: 23 API tests once, plus 24 UI tests on each of Chromium, Firefox and WebKit.',
      text='Page objects with a header component, typed API clients with zod contracts, login through the API, network mocking; CI runs lint and type checks first, then four parallel jobs.',
      tags=['Playwright Test', 'TypeScript', 'zod', 'ESLint', 'GitHub Actions']),
 dict(n=3, badge='Web + API', title='Playwright for Java Framework', repo='playwright-framework', wf='tests.yml', wfname='Tests',
      img='playwright-java', alt='Playwright for Java HTML report with summary and test groups', page='playwright-java', report='docs/images/html-report.png',
      fact='57 UI, API and network tests, run in CI on Chromium, Firefox and WebKit (one job per browser engine).',
      text='Annotation-based page factory, a browser per thread and a context per test, API tests with their own data clean-up, and a trace, video and screenshot kept for every failed UI test.',
      tags=['Playwright', 'Java 17', 'TestNG', 'Jackson', 'GitHub Actions']),
 dict(n=4, badge='Mobile', title='Appium Android Framework', repo='appium-framework', wf='tests.yml', wfname='Tests',
      img='appium', alt='Appium framework report: 40 of 40 Android 15 emulator test executions passed', page='appium', report='docs/images/report-overview.png',
      fact='Repository: 40 TestNG methods. Run #7: 40 Android 15 test executions passed; three demo-app defects remain as regression checks.',
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
      fact='81 unique Cypress test cases: 31 API, 33 UI and 17 component; CI runs the UI cases on Chrome, Firefox and Edge.',
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

 # Facts checked 19 Oct 2026: 52 unit/tooling tests and the UI suite green locally and in CI (Chromium, Firefox, WebKit); CI job 'samples' green on hand-written sample answers (labelled as such).
 # Not claimed yet: any Claude result (AI-generated test counts, triage accuracy): the first live recording run is still to do.
 dict(n=11, badge='AI-assisted testing', title='AI-Assisted Test Automation (Claude)', repo='ai-assisted-test-automation', wf='ci.yml', wfname='CI',
      img='ai-testing', alt='Pipeline: a test case goes to Claude, then a quality gate, then human review; failed runs go to AI triage', page='ai-assisted-testing',
      report='docs/images/pipeline.png',
      fact='Claude drafts Playwright tests from plain-language test cases; a three-stage gate (rules, compile, three runs) decides what a person reviews, and nothing is merged without a named reviewer.',
      text='All Java: a demo app in the repository, the Anthropic Java SDK with typed structured outputs, repair rounds fed by the gate, an approve step that marks AI-written tests, and AI failure triage into product bug, test bug, environment or flaky. Answers are recorded, so CI replays them without an API key; until the first live run, CI runs the pipeline on hand-written sample answers that every report labels as samples.',
      tags=['Java 21', 'Claude API', 'Playwright', 'TestNG', 'GitHub Actions']),

 # Facts checked 19 Oct 2026: 90 harness tests green locally and in CI (no model calls), incl. the eval on hand-written samples with planted flaws (all caught). Not claimed yet: Claude's eval pass rates
 # (the first live recording run is still to do).
 dict(n=12, badge='LLM evals', title='Testing an LLM Feature (Claude)', repo='llm-feature-testing', wf='ci.yml', wfname='CI',
      img='llm-evals', alt='Eval flow: golden set, assistant, deterministic checks, calibrated LLM judge, pass rate per tag', page='llm-feature-testing',
      report='docs/images/eval-flow.png',
      fact='32 hand-written eval cases in six areas, each run three times; prompt-injection and data-leak areas must pass 100%, and the LLM judge is only trusted after it agrees with hand-labelled answers.',
      text='An HR policy assistant on Claude and the harness that decides whether it can ship: structured replies, deterministic checks for facts, citations, a canary and colleagues\' data, a calibrated groundedness judge, pass rates per area, and 90 tests of the harness itself, including a run on hand-written answers with planted leaks that the harness must catch.',
      tags=['Java 21', 'Claude API', 'LLM evals', 'TestNG', 'GitHub Actions']),

 # Facts checked 17 Oct 2026: CI run 39007129438 green on all 4 jobs; 86 Playwright + 28 unit tests; 8 of 8 planted defects caught.
 dict(n=13, badge='Accessibility + visual', title='Accessibility and Visual Regression Testing', repo='accessibility-visual-testing', wf='ci.yml', wfname='CI',
      img='a11y-visual', alt='Screenshot diff: the planted spacing and button colour changes highlighted in red', page='accessibility-visual-testing',
      report='docs/images/visual-diff.png',
      fact='Eight realistic defects are planted in a regressed build of the app, and the suite must report each one with the check named for it: all eight are caught.',
      text='WCAG 2.2 AA checks with axe-core in light and dark mode and in every state, keyboard and focus tests for what axe cannot see, reflow and reduced motion, and 21 screenshot baselines rendered in the Playwright Linux image with zero pixel tolerance.',
      tags=['Playwright', 'TypeScript', 'axe-core', 'WCAG 2.2', 'Docker', 'GitHub Actions']),

 # Facts checked 17 Oct 2026: CI run 39034198614 green on all 4 jobs; hardened build: no FAIL/WARN alerts; 10 of 10 planted defects caught (7 by ZAP, 3 by API tests); 36 node:test tests.
 dict(n=14, badge='Security testing', title='Security Testing with OWASP ZAP', repo='security-testing-zap', wf='ci.yml', wfname='CI',
      img='zap-security', alt='ZAP verdict: hardened build clean, every planted vulnerability caught', page='security-testing-zap',
      report='docs/images/zap-verdict.png',
      fact='Ten vulnerabilities are planted in a second build of the app: ZAP catches the seven it can see, API tests catch the three access-control flaws no scanner can, and the hardened build must scan clean.',
      text='OWASP ZAP baseline and full scans of a hardened and a vulnerable build on a private Docker network, a rules file with FAIL/WARN/IGNORE decisions, a verdict job in CI, and API tests for IDOR, mass assignment and brute force.',
      tags=['OWASP ZAP', 'DAST', 'OWASP Top 10', 'Docker', 'TypeScript', 'GitHub Actions']),

 # Facts checked 17 Oct 2026: CI run 39044080833 green; 21 tests (18 against real PostgreSQL 18 + Kafka 4.1 containers, 3 unit tests), about 21 s of test time; two mutation checks.
 dict(n=15, badge='Integration testing', title='Integration Testing with Testcontainers (Kafka, GraphQL)', repo='integration-testing-testcontainers', wf='ci.yml', wfname='CI',
      img='testcontainers', alt='Overview of the integration tests: what each test class proves and how events are handled', page='integration-testing-testcontainers',
      report='docs/images/test-overview.png',
      fact='Every run starts real PostgreSQL and Kafka in Docker; the tests prove duplicate events are applied once and broken events reach the dead-letter topic without blocking the partition, with no sleeps anywhere.',
      text='An event-driven order service tested through its GraphQL API and Kafka topics: migrations on the real database, schema and validation errors, published events, idempotent consumption, retries and dead-letter handling, plus mutation checks of the tests themselves.',
      tags=['Java 21', 'Spring Boot', 'Testcontainers', 'Kafka', 'GraphQL', 'PostgreSQL']),

 # Facts checked 17 Oct 2026: BrowserStack runs: web 13/13 on iPhone 16 (iOS 18.6, Safari, 109 s) and Galaxy S24 (Android 14, Chrome, 79 s); native app 5/5 on iPhone 16 (54 s); CI run green (emulation); ~9.5 Automate + 1.3 App Automate minutes used.
 dict(n=16, badge='Real devices', title='Mobile Testing on Real Devices (BrowserStack)', repo='mobile-real-device-testing', wf='ci.yml', wfname='CI',
      img='real-devices', alt='Results table: web suite passed on a real iPhone and a real Android phone, native app suite passed on a real iPhone', page='mobile-real-device-testing',
      report='docs/images/real-device-results.png',
      fact='The same mobile web suite passed on Safari on a real iPhone and Chrome on a real Android phone, and the Android phone found a failure emulation never showed: with the keyboard open, the tap missed the checkout button.',
      text='A mobile-first shop tested with Selenium on real phones through BrowserStack Local (layout, touch targets, keyboards, iOS zoom, checkout), a native iOS app tested with Appium XCUITest on a real iPhone, all within a 100-minute trial.',
      tags=['BrowserStack', 'Real devices', 'Selenium', 'Appium', 'iOS', 'Android']),

 # Facts checked 26 Oct 2026 against release v1.2.0, main 4287e89 (CI run 40269471866 green, self gate 31/31 requirements;
 # deployment smoke 40269927960 green) and the live report: 23 repositories / 24 workflows / 59 jobs collected; 1,143
 # unit/integration/performance + 229 browser tests; live overview 3,905 latest results, 100 % pass rate (3,893/3,893),
 # 86 % automation coverage (sample catalog), 2 critical gaps, release readiness "at risk". Only the requirement catalog is synthetic; the executions are real CI results.
 dict(n=17, badge='Quality engineering', title='Automation Coverage & Quality Intelligence', repo='automation-coverage-quality-intelligence',
      wf='ci.yml', wfname='CI', img='quality-intelligence-report-2026-10-26',
      alt='Live Quality Intelligence report overview on 26 Oct 2026: 3,905 latest results from 23 repositories, execution pass rate 100 %, automation coverage 86 % of the synthetic sample catalog, two critical gaps, release readiness at risk',
      page='quality-intelligence', report='docs/images/gate-report-release.png',
      fact='Collects the CI results of 23 of my repositories every day and shows them as a live report: the latest result of every suite, pass rate per browser, failures grouped by cause, trends, and requirement coverage. Every figure opens the executions behind it, and a test opens the exact run that was clicked.',
      text='A platform on top of existing test automation, for release decisions: it reads the JUnit XML, mochawesome and Allure files the frameworks already write, keeps coverage and pass rate as separate documented metrics, classifies flaky tests with evidence, decides CI quality gates (0 passed, 1 failed, 3 incomplete, so missing results never pass) and explains release readiness row by row. The live report is checked after every deployment.',
      tags=['Python', 'FastAPI', 'SQLite', 'pydantic', 'Playwright', 'GitHub Actions']),
]

MORE = [
 # No CI: the app under test (Google Calculator) cannot be redistributed, so a CI machine has no APK.
 # Facts checked 13 Oct 2026: Android suite 1/1 on an Android 15 emulator with Appium 3.8; iOS not run (needs a Mac).
 dict(title='Mobile Framework (2021, upgraded for Android + iOS)', repo='mobile-test-automation-framework',
      report='docs/images/report-dashboard.png',
      text='My 2021 Appium + TestNG framework, upgraded in 2026 to Appium 3, Java client 11 and Selenium 4 without changing its design: '
           'one set of tests for Android and iOS through a platform layer, capabilities per platform in properties files, '
           'and a custom HTML report with failure screenshots. Runs green on an Android 15 emulator; the iOS side is ready but not yet run.',
      tags=['Java 17', 'Appium 3', 'TestNG', 'Selenium 4']),
 # No CI: tests run against the shared public OrangeHRM demo. Facts checked 13 Oct 2026: 4/4 on visible Chrome
 # and headless Chrome, Edge and Firefox; the logout test had failed since 2024 because of a missing @ in its XPath.
 dict(title='Selenium Page Object Framework (2024, upgraded)', repo='java-selenium-testng-pom-framework',
      report='docs/images/extent-tests.png',
      text='My January 2024 Selenium + TestNG page object framework for OrangeHRM, upgraded step by step in 2026: '
           'explicit waits instead of fixed sleeps, browser and headless mode from a config file, and an Extent report '
           'with a screenshot on every failure. The upgrade also fixed a locator bug that had failed the logout test since 2024.',
      tags=['Java', 'Selenium', 'TestNG', 'Maven']),
 # No CI: tests run against public practice sites. Facts checked 13 Oct 2026 (after the layer split, commit 5bc9fb8): 5/5 scenarios on visible Chrome and
 # headless Chrome, Edge and Firefox; the 2022 build no longer compiled (Java 1.7 target, mixed Cucumber versions).
 dict(title='Cucumber BDD Demo (2022, upgraded)', repo='cucumber-bdd-demo',
      report='docs/images/report-passing.png',
      text='My first Cucumber project from 2022, which no longer built, brought to Java 17, Cucumber 8 (JUnit Platform '
           'runners) and Selenium 4 step by step, then split into layers: runners, step definitions, page objects, hooks '
           'and utils. Hooks attach a screenshot on failure, and a Scenario Outline that used to pass without checking '
           'anything now asserts each row.',
      tags=['Java 17', 'Cucumber 8', 'Selenium 4', 'JUnit']),
 dict(title='Selenium Java Interview Lab', repo='selenium-java-framework', wf='tests.yml', report='docs/images/html-report.png',
      text='148 runnable tests, one per Selenium, TestNG and framework-design topic, plus a PDF of 100+ interview questions.',
      tags=['Java', 'Selenium', 'TestNG']),
 dict(title='Cucumber BDD Framework', repo='cucumber-java-framework', wf='tests.yml', report='docs/images/html-report.png',
      text='8 BDD scenarios with Cucumber, Selenium 4 and JUnit, and a custom self-contained HTML report.',
      tags=['Java', 'Cucumber', 'Selenium', 'JUnit']),
 dict(title='REST API Automation', repo='api-automation', wf='tests.yml', report='docs/images/html-report.png', page='rest-api',
      text='A layered REST Assured framework (one manager per API resource) with one end-to-end scenario and a custom HTML report.',
      tags=['Java', 'REST Assured', 'TestNG']),
 dict(title='API Framework (2024 version)', repo='api-automation-framework', wf='tests.yml', report='docs/images/allure-report.png',
      text='An earlier REST Assured framework with Extent, Allure and custom TestNG reports on the same suite.',
      tags=['Java', 'REST Assured', 'TestNG', 'Allure']),
 dict(title='JSONPlaceholder API Tests', repo='jsonplaceholder-auto', wf='tests.yml', report='docs/images/extent-report.png',
      text='The original version of the API framework, kept to show how it evolved; Hamcrest matchers and an Extent report.',
      tags=['Java', 'REST Assured', 'Hamcrest', 'TestNG']),
]

# Categories are deliberately constrained to the public Projects page filters.
CATEGORY_BY_REPO = {
    'enterprise-test-automation-framework': ['Web & API', 'CI/CD'],
    'playwright-typescript-framework': ['Web & API'],
    'playwright-framework': ['Web & API'],
    'appium-framework': ['Mobile'],
    'robot-framework-automation': ['Web & API', 'CI/CD'],
    'python-pytest-framework': ['Web & API'],
    'k6-performance-testing': ['Performance'],
    'cypress-typescript-framework': ['Web & API'],
    'pact-contract-testing': ['Web & API', 'CI/CD'],
    'jenkins-kubernetes-pipeline': ['CI/CD'],
    'ai-assisted-test-automation': ['AI & LLM'],
    'llm-feature-testing': ['AI & LLM'],
    'accessibility-visual-testing': ['Accessibility'],
    'security-testing-zap': ['Security'],
    'integration-testing-testcontainers': ['Web & API'],
    'mobile-real-device-testing': ['Mobile'],
    'automation-coverage-quality-intelligence': ['Quality Intelligence'],
    'mobile-test-automation-framework': ['Mobile', 'Learning Labs'],
    'java-selenium-testng-pom-framework': ['Web & API', 'Learning Labs'],
    'cucumber-bdd-demo': ['Web & API', 'Learning Labs'],
    'selenium-java-framework': ['Learning Labs'],
    'cucumber-java-framework': ['Web & API', 'Learning Labs'],
    'api-automation': ['Web & API', 'Learning Labs'],
    'api-automation-framework': ['Web & API', 'Learning Labs'],
    'jsonplaceholder-auto': ['Web & API', 'Learning Labs'],
}

IMAGE_BY_REPO = {
    'mobile-test-automation-framework': 'real-devices',
    'java-selenium-testng-pom-framework': 'selenium',
    'cucumber-bdd-demo': 'cucumber',
    'selenium-java-framework': 'selenium',
    'cucumber-java-framework': 'cucumber',
    'api-automation': 'api',
    'api-automation-framework': 'api-2024',
    'jsonplaceholder-auto': 'jsonplaceholder',
}

EVIDENCE_BY_REPO = {
    'enterprise-test-automation-framework': {
        'date': '2026-10-21',
        'url': 'https://github.com/niranjankagri/enterprise-test-automation-framework/actions/runs/39553795238',
        'label': 'Nightly regression #30 on main',
        'result': '21 Oct 2026 nightly execution results: Chrome 233/233 passed; Firefox, Edge and Selenium Grid each 174/174 passed; 0 failures, errors or skips.',
        'result_kind': 'Historical workflow run · verified 21 Oct 2026',
    },
    'playwright-typescript-framework': {
        'date': '2026-10-20',
        'url': 'https://github.com/niranjankagri/playwright-typescript-framework/actions/workflows/ci.yml',
        'label': 'CI workflow (latest successful run: 20 Oct 2026)',
    },
    'playwright-framework': {
        'date': '2026-10-20',
        'url': 'https://github.com/niranjankagri/playwright-framework/actions/workflows/tests.yml',
        'label': 'CI workflow and README test matrix',
    },
    'appium-framework': {
        'date': '2026-10-20',
        'url': 'https://github.com/niranjankagri/appium-framework/actions/runs/39489105200',
        'label': 'Android 15 emulator workflow run #7',
        'result': 'Run #7 passed all 40 Android 15 emulator test executions. The repository has 40 TestNG methods and preserves three demo-app defects as known-bug checks.',
        'result_kind': 'Historical Android emulator workflow run',
    },
    'robot-framework-automation': {
        'date': '2026-10-19',
        'url': 'https://github.com/niranjankagri/robot-framework-automation/actions/workflows/ci.yml',
        'label': 'CI workflow and README test matrix',
    },
    'python-pytest-framework': {
        'date': '2026-10-19',
        'url': 'https://github.com/niranjankagri/python-pytest-framework/actions/workflows/ci.yml',
        'label': 'CI workflow and README test matrix',
    },
    'k6-performance-testing': {
        'date': '2026-10-20',
        'url': 'https://github.com/niranjankagri/k6-performance-testing/actions/runs/39490025975',
        'label': 'Performance workflow run #26',
        'result_kind': 'Historical performance workflow run',
    },
    'cypress-typescript-framework': {
        'date': '2026-10-20',
        'url': 'https://github.com/niranjankagri/cypress-typescript-framework/actions/runs/39403537526',
        'label': 'CI run #12 on main',
        'result': 'The repository has 81 unique Cypress test cases (31 API, 33 UI and 17 component) plus 15 Node unit tests. The static report shows 64 passing API and UI executions; component and Node results are separate.',
        'alt': 'Static Cypress report screenshot of one API and UI run: 64 test executions passed; component executions are separate',
        'result_kind': 'Static report image and dated repository test inventory',
    },
    'pact-contract-testing': {
        'date': '2026-10-16',
        'url': 'https://github.com/niranjankagri/pact-contract-testing/actions/workflows/contract.yml',
        'label': 'Contract workflow and README evidence',
    },
    'jenkins-kubernetes-pipeline': {
        'date': '2026-10-16',
        'url': 'https://github.com/niranjankagri/jenkins-kubernetes-pipeline/actions/workflows/ci.yml',
        'label': 'CI workflow and README evidence',
    },
    'ai-assisted-test-automation': {
        'date': '2026-10-20',
        'url': 'https://github.com/niranjankagri/ai-assisted-test-automation/actions/runs/39489161371',
        'label': 'CI run #16 (hand-written sample answers)',
        'result': 'CI passed on labelled, hand-written sample answers; no live model result is claimed.',
        'result_kind': 'Recorded CI replay',
    },
    'llm-feature-testing': {
        'date': '2026-10-20',
        'url': 'https://github.com/niranjankagri/llm-feature-testing/actions/runs/39489149450',
        'label': 'CI run #12 (hand-written sample answers)',
        'result': 'CI replayed hand-written samples with planted flaws; no live model result is claimed.',
        'result_kind': 'Recorded CI replay',
    },
    'accessibility-visual-testing': {
        'date': '2026-10-17',
        'url': 'https://github.com/niranjankagri/accessibility-visual-testing/actions/runs/39007129438',
        'label': 'CI run #1 on main',
    },
    'security-testing-zap': {
        'date': '2026-10-17',
        'url': 'https://github.com/niranjankagri/security-testing-zap/actions/runs/39034198614',
        'label': 'CI run #1 on main',
    },
    'integration-testing-testcontainers': {
        'date': '2026-10-17',
        'url': 'https://github.com/niranjankagri/integration-testing-testcontainers/actions/runs/39044080833',
        'label': 'CI run on main',
    },
    'mobile-real-device-testing': {
        'date': '2026-10-17',
        'url': 'https://github.com/niranjankagri/mobile-real-device-testing/actions/workflows/ci.yml',
        'label': 'Real-device evidence and CI workflow',
    },
    'automation-coverage-quality-intelligence': {
        'date': '2026-10-26',
        'url': 'https://github.com/niranjankagri/automation-coverage-quality-intelligence/actions/runs/40269927960',
        'label': 'Deployment smoke check of the live report',
        'result': 'Deployment smoke check passed on 26 Oct 2026 for release v1.2.0: the live report runs the latest commit, its sections, filters and drill-downs work in Chromium, and its figures match the API. It shows daily collected results from 23 public repositories and 59 workflow jobs; the requirement catalog is synthetic.',
        'result_kind': 'Deployment smoke check plus real collected CI history and synthetic requirement catalogue',
        'alt': 'Screenshot of the live Quality Intelligence report on 26 Oct 2026: 3,905 latest results, 100 percent execution pass rate, 86 percent automation coverage of the synthetic sample catalog, two critical gaps and release readiness at risk',
        'description': 'A quality engineering platform that collects daily CI results from 23 public repositories and 59 workflow jobs and presents them as a live report: overview, test results, failures and stability, trends, and coverage of a synthetic requirement catalog, with release gates and a readiness scorecard. The original dashboard remains available.',
    },
    'mobile-test-automation-framework': {
        'date': '2026-10-13',
        'url': 'https://github.com/niranjankagri/mobile-test-automation-framework',
        'label': 'Repository evidence (manual run)',
        'result': 'Android 15 emulator check: 1/1 passed. The iOS side is documented but has not been run.',
    },
    'java-selenium-testng-pom-framework': {
        'date': '2026-10-13',
        'url': 'https://github.com/niranjankagri/java-selenium-testng-pom-framework',
        'label': 'Repository evidence (manual run)',
        'result': 'Four smoke checks passed across Chrome, Edge and Firefox; no automated CI workflow is configured.',
    },
    'cucumber-bdd-demo': {
        'date': '2026-10-13',
        'url': 'https://github.com/niranjankagri/cucumber-bdd-demo',
        'label': 'Repository evidence (manual run)',
        'result': 'Five scenarios passed across Chrome, Edge and Firefox; no automated CI workflow is configured.',
    },
    'selenium-java-framework': {
        'date': '2026-10-06',
        'url': 'https://github.com/niranjankagri/selenium-java-framework',
        'label': 'Frozen learning lab',
        'result': 'A frozen interview lab with runnable Selenium, TestNG and framework-design examples plus a question guide.',
    },
    'cucumber-java-framework': {
        'date': '2026-10-10',
        'url': 'https://github.com/niranjankagri/cucumber-java-framework/actions/workflows/tests.yml',
        'label': 'Latest CI workflow',
        'result': 'Eight BDD scenarios with Cucumber and Selenium, with a self-contained HTML report.',
    },
    'api-automation': {
        'date': '2026-10-10',
        'url': 'https://github.com/niranjankagri/api-automation/actions/workflows/tests.yml',
        'label': 'Latest CI workflow',
        'result': 'One end-to-end scenario traverses the user, posts and comments APIs; the repository is a learning example, not broad API coverage.',
    },
    'api-automation-framework': {
        'date': '2026-10-10',
        'url': 'https://github.com/niranjankagri/api-automation-framework/actions/workflows/tests.yml',
        'label': 'Latest CI workflow',
        'result': 'An earlier layered API framework retained to show its evolution across Extent, Allure and custom TestNG reports.',
    },
    'jsonplaceholder-auto': {
        'date': '2026-10-10',
        'url': 'https://github.com/niranjankagri/jsonplaceholder-auto/actions/workflows/tests.yml',
        'label': 'Latest CI workflow',
        'result': 'The original API automation example retained as a learning lab; it uses Hamcrest matchers and an Extent report.',
    },
}

FEATURED_ORDER = (
    'enterprise-test-automation-framework',
    'playwright-typescript-framework',
    'automation-coverage-quality-intelligence',
    'appium-framework',
    'k6-performance-testing',
    'ai-assisted-test-automation',
)
FEATURED_IDS = set(FEATURED_ORDER)

LIVE_DASHBOARD = 'https://quality-intelligence-0ur1.onrender.com'
# Headline figures of the live report, read from its API (/api/report/overview, /api/summary,
# /api/readiness) on 24 Oct 2026. A dated snapshot: the live report changes every day.
QI_REPORT_SNAPSHOT = {
    'date': '2026-10-26',
    'repositories': 23,
    'results': 3905,
    'tiles': [
        ('passed', 'Execution pass rate', '100%', '3,893 of 3,893 verdicts passed; 12 skipped not counted', '#/results'),
        ('accent', 'Automation coverage', '86%', '37 of 43 test cases in the synthetic sample catalog automated', '#/coverage'),
        ('failed', 'Critical gaps', '2', 'critical requirements without an automated test', '#/coverage?show=gaps'),
        ('warning', 'Release readiness', 'At risk', 'gate passed; 3 flaky candidates and 3 incomplete collections in 7 days', '#/overview?panel=readiness'),
    ],
}
PROJECTS_URL = 'https://niranjankagri.github.io/projects.html'

# Role views highlight work without removing any item from the project collection.
ROLE_VIEWS = {
    'senior-sdet': {
        'label': 'Senior SDET',
        'summary': 'Hands-on framework engineering across API, browser, mobile, performance and quality tooling.',
        'skills': ['Framework design', 'API testing', 'Browser automation', 'Test data isolation', 'CI evidence'],
        'projects': ['enterprise-test-automation-framework', 'playwright-typescript-framework',
                     'playwright-framework', 'python-pytest-framework', 'appium-framework',
                     'k6-performance-testing'],
        'impact': '12+ years across software engineering and QA, including automation of 84% of one regulated product release test scope.',
    },
    'qa-lead': {
        'label': 'QA Lead',
        'summary': 'Team leadership, test strategy, traceability, defect triage and evidence-based release sign-off.',
        'skills': ['Test strategy', 'Requirements traceability', 'Release readiness', 'Team leadership', 'Risk evidence'],
        'projects': ['automation-coverage-quality-intelligence', 'enterprise-test-automation-framework',
                     'robot-framework-automation', 'k6-performance-testing', 'mobile-real-device-testing'],
        'impact': 'Led and mentored four QA engineers and owned test strategy, traceability, defect triage and release sign-off.',
    },
    'automation-architect': {
        'label': 'Automation Architect',
        'summary': 'Layered test platforms, reusable interfaces, parallel execution, CI gates and actionable reporting.',
        'skills': ['Layered architecture', 'Parallel execution', 'CI/CD', 'Reporting', 'Contract testing'],
        'projects': ['enterprise-test-automation-framework', 'automation-coverage-quality-intelligence',
                     'playwright-typescript-framework', 'pact-contract-testing', 'jenkins-kubernetes-pipeline'],
        'impact': 'Portfolio examples document framework boundaries, execution tradeoffs and the evidence each automation layer produces.',
    },
}

# Problem-led paths reuse the same project records as cards, comparison and case studies.
EXPLORATION_FOCUSES = {
    'maintainable-automation': {
        'label': 'Build maintainable automation',
        'summary': 'Compare layered frameworks, reusable page objects, typed API clients and test-owned data.',
        'experience': 'Built a hybrid Selenium WebDriver framework and progressed through software engineering and architecture roles at bebo Technologies.',
        'projects': ['enterprise-test-automation-framework', 'playwright-typescript-framework',
                     'playwright-framework', 'python-pytest-framework', 'cypress-typescript-framework'],
    },
    'release-quality': {
        'label': 'Investigate release quality',
        'summary': 'Trace requirements to tests, inspect execution evidence and see how incomplete or failed gates are reported.',
        'experience': 'Lead a four-person QA team and own test strategy, requirements traceability, defect triage and release sign-off.',
        'projects': ['automation-coverage-quality-intelligence', 'enterprise-test-automation-framework',
                     'robot-framework-automation', 'integration-testing-testcontainers'],
    },
    'browser-device-testing': {
        'label': 'Test across browsers and devices',
        'summary': 'Explore cross-engine web checks, responsive behavior, Android automation and real-device coverage.',
        'experience': 'Built browser automation across Selenium and Playwright; mobile and device projects in this portfolio are identified as demonstrations.',
        'projects': ['playwright-typescript-framework', 'playwright-framework', 'python-pytest-framework',
                     'appium-framework', 'mobile-real-device-testing', 'mobile-test-automation-framework'],
    },
    'performance-bottlenecks': {
        'label': 'Find performance bottlenecks',
        'summary': 'Inspect workload models, latency thresholds, load evidence and the limits of a demo-shop measurement.',
        'experience': 'Designed rfswarm benchmarks with real browser sessions, up to 135 concurrent users and 1,400+ seeded accounts; used them to flag response-time drift of 10% or more.',
        'projects': ['k6-performance-testing', 'enterprise-test-automation-framework'],
    },
    'ai-testing': {
        'label': 'Evaluate AI-assisted testing',
        'summary': 'Review test-generation and evaluation harnesses, including sample and replay evidence without live-model claims.',
        'experience': 'Use Claude for test design and test-data suggestions with human review; portfolio CI examples label hand-written samples and replay runs.',
        'projects': ['ai-assisted-test-automation', 'llm-feature-testing'],
    },
    'qa-strategy': {
        'label': 'Lead QA strategy',
        'summary': 'See how team leadership, traceability, risk-based coverage and evidence support release decisions.',
        'experience': 'Led and mentored four QA engineers and owned test strategy, requirements traceability, defect triage and release sign-off.',
        'projects': ['automation-coverage-quality-intelligence', 'enterprise-test-automation-framework',
                     'robot-framework-automation', 'k6-performance-testing', 'mobile-real-device-testing'],
    },
}

# Project-card reporting links are static examples; labels identify their format without
# implying that the screenshot is a live report or a current run.
REPORT_LABELS = {
    'enterprise-test-automation-framework': 'Allure report overview screenshot',
    'playwright-typescript-framework': 'Playwright HTML report overview screenshot',
    'playwright-framework': 'Playwright test report screenshot',
    'appium-framework': 'Custom HTML test report screenshot',
    'robot-framework-automation': 'Robot Framework execution report screenshot',
    'python-pytest-framework': 'pytest and Playwright report screenshot',
    'k6-performance-testing': 'k6 performance dashboard screenshot',
    'cypress-typescript-framework': 'Mochawesome HTML report screenshot',
    'pact-contract-testing': 'Pact verification evidence screenshot',
    'jenkins-kubernetes-pipeline': 'Jenkins pipeline evidence screenshot',
    'ai-assisted-test-automation': 'Test-generation pipeline diagram',
    'llm-feature-testing': 'LLM evaluation report screenshot',
    'accessibility-visual-testing': 'Accessibility and visual-diff report screenshot',
    'security-testing-zap': 'OWASP ZAP scan report screenshot',
    'integration-testing-testcontainers': 'Integration test report screenshot',
    'mobile-real-device-testing': 'Real-device execution evidence screenshot',
    'automation-coverage-quality-intelligence': 'Live report screenshot',
    'mobile-test-automation-framework': 'Android test report screenshot',
    'java-selenium-testng-pom-framework': 'Selenium and TestNG report screenshot',
    'cucumber-bdd-demo': 'Cucumber execution report screenshot',
    'selenium-java-framework': 'Selenium interview-lab report screenshot',
    'cucumber-java-framework': 'Cucumber HTML report screenshot',
    'api-automation': 'Custom API test report screenshot',
    'api-automation-framework': 'API report-format comparison screenshot',
    'jsonplaceholder-auto': 'Extent API report screenshot',
}

# Concise, evidence-backed comparison facts used by the explorer. Rows deliberately
# say when a browser matrix is not part of the project (for example, API-only work).
COMPARISON_DETAILS = {
    'enterprise-test-automation-framework': ('UI, API, database, integration, end-to-end and unit tests', 'Chrome, Firefox, Edge and Docker Selenium Grid', 'Test-owned data, infrastructure-only retries, Allure evidence'),
    'playwright-typescript-framework': ('UI, API and network tests', 'Chromium, Firefox and WebKit', 'API login per test, zod response contracts, per-worker users'),
    'playwright-framework': ('UI, API and network tests', 'Chromium, Firefox and WebKit', 'Browser per thread, context per test, failure traces and videos'),
    'appium-framework': ('Android UI and device behavior', 'Android 15 emulator', 'Screen objects, state-aware waits, infrastructure-specific retries'),
    'robot-framework-automation': ('Browser UI and API tests', 'Chrome and Firefox', 'Robot resource page objects, API service objects, parallel pabot runs'),
    'python-pytest-framework': ('API, UI and hybrid API + UI tests', 'Chromium, Firefox and WebKit in CI', 'Typed API contracts, API login, per-test users'),
    'k6-performance-testing': ('HTTP smoke, load, stress, spike and soak tests', 'HTTP workload; no browser matrix', 'Endpoint SLO thresholds and open/closed workload models'),
    'cypress-typescript-framework': ('API, UI and component tests', 'Chrome, Firefox and Edge in CI', 'Network control, component mounting and zod contracts'),
    'pact-contract-testing': ('Consumer/provider contract verification', 'No browser matrix; TypeScript consumer and Java provider', 'Pact V4 states, broker verification and can-i-deploy'),
    'jenkins-kubernetes-pipeline': ('Pipeline smoke and API tests', 'kind Kubernetes cluster', 'Jenkins configured as code, isolated namespace per build, quality gate'),
    'ai-assisted-test-automation': ('Test-generation and triage harness; generated Playwright tests', 'CI replays hand-written samples; no live model result claimed', 'Rules, compilation and repeated-run gate before human review'),
    'llm-feature-testing': ('LLM evaluation harness and deterministic safety checks', 'CI replays hand-written samples; no live model result claimed', 'Calibrated judge beside deterministic checks; sensitive areas have explicit gates'),
    'accessibility-visual-testing': ('Accessibility, keyboard/focus and visual regression checks', 'Playwright browser matrix; see workflow evidence', 'axe-core plus checks axe cannot cover and zero-tolerance image comparisons'),
    'security-testing-zap': ('DAST scans and API access-control tests', 'Docker private network', 'Separate scanner findings from API-only authorization checks'),
    'integration-testing-testcontainers': ('GraphQL, database and Kafka integration tests', 'PostgreSQL and Kafka containers', 'Real service dependencies, idempotency and dead-letter assertions'),
    'mobile-real-device-testing': ('Mobile web and native iOS tests', 'Real iPhone, Galaxy S24 and mobile emulation', 'Device minutes reserved for checks emulation cannot establish'),
    'automation-coverage-quality-intelligence': ('CLI, ingestion, traceability, history, gates, report and dashboard browser tests', 'Chromium, Firefox and WebKit browser tests; daily CI artifacts from 23 repositories', 'Typed common result model, SQLite history, incomplete gate exit code'),
    'mobile-test-automation-framework': ('Android run; iOS implementation documented but not run', 'Android 15 emulator', 'Platform layer with per-platform capabilities'),
    'java-selenium-testng-pom-framework': ('UI smoke checks', 'Chrome, Edge and Firefox (manual run)', 'Page objects, explicit waits and configurable headless execution'),
    'cucumber-bdd-demo': ('BDD UI scenarios', 'Chrome, Edge and Firefox (manual run)', 'Cucumber runners and separated framework layers'),
    'selenium-java-framework': ('Selenium and TestNG interview examples', 'See repository guide; no current browser matrix recorded', 'One runnable example per framework-design topic'),
    'cucumber-java-framework': ('BDD UI scenarios', 'See linked CI workflow evidence', 'Cucumber scenarios with a self-contained HTML report'),
    'api-automation': ('REST API end-to-end scenario', 'HTTP API; no browser matrix', 'One manager per API resource and a custom HTML report'),
    'api-automation-framework': ('REST API checks', 'HTTP API; no browser matrix', 'Same suite retained across Extent, Allure and custom TestNG reports'),
    'jsonplaceholder-auto': ('REST API checks', 'HTTP API; no browser matrix', 'Original API example with Hamcrest matchers and Extent report'),
}

COMPARISON_LIMITATIONS = {
    'enterprise-test-automation-framework': 'The demo application uses an in-memory H2 database and demo-grade security; it is not a production deployment.',
    'playwright-typescript-framework': 'The shared public demo shop can change or be unavailable; two form-login UI checks are skipped in CI when its bot check blocks them.',
    'playwright-framework': 'Evidence describes the public portfolio repository and its linked CI runs, not customer production impact.',
    'appium-framework': 'The verified run uses an Android emulator and a demo application; no real-device result is claimed.',
    'k6-performance-testing': 'The measured limit and load-shedding result apply to the repository demo shop and the linked stress-test profile.',
    'ai-assisted-test-automation': 'CI replays hand-written sample answers; no live model output or model-quality score is claimed.',
    'automation-coverage-quality-intelligence': 'The requirement catalog is synthetic; collected CI results are real. The shared dashboard account is documented in the case study.',
    'llm-feature-testing': 'CI uses hand-written examples with planted flaws; no live model pass rate is claimed.',
    'mobile-real-device-testing': 'The device matrix covers one iPhone and one Android phone; it is not a representative customer device matrix.',
}

ARCHITECTURE_PREVIEWS = {
    'enterprise-test-automation-framework': ('img/enterprise-architecture.svg', 'Architecture diagram of TestNG suites, framework layers, browsers, the demo shop, API, database and Allure evidence.'),
    'automation-coverage-quality-intelligence': ('https://raw.githubusercontent.com/niranjankagri/automation-coverage-quality-intelligence/main/docs/images/data-flow.svg', 'Architecture diagram showing result ingestion, traceability, history, gates and the dashboard.'),
}

CARD_PURPOSE = {
    'enterprise-test-automation-framework': 'One demo shop tested through browser, API, database and integration layers.',
    'playwright-typescript-framework': 'Typed UI and API checks for a shared demo shop across three browser engines.',
    'automation-coverage-quality-intelligence': 'A live report of daily CI results from 23 repositories, with coverage and release gates.',
    'appium-framework': 'Android checks with device-aware waits and preserved failure evidence.',
    'k6-performance-testing': 'Shop API load tests with endpoint service-level thresholds.',
    'ai-assisted-test-automation': 'A human-reviewed pipeline for drafting and triaging Playwright tests.',
}

# Captions describe the thumbnail itself, not the separately linked verification
# record. Unknown screenshot dates are stated explicitly rather than inferred.
FEATURED_PREVIEW_CAPTIONS = {
    'enterprise-test-automation-framework': ('Historical report', '7 Oct 2026 · separate local run; not the nightly evidence linked below.'),
    'playwright-typescript-framework': ('Playwright HTML report', 'Static screenshot from 10 Oct 2026; CI evidence checked 20 Oct 2026.'),
    'automation-coverage-quality-intelligence': ('Live report screenshot', 'Captured 24 Oct 2026 from the live report; the requirement catalog is synthetic.'),
    'appium-framework': ('Android test report', 'Historical emulator run from 12 Oct 2026; workflow checked 20 Oct 2026.'),
    'k6-performance-testing': ('k6 dashboard screenshot', 'Demo-shop stress run from 13 Oct 2026; scope is the linked workload profile.'),
    'ai-assisted-test-automation': ('Pipeline architecture diagram', 'Static architecture diagram; capture date unknown.'),
}

CARD_RESULTS = {
    'enterprise-test-automation-framework': '21 Oct 2026: 755 test executions passed (Chrome 233; Firefox, Edge and Selenium Grid 174 each).',
    'playwright-typescript-framework': '47 unique tests; 95 test executions per run across Chromium, Firefox and WebKit.',
    'automation-coverage-quality-intelligence': 'Deployment smoke passed 24 Oct 2026; the live report covers 23 public repositories.',
    'appium-framework': 'Run #7 passed 40 Android 15 emulator test executions; the repository has 40 TestNG methods and three known-bug checks.',
    'k6-performance-testing': 'Above ~90 orders/s checkout exceeded 3 s p95; after load shedding it stayed below 650 ms in the same profile.',
    'ai-assisted-test-automation': 'CI replayed hand-written samples; no live model result is claimed.',
}


def normalise_project(source):
    """Return one complete record for page, card, evidence, and filter generation."""
    project = dict(source)
    repo = project['repo']
    evidence = EVIDENCE_BY_REPO.get(repo, {})
    page_slug = project.get('page') or repo
    image = project.get('img') or IMAGE_BY_REPO.get(repo, 'api')
    description = evidence.get('description') or project.get('text') or 'Project history and setup are available in the repository README.'
    result = evidence.get('result') or project.get('fact') or description
    workflow_url = f'https://github.com/niranjankagri/{repo}/actions/workflows/{project["wf"]}' if project.get('wf') else ''
    evidence_date = evidence.get('date', '')
    result_kind = evidence.get('result_kind', 'Historical repository or workflow evidence')
    if evidence_date:
        try:
            if (date.today() - date.fromisoformat(evidence_date)).days > 30:
                result_kind += ' · older evidence; recheck the linked source'
        except ValueError:
            pass
    original_text = project.get('text') or description
    short_purpose = CARD_PURPOSE.get(repo) or original_text.split('. ', 1)[0].rstrip('.')
    if len(short_purpose) > 145:
        short_purpose = short_purpose[:142].rsplit(' ', 1)[0].rstrip(' ,;:') + '…'
    comparison = COMPARISON_DETAILS[repo]
    roles = [role_id for role_id, role in ROLE_VIEWS.items() if repo in role['projects']]
    architecture_preview = ARCHITECTURE_PREVIEWS.get(repo, ('', ''))
    return {
        **project,
        'id': repo,
        'page': page_slug,
        'title': project['title'],
        'category': CATEGORY_BY_REPO[repo],
        'technologies': project.get('tags', []),
        'description': description,
        'short_purpose': short_purpose,
        'result': result,
        'card_result': CARD_RESULTS.get(repo, result),
        'result_kind': result_kind,
        'image': image,
        'preview_caption': FEATURED_PREVIEW_CAPTIONS.get(repo, ''),
        'alt': evidence.get('alt') or project.get('alt') or f'{project["title"]} project evidence',
        'evidence_date': evidence_date,
        'evidence_url': evidence.get('url') or f'https://github.com/niranjankagri/{repo}#readme',
        'evidence_label': evidence.get('label', 'Repository documentation and workflow records'),
        'workflow_url': workflow_url,
        'workflow_file': project.get('wf', ''),
        'workflow_name': project.get('wfname') or ('GitHub Actions workflow' if project.get('wf') else 'No automated workflow'),
        'source_url': f'https://github.com/niranjankagri/{repo}',
        'readme_url': f'https://github.com/niranjankagri/{repo}#readme',
        'report_url': f'https://github.com/niranjankagri/{repo}/blob/main/{project.get("report", "README.md")}',
        'report_label': REPORT_LABELS.get(repo, 'Static project evidence image'),
        'live_demo': LIVE_DASHBOARD if repo == 'automation-coverage-quality-intelligence' else '',
        'featured': repo in FEATURED_IDS,
        'project_kind': 'Featured project' if repo in FEATURED_IDS else ('Learning lab' if 'Learning Labs' in CATEGORY_BY_REPO[repo] else 'Project'),
        'roles': roles,
        'focuses': [focus_id for focus_id, focus in EXPLORATION_FOCUSES.items() if repo in focus['projects']],
        'comparison_layers': comparison[0],
        'comparison_targets': comparison[1],
        'comparison_approach': comparison[2],
        'comparison_limits': COMPARISON_LIMITATIONS.get(
            repo, 'The evidence is limited to the public repository and linked run; it does not establish customer production impact.'),
        'architecture_preview': architecture_preview[0],
        'architecture_preview_alt': architecture_preview[1],
    }


PROJECTS = [normalise_project(p) for p in [*FEATURED, *MORE]]
PROJECT_BY_ID = {p['id']: p for p in PROJECTS}
PROJECT_BY_PAGE = {p['page']: p for p in PROJECTS}
FEATURED_PROJECTS = [PROJECT_BY_ID[project_id] for project_id in FEATURED_ORDER]
