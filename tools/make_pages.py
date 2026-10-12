# Generates the project pages (projects/*.html) from one template. Run: python tools/make_pages.py
# Every project fact comes from that project's own README or CI runs.
import html
import os

# Repository root (this file lives in tools/)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'projects')
GH = 'https://github.com/niranjankagri/'
e = html.escape


def ul(items):
    return '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


def table(rows, head):
    h = ''.join(f'<th scope="col">{c}</th>' for c in head)
    b = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="table-wrap"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def page(p):
    repo = GH + p['repo']
    sections = [
        ('purpose', 'Purpose', p['purpose']),
        ('stack', 'Technology stack', table(p['stack'], ['Area', 'Tools'])),
        ('architecture', 'Architecture overview', p['architecture']),
        *p.get('extra', []),
        ('decisions', 'Key engineering decisions', ul(p['decisions'])),
        ('features', 'Implemented features', ul(p['features'])),
        ('run', 'Setup and execution', p['run']),
        ('results', 'Sample test results', p['results']),
        ('ci', 'CI workflow', p['ci']),
        ('limitations', 'Known limitations and future improvements',
         '<h3>Limitations</h3>' + ul(p['limits']) + '<h3>Next steps</h3>' + ul(p['next'])),
    ]
    body = ''.join(f'<section aria-labelledby="{i}"><h2 id="{i}">{t}</h2>{c}</section>' for i, t, c in sections)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p['title'])} · Niranjan Kumar Agri</title>
<meta name="description" content="{e(p['summary'])}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%234f43d6'/%3E%3Ctext x='32' y='42' font-family='Segoe UI,Arial' font-size='28' font-weight='700' fill='white' text-anchor='middle'%3ENA%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="../style.css">
<script>try{{var t=localStorage.getItem('na-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav">
  <div class="wrap">
    <a class="home" href="../"><picture><source srcset="../img/avatar-2026-10c.webp" type="image/webp"><img class="avatar" src="../img/avatar-2026-10c.jpg" alt="" width="40" height="40"></picture>Niranjan Kumar Agri</a>
    <nav aria-label="Sections"><a href="../#projects">Projects</a><a href="../#experience">Experience</a><a href="../#contact">Contact</a></nav>
    <button class="theme" id="theme" type="button" aria-label="Switch between light and dark mode">◐</button>
  </div>
</header>
<main id="main" class="wrap page">
  <p class="crumbs"><a href="../#projects">← All projects</a></p>
  <p class="eyebrow">{e(p['eyebrow'])}</p>
  <h1>{e(p['title'])}</h1>
  <p class="lead">{e(p['summary'])}</p>
  <p><a href="{repo}/actions/workflows/{p['workflow']}" aria-label="Live CI status on GitHub Actions"><img class="ci" width="150" height="20" src="{repo}/actions/workflows/{p['workflow']}/badge.svg" alt="Live CI status of {e(p['title'])}"></a></p>
  <div class="btns" style="margin:18px 0 26px">
    <a class="btn primary" href="{repo}" target="_blank" rel="noopener">View source code</a>
    <a class="btn" href="{repo}#readme" target="_blank" rel="noopener">View documentation</a>
    <a class="btn" href="{repo}/actions/workflows/{p['workflow']}" target="_blank" rel="noopener">View latest CI runs</a>
    <a class="btn" href="{repo}/blob/main/{p['report']}" target="_blank" rel="noopener">View test report</a>
  </div>
  {body}
</main>
<footer>© 2026 Niranjan Kumar Agri · <a href="../">Portfolio home</a></footer>
<script src="../theme.js"></script>
</body>
</html>
'''


def fig(src, alt, caption):
    return f'<figure><img src="{src}" alt="{e(alt)}" loading="lazy"><figcaption>{caption}</figcaption></figure>'


ENTERPRISE_SVG = '''<div class="diagram" role="img" aria-label="Architecture: tests use pages, API services and database queries, which use components, an API client and a query executor, which use the driver and configuration; the browsers run locally or on Selenium Grid and drive the ShopEase UI; the API client calls the ShopEase API; the query executor reads the database; tests write evidence into the Allure report.">
<svg viewBox="0 0 760 330" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="150" height="46" rx="10"/><text x="95" y="48" text-anchor="middle">Tests (TestNG)</text>
  <rect x="20" y="96" width="150" height="62" rx="10"/><text x="95" y="122" text-anchor="middle">Pages · API services</text><text x="95" y="142" text-anchor="middle">· DB queries</text>
  <rect x="20" y="188" width="150" height="62" rx="10"/><text x="95" y="214" text-anchor="middle">Components · ApiClient</text><text x="95" y="234" text-anchor="middle">· QueryExecutor · Waits</text>
  <rect x="20" y="268" width="150" height="46" rx="10"/><text x="95" y="296" text-anchor="middle">Driver · Config</text>
  <line x1="95" y1="66" x2="95" y2="96"/><line x1="95" y1="158" x2="95" y2="188"/><line x1="95" y1="250" x2="95" y2="268"/>
  <rect class="ext" x="280" y="268" width="170" height="46" rx="10"/><text x="365" y="290" text-anchor="middle">Browsers</text><text class="lbl" x="365" y="306" text-anchor="middle">local or Selenium Grid (Docker)</text>
  <path d="M170 291 H280"/><text class="lbl" x="225" y="284" text-anchor="middle">WebDriver</text>
  <rect class="ext" x="560" y="268" width="180" height="46" rx="10"/><text x="650" y="296" text-anchor="middle">ShopEase UI</text>
  <path d="M450 291 H560"/>
  <rect class="ext" x="560" y="188" width="180" height="46" rx="10"/><text x="650" y="216" text-anchor="middle">ShopEase REST API</text>
  <rect class="ext" x="560" y="108" width="180" height="46" rx="10"/><text x="650" y="136" text-anchor="middle">Database (H2)</text>
  <path d="M170 219 H480"/><path d="M480 131 V219"/><path d="M480 131 H560"/><path d="M480 211 H560"/>
  <text class="lbl" x="520" y="124" text-anchor="middle">JDBC</text><text class="lbl" x="520" y="204" text-anchor="middle">REST</text>
  <text class="lbl" x="325" y="212" text-anchor="middle">ApiClient · QueryExecutor</text>
  <rect class="ext" x="560" y="20" width="180" height="46" rx="10"/><text x="650" y="48" text-anchor="middle">Allure report</text>
  <path d="M170 43 H560" stroke-dasharray="5 4"/><text class="lbl" x="365" y="36" text-anchor="middle">evidence: steps, requests, rows, screenshots, logs</text>
  <text class="lbl" x="650" y="92" text-anchor="middle">application under test (same repository)</text>
</svg></div>'''

PAGES = {
 'enterprise': dict(
  repo='enterprise-test-automation-framework', workflow='nightly.yml', report='docs/images/report-overview.png',
  eyebrow='Featured project 1 · Java · UI, API, database',
  title='Enterprise Test Automation Framework',
  summary='A production-style test automation platform: UI, API, database, integration and end-to-end tests of one application, with parallel execution, evidence-rich reporting, Docker + Selenium Grid and GitHub Actions pipelines.',
  purpose='<p>Shows how a test platform for a real product is designed, built, documented and operated, not just a test suite. '
          'It tests <b>ShopEase Admin</b>, a small shop back office kept in the same repository, so one business record can be checked '
          'through the UI, the REST API and the database. It is a portfolio project, not a framework running in a company.</p>',
  stack=[['Language / build', 'Java 17, Maven (multi-module)'], ['Test runner', 'TestNG 7.12'], ['UI', 'Selenium 4 (local and Selenium Grid)'],
         ['API', 'REST Assured 6, Jackson, JSON Schema validation'], ['Database', 'JDBC (H2), parameterised queries'], ['Assertions / data', 'AssertJ, Datafaker, JSON and CSV files'],
         ['Logging / reporting', 'SLF4J + Logback per thread and test; Allure 3'], ['Containers', 'Docker, docker compose, Selenium Grid (hub + Chrome, Firefox, Edge nodes)'],
         ['CI/CD', 'GitHub Actions, Dependabot, dependency review, Checkstyle']],
  architecture=ENTERPRISE_SVG + '<p>Layers depend downwards only: tests contain no Selenium, HTTP or SQL. The repository documents the architecture in '
          '<a href="https://github.com/niranjankagri/enterprise-test-automation-framework/blob/main/docs/architecture.md" target="_blank" rel="noopener">docs/architecture.md</a> '
          'and 21 architecture decision records in '
          '<a href="https://github.com/niranjankagri/enterprise-test-automation-framework/tree/main/docs/adr" target="_blank" rel="noopener">docs/adr</a>.</p>',
  extra=[('layers', 'Layers and responsibilities', table([
            ['Tests', 'What is checked, in business terms; no Selenium, HTTP or SQL', '<code>tests/api</code>, <code>tests/ui</code>, <code>tests/db</code>, <code>tests/integration</code>, <code>tests/e2e</code>'],
            ['Pages, API services, DB queries', 'One class per screen, API resource or query area; the only place that knows locators, endpoints and SQL', 'page objects, service objects, query classes'],
            ['Components and clients', 'Reusable UI components, the REST client, the query executor, waits on real state', '<code>ApiClient</code>, <code>QueryExecutor</code>, components'],
            ['Driver and configuration', 'Browser per thread (local or Grid), layered configuration, secrets from the environment', '<code>DriverFactory</code>, configuration loader'],
            ['Execution and evidence', 'Retry policy for infrastructure failures, logging, Allure steps and attachments', 'listeners, <code>SecretMasker</code>, Allure'],
          ], ['Layer', 'Responsibility', 'Examples'])),
         ('configuration', 'Configuration and execution',
          '<p>Settings are layered: defaults, an environment (<code>-Denv=qa</code>), then system properties, so the same tests run on a laptop, in Docker, against Grid or in CI without edits. Examples: <code>-Dbrowser=firefox</code>, <code>-Dthreads=4</code>, <code>-Dsuite=smoke</code>, <code>-Dexecution=remote -Dgrid.url=...</code>.</p>'
          '<p><b>Parallel execution:</b> one browser per thread, unique data per test, per-thread clean-up and logs; the full suite took about 242 s serial, 171 s with 2 threads and 148 s with 4 (clean clone).</p>'
          '<p><b>Retries:</b> only transient infrastructure failures (browser start-up, lost sessions, refused connections) are retried, for test methods and for browser start-up; assertion failures and wait timeouts never are, and every retry is visible in the report.</p>'
          '<p><b>Reporting:</b> Allure shows every UI action, API call (request and response attached) and SQL query as a step; failed UI tests get screenshot, URL, page source and browser console; failures are categorised (configuration, infrastructure, timeout, authentication, database, UI, API, assertion); logs mask secrets.</p>')],
  decisions=['Test at the cheapest level (API) and check consistency across UI, API and database',
             'Every test owns its data: independent, parallel-safe, no order dependencies, no shared fixtures, no sleeps',
             'Retry only transient infrastructure failures (browser start-up, lost sessions, refused connections); assertion failures and wait timeouts never',
             'Every failure explains itself: steps, request/response, rows, screenshot, log, environment and build in the report',
             'Same tests everywhere: laptop, Docker, Grid and CI are configured, never edited',
             'Cloud device farms deferred on purpose; Grid covers remote browsers'],
  features=['169 TestNG test executions from 124 test methods (data-driven tests run once per data row), all passing in the scheduled nightly run of 12 Oct 2026; by package, without overlap: API 57, UI 48, database 13, integration 9, end-to-end 2, framework unit tests 40. Evidence: <a href="https://github.com/niranjankagri/enterprise-test-automation-framework/actions/runs/38226623404" target="_blank" rel="noopener">nightly run 38226623404</a>',
            'Named suites (TestNG groups, which overlap): smoke 20, sanity 11, regression 121',
            'Parallel execution: one browser per thread; full suite about 242 s serial, 171 s with 2 threads, 148 s with 4 (clean clone)',
            'Allure report with every UI action, API call and SQL query as a step, failure categories and an environment panel',
            'Secrets masked in every log line, report attachment and failure message',
            'Docker compose: application, Selenium hub, Chrome/Firefox/Edge nodes and the test runner'],
  run='<pre><code>mvn clean test                                   # full suite, local app, Chrome\nmvn clean test -Dsuite=smoke -Dheadless=true     # one suite\nmvn clean test -Dbrowser=firefox -Dthreads=4     # another browser, 4 threads\ndocker compose -f docker/docker-compose.yml up --build --abort-on-container-exit --exit-code-from tests</code></pre>'
      '<p>Requirements: JDK 17+, Maven 3.9+, Chrome or Edge; Node.js for the Allure CLI. Full instructions in the '
      '<a href="https://github.com/niranjankagri/enterprise-test-automation-framework#running-tests" target="_blank" rel="noopener">README</a>.</p>',
  results=fig('https://raw.githubusercontent.com/niranjankagri/enterprise-test-automation-framework/main/docs/images/report-overview.png',
              'Allure overview of a smoke run', 'Allure overview of a smoke run with one deliberately failing demo check.')
          + fig('https://raw.githubusercontent.com/niranjankagri/enterprise-test-automation-framework/main/docs/images/grid-ui.png',
              'Selenium Grid console with Chrome, Firefox and Edge nodes', 'The Docker Selenium Grid used by the nightly run.'),
  ci='<p>Five workflows: <b>CI</b> on pull requests (compile with warnings as errors, Checkstyle, unit tests, smoke, dependency review), '
     '<b>Main</b> on every push (API, UI, smoke on Edge), <b>Nightly</b> (full suite on Chrome, regression on Firefox and Edge, and regression on Docker + Grid), '
     'plus report publishing and a manual suite runner.</p>'
     + fig('https://raw.githubusercontent.com/niranjankagri/enterprise-test-automation-framework/main/docs/images/ci-nightly.png',
           'Nightly workflow with every job green', 'A nightly run: every job green, including Docker + Selenium Grid.'),
  limits=['Cloud device farms are not integrated (deliberate, see the decision records)',
          'The application under test uses an in-memory H2 database and demo-grade security; it exists to be tested',
          'Allure steps are at user-action level; no business-level step names yet'],
  next=['BrowserStack or LambdaTest as another remote target', 'Allure report with history on GitHub Pages',
        'Contract tests (OpenAPI) and performance smoke tests in the nightly run', 'Accessibility checks (axe) on key pages', 'PostgreSQL in Docker'],
 ),
 'playwright-typescript': dict(
  repo='playwright-typescript-framework', workflow='ci.yml', report='docs/images/report-overview.png',
  eyebrow='Featured project 2 · TypeScript · Web + API',
  title='Playwright + TypeScript Framework',
  summary='UI and API test automation for a demo web shop (Angular front end + REST API) with Playwright Test and strict TypeScript: 47 tests, 95 runs per full run on Chromium, Firefox and WebKit.',
  purpose='<p>Tests the <a href="https://practicesoftwaretesting.com" target="_blank" rel="noopener">Practice Software Testing Toolshop</a>, '
          'a public demo shop built for testers, through its UI and its REST API, to show modern TypeScript test design: page objects, fixtures, typed API contracts and network control.</p>',
  stack=[['Test runner', 'Playwright Test 1.64'], ['Language', 'TypeScript 6, strict mode'], ['API contracts', 'zod 4 schemas (also the TypeScript types)'],
         ['Static checks', 'tsc, ESLint (type-aware, eslint-plugin-playwright), Prettier'], ['CI', 'GitHub Actions: checks, then api/chromium/firefox/webkit in parallel, then one merged report']],
  architecture='<pre><code>tests/api/*.api.spec.ts   tests/ui/*.spec.ts\n        │                         │\n  fixtures/test.ts (page objects, API clients, test user, loggedIn option)\n        │                         │\n  api/ AuthApi · ProductsApi · CartsApi        pages/ + components/HeaderComponent\n  + zod schemas                                + @step decorator\n        │                         │\n     REST API                 Browser (3 engines)</code></pre>',
  decisions=['Fixtures instead of <code>new</code>: tests declare what they need; API tests never start a browser',
             'Login through the API per test (token injected before page load); a saved login was not used because the shop\'s tokens expire after 5 minutes',
             'zod schemas validate every response and provide the types, so contract and code cannot drift; they found a real inconsistency between two endpoints',
             '<code>@step</code> decorator on page-object methods for readable reports and traces; passwords never in step titles',
             'Each worker registers its own customer, so no shared credentials and no collisions in parallel runs'],
  features=['Login, catalogue search/filter/sort, product, full checkout of two products, guest sign-in step',
            'Network tests: mocked product list, empty list, 500 error, inspection of requests the front end sends',
            'API tests: registration, JWT login, paging contract, carts with 422 validation and a business rule, 404s',
            'Exact money maths in cents; tags for smoke, negative, e2e, hybrid and network runs'],
  run='<pre><code>npm ci\nnpx playwright install --with-deps\nnpm test                 # API + 3 browsers\nnpm run test:api         # API only\nnpm run check            # typecheck + lint + format (what CI runs first)</code></pre>',
  results=fig('https://raw.githubusercontent.com/niranjankagri/playwright-typescript-framework/main/docs/images/report-overview.png',
              'Playwright HTML report overview', 'Merged Playwright HTML report of a full run.'),
  ci='<p>One workflow: static checks first, then four parallel jobs (API, Chromium, Firefox, WebKit), then a single merged HTML report kept as an artifact.</p>',
  limits=['The suite depends on a public demo site; its availability and data affect runs',
          'Two form-login UI tests are skipped in CI, where the site\'s bot check blocks automated form logins; login itself is covered through the API'],
  next=['Publish the merged HTML report to GitHub Pages', 'Visual comparison of key pages'],
 ),
 'appium': dict(
  repo='appium-framework', workflow='tests.yml', report='docs/images/report-overview.png',
  eyebrow='Featured project 4 · Java · Android',
  title='Appium Android Framework',
  summary='Android test automation with Appium 3, Java 17 and TestNG for the Sauce Labs My Demo App: 40 tests on an Android 15 emulator, locally and in GitHub Actions, with three real app bugs found.',
  purpose='<p>Shows mobile test automation end to end: setup on Windows without Android Studio, screen objects, device behaviour, evidence for every failure, and an Android emulator in CI.</p>',
  stack=[['Mobile automation', 'Appium 3.8 server, UiAutomator2 driver 8.7, Appium Java client 11'], ['Test runner', 'TestNG 7.12 (groups, suites, retry analyzer)'],
         ['Device', 'Android 15 emulator (API 35), or a real phone over USB'], ['Reporting', 'Custom HTML report with steps, screenshots and screen recordings'],
         ['CI', 'GitHub Actions with reactivecircus/android-emulator-runner']],
  architecture='<pre><code>Tests (TestNG) ──▶ Screen objects + Header component + Device actions\n                        │\n                   BaseScreen (wait, tap, type, scroll, log each step)\n                        │\n                   DriverManager (one session per thread; app data cleared before each test)\n                        │\n        Appium server ──▶ UiAutomator2 ──▶ emulator / phone</code></pre>'
               '<p>Design reasons, and the failures that shaped them, are in '
               '<a href="https://github.com/niranjankagri/appium-framework/blob/main/docs/framework-design.md" target="_blank" rel="noopener">docs/framework-design.md</a>.</p>',
  decisions=['One Appium session per thread, reset per test with <code>mobile: clearApp</code> (about 2 s instead of 5–10 s for a new session)',
             'Locators: resource ids first, accessibility ids next, UiAutomator text only where there is no id, never XPath',
             'Swipe-based scrolling in both directions with end-of-list detection, because the app\'s list is not marked scrollable',
             'Retry only when Android shows "app isn\'t responding"; assertion failures are never retried',
             'Known app bugs kept as tests that assert the correct behaviour, outside the main suite'],
  features=['Login, sorting, cart and a full checkout with the order total checked as cart total + delivery (BigDecimal)',
            'Device tests: back button, background and resume, cold start, rotation lock, keyboard',
            '17 interview scenario tests: locator strategies, W3C gestures, permission dialogs, mocked GPS, files, logcat, WebView context',
            'Every failure keeps a screenshot and a screen recording in the report'],
  run='<pre><code>scripts/get-app.sh                           # downloads the pinned APK\nemulator -avd Pixel_API_35 -no-snapshot-save\nappium --use-plugins=inspector --allow-cors\nmvn test                                     # 40 tests, about 16 min locally\nmvn test -DsuiteXmlFile=known-bugs.xml       # the 3 known app bugs</code></pre>'
      '<p>Full setup guide: <a href="https://github.com/niranjankagri/appium-framework/blob/main/docs/setup.md" target="_blank" rel="noopener">docs/setup.md</a>.</p>',
  results=fig('https://raw.githubusercontent.com/niranjankagri/appium-framework/main/docs/images/report-overview.png',
              'Appium report: 40 of 40 passed', '40 of 40 passed on the Android 15 emulator.')
          + '<h3 id="bugs">Bugs found in the demo app (My Demo App 2.3.0)</h3>'
          + ul(['Opening the 7th or a later catalog product crashes the app (<code>ArrayIndexOutOfBoundsException</code>, from logcat)',
                'The product quantity can be lowered to 0', 'The missing-country message is cut off ("Please provide your")'])
          + fig('https://raw.githubusercontent.com/niranjankagri/appium-framework/main/docs/images/report-failure.png',
              'Report of the crash test with steps, error, screenshot and recording', 'The crash in the report: steps, error, the home screen at failure and the recording.'),
  ci='<p>On every push: Java 17, Node 24, Appium and the driver at the same versions as the setup guide, KVM, an API 35 Pixel 7 emulator with animations off, '
     'totals in the run summary and the report, failure videos and Appium log as an artifact. 40 of 40 pass in about 9.5 minutes.</p>',
  limits=['Android only: iOS needs a Mac with Xcode', 'One device, so the suite runs on one thread (the design supports one device per thread)',
          'WebView screens are checked for their context but not automated inside (needs a matching Chromedriver)'],
  next=['Parallel runs on several emulators (one udid and systemPort per thread)', 'Real-device or device-cloud run', 'iOS screens with shared accessibility ids'],
 ),
 'robot-framework': dict(
  repo='robot-framework-automation', workflow='ci.yml', report='docs/images/report-overview.png',
  eyebrow='Featured project 5 · Python · Keyword-driven',
  title='Robot Framework UI + API',
  summary='UI and API test automation with Robot Framework 7, SeleniumLibrary and RequestsLibrary on the Page Object Model: 30 tests in about 70 seconds with 4 parallel pabot processes.',
  purpose='<p>Shows keyword-driven automation built like maintainable software: the same tool I use at work (Robot Framework + Python), '
          'applied to a public demo shop (<a href="https://www.saucedemo.com" target="_blank" rel="noopener">Sauce Demo</a>) and a public API '
          '(<a href="https://dummyjson.com" target="_blank" rel="noopener">DummyJSON</a>).</p>',
  stack=[['Framework', 'Robot Framework 7'], ['UI', 'SeleniumLibrary 6.9'], ['API', 'RequestsLibrary 0.9'], ['Parallel runs', 'pabot'],
         ['Code quality', 'Robocop linter (documentation required on every test and keyword)'], ['CI', 'GitHub Actions: lint gate, Chrome and Firefox matrix, nightly run']],
  architecture='<pre><code> tests/*.robot           business language, no locators, no HTTP calls\n        │\n pages / components      api service objects\n (locators live here)    (URLs and bodies live here)\n        │                        │\n common.resource + ShopLibrary.py    ApiSession.resource\n        │                        │\n   SeleniumLibrary            RequestsLibrary</code></pre>',
  decisions=['Tests never touch a locator, URL path or HTTP verb; a UI or API change is one edit in one resource file',
             'One page object per screen; shared screen parts (the header) are components',
             'Action keywords do not assert; check keywords say "Should" (Submit Login Form vs Login Error Message Should Be)',
             'Python only where Robot syntax is awkward: money with Decimal, sort checks, random test data'],
  features=['15 UI tests: login, product list and sorting, cart, checkout with the tax maths',
            '15 API tests: auth, products, carts',
            'Argument files for common, CI and smoke runs; tags for selection',
            'Keyword names that read like a manual test script, with documentation on every test and keyword'],
  run='<pre><code>python -m venv .venv &amp;&amp; .venv\\Scripts\\activate\npip install -r requirements.txt\npabot --processes 4 --testlevelsplit --artifacts png --artifactsinsubfolders \\\n      --outputdir results -A args/common.args tests\nrobocop check</code></pre>',
  results=fig('https://raw.githubusercontent.com/niranjankagri/robot-framework-automation/main/docs/images/report-overview.png',
              'Robot Framework report: 30 tests passed', 'Robot Framework report of a full parallel run.'),
  ci='<p>Lint first (Robocop and a dry run), then the suite on Chrome and Firefox in parallel with pabot, a pass/fail table in the run summary, and the logs as artifacts; also a nightly run.</p>',
  limits=['Runs against public demo sites, whose availability affects results', 'No performance tests in this public project (I use rfswarm for that at work)'],
  next=['A small rfswarm load scenario against a self-hosted app', 'Libdoc keyword documentation published to GitHub Pages'],
 ),
 'playwright-java': dict(
  repo='playwright-framework', workflow='tests.yml', report='docs/images/html-report.png',
  eyebrow='Featured project 3 · Java · Web + API',
  title='Playwright for Java Framework',
  summary='UI, API and network test automation with Playwright for Java and TestNG: the Sauce Demo shop and the Restful Booker API, 57 tests run in CI on Chromium, Firefox and WebKit.',
  purpose='<p>Shows Playwright in a Java/TestNG stack, the combination many Java teams move to from Selenium: UI tests on '
          '<a href="https://www.saucedemo.com" target="_blank" rel="noopener">Sauce Demo</a>, API tests on '
          '<a href="https://restful-booker.herokuapp.com" target="_blank" rel="noopener">Restful Booker</a> through Playwright&#39;s own request context, and network control in the browser.</p>',
  stack=[['Language', 'Java 17'], ['Browser and API automation', 'Playwright for Java 1.63 (Chromium, Firefox, WebKit; APIRequestContext)'],
         ['Test runner', 'TestNG 7.12 (groups, data providers, parallel classes)'], ['JSON', 'Jackson (Java records)'],
         ['Report', 'Custom TestNG IReporter: one HTML file with screenshots, videos and traces'], ['CI', 'GitHub Actions: one job per browser engine']],
  architecture='<pre><code>tests (ui, api, network, interview, framework)\n      │\npages (PageFactory: @TestId, @Role, @Placeholder ...)     api (ApiClient, BookingApi, records)\n      │                                                     │\nBrowserManager: Playwright + browser per thread,     Playwright APIRequestContext\ncontext per test, trace + video\n      │\nChromium / Firefox / WebKit</code></pre>',
  decisions=['One Playwright and browser per thread, a fresh BrowserContext per test: isolated, fast, safe for parallel classes',
             'An annotation-based page factory gives Selenium-style declarative locators; Playwright locators are lazy already',
             'No waits in tests: Playwright auto-waits, and pages only wait for one element unique to the page',
             'API tests create their own bookings and delete them afterwards, so the shared demo API is left as it was',
             'Login failures throw the shop&#39;s own message at once instead of timing out'],
  features=['UI: login (including 5 data-driven rejections), sorting, cart, full checkout with total = item total + tax',
            'API: auth, create, read, update, patch and delete bookings, 403 and 404 cases',
            'Network: images blocked, no failing requests while shopping, mocked responses',
            'Every UI test records a trace and a video; both are kept, with a full-page screenshot, only when the test fails'],
  run='<pre><code>mvn exec:java -Dexec.args="install"   # once: download Chromium, Firefox and WebKit\nmvn clean test                        # all tests, headless Chromium\nmvn clean test -Dbrowser=firefox      # chromium, firefox or webkit\nmvn clean test -Dgroups=api           # one group</code></pre>',
  results=fig('https://raw.githubusercontent.com/niranjankagri/playwright-framework/main/docs/images/html-report.png',
              'Playwright for Java HTML report', 'The custom HTML report (this run includes the deliberate demo failures).'),
  ci='<p>On every push and pull request: one job each for Chromium, Firefox and WebKit; each installs its browser with the Linux libraries it needs, runs the tests headless and keeps the HTML report plus any failure screenshots, videos and traces as an artifact.</p>',
  limits=['UI and API tests depend on public demo sites', 'The README report screenshot shows a run that includes the deliberate demo failures (run with -Pdemo)'],
  next=['Publish the HTML report to GitHub Pages', 'Visual comparison of key pages'],
 ),
 'rest-api': dict(
  repo='api-automation', workflow='tests.yml', report='docs/images/html-report.png',
  eyebrow='More projects · Java · API',
  title='REST API Automation Framework',
  summary='A layered REST API test framework with Java 17, REST Assured and TestNG against the public JSONPlaceholder API, with a custom self-contained HTML report.',
  purpose='<p>Shows how an API framework separates the test scenario from HTTP details: tests speak in business terms, one manager per API resource '
          'handles requests, and builders do the low-level work.</p>',
  stack=[['Language / build', 'Java 17, Maven'], ['HTTP', 'REST Assured'], ['Test runner', 'TestNG (soft assertions)'],
         ['JSON mapping', 'Jackson'], ['Logging', 'Log4j2'], ['CI', 'GitHub Actions (CircleCI configuration also included)']],
  architecture='<pre><code>tests (CommentTest)          scenario in business terms, no HTTP code\n      │\nmanager (UserManager, PostManager, CommentManager)\n      │   base Manager: send request, log + assert status, map JSON\nbuilder (RequestBuilder, ResponseBuilder)\n      │\nREST Assured + Jackson ──▶ JSONPlaceholder API</code></pre>',
  decisions=['One manager per API resource and no global state', 'Responses mapped to POJOs instead of JSON paths in tests',
             'Soft assertions so one run reports every bad value, not just the first', 'Test data in a properties file, overridable with -D'],
  features=['End-to-end scenario: find a user by username, fetch all their posts, fetch all comments on those posts, validate every comment\'s e-mail format',
            'Custom self-contained HTML report written by a TestNG listener'],
  run='<pre><code>mvn clean test\nmvn clean test -Dusername=Bret      # other test data</code></pre><p>Requirements: JDK 17+, Maven 3.6+, internet access (the tests call the live API).</p>',
  results=fig('https://raw.githubusercontent.com/niranjankagri/api-automation/main/docs/images/html-report.png',
              'Custom HTML report of the API framework', 'The custom HTML report.'),
  ci='<p>GitHub Actions runs <code>mvn clean test</code> on every push. A CircleCI configuration is included but not connected.</p>',
  limits=['One test scenario: the project shows the framework structure rather than broad API coverage',
          'Depends on a public API that returns fixed demo data (writes are not persisted)'],
  next=['Negative tests (404, invalid payloads) and JSON schema validation', 'Data-driven tests across several users',
        'See the Enterprise framework for broad API coverage (57 API tests with schema validation)'],
 ),
}

os.makedirs(OUT, exist_ok=True)
for name, p in PAGES.items():
    open(f'{OUT}/{name}.html', 'w', encoding='utf-8', newline='\n').write(page(p))
    print('written', name)
