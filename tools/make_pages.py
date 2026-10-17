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
 'python-pytest': dict(
  repo='python-pytest-framework', workflow='ci.yml', report='docs/images/report-all-passed.png',
  eyebrow='Featured project 6 · Python · API + UI',
  title='Python pytest + Playwright Framework',
  summary='API, UI and hybrid test automation in Python with pytest, Playwright, requests and pydantic: 46 tests of a notes app in about 1 m 45 s with 4 parallel workers, on Chromium, Firefox and WebKit in GitHub Actions.',
  purpose='<p>Shows a Python test stack for one application with a web UI and a REST API on the same backend: the public '
          '<a href="https://practice.expandtesting.com/notes/app" target="_blank" rel="noopener">Expand Testing Notes app</a>. '
          'The API carries most of the checks, the browser checks what a user sees, and hybrid tests check that the two sides agree.</p>',
  stack=[['Language', 'Python 3.12'], ['Test runner', 'pytest 9 (fixtures, markers, parametrize, hooks)'],
         ['Browser automation', 'Playwright for Python 1.63 with pytest-playwright (Chromium, Firefox, WebKit)'],
         ['API', 'requests 2.34 (one Session per client)'], ['Contracts', 'pydantic 2 models with extra fields forbidden'],
         ['Parallel runs and report', 'pytest-xdist, pytest-html (one self-contained file), Playwright traces and videos'],
         ['Code quality and CI', 'ruff (lint + format), GitHub Actions: lint gate, API job, browser matrix, nightly run']],
  architecture='<pre><code>tests/api, tests/ui, tests/e2e        what is checked\n      │  fixtures (tests/conftest.py): throwaway user per test, logged-in client,\n      │  page with ads blocked, page already logged in, report hooks\n      │\nframework/api        NotesApiClient (requests) + pydantic models\nframework/pages      LoginPage, NotesPage (data-testid locators, no assertions)\nframework/data       unique users and notes (uuid)\n      │\nframework/config     URLs and timeouts from environment variables</code></pre>',
  decisions=['Every test registers its own user through the API and deletes it in teardown, so tests are independent and safe with pytest-xdist on a shared public site',
             'UI tests log in by putting the API token into localStorage before the page loads; the login form itself is tested once',
             'The API client returns raw responses and never asserts, so the same client serves positive and negative tests',
             'pydantic models with extra=&quot;forbid&quot;: an added or renamed field fails a test at once instead of passing silently',
             'Page objects hold data-testid locators and actions; tests assert with Playwright&#39;s retrying expect, with no sleeps anywhere',
             'Demo tests that fail, skip and xfail on purpose carry their own marker and stay out of normal runs'],
  features=['32 API tests: registration and validation, login, the same 401 for a wrong password and an unknown user, token checks, profile, password change, logout, notes CRUD with PUT and PATCH, bad ids, one user cannot see another user&#39;s notes',
            '9 UI tests: login form, adding, completing, deleting and searching notes',
            '5 hybrid tests: data created through the API shown in the app, changes made in the app checked through the API',
            'HTML report with an embedded screenshot for every failed UI test; Playwright screenshot, video and trace kept for failures',
            'Framework design notes and 86 interview questions with answers linked to the code (Markdown + PDF)'],
  run='<pre><code>python -m venv .venv &amp;&amp; .venv\\Scripts\\activate\npip install -r requirements.txt\nplaywright install chromium firefox webkit\npytest -n 4                              # all 46 tests\npytest -m api                            # API only\npytest -m "ui or e2e" --browser firefox  # browser tests on Firefox\npytest -m demo                           # report demo: 2 failed, 1 skipped, 1 xfailed</code></pre>',
  results=fig('https://raw.githubusercontent.com/niranjankagri/python-pytest-framework/main/docs/images/report-all-passed.png',
              'pytest-html report: 46 tests passed', 'pytest-html report of a full run: 46 passed.')
          + fig('https://raw.githubusercontent.com/niranjankagri/python-pytest-framework/main/docs/images/report-demo-failures.png',
                'pytest-html report of the demo run with failures, a skip and an xfail',
                'The report demo: a UI failure with its screenshot, an API failure with the API&#39;s message, a strict xfail and a skip.'),
  ci='<p>On every push, pull request and night: ruff lint and format check first, then the API tests with 4 workers and the UI + hybrid tests on Chromium, Firefox and WebKit as three parallel jobs. Each job writes a pass/fail table to the run summary and keeps its HTML report and traces as an artifact.</p>',
  limits=['Runs against a shared public demo site, whose availability affects results',
          'Visual and accessibility checks are not included yet'],
  next=['Accessibility checks with axe-core', 'Publish the HTML report to GitHub Pages'],
 ),
 'k6-performance': dict(
  repo='k6-performance-testing', workflow='perf.yml', report='docs/images/load-dashboard.png',
  eyebrow='Featured project 7 · JavaScript · Performance',
  title='k6 Performance Testing',
  summary='Smoke, load, stress, spike and soak tests with Grafana k6 for a shop API kept in the repository: service level objectives as thresholds that fail the CI job, and a stress test that found a real bottleneck.',
  purpose='<p>Shows how I approach performance testing: one test per question, pass/fail criteria agreed up front, realistic workload models, '
          'and results that lead to a fix. The app under test, a small shop API, is part of the repository, so the tests never put load on '
          'someone else&#39;s server and every CI job measures its own copy.</p>',
  stack=[['Load testing', 'Grafana k6 2.3 (scenarios, executors, checks, thresholds, custom metrics)'],
         ['Scripts', 'JavaScript ES modules (k6 runtime)'], ['App under test', 'QuickShop: Node.js 24 HTTP API, no dependencies, with functional tests'],
         ['Reports', 'k6 web dashboard (HTML), Markdown summary per run, JSON of every metric'],
         ['Code quality and CI', 'ESLint, Prettier, GitHub Actions: lint, smoke gate, load/stress/spike in parallel, nightly soak']],
  architecture='<pre><code>k6/tests/*.js     scenarios (who, how many, which executor) + thresholds (SLOs)\n      │\nk6/lib/flows.js   journeys browse() and buy(): checks, think time, business metrics\nk6/lib/api.js     one function per endpoint, stable name tag per request\nk6/lib/config.js  BASE_URL, PROFILE (ci | full), THINK\n      │\nQuickShop (app/)  started by each CI job; checkout limited by 8 &quot;database connections&quot;</code></pre>',
  decisions=['SLOs per endpoint as thresholds (p95 per endpoint, error rate, checks, business metrics): a missed SLO exits with 99 and fails the job',
             'Visitors in a closed model (ramping-vus) and orders in an open model (arrival rate) in the same test; dropped iterations have a threshold',
             'One login per virtual user, a different test user per VU from a SharedArray, random think time',
             'Each test has a ci size for every push and a full size for a dedicated environment, side by side in the script',
             'The stress test asserts graceful degradation (every order placed or refused with 503, bounded wait), not the normal SLOs'],
  features=['Five test types: smoke (gate), load, stress, spike and soak; soak samples the server&#39;s memory every 10 s',
            'Finding: past about 90 orders/s checkout queued without limit (p95 over 3 s and rising); fixed with load shedding, the slowest checkout is now 624 ms',
            'Regression demo: a 300 ms slower checkout passes every functional check but fails the checkout SLO (p95 425 ms vs 400 ms)',
            'Markdown result table on every CI run page; HTML dashboard and JSON as artifacts',
            'Design notes and 78 interview questions on performance testing and k6, linked to the code (Markdown + PDF)'],
  run='<pre><code>npm install\nnpm start                               # QuickShop on http://localhost:3000\nk6 run k6/tests/smoke.js\nk6 run k6/tests/load.js\nk6 run -e THINK=0 k6/tests/stress.js\nk6 run -e PROFILE=full k6/tests/load.js  # realistic size and duration</code></pre>',
  results=fig('https://raw.githubusercontent.com/niranjankagri/k6-performance-testing/main/docs/images/stress-before-fix.png',
              'k6 dashboard of the first stress test: response times climb without limit',
              'Stress test before the fix: past the limit, checkout times climb until the abort threshold stops the run.')
          + fig('https://raw.githubusercontent.com/niranjankagri/k6-performance-testing/main/docs/images/stress-after-fix.png',
                'k6 dashboard of the stress test after the fix: response times level off',
                'The same test after adding load shedding: response times level off and every answer is correct.')
          + fig('https://raw.githubusercontent.com/niranjankagri/k6-performance-testing/main/docs/images/regression-demo-summary.png',
                'Markdown summary of the regression demo with the failed checkout threshold',
                'Regression demo: one threshold fails, so the run fails.'),
  ci='<p>On every push and pull request: ESLint, Prettier and the app&#39;s functional tests, then the smoke test as the gate, then the load, stress and spike tests as three parallel jobs, each with its own copy of the app. The soak test runs nightly. Each job writes its result table to the run summary and keeps the HTML dashboard as an artifact.</p>',
  limits=['Shared CI runners are noisy: the CI sizes catch regressions; capacity numbers need dedicated load generators and a production-like environment',
          'The app under test is a demo with simulated latencies'],
  next=['Stream metrics to Grafana (Prometheus remote write) next to server metrics', 'A k6 browser scenario for Web Vitals under load'],
 ),
 'cypress-typescript': dict(
  repo='cypress-typescript-framework', workflow='ci.yml', report='docs/images/report-all-passed.png',
  eyebrow='Featured project 8 · TypeScript · E2E + API + Component',
  title='Cypress + TypeScript Framework',
  summary='End-to-end, API and component tests with Cypress 16 and TypeScript for a React + Node task app kept in the repository: 81 Cypress tests, green in GitHub Actions on Chrome, Firefox and Edge.',
  purpose='<p>Shows what Cypress does best: tests that control the browser&#39;s network, clock and login, and component tests next to '
          'end-to-end tests. The app under test, TaskBoard, is part of the repository, so no public demo site can break a run, '
          'every test can reset the data, and the React components can be mounted on their own.</p>',
  stack=[['Test framework', 'Cypress 16.2 (e2e and component testing)'], ['Language', 'TypeScript 6.0'],
         ['Contracts', 'zod 4 strict schemas'], ['App under test', 'React 19 + Vite 8 web app, Node.js 24 API with no dependencies (and its own node:test tests)'],
         ['Report', 'cypress-mochawesome-reporter: one HTML file per run with failure screenshots'],
         ['Code quality and CI', 'ESLint (type-aware + Cypress rules), Prettier, GitHub Actions with cypress-io/github-action']],
  architecture='<pre><code>cypress/e2e/api, e2e/ui, component     what is checked\n      │\ncypress/pages        LoginPage, BoardPage (data-cy selectors, no assertions)\ncypress/support      commands: resetData, loginAs (cy.session), createTask\n                     api.ts (typed cy.request client), schemas.ts (zod)\n      │\nTaskBoard (app/)     React UI + Node API; POST /api/test/reset before every test</code></pre>',
  decisions=['The app under test lives in the repository: a reset hook and seeded users make every test start from the same data',
             'Login through cy.session with a validate step; the login form itself is tested once',
             'Setup data is created through the API, the screen under test through page objects',
             'zod strictObject contracts: a leaked field fails with its name (checked by leaking a server field on purpose)',
             'cy.intercept for states the real server rarely produces, the real backend for user flows',
             'No fixed waits and no chaining after actions: both are lint errors'],
  features=['31 API tests: login and logout, token checks, tasks CRUD, filters, validation with boundary values, another user&#39;s task answers 404',
            '33 UI tests: login, adding, completing, renaming and deleting tasks (confirm accepted and cancelled), filters, search',
            'Network: slow answers, server errors with Retry, network failure, fixture stub, expired login, request body and header checks',
            'Time: the Overdue badge before, on and after the due date, a 300 ms search debounce and a 3 s toast, with cy.clock',
            '17 component tests: the form, the task row, the filter bar and the toast mounted alone, callbacks recorded with cy.stub()',
            'Framework design notes and 86 interview questions with answers linked to the code (Markdown + PDF)'],
  run='<pre><code>npm ci\nnpm test                  # build the app, start it, run all API + UI tests\nnpm run cy:component      # component tests\nnpm run cy:open           # interactive runner\nnpm run cy:demo           # report demo: 1 pass, 2 fail, 1 skip on purpose</code></pre>',
  results=fig('https://raw.githubusercontent.com/niranjankagri/cypress-typescript-framework/main/docs/images/report-all-passed.png',
              'Mochawesome report: 64 of 64 end-to-end and API tests passed', 'HTML report of a full end-to-end run: 64 passed.')
          + fig('https://raw.githubusercontent.com/niranjankagri/cypress-typescript-framework/main/docs/images/failure-screenshot.png',
                'Cypress screenshot of a failed demo test with the command log and the task board',
                'Failure screenshot from the report demo: the restored login session, the failed assertion and the board at that moment.'),
  ci='<p>On every push, pull request and night: lint, Prettier, type checks and the app&#39;s own tests first; then the API tests, the UI tests on Chrome, Firefox and Edge, and the component tests as parallel jobs. Each job builds and starts its own copy of the app, writes a summary and keeps its HTML report as an artifact.</p>',
  limits=['Specs run one after another against one server; parallel specs would need a server or data set per worker',
          'Visual and accessibility checks are not included yet; WebKit is not covered'],
  next=['Accessibility checks with axe-core and visual comparison', 'Publish the HTML report to GitHub Pages'],
 ),
 'pact-contract': dict(
  repo='pact-contract-testing', workflow='contract.yml', report='docs/images/broker-matrix.png',
  eyebrow='Featured project 9 · TypeScript + Java · Contract testing',
  title='Pact Contract Testing',
  summary='Consumer-driven contract testing with Pact between a TypeScript checkout client and a Java Spring Boot product API, through a self-hosted Pact Broker with can-i-deploy, in one command locally and in GitHub Actions.',
  purpose='<p>Shows how two teams can change and deploy their services independently without an end-to-end environment: '
          'the consumer writes down what it needs, the provider proves it delivers that, and the broker answers before every '
          'deployment whether the versions fit together. Two languages on purpose: the teams share only the contract.</p>',
  stack=[['Consumer', 'TypeScript, fetch, Pact JS 17 (Pact specification V4), Vitest'],
         ['Provider', 'Java 17, Spring Boot 4.1, Pact JVM 4.7 with JUnit 5, Maven wrapper'],
         ['Broker', 'Self-hosted Pact Broker 2.121 with PostgreSQL 17 in Docker Compose'],
         ['Deployment checks', 'pact-broker CLI: publish, can-i-deploy, create-environment, record-deployment'],
         ['CI', 'GitHub Actions: consumer and provider jobs, then the full broker workflow with the matrix on the run page']],
  architecture='<pre><code>checkout-web (TypeScript)      contract tests run the real client against Pact\'s mock server\n      │  pact file (6 interactions)\n      ▼\nPact Broker (Docker)           contracts, verification results, branches, environments, deployments\n      │                        can-i-deploy?  record-deployment\n      ▼\nproduct-service (Spring Boot)  JUnit 5 verification of the real app: provider states, token filter</code></pre>',
  decisions=['The consumer\'s contract tests run its real HTTP client, so the contract records what the code really sends',
             'Only the fields the consumer uses are in the contract, with type and format matchers; the provider may change the rest',
             'Provider states with parameters ("a product exists" with id, price and stock) instead of one state per example',
             'The contract accepts any Bearer token; the provider\'s request filter injects a valid one, but leaves the no-token case alone',
             'Pending and WIP pacts: a consumer\'s new expectation never breaks the provider\'s build; can-i-deploy blocks the consumer instead',
             'The breaking-change demo checks why can-i-deploy said no, so a no for another reason cannot pass as success'],
  features=['6 interactions: one product, 404, products by ids, reservation 201, 409 with the available stock, 401 without a token',
            'Provider verification from the pacts folder (local) or the broker (CI), chosen by one environment variable',
            'npm run contract: broker, consumer tests, publish, provider verification with results, can-i-deploy and record-deployment in about 35 seconds',
            'npm run demo:breaking: a consumer feature branch expects a field the provider lacks; the provider stays green, the consumer is blocked',
            'Mutation checks: renaming a field in the provider fails verification with the missing key named',
            'Framework design notes and 76 interview questions on contract testing and Pact, linked to the code (Markdown + PDF)'],
  run='<pre><code>npm ci &amp;&amp; npm ci --prefix checkout-web\nnpm run contract        # the whole workflow (needs Docker and Java 17+)\nnpm run demo:breaking   # a breaking consumer change, blocked by can-i-deploy\nnpm run broker:down</code></pre>',
  results=fig('https://raw.githubusercontent.com/niranjankagri/pact-contract-testing/main/docs/images/broker-matrix.png',
              'Pact Broker matrix with a verified main version and a failed feature-branch version',
              'The broker\'s matrix: the main version verified and deployed to production, the feature-branch version failed.')
          + fig('https://raw.githubusercontent.com/niranjankagri/pact-contract-testing/main/docs/images/can-i-deploy.png',
                'can-i-deploy output: yes for the main version, no for the feature branch',
                'can-i-deploy: yes for the main version, no for the feature version, with the reason.'),
  ci='<p>On every push and pull request: the consumer job (lint, types, unit and contract tests) and the provider job (Maven tests) in parallel, then a job that starts the Pact Broker with Docker Compose and runs the whole workflow and the breaking-change demo, and writes the broker\'s matrix to the run page.</p>',
  limits=['One consumer; message (event) contracts are not included yet',
          'The broker in CI is new for every run and has no authentication (a shared broker needs both)'],
  next=['A second consumer and a message pact for an event', 'A broker webhook that starts the provider verification, and can-i-merge on pull requests'],
 ),
 'jenkins-kubernetes': dict(
  repo='jenkins-kubernetes-pipeline', workflow='ci.yml', report='docs/images/jenkins-stages.png',
  eyebrow='Featured project 10 · CI/CD · Jenkins + Kubernetes',
  title='Jenkins + Kubernetes Test Pipeline',
  summary='A Jenkins pipeline, configured entirely as code, that builds a small API, deploys it to a kind Kubernetes cluster in a namespace per build and runs unit, smoke and regression tests against the deployment; GitHub Actions starts a real Jenkins on every push and requires the pipeline to pass.',
  purpose='<p>Shows the CI/CD side of test automation: getting tests to run reliably against a freshly deployed system, on every change, with results people can read. '
          'The service under test lives in the repository, so the pipeline depends on nothing outside it, and the Jenkinsfile itself is tested in CI like any other code.</p>',
  stack=[['CI server', 'Jenkins 2.580 LTS in Docker: Configuration as Code, Job DSL, Pipeline Graph View, JUnit, HTML Publisher, credentials binding'],
         ['Kubernetes', 'kind 0.33 (Kubernetes in Docker), kubectl 1.37: Deployment with probes, Service, Job, a namespace per build'],
         ['System under test', 'room-booking: Node.js 24 API, no dependencies, with node:test unit tests'],
         ['Tests', 'pytest 9 + requests: smoke and regression suites, JUnit XML and pytest-html reports, Ruff'],
         ['CI', 'GitHub Actions: checks, the Kubernetes path with the same scripts, and a real Jenkins that runs the Jenkinsfile']],
  architecture='<pre><code>Jenkinsfile                    stages, parallelism, parameters, quality gate, reports\n      │  calls\nscripts/*.sh                   kind-up, deploy, smoke-job, api-tests, teardown (also used by GitHub Actions)\n      │\nkind cluster \'qa\'              namespace qa-&lt;build&gt;: Deployment (2 pods, probes) + Service + smoke Job\n      ▲\nJenkins controller (Docker)    JCasC + Job DSL, uses the host\'s Docker for images and the cluster</code></pre>',
  decisions=['Everything as code: plugins in the image, users, credentials and the job in JCasC and Job DSL, the pipeline in the Jenkinsfile',
             'Scripts do the work and the Jenkinsfile orchestrates, so GitHub Actions runs the same deployment and tests without Jenkins',
             'A namespace per build on a reused cluster: isolated runs, one-command cleanup, about 30 seconds per build',
             'Two deployment checks: a Kubernetes Job inside the cluster through the Service name, and API tests from outside through port-forward',
             'The deployment reports its build number, and a smoke test asserts it, so a stale pod or wrong image cannot pass',
             'The quality gate also fails when too few tests ran; each stage records its results once (an early version counted every test twice)'],
  features=['Parallel unit tests and lint, then image build, kind cluster and image load, deploy with rollout wait, in-cluster smoke Job, parallel API smoke and regression',
            'Parameters for the test scope and keeping the deployment; timeouts, timestamps, no concurrent builds, log rotation',
            'JUnit results with trend, published HTML reports, archived artifacts, a masked credential in the notification step',
            'A deliberately broken rule failed the build at the first stage, before anything was built or deployed',
            'CI starts the Jenkins image, triggers the job through the REST API and fails unless the Jenkins build ends with SUCCESS',
            'Design notes and 76 interview questions on Jenkins, pipelines, Docker and Kubernetes, linked to the code (Markdown + PDF)'],
  run='<pre><code>docker compose -f jenkins/docker-compose.yml up -d --build --wait   # Jenkins on http://localhost:8088\nscripts/run-jenkins-build.sh                                      # start the job, wait, print the result</code></pre>',
  results=fig('https://raw.githubusercontent.com/niranjankagri/jenkins-kubernetes-pipeline/main/docs/images/jenkins-stages.png',
              'Jenkins stage graph of a successful build', 'A successful build in Jenkins\' stage graph: every stage of the pipeline in 31 seconds.')
          + fig('https://raw.githubusercontent.com/niranjankagri/jenkins-kubernetes-pipeline/main/docs/images/jenkins-job.png',
                'Jenkins job page with the test result trend',
                'The job page with the test trend; the drop from 42 to 21 is the fix that stopped tests from being counted twice.'),
  ci='<p>On every push and pull request: unit tests, lint and the API tests against the service on the runner; then, in parallel, the Kubernetes path without Jenkins (kind, deploy, smoke Job, API tests) and a job that builds and starts the Jenkins image and runs the pipeline in it.</p>',
  limits=['Builds run on the controller and it uses the host\'s Docker socket: fine for a local demo, not for a shared Jenkins',
          'Images are loaded into kind instead of pushed to a registry; plugins are not pinned yet'],
  next=['Kubernetes pod agents instead of controller executors', 'A registry, pinned plugins and a shared library for common steps'],
 ),
 'ai-assisted-testing': dict(
  repo='ai-assisted-test-automation', workflow='ci.yml', report='docs/images/pipeline.png',
  eyebrow='Featured project 11 · AI-assisted testing · Java',
  title='AI-Assisted Test Automation (Claude)',
  summary='Claude drafts Playwright for Java tests from plain-language test cases, a three-stage quality gate decides which drafts are worth a person\'s time, a named reviewer approves every merged test, and Claude triages failed runs into product bug, test bug, environment or flaky.',
  purpose='<p>Shows how to use a large language model in test automation without letting it lower the bar. '
          'Generating a plausible test is fast; the expensive failure is a test that passes and checks the wrong thing. '
          'So the project is mostly guardrails: automatic gates before review, a review file built for a five-minute check, an explicit approval recorded in the code, and evidence-based failure triage.</p>',
  stack=[['Language', 'Java 21, Maven wrapper'],
         ['AI', 'Anthropic Java SDK 2.73, Claude Opus 5.5: structured outputs into Java records, prompt caching, effort per task, refusal fallback'],
         ['Tests', 'Playwright for Java 1.63 + TestNG 7.12, page objects, failure evidence (DOM, screenshot, console, trace)'],
         ['System under test', 'LeaveDesk: a leave-request app in the repository (JDK HttpServer + plain JavaScript UI) with a switchable planted bug'],
         ['CI', 'GitHub Actions: unit and tooling tests, UI tests on Chromium, Firefox and WebKit, AI replay and triage jobs without an API key']],
  architecture='<pre><code>test-cases/TC-*.md ──► Claude draft ──► gate: rules ─► javac ─► 3 runs ──► review.md ──► approve ──► src/test (@AiDrafted)\n                         ▲                                    │\n                         └──── findings, up to 2 repair rounds ◄┘\n\nfailed UI run ──► evidence per failure ──► Claude triage ──► triage.md (verdict, quoted evidence, draft ticket)</code></pre>',
  decisions=['One class talks to Claude: typed answers, recording and replay, cost logging and refusal handling in one place',
             'Answers are recorded and keyed on model, prompt, test case and framework code, so CI replays them deterministically and a changed prompt shows up as a missing recording',
             'The gate runs cheapest first and stops at the first failure: text rules, in-process compilation, three TestNG runs against a fresh app',
             'Gate rules explain themselves ("found Thread.sleep on line 18"), because the same message goes back to Claude in a repair round',
             'The model may only use page objects; if a step needs a missing method it reports it instead of using a selector',
             'No auto-merge and no self-healing: approval names the reviewer, and failures go to triage with the evidence'],
  features=['Generator: test case and framework code in, a draft with coverage per expected result, assumptions and missing page methods out',
            'Quality gate: framework and safety rules, javac against the test classpath, three runs each with its own evidence folder',
            'Approve step: only gate-passed drafts, rules re-checked after reviewer edits, @AiDrafted(model, reviewedBy, reviewedOn) added',
            'Failure triage: error, console, DOM, screenshot, test case and test code in; verdict, confidence, quoted evidence and a draft bug ticket out',
            '48 tests that need no API key: app rules and API, every gate rule rejecting a crafted bad draft, real gate runs, replay, approve marking',
            'Design notes and 82 interview questions on AI-assisted testing, linked to the code (Markdown + PDF)'],
  run='<pre><code>mvnw.cmd test                       :: app + tooling tests, no key needed\nmvnw.cmd test -Dsuite=ui            :: UI tests\nai generate TC-103                  :: Claude drafts, the gate checks (needs ANTHROPIC_API_KEY)\nai approve TC-103 Your Name         :: move a passed draft into src/test</code></pre>',
  results=fig('https://raw.githubusercontent.com/niranjankagri/ai-assisted-test-automation/main/docs/images/pipeline.png',
              'Pipeline diagram of the AI-assisted test automation project',
              'The pipeline: drafts go through the gate to a person; failed runs go to AI triage. Results of the first live generation run will be added here.'),
  ci='<p>On every push: the app and tooling tests (including real gate runs in a browser), and the UI suite on Chromium, Firefox and WebKit. Two more jobs replay the recorded AI answers: approved drafts go through today\'s gate again, and a planted product bug must be triaged as PRODUCT_BUG. No job needs an API key.</p>',
  limits=['The rule stage is text matching, a filter and not a sandbox; the human review is the control',
          'One small demo app; triage looks at one failure at a time'],
  next=['The first live generation and triage recordings', 'An evaluation set of cases with known-good tests, and batch generation for larger backlogs'],
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
