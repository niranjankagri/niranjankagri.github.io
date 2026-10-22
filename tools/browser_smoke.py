"""Exercise portfolio navigation and project interactions in installed Playwright browsers."""

from __future__ import annotations

import argparse
import json
import os
import traceback
from hashlib import sha1
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

AXE_SCRIPT: Path | None = None
EXPECTED_MISSING_PATHS = {
    "/portfolio-smoke-missing-root.html",
    "/projects/portfolio-smoke-missing-case.html",
}


def audit_accessibility(page) -> None:
    if AXE_SCRIPT is None:
        return
    if page.evaluate("typeof window.axe === 'undefined'"):
        page.add_script_tag(path=str(AXE_SCRIPT))
    result = page.evaluate(
        "async () => await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}})"
    )
    violations = [
        {
            "id": item["id"],
            "impact": item["impact"],
            "help": item["help"],
            "nodes": [node["target"] for node in item["nodes"]],
        }
        for item in result["violations"]
    ]
    assert not violations, json.dumps(violations, indent=2)


def exercise_architecture(
    page, base_url: str, route: str, expected_components: int
) -> None:
    page.goto(base_url + route)
    explorer = page.locator(".architecture-explorer")
    tabs = explorer.locator('[role="tab"]')
    panel = explorer.locator('[role="tabpanel"]')
    assert tabs.count() == expected_components
    assert panel.is_visible()
    detail_padding = float(
        panel.evaluate(
            "element => getComputedStyle(element).paddingLeft.replace('px', '')"
        )
    )
    assert detail_padding >= 16, (route, detail_padding)
    for index in range(expected_components):
        tab = tabs.nth(index)
        tab.click()
        assert tab.get_attribute("aria-selected") == "true"
        for label in ("Technology", "Inputs", "Outputs"):
            assert panel.get_by_text(label, exact=True).is_visible()
        assert panel.locator(".architecture-purpose").inner_text().strip()
        assert panel.locator(".architecture-source a").inner_text() == "View source"
        assert panel.locator(".architecture-source code").inner_text().strip()
        assert panel.locator(".architecture-source code").evaluate(
            "element => element.scrollWidth <= element.clientWidth + 1"
        )
        assert (
            panel.locator(".architecture-source a")
            .get_attribute("href")
            .startswith("https://github.com/")
        )
    tabs.first.focus()
    page.keyboard.press("End")
    assert tabs.nth(expected_components - 1).get_attribute("aria-selected") == "true"
    assert (
        page.evaluate("getComputedStyle(document.activeElement).outlineWidth") == "3px"
    )

    page.set_viewport_size({"width": 390, "height": 844})
    assert not explorer.locator(".architecture-interactive").is_visible()
    details = explorer.locator(".architecture-fallback [data-architecture-item]")
    assert details.count() == expected_components
    assert details.evaluate_all(
        "items => getComputedStyle(items[0].parentElement).gridTemplateColumns.split(' ').length === 1"
    )
    left_padding = float(
        explorer.evaluate(
            "element => getComputedStyle(element).paddingLeft.replace('px', '')"
        )
    )
    assert left_padding >= 18
    for index in range(expected_components):
        item = details.nth(index)
        item.locator("summary").click()
        assert item.evaluate("element => element.open")
        assert (
            details.evaluate_all("items => items.filter(item => item.open).length") == 1
        )
        for label in ("Technology", "Inputs", "Outputs"):
            assert item.locator("dt").filter(has_text=label).is_visible()
        assert item.locator(".architecture-source a").inner_text() == "View source"
        assert item.locator(".architecture-source code").evaluate(
            "element => element.scrollWidth <= element.clientWidth + 1"
        )
    page.set_viewport_size(
        {"width": 720, "height": 900}
    )  # 200% desktop zoom equivalent (720 CSS px).
    page.goto(base_url + route)
    assert not page.evaluate(
        "document.documentElement.scrollWidth > document.documentElement.clientWidth"
    )
    page.set_viewport_size({"width": 1440, "height": 1000})


def reveal_and_verify_images(page, route: str) -> None:
    """Reveal lazy content and require every content image to decode successfully."""
    page.evaluate(
        """() => {
          document.querySelectorAll('details').forEach(item => { item.open = true; });
          document.querySelectorAll('img').forEach(image => { image.loading = 'eager'; });
          window.scrollTo(0, document.body.scrollHeight);
        }"""
    )
    page.wait_for_function(
        "Array.from(document.images).every(image => image.complete)", timeout=30000
    )
    failures = page.evaluate(
        """() => Array.from(document.images)
          .filter(image => !image.classList.contains('ci') && image.naturalWidth === 0)
          .map(image => ({src: image.currentSrc || image.src, alt: image.alt}))"""
    )
    assert not failures, (route, failures)


def exercise(
    browser_name: str,
    base_url: str,
    expected_build_id: str = "",
    expected_asset_version: str = "",
) -> None:
    with sync_playwright() as playwright:
        browser = getattr(playwright, browser_name).launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 1000}, reduced_motion="reduce"
        )
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        console_errors: list[str] = []
        request_errors: list[str] = []
        page_errors: list[str] = []
        same_origin_request_errors: list[str] = []
        same_origin_response_errors: list[str] = []

        def capture_console_error(message) -> None:
            source = message.location.get("url", "")
            if source.startswith(base_url) or "uncaught" in message.text.casefold():
                console_errors.append(message.text)

        def capture_request_error(request) -> None:
            message = f"{request.method} {request.url}: {request.failure}"
            request_errors.append(message)
            if request.url.startswith(base_url.rstrip("/") + "/"):
                same_origin_request_errors.append(message)

        def capture_response_error(response) -> None:
            if (
                response.url.startswith(base_url.rstrip("/") + "/")
                and response.status >= 400
                and urlparse(response.url).path not in EXPECTED_MISSING_PATHS
            ):
                same_origin_response_errors.append(
                    f"{response.status} {response.url}"
                )

        page.on(
            "console",
            lambda message: (
                capture_console_error(message) if message.type == "error" else None
            ),
        )
        page.on("requestfailed", capture_request_error)
        page.on("response", capture_response_error)
        try:
            page.on("pageerror", lambda error: page_errors.append(str(error)))

            page.goto(base_url + "/", wait_until="domcontentloaded")
            build_id = page.locator('meta[name="portfolio-build"]').get_attribute(
                "content"
            )
            if expected_build_id:
                assert build_id == expected_build_id, (build_id, expected_build_id)
            release_response = context.request.get(base_url + "/release.json")
            assert release_response.status == 200
            release = release_response.json()
            assert release.get("build_id") == build_id
            if expected_asset_version:
                assert expected_asset_version in page.locator(
                    'link[rel="stylesheet"]'
                ).get_attribute("href")
                assert release.get("asset_version") == expected_asset_version
            assert page.locator("main h1").count() == 1
            assert page.evaluate(
                'matchMedia("(prefers-reduced-motion: reduce)").matches'
            )
            assert (
                page.evaluate(
                    "getComputedStyle(document.documentElement).scrollBehavior"
                )
                == "auto"
            )
            if browser_name == "webkit":
                # WebKit automation defaults to controls-only tabbing, like Safari's system preference.
                page.locator(".skip").focus()
            else:
                page.keyboard.press("Tab")
            assert page.evaluate('document.activeElement.matches(".skip")')
            assert (
                page.evaluate("getComputedStyle(document.activeElement).outlineWidth")
                == "3px"
            )
            if browser_name == "webkit":
                assert (
                    page.evaluate("getComputedStyle(document.activeElement).opacity")
                    == "1"
                )
                page.keyboard.press("Enter")
                page.wait_for_function("location.hash === '#main'")
                page.goto(base_url + "/")
            role_panels = page.locator("[data-role-panel]")
            assert role_panels.count() == 3
            focus_panels = page.locator("[data-exploration-panel]")
            assert focus_panels.count() == 6
            # 720 CSS px approximates a 1440 px desktop at 200% browser zoom.
            for width in (1440, 1280, 1024, 900, 860, 768, 720, 390, 375, 320):
                page.set_viewport_size({"width": width, "height": 1000})
                if width <= 480:
                    hero_text_width = page.locator(".hero-text").evaluate(
                        "element => element.getBoundingClientRect().width"
                    )
                    assert hero_text_width >= width * 0.65, (width, hero_text_width)
                collapsed = role_panels.evaluate_all(
                    "items => items.map(item => item.getBoundingClientRect().height)"
                )
                assert max(collapsed) - min(collapsed) <= 1, (width, collapsed)
                collapsed_focus = focus_panels.evaluate_all(
                    "items => items.map(item => item.getBoundingClientRect().height)"
                )
                assert max(collapsed_focus) - min(collapsed_focus) <= 1, (
                    width,
                    collapsed_focus,
                )
                for panel in role_panels.all():
                    assert not panel.evaluate("item => item.open")
                    summary = panel.locator("summary")
                    assert (
                        summary.locator("span").nth(1).bounding_box()["y"]
                        > summary.locator("span").nth(0).bounding_box()["y"]
                    )
                    assert (
                        summary.evaluate(
                            "element => getComputedStyle(element, '::after').gridArea"
                        )
                        == "control"
                    )
                for panel in focus_panels.all():
                    assert not panel.evaluate("item => item.open")
                    summary = panel.locator("summary")
                    assert (
                        summary.locator("span").nth(1).bounding_box()["y"]
                        > summary.locator("span").nth(0).bounding_box()["y"]
                    )
                    assert (
                        summary.evaluate(
                            "element => getComputedStyle(element, '::after').gridArea"
                        )
                        == "control"
                    )
                if browser_name == "chromium":
                    page.evaluate(
                        "document.documentElement.style.scrollbarGutter = 'stable'"
                    )
                    assert not page.evaluate(
                        "document.documentElement.scrollWidth > document.documentElement.clientWidth"
                    ), ("classic scrollbar gutter", width)
                    if width == 1440:
                        assert page.evaluate(
                            "document.documentElement.clientWidth < innerWidth"
                        ), "scrollbar-gutter did not reserve a classic scrollbar lane"
                    section = page.locator("#exploration")
                    extent = section.evaluate(
                        "element => { const style = getComputedStyle(element, '::before'); return {width: parseFloat(style.width), sectionWidth: element.getBoundingClientRect().width, shadow: style.boxShadow}; }"
                    )
                    assert abs(extent["width"] - extent["sectionWidth"]) <= 1, (
                        width,
                        extent,
                    )
                    assert extent["shadow"] != "none", (width, extent)
            page.set_viewport_size({"width": 1440, "height": 1000})
            for panel in role_panels.all():
                role_id = panel.get_attribute("data-role-panel")
                panel.locator("summary").focus()
                assert panel.locator("summary").evaluate(
                    "element => document.activeElement === element"
                )
                panel.locator("summary").click()
                page.wait_for_function(
                    "new URLSearchParams(location.search).has('role')"
                )
                assert (
                    page.locator("#role-selection-status")
                    .inner_text()
                    .endswith("all other work remains available.")
                )
                assert panel.evaluate("item => item.open")
                assert panel.locator(".role-projects a").count() > 0
                for other in role_panels.all():
                    if other.get_attribute("data-role-panel") != role_id:
                        assert not other.evaluate("item => item.open")
                        assert (
                            other.evaluate(
                                "item => item.getBoundingClientRect().height"
                            )
                            <= 101
                        )
                page.locator("[data-role-reset]").click()
                page.wait_for_function(
                    "!new URLSearchParams(location.search).has('role')"
                )
            page.locator('[data-role-panel="qa-lead"] summary').click()
            page.wait_for_function(
                "new URLSearchParams(location.search).get('role') === 'qa-lead'"
            )
            page.go_back()
            assert not page.locator('[data-role-panel="qa-lead"]').evaluate(
                "item => item.open"
            )
            page.go_forward()
            assert page.locator('[data-role-panel="qa-lead"]').evaluate(
                "item => item.open"
            )
            page.reload()
            assert page.locator('[data-role-panel="qa-lead"]').evaluate(
                "item => item.open"
            )
            page.locator("[data-role-reset]").click()
            for width in (320, 390):
                page.set_viewport_size({"width": width, "height": 1000})
                for panel in role_panels.all():
                    role_id = panel.get_attribute("data-role-panel")
                    panel.locator("summary").click()
                    assert panel.evaluate("item => item.open")
                    assert panel.locator(".role-projects a").count() > 0
                    for other in role_panels.all():
                        if other.get_attribute("data-role-panel") != role_id:
                            assert not other.evaluate("item => item.open")
                            assert (
                                other.evaluate(
                                    "item => item.getBoundingClientRect().height"
                                )
                                <= 101
                            )
                    assert not page.evaluate(
                        "document.documentElement.scrollWidth > document.documentElement.clientWidth"
                    ), (browser_name, width, role_id)
                    page.locator("[data-role-reset]").click()
            page.set_viewport_size({"width": 1440, "height": 1000})
            page.locator("#projects").scroll_into_view_if_needed()
            featured = page.locator("#projects .featured-grid .project-card")
            assert featured.count() == 6
            assert (
                page.locator('#projects a[href="projects.html"]')
                .inner_text()
                .startswith("View all 25")
            )
            for card in featured.all():
                card.scroll_into_view_if_needed()
                assert card.locator(".card-title a").inner_text().strip()
                assert card.locator(".desc").inner_text().strip()
                assert card.locator(".fact").inner_text().strip()
                assert card.locator(".actions .go").count() == 1
                assert card.locator(".actions .source-action").count() == 1
                assert card.locator(".card-meta .evidence").inner_text().strip()
                assert card.locator(".featured-preview figcaption").is_visible()
                assert card.locator(".featured-preview img").get_attribute("alt")
                assert card.locator(".featured-preview img").evaluate(
                    "image => getComputedStyle(image).objectFit === 'contain'"
                )
                page.wait_for_function(
                    "image => image.complete && image.naturalWidth > 0",
                    arg=card.locator(".featured-preview img").element_handle(),
                )
            enterprise_preview = page.locator(
                '#projects [data-project-id="enterprise-test-automation-framework"] .featured-preview figcaption'
            ).inner_text()
            assert (
                "Historical report" in enterprise_preview
                and "separate local run" in enterprise_preview
            )
            preview_button = page.locator("#projects .featured-preview button").first
            preview_button.focus()
            preview_dialog_id = preview_button.get_attribute("data-image-dialog")
            preview_button.press("Enter")
            assert page.locator("#" + preview_dialog_id).evaluate(
                "dialog => dialog.open"
            )
            if browser_name == "chromium":
                audit_accessibility(page)
            page.keyboard.press("Escape")
            assert preview_button.evaluate(
                "element => document.activeElement === element"
            )
            page.locator('[data-role-panel="senior-sdet"] summary').click()
            page.wait_for_function("location.search.includes('role=senior-sdet')")
            assert (
                page.locator("#role-selection-status")
                .inner_text()
                .startswith("Senior SDET focus selected.")
            )
            assert "role=senior-sdet" in page.url
            assert page.locator('[data-role-panel="senior-sdet"]').evaluate(
                "element => element.open"
            )
            page.locator("[data-role-reset]").click()
            page.wait_for_function("!location.search.includes('role=')")
            assert "role=" not in page.url
            page.locator(
                '[data-exploration-panel="performance-bottlenecks"] summary'
            ).focus()
            page.keyboard.press("Enter")
            page.wait_for_function(
                "location.search.includes('focus=performance-bottlenecks')"
            )
            assert (
                page.locator("#focus-selection-status")
                .inner_text()
                .startswith("Find performance bottlenecks selected.")
            )
            assert (
                "Supporting experience:"
                in page.locator(
                    '[data-exploration-panel="performance-bottlenecks"]'
                ).inner_text()
            )
            maintainable = page.locator(
                '[data-exploration-panel="maintainable-automation"]'
            )
            maintainable.locator("summary").focus()
            page.keyboard.press("Enter")
            page.wait_for_function(
                "location.search.includes('focus=maintainable-automation')"
            )
            assert maintainable.evaluate("item => item.open")
            assert page.locator(
                '[data-exploration-panel="performance-bottlenecks"]'
            ).evaluate("item => item.open")
            assert "2 paths are open" in page.locator(
                "#focus-selection-status"
            ).inner_text()
            page.locator(
                '[data-exploration-panel="performance-bottlenecks"] summary'
            ).focus()
            page.keyboard.press("Enter")
            assert not page.locator(
                '[data-exploration-panel="performance-bottlenecks"]'
            ).evaluate("item => item.open")
            assert maintainable.evaluate("item => item.open")
            assert "focus=maintainable-automation" in page.url
            page.locator("[data-focus-reset]").click()
            page.wait_for_function("!location.search.includes('focus=')")
            assert focus_panels.evaluate_all(
                "items => items.every(item => !item.open)"
            )
            page.locator('#skills a[href*="skill="]').first.click()
            page.wait_for_url("**/projects.html?skill=*")
            assert page.locator("#skill-search").input_value()

            page.goto(base_url + "/projects.html")
            assert (
                page.locator('link[rel="stylesheet"]')
                .get_attribute("href")
                .split("?v=")[1]
            )
            assert (
                page.locator('script[src*="theme.js"]')
                .get_attribute("src")
                .split("?v=")[1]
            )
            assert page.evaluate("document.styleSheets.length > 0")
            assert page.locator("#project-grid .project-card").count() == 25
            for project_id in (
                "ai-assisted-test-automation",
                "llm-feature-testing",
            ):
                ai_card = page.locator(
                    f'#project-grid [data-project-id="{project_id}"]'
                )
                assert ai_card.locator(".evidence-kind").inner_text() == (
                    "Recorded CI replay"
                )
                assert "no live model result is claimed" in ai_card.locator(
                    ".fact"
                ).inner_text()
                assert "no live model result" not in ai_card.locator(
                    ".desc"
                ).inner_text()
                assert ai_card.inner_text().count("no live model result") == 1
            case_routes = page.locator(
                "#project-grid .project-card .card-title a"
            ).evaluate_all("links => links.map(link => new URL(link.href).pathname)")
            assert page.locator("#project-grid .project-card").evaluate_all(
                "cards => cards.every(card => ['workflowName', 'report', 'layers', 'targets', 'approach', 'comparisonLimits'].every(key => card.dataset[key] && !/^(undefined|null)$/i.test(card.dataset[key])))"
            )
            page.locator("#project-focus").select_option("release-quality")
            page.wait_for_function("location.search.includes('focus=release-quality')")
            assert page.locator("#project-grid .project-card:visible").count() == 4
            assert (
                page.locator("#active-filters li")
                .filter(has_text="Focus: Investigate release quality")
                .count()
                == 1
            )
            page.locator("#clear-filters").click()
            search = page.locator("#project-search")
            search.fill("no-such-project-query")
            assert page.locator("#project-grid .project-card:visible").count() == 0
            assert page.locator("#empty-results").is_visible()
            page.locator("#clear-filters").click()
            search.fill("Playwright")
            page.locator("#project-sort").select_option("alpha")
            assert "q=Playwright" in page.url and "sort=alpha" in page.url
            assert page.locator("#active-filters li").count() >= 2

            page.locator("#clear-filters").click()
            category = page.locator('input[name="category"][value="Web & API"]')
            language = page.locator('input[name="tech"][value="Java"]')
            category.locator("xpath=..").click()
            language.locator("xpath=..").click()
            assert "category=Web" in page.url and "tech=Java" in page.url
            assert page.locator("#active-filters li").count() == 2
            page.go_back()
            assert "category=" in page.url and "tech=" not in page.url
            page.go_forward()
            assert "category=" in page.url and "tech=" in page.url
            page.reload()
            assert category.is_checked() and language.is_checked()
            page.locator("#active-filters button").first.click()
            page.locator("#clear-filters").click()
            page.locator("#role-focus").select_option("senior-sdet")
            assert (
                "role=senior-sdet" in page.url
                and page.locator("#project-grid .project-card:visible").count() == 25
            )
            page.locator("#clear-filters").click()

            first_card = page.locator("#project-grid .project-card").first
            preview_button = first_card.locator("[data-preview-project]")
            preview_button.focus()
            preview_button.click()
            assert page.locator("#project-preview").evaluate("dialog => dialog.open")
            assert page.locator("#preview-content").inner_text().strip()
            page.keyboard.press("Tab")
            assert page.evaluate('document.activeElement.closest("dialog") !== null')
            page.keyboard.press("Escape")
            assert not page.locator("#project-preview").evaluate(
                "dialog => dialog.open"
            )
            assert page.evaluate(
                'document.activeElement.matches("[data-preview-project]")'
            )

            cards = page.locator("#project-grid .project-card")
            cards.nth(0).locator("[data-compare-project]").click()
            cards.nth(1).locator("[data-compare-project]").click()
            assert page.locator("#compare-count").inner_text().startswith("2")
            page.locator("#open-comparison").click()
            assert page.locator("#comparison-content table tbody tr").count() == 7
            page.keyboard.press("Escape")
            page.locator("#clear-comparison").click()
            for index in range(4):
                cards.nth(index).locator("[data-compare-project]").click()
            assert page.locator("#compare-count").inner_text().startswith("3")
            assert page.url.count("compare=") == 3
            assert (
                cards.nth(3)
                .locator("[data-compare-project]")
                .get_attribute("aria-pressed")
                == "false"
            )
            assert (
                "up to three projects"
                in page.locator("#compare-announcement").inner_text()
            )
            page.reload()
            assert page.locator("#compare-count").inner_text().startswith("3")
            page.locator("#open-comparison").click()
            assert page.locator("#comparison-dialog").evaluate("dialog => dialog.open")
            assert page.locator("#comparison-content table").count() == 1
            if browser_name == "chromium":
                audit_accessibility(page)
            comparison_text = page.locator("#comparison-content").inner_text()
            assert "undefined" not in comparison_text.lower()
            assert "docs/images/" not in comparison_text
            page.keyboard.press("Tab")
            assert page.evaluate('document.activeElement.closest("dialog") !== null')
            page.keyboard.press("Escape")
            page.locator("#clear-comparison").click()

            # Render comparison values for the full catalog in groups so each project
            # exercises every displayed dimension and readable fallback.
            card_count = page.locator("#project-grid .project-card").count()
            for start in range(0, card_count, 3):
                indices = list(range(start, min(start + 3, card_count)))
                if len(indices) == 1:
                    indices.append(0)
                for index in indices:
                    page.locator("#project-grid .project-card").nth(index).locator(
                        "[data-compare-project]"
                    ).click()
                page.locator("#open-comparison").click()
                cells = page.locator("#comparison-content .comparison-table tbody td")
                assert cells.count() == 7 * len(indices)
                for cell in cells.all():
                    value = cell.inner_text().strip()
                    assert (
                        value
                        and "undefined" not in value.lower()
                        and "null" not in value.lower()
                    )
                    assert "docs/images/" not in value
                page.keyboard.press("Escape")
                page.locator("#clear-comparison").click()

            page.locator("#project-search").fill("Playwright")
            page.evaluate("window.scrollTo(0, 620)")
            page.locator("#project-grid .project-card:visible a.go").first.click()
            page.wait_for_url("**/projects/*.html")
            back_link = page.locator("[data-project-return]")
            assert "filtered" in back_link.inner_text().lower()
            back_link.click()
            page.wait_for_url("**/projects.html*")
            assert page.locator("#project-search").input_value() == "Playwright"
            assert page.evaluate("window.scrollY") >= 500

            page.goto(base_url + "/projects/enterprise.html")
            for anchor in ("contribution", "features", "defects"):
                assert page.locator("#" + anchor).count() == 1
            assert (
                page.locator('section[aria-labelledby="limitations"] h3').count() == 0
            )
            assert (
                "Earlier inventory (12 Oct 2026)"
                in page.locator('section[aria-labelledby="scope"]').inner_text()
            )
            page.goto(base_url + "/projects/playwright-typescript.html")
            assert page.locator(".engineering-story").count() == 1
            story = page.locator(".engineering-story")
            assert "public demo shop is shared and mutable" in story.inner_text()
            assert "47 unique tests" in story.inner_text()
            assert "95 test executions" in story.inner_text()
            exercise_architecture(page, base_url, "/projects/enterprise.html", 5)
            exercise_architecture(
                page, base_url, "/projects/quality-intelligence.html", 6
            )
            exercise_architecture(
                page, base_url, "/projects/playwright-typescript.html", 5
            )
            page.goto(base_url + "/projects/enterprise.html")
            old_report_id = (
                "image-"
                + sha1(
                    b"https://raw.githubusercontent.com/niranjankagri/enterprise-test-automation-framework/main/docs/images/report-overview.png"
                ).hexdigest()[:12]
            )
            assert page.locator("#" + old_report_id).count() == 1
            architecture_link = page.locator('.toc a[href="#architecture"]')
            architecture_link.click()
            page.wait_for_function(
                'document.querySelector(".toc a[href=\'#architecture\']").getAttribute("aria-current") === "location"'
            )
            tabs = page.locator(".evidence-tablist [role='tab']")
            assert tabs.count() >= 3
            tabs.first.focus()
            page.keyboard.press("ArrowRight")
            assert tabs.nth(1).get_attribute("aria-selected") == "true"
            image_trigger = page.locator(
                ".evidence-panel:not([hidden]) [data-image-dialog]"
            ).first
            image_trigger.click()
            assert page.locator("dialog.image-viewer").first.evaluate(
                "dialog => dialog.open"
            )
            page.keyboard.press("Tab")
            assert page.evaluate('document.activeElement.closest("dialog") !== null')
            page.keyboard.press("Escape")
            assert page.evaluate(
                'document.activeElement.matches("[data-image-dialog]")'
            )

            page.goto(base_url + "/")
            page.set_viewport_size({"width": 390, "height": 844})
            menu = page.locator(".menu-toggle")
            menu.click()
            assert menu.get_attribute("aria-expanded") == "true"
            page.keyboard.press("Escape")
            assert menu.get_attribute("aria-expanded") == "false"
            assert page.evaluate(
                'document.activeElement === document.querySelector(".menu-toggle")'
            )
            accordion = page.locator("#experience details").first
            accordion.locator("summary").click()
            assert accordion.evaluate("element => element.open")
            page.locator("#theme").click()
            assert page.locator("html").get_attribute("data-theme") in {"light", "dark"}
            page.goto(base_url + "/projects/enterprise.html")
            assert not page.locator("#case-toc").evaluate("element => element.open")
            page.locator("#case-toc summary").click()
            assert page.locator("#case-toc").evaluate("element => element.open")

            if browser_name == "chromium":
                for theme in ("light", "dark"):
                    for route in ("/", "/projects.html"):
                        page.goto(base_url + route)
                        page.evaluate(
                            "value => document.documentElement.dataset.theme = value",
                            theme,
                        )
                        for width in (320, 375, 390, 720, 768, 1024, 1182, 1280, 1440):
                            page.set_viewport_size({"width": width, "height": 900})
                            viewport = page.evaluate(
                                """() => {
                                  const root = document.documentElement;
                                  const overflow = [...document.body.querySelectorAll('*')]
                                    .map(element => {
                                      const rect = element.getBoundingClientRect();
                                      const style = getComputedStyle(element);
                                      return {
                                        tag: element.tagName.toLowerCase(),
                                        id: element.id,
                                        className: String(element.className || '').slice(0, 80),
                                        left: Math.round(rect.left * 100) / 100,
                                        right: Math.round(rect.right * 100) / 100,
                                        width: Math.round(rect.width * 100) / 100,
                                        scrollWidth: element.scrollWidth,
                                        clientWidth: element.clientWidth,
                                        display: style.display,
                                        position: style.position
                                      };
                                    })
                                    .filter(item => item.display !== 'none' &&
                                      (item.left < -1 || item.right > innerWidth + 1 ||
                                       item.scrollWidth > item.clientWidth + 1))
                                    .slice(0, 20);
                                  return {
                                    innerWidth,
                                    clientWidth: root.clientWidth,
                                    scrollWidth: root.scrollWidth,
                                    overflow
                                  };
                                }"""
                            )
                            assert viewport["scrollWidth"] <= viewport["clientWidth"], (
                                route,
                                theme,
                                width,
                                viewport,
                            )
                            if route == "/":
                                role_heights = page.locator(
                                    "[data-role-panel]"
                                ).evaluate_all(
                                    "items => items.map(item => item.getBoundingClientRect().height)"
                                )
                                assert max(role_heights) - min(role_heights) <= 1, (
                                    theme,
                                    width,
                                    role_heights,
                                )
                                for section_id in ("role-explorer", "projects"):
                                    extent = page.locator("#" + section_id).evaluate(
                                        "element => { const rect = element.getBoundingClientRect(); const style = getComputedStyle(element, '::before'); return {width: parseFloat(style.width), parentWidth: rect.width, left: rect.left, shadow: style.boxShadow, clip: style.clipPath}; }"
                                    )
                                    assert (
                                        abs(extent["width"] - extent["parentWidth"]) <= 1
                                        and "100vmax" in extent["shadow"]
                                        and extent["clip"].startswith("inset(")
                                    ), (theme, width, section_id, extent)
                                cards = page.locator(
                                    "#projects .featured-grid .project-card"
                                )
                                assert cards.count() == 6
                                grouped: dict[int, list] = {}
                                for card in cards.all():
                                    top = round(card.bounding_box()["y"])
                                    grouped.setdefault(top, []).append(card)
                                    assert card.locator(
                                        ".featured-preview figcaption"
                                    ).is_visible()
                                for row in grouped.values():
                                    if len(row) > 1:
                                        for selector in (
                                            ".kind",
                                            ".card-title",
                                            ".desc",
                                            ".card-result",
                                            ".card-foot",
                                        ):
                                            y_positions = [
                                                round(
                                                    card.locator(
                                                        selector
                                                    ).bounding_box()["y"]
                                                )
                                                for card in row
                                            ]
                                            assert (
                                                max(y_positions) - min(y_positions) <= 2
                                            ), (theme, width, selector, y_positions)
                    for route in case_routes:
                        page.goto(base_url + route)
                        page.evaluate(
                            "value => document.documentElement.dataset.theme = value",
                            theme,
                        )
                        # Include 720 CSS px as the desktop 200% zoom reflow width.
                        for width in (320, 375, 720, 768, 1024, 1440):
                            page.set_viewport_size({"width": width, "height": 900})
                            assert not page.evaluate(
                                "document.documentElement.scrollWidth > document.documentElement.clientWidth"
                            ), (route, theme, width)
                            if route in (
                                "/projects/enterprise.html",
                                "/projects/quality-intelligence.html",
                                "/projects/playwright-typescript.html",
                            ):
                                panel_padding = float(
                                    page.locator(".architecture-explorer").evaluate(
                                        "element => getComputedStyle(element).paddingLeft.replace('px', '')"
                                    )
                                )
                                assert panel_padding >= 18, (
                                    route,
                                    theme,
                                    width,
                                    panel_padding,
                                )
                            for selector in (".related-projects li", ".neighbor"):
                                for item in page.locator(selector).all():
                                    assert item.evaluate(
                                        "element => element.scrollWidth <= element.clientWidth + 1"
                                    ), (route, theme, width, selector)
                            related_padding = page.locator(".related-projects").evaluate(
                                "element => ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft'].map(property => parseFloat(getComputedStyle(element)[property]))"
                            )
                            assert min(related_padding) >= 16, (
                                route,
                                theme,
                                width,
                                related_padding,
                            )
                            if width <= 375:
                                for block in page.locator(".case-body pre").all():
                                    assert block.evaluate(
                                        "element => element.scrollWidth <= element.clientWidth + 1"
                                    ), (route, theme, width, "code block")
                page.set_viewport_size({"width": 1440, "height": 1000})
                page.goto(base_url + "/")
                context.grant_permissions(
                    ["clipboard-read", "clipboard-write"], origin=base_url
                )
                page.locator("[data-copy-email]").click()
                page.wait_for_function(
                    "document.querySelector('.copy-status').textContent === 'Email address copied.'"
                )
                page.mouse.move(250, 250)
                assert page.locator(".hero-grid").evaluate(
                    "element => !element.style.getPropertyValue('--glow-x')"
                )

                page.goto(base_url + "/projects.html")
                enterprise = page.locator(
                    '[data-project-id="enterprise-test-automation-framework"]'
                )
                enterprise.locator("[data-preview-project]").click()
                page.wait_for_function(
                    "(() => { const image = document.querySelector('#preview-content img'); return image && image.complete && image.naturalWidth > 0; })()"
                )
                assert page.locator("#preview-content img").evaluate(
                    "image => image.naturalWidth > 0"
                )
                page.keyboard.press("Escape")

                touch_context = browser.new_context(
                    viewport={"width": 390, "height": 844},
                    is_mobile=True,
                    has_touch=True,
                )
                touch_page = touch_context.new_page()
                touch_page.goto(base_url + "/")
                touch_page.locator(".hero-grid").dispatch_event(
                    "pointermove",
                    {"pointerType": "touch", "clientX": 250, "clientY": 250},
                )
                assert touch_page.locator(".hero-grid").evaluate(
                    "element => !element.style.getPropertyValue('--glow-x')"
                )
                touch_context.close()

                no_script = browser.new_context(java_script_enabled=False)
                static_page = no_script.new_page()
                static_page.goto(
                    base_url + "/projects.html", wait_until="domcontentloaded"
                )
                assert static_page.locator("#project-grid .project-card").count() == 25
                assert (
                    static_page.locator("#project-grid .card-title a:visible").count()
                    == 25
                )
                static_page.goto(base_url + "/projects/enterprise.html")
                assert (
                    static_page.locator(
                        ".architecture-fallback [data-architecture-item]"
                    ).count()
                    == 5
                )
                assert static_page.locator(".architecture-fallback").is_visible()
                no_script.close()

            required_routes = ["/", "/projects.html", *case_routes, "/404.html"]
            assert len(required_routes) == 28
            for route in required_routes:
                response = page.goto(base_url + route, wait_until="domcontentloaded")
                assert response and response.status in (200, 304), (
                    route,
                    response.status if response else None,
                )
                assert (
                    page.locator("main").count() == 1
                    and page.locator("main h1").count() == 1
                )
                assert page.title().strip()
                assert page.evaluate(
                    "Array.from(document.styleSheets).some(sheet => sheet.href && sheet.href.includes('style.css'))"
                )
                css_href = page.locator('link[rel="stylesheet"]').get_attribute("href")
                assert css_href and ".css?v=" in css_href
                script_src = page.locator('script[src*="theme.js"]').get_attribute(
                    "src"
                )
                assert script_src and ".js?v=" in script_src
                if expected_asset_version:
                    assert (
                        expected_asset_version in css_href
                        and expected_asset_version in script_src
                    )
                if route.startswith("/projects/"):
                    assert page.locator(".related-projects").count() == 1
                    related_padding = page.locator(".related-projects").evaluate(
                        "element => ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft'].map(property => parseFloat(getComputedStyle(element)[property]))"
                    )
                    assert min(related_padding) >= 16, (route, related_padding)
                    assert (
                        page.locator("[data-project-return]").inner_text()
                        == "Back to Projects"
                    )
                    next_link = page.locator(".neighbor.next")
                    if next_link.count():
                        assert (
                            next_link.locator("span").inner_text().strip()
                            == "Next project"
                        )
                        assert next_link.locator("b").inner_text().strip()
                    assert "undefined" not in page.locator("main").inner_text().lower()
                if browser_name == "chromium":
                    reveal_and_verify_images(page, route)
                    audit_accessibility(page)
            assert page.locator(".not-found").count() == 1
            for missing_route in sorted(EXPECTED_MISSING_PATHS):
                missing = page.goto(base_url.rstrip("/") + missing_route)
                assert missing and missing.status == 404, (
                    missing_route,
                    missing.status if missing else None,
                )
                assert page.locator(".not-found").is_visible()
                stylesheet_href = page.locator('link[rel="stylesheet"]').get_attribute(
                    "href"
                )
                theme_src = page.locator('script[src*="theme.js"]').get_attribute(
                    "src"
                )
                avatar_src = page.locator(".avatar").get_attribute("src")
                assert stylesheet_href and stylesheet_href.startswith("/style.css?v=")
                assert theme_src and theme_src.startswith("/theme.js?v=")
                assert avatar_src and avatar_src.startswith("/img/")
                recovery_paths = ("/projects.html", "/")
                for recovery_path in recovery_paths:
                    recovery = context.request.get(base_url.rstrip("/") + recovery_path)
                    assert recovery.status == 200, (
                        missing_route,
                        recovery_path,
                        recovery.status,
                    )
                page.locator('.not-found a[href="/projects.html"]').click()
                page.wait_for_url("**/projects.html")
                assert page.locator("#project-grid .project-card").count() == 25
                page.goto(base_url.rstrip("/") + missing_route)
                page.locator('.not-found a[href="/"]').click()
                page.wait_for_url(base_url.rstrip("/") + "/")
                assert page.locator("#hero-title").is_visible()
            cv_response = context.request.get(
                base_url + "/Niranjan_Kumar_Agri_CV_Technical_Lead_QA_SDET.pdf"
            )
            assert cv_response.status == 200
            assert cv_response.headers.get("content-type", "").startswith(
                "application/pdf"
            )
            assert cv_response.body().startswith(b"%PDF-")

            if browser_name == "chromium" and AXE_SCRIPT is not None:
                for route in (
                    "/",
                    "/projects.html",
                    "/projects/enterprise.html",
                    "/projects/quality-intelligence.html",
                    "/projects/playwright-typescript.html",
                    "/404.html",
                ):
                    page.goto(base_url + route, wait_until="domcontentloaded")
                    for theme in ("light", "dark"):
                        page.evaluate(
                            "value => document.documentElement.dataset.theme = value",
                            theme,
                        )
                        audit_accessibility(page)

            assert not page_errors, page_errors
            assert not console_errors, console_errors
            assert not same_origin_request_errors, same_origin_request_errors
            assert not same_origin_response_errors, same_origin_response_errors
            context.tracing.stop()
        except Exception:
            artifact_dir = Path(
                os.environ.get("PORTFOLIO_SMOKE_ARTIFACTS", "artifacts/browser-smoke")
            )
            artifact_dir.mkdir(parents=True, exist_ok=True)
            screenshot = artifact_dir / f"{browser_name}-failure.png"
            try:
                page.screenshot(path=str(screenshot), full_page=False)
            except Exception as screenshot_error:
                screenshot_error_text = f"Screenshot capture failed: {screenshot_error}"
            else:
                screenshot_error_text = f"Screenshot: {screenshot}"
            trace = artifact_dir / f"{browser_name}-failure.zip"
            try:
                context.tracing.stop(path=str(trace))
                trace_text = f"Trace: {trace}"
            except Exception as trace_error:
                trace_text = f"Trace capture failed: {trace_error}"
            log = artifact_dir / f"{browser_name}-failure.log"
            log.write_text(
                "\n".join(
                    [
                        traceback.format_exc(),
                        screenshot_error_text,
                        trace_text,
                        "Page errors:",
                        *page_errors,
                        "Console errors:",
                        *console_errors,
                        "Failed requests:",
                        *request_errors,
                    ]
                ),
                encoding="utf-8",
            )
            raise
        finally:
            browser.close()
        print(
            f"{browser_name}: role views, URL filters/history, preview, comparison, return state, evidence tabs, architecture, image viewer, mobile navigation and theme passed"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8765",
        help="URL of the locally served static site",
    )
    parser.add_argument(
        "--browser", choices=("chromium", "firefox", "webkit", "all"), default="all"
    )
    parser.add_argument(
        "--expected-build-id",
        default="",
        help="Required meta build id for a staged/deployed release",
    )
    parser.add_argument(
        "--expected-asset-version",
        default="",
        help="Required version query on generated CSS and JS",
    )
    parser.add_argument(
        "--axe-script", default="", help="Path to the pinned axe-core browser script"
    )
    arguments = parser.parse_args()
    global AXE_SCRIPT
    AXE_SCRIPT = Path(arguments.axe_script).resolve() if arguments.axe_script else None
    if AXE_SCRIPT is not None and not AXE_SCRIPT.is_file():
        parser.error(f"axe-core script was not found: {AXE_SCRIPT}")
    names = (
        ("chromium", "firefox", "webkit")
        if arguments.browser == "all"
        else (arguments.browser,)
    )
    for name in names:
        exercise(
            name,
            arguments.base_url.rstrip("/"),
            arguments.expected_build_id,
            arguments.expected_asset_version,
        )


if __name__ == "__main__":
    main()
