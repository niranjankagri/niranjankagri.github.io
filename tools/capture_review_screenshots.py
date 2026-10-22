"""Capture the reviewed visual-regression regions in both themes and layouts."""

from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

ROOT = Path(__file__).resolve().parent.parent
VIEWPORTS = (("desktop", 1440), ("mobile", 390))
THEMES = ("light", "dark")
QUIET_STYLE = "*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}"


def open_page(page: Page, base_url: str, route: str, width: int, theme: str) -> None:
    page.set_viewport_size({"width": width, "height": 1000 if width > 600 else 900})
    page.goto(base_url + route, wait_until="domcontentloaded")
    page.add_style_tag(content=QUIET_STYLE)
    page.evaluate(
        "theme => { document.documentElement.dataset.theme = theme; "
        "document.documentElement.style.scrollbarGutter = 'stable'; }",
        theme,
    )
    page.evaluate(
        "() => document.querySelectorAll('img').forEach(image => image.loading = 'eager')"
    )
    page.evaluate(
        "async () => { await document.fonts.ready; "
        "await Promise.all(Array.from(document.images).map(image => image.decode().catch(() => {}))); }"
    )


def capture_region(page: Page, selector: str, destination: Path, width: int) -> None:
    target = page.locator(selector)
    target.wait_for(state="visible")
    geometry = target.evaluate(
        "element => { const rect = element.getBoundingClientRect(); "
        "return { y: rect.top + scrollY, height: rect.height }; }"
    )
    nav_height = page.locator(".nav").evaluate(
        "element => element.getBoundingClientRect().height"
    )
    page.set_viewport_size(
        {"width": width, "height": max(500, round(geometry["height"] + nav_height))}
    )
    page.evaluate("y => window.scrollTo(0, Math.max(0, y))", geometry["y"] - nav_height)
    page.screenshot(path=str(destination), animations="disabled")


def output_path(output: Path, name: str, width_name: str, theme: str) -> Path:
    return output / f"{name}-{width_name}-{theme}.png"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8765")
    parser.add_argument("--output", default="artifacts/visual-review/actual")
    arguments = parser.parse_args()
    output = (ROOT / arguments.output).resolve()
    try:
        output.relative_to(ROOT.resolve())
    except ValueError as error:
        raise SystemExit(
            "Screenshot output must stay inside the repository."
        ) from error
    output.mkdir(parents=True, exist_ok=True)
    base_url = arguments.base_url.rstrip("/")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(reduced_motion="reduce")

        # Primary homepage components, including the collapsed role and problem paths.
        for width_name, width in VIEWPORTS:
            for theme in THEMES:
                open_page(page, base_url, "/", width, theme)
                for name, selector in (
                    ("hero", ".hero"),
                    ("role-cards", "#role-explorer"),
                    ("problem-cards", "#focus-explorer"),
                    ("featured-projects", "#projects"),
                ):
                    capture_region(
                        page,
                        selector,
                        output_path(output, name, width_name, theme),
                        width,
                    )

                # Capture one expanded example of each disclosure set at every size/theme.
                role = page.locator("[data-role-panel]").first
                role.evaluate("element => element.open = true")
                capture_region(
                    page,
                    "#role-explorer",
                    output_path(output, "role-card-expanded", width_name, theme),
                    width,
                )
                focus = page.locator("[data-exploration-panel]").first
                focus.evaluate("element => element.open = true")
                capture_region(
                    page,
                    "#focus-explorer",
                    output_path(output, "problem-card-expanded", width_name, theme),
                    width,
                )

        # Architecture, Related Projects and footer from a generated case study.
        for width_name, width in VIEWPORTS:
            for theme in THEMES:
                open_page(page, base_url, "/projects/enterprise.html", width, theme)
                capture_region(
                    page,
                    "#architecture",
                    output_path(output, "architecture", width_name, theme),
                    width,
                )
                capture_region(
                    page,
                    ".related-projects",
                    output_path(output, "related-projects", width_name, theme),
                    width,
                )
                capture_region(
                    page,
                    "footer",
                    output_path(output, "case-footer", width_name, theme),
                    width,
                )

        # The same comparison dialog is reviewed at a desktop and mobile width.
        for width_name, width in VIEWPORTS:
            for theme in THEMES:
                open_page(page, base_url, "/projects.html", width, theme)
                for index in range(3):
                    page.locator("#project-grid .project-card").nth(index).locator(
                        "[data-compare-project]"
                    ).click()
                page.locator("#open-comparison").click()
                page.locator("#comparison-dialog").wait_for(state="visible")
                page.locator("#comparison-dialog").screenshot(
                    path=str(output_path(output, "comparison", width_name, theme)),
                    animations="disabled",
                )
                page.keyboard.press("Escape")

        browser.close()
    print(f"Visual regression screenshots written to {output}.")


if __name__ == "__main__":
    main()
