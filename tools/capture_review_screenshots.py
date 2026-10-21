"""Capture repeatable screenshots of key portfolio UI sections for PR review."""

from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent


def capture_visible_section(page, target, destination: Path, width: int) -> None:
    rect = target.evaluate(
        "element => { const box = element.getBoundingClientRect(); return {y: box.top + scrollY, height: box.height}; }"
    )
    header_height = page.locator(".nav").evaluate(
        "element => element.getBoundingClientRect().height"
    )
    page.set_viewport_size(
        {"width": width, "height": round(rect["height"] + header_height)}
    )
    page.evaluate("y => window.scrollTo(0, Math.max(0, y))", rect["y"] - header_height)
    page.screenshot(path=str(destination), animations="disabled")


def capture_section(
    page,
    base_url: str,
    route: str,
    selector: str,
    destination: Path,
    theme: str,
    width: int,
) -> None:
    height = 1000 if width >= 1000 else 900
    page.set_viewport_size({"width": width, "height": height})
    page.goto(base_url + route, wait_until="domcontentloaded")
    page.add_style_tag(
        content="*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}"
    )
    page.evaluate("theme => document.documentElement.dataset.theme = theme", theme)
    target = page.locator(selector)
    target.scroll_into_view_if_needed()
    page.evaluate("() => document.fonts.ready")
    page.evaluate(
        "selector => { document.querySelectorAll(selector + ' img').forEach(image => image.loading = 'eager'); }",
        selector,
    )
    page.evaluate(
        "async selector => { await Promise.all(Array.from(document.querySelectorAll(selector + ' img')).map(image => image.decode().catch(() => {}))); }",
        selector,
    )
    capture_visible_section(page, target, destination, width)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8765")
    parser.add_argument("--output", default="screenshots/portfolio-ux-review")
    arguments = parser.parse_args()
    output = (ROOT / arguments.output).resolve()
    try:
        output.relative_to(ROOT.resolve())
    except ValueError as error:
        raise SystemExit(
            "Screenshot output must stay inside the repository."
        ) from error
    output.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 1000}, reduced_motion="reduce"
        )
        page = context.new_page()
        page.add_style_tag(
            content="*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}"
        )
        base_url = arguments.base_url.rstrip("/")

        for selector_name, selector in (
            ("hero", ".hero"),
            ("role", "#role-explorer"),
            ("featured", "#projects"),
            ("contact", "#contact"),
        ):
            for width_name, width in (
                ("desktop", 1440),
                ("tablet", 768),
                ("mobile", 390),
            ):
                for theme in ("light", "dark"):
                    path = output / f"{selector_name}-{width_name}-{theme}.png"
                    capture_section(page, base_url, "/", selector, path, theme, width)

        for role_id in ("senior-sdet", "qa-lead", "automation-architect"):
            for width_name, width, theme in (
                ("desktop", 1440, "light"),
                ("mobile", 390, "dark"),
            ):
                page.set_viewport_size({"width": width, "height": 1000})
                page.goto(base_url + "/", wait_until="domcontentloaded")
                page.add_style_tag(
                    content="*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}"
                )
                page.evaluate(
                    "value => document.documentElement.dataset.theme = value", theme
                )
                panel = page.locator(f'[data-role-panel="{role_id}"]')
                panel.locator("summary").click()
                page.evaluate("() => document.fonts.ready")
                capture_visible_section(
                    page,
                    page.locator("#role-explorer"),
                    output / f"role-expanded-{role_id}-{width_name}-{theme}.png",
                    width,
                )

        for width_name, width, height in (
            ("desktop", 1440, 1100),
            ("mobile", 390, 900),
        ):
            for theme in ("light", "dark"):
                page.set_viewport_size({"width": width, "height": height})
                page.goto(base_url + "/projects.html", wait_until="domcontentloaded")
                page.add_style_tag(
                    content="*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}"
                )
                page.evaluate(
                    "value => document.documentElement.dataset.theme = value", theme
                )
                page.evaluate("() => document.fonts.ready")
                page.evaluate(
                    "() => document.querySelectorAll('img').forEach(image => image.loading = 'eager')"
                )
                page.evaluate(
                    "async () => await Promise.all(Array.from(document.images).map(image => image.decode().catch(() => {})))"
                )
                page.screenshot(
                    path=str(output / f"collection-{width_name}-{theme}.png"),
                    full_page=False,
                    animations="disabled",
                )

        architecture_pages = (
            ("enterprise", "/projects/enterprise.html", 0),
            ("quality-intelligence", "/projects/quality-intelligence.html", 0),
            ("playwright-typescript", "/projects/playwright-typescript.html", 0),
        )
        for slug, route, selected in architecture_pages:
            for theme in ("light", "dark"):
                page.set_viewport_size({"width": 1440, "height": 1000})
                page.goto(base_url + route, wait_until="domcontentloaded")
                page.add_style_tag(
                    content="*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}"
                )
                page.evaluate(
                    "value => document.documentElement.dataset.theme = value", theme
                )
                page.evaluate("() => document.fonts.ready")
                tabs = page.locator(".architecture-component-tabs [role=tab]")
                tabs.nth(selected).click()
                page.locator(".architecture-explorer").screenshot(
                    path=str(output / f"architecture-{slug}-desktop-{theme}.png"),
                    animations="disabled",
                )
            page.set_viewport_size({"width": 390, "height": 844})
            page.goto(base_url + route, wait_until="domcontentloaded")
            page.add_style_tag(
                content="*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}"
            )
            page.evaluate("document.documentElement.dataset.theme = 'dark'")
            mobile_component = page.locator(
                ".architecture-fallback [data-architecture-item]"
            ).last
            mobile_component.locator("summary").click()
            page.locator(".architecture-explorer").screenshot(
                path=str(output / f"architecture-{slug}-mobile-expanded-dark.png"),
                animations="disabled",
            )

        for slug, route in (
            ("enterprise", "/projects/enterprise.html"),
            ("playwright-typescript", "/projects/playwright-typescript.html"),
        ):
            page.set_viewport_size({"width": 1182, "height": 520})
            page.goto(base_url + route, wait_until="domcontentloaded")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.screenshot(
                path=str(output / f"case-footer-{slug}.png"), animations="disabled"
            )

        page.set_viewport_size({"width": 1440, "height": 1000})
        page.goto(base_url + "/projects.html", wait_until="domcontentloaded")
        page.add_style_tag(
            content="*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}"
        )
        for index in range(3):
            page.locator("#project-grid .project-card").nth(index).locator(
                "[data-compare-project]"
            ).click()
        page.locator("#open-comparison").click()
        page.locator("#comparison-dialog").screenshot(
            path=str(output / "comparison-desktop-light.png"), animations="disabled"
        )
        page.keyboard.press("Escape")
        browser.close()
    print(f"Review screenshots written to {output}.")


if __name__ == "__main__":
    main()
