"""Exercise portfolio navigation and project interactions in installed Playwright browsers."""

from __future__ import annotations

import argparse
from hashlib import sha1
from playwright.sync_api import sync_playwright


def exercise(browser_name: str, base_url: str) -> None:
    with sync_playwright() as playwright:
        browser = getattr(playwright, browser_name).launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 1000}, reduced_motion="reduce"
        )
        page = context.new_page()
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))

        page.goto(base_url + "/", wait_until="domcontentloaded")
        assert page.evaluate('matchMedia("(prefers-reduced-motion: reduce)").matches')
        assert page.evaluate('getComputedStyle(document.documentElement).scrollBehavior') == "auto"
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
                page.evaluate("getComputedStyle(document.activeElement).opacity") == "1"
            )
            page.keyboard.press("Enter")
            page.wait_for_function("location.hash === '#main'")
            page.goto(base_url + "/")
        page.locator('[data-role-panel="senior-sdet"] summary').click()
        page.wait_for_function("location.search.includes('role=senior-sdet')")
        assert "role=senior-sdet" in page.url
        assert page.locator('[data-role-panel="senior-sdet"]').evaluate(
            "element => element.open"
        )
        page.locator("[data-role-reset]").click()
        page.wait_for_function("!location.search.includes('role=')")
        assert "role=" not in page.url
        page.locator('#skills a[href*="skill="]').first.click()
        page.wait_for_url("**/projects.html?skill=*")
        assert page.locator("#skill-search").input_value()

        page.goto(base_url + "/projects.html")
        search = page.locator("#project-search")
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
        assert not page.locator("#project-preview").evaluate("dialog => dialog.open")
        assert page.evaluate('document.activeElement.matches("[data-preview-project]")')

        cards = page.locator("#project-grid .project-card")
        for index in range(4):
            cards.nth(index).locator("[data-compare-project]").click()
        assert page.locator("#compare-count").inner_text().startswith("3")
        assert page.url.count("compare=") == 3
        page.reload()
        assert page.locator("#compare-count").inner_text().startswith("3")
        page.locator("#open-comparison").click()
        assert page.locator("#comparison-dialog").evaluate("dialog => dialog.open")
        assert page.locator("#comparison-content table").count() == 1
        page.keyboard.press("Tab")
        assert page.evaluate('document.activeElement.closest("dialog") !== null')
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
        tabs = page.get_by_role("tab")
        assert tabs.count() >= 3
        tabs.first.focus()
        page.keyboard.press("ArrowRight")
        assert tabs.nth(1).get_attribute("aria-selected") == "true"
        component = page.locator(".architecture-components details").nth(1)
        component.locator("summary").click()
        assert component.evaluate("element => element.open")
        image_trigger = page.locator("[data-image-dialog]").first
        image_trigger.click()
        assert page.locator("dialog.image-viewer").first.evaluate(
            "dialog => dialog.open"
        )
        page.keyboard.press("Tab")
        assert page.evaluate('document.activeElement.closest("dialog") !== null')
        page.keyboard.press("Escape")
        assert page.evaluate('document.activeElement.matches("[data-image-dialog]")')

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
                        "value => document.documentElement.dataset.theme = value", theme
                    )
                    for width in (320, 375, 390, 768, 1024, 1440):
                        page.set_viewport_size({"width": width, "height": 900})
                        assert not page.evaluate(
                            "document.documentElement.scrollWidth > document.documentElement.clientWidth"
                        ), (route, theme, width)
                for route in (
                    "/projects/enterprise.html",
                    "/projects/quality-intelligence.html",
                ):
                    page.goto(base_url + route)
                    page.evaluate(
                        "value => document.documentElement.dataset.theme = value", theme
                    )
                    for width in (320, 375, 390, 768, 1024, 1440):
                        page.set_viewport_size({"width": width, "height": 900})
                        assert not page.evaluate(
                            "document.documentElement.scrollWidth > document.documentElement.clientWidth"
                        ), (route, theme, width)
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

            touch_context = browser.new_context(
                viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True
            )
            touch_page = touch_context.new_page()
            touch_page.goto(base_url + "/")
            touch_page.locator(".hero-grid").dispatch_event(
                "pointermove", {"pointerType": "touch", "clientX": 250, "clientY": 250}
            )
            assert touch_page.locator(".hero-grid").evaluate(
                "element => !element.style.getPropertyValue('--glow-x')"
            )
            touch_context.close()

            no_script = browser.new_context(java_script_enabled=False)
            static_page = no_script.new_page()
            static_page.goto(base_url + "/projects.html", wait_until="domcontentloaded")
            assert static_page.locator("#project-grid .project-card").count() == 25
            assert (
                static_page.locator("#project-grid .card-title a:visible").count() == 25
            )
            no_script.close()

        assert not errors, "; ".join(errors)
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
    arguments = parser.parse_args()
    names = (
        ("chromium", "firefox", "webkit")
        if arguments.browser == "all"
        else (arguments.browser,)
    )
    for name in names:
        exercise(name, arguments.base_url.rstrip("/"))


if __name__ == "__main__":
    main()
