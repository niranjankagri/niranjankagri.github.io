"""Capture the reviewed visual-regression regions in both themes and layouts."""

from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

ROOT = Path(__file__).resolve().parent.parent
VIEWPORTS = (("desktop", 1440), ("mobile", 390))
THEMES = ("light", "dark")
CAPTURE_STYLE = (
    ".nav{visibility:hidden!important}.drawer-head{position:static!important}"
)
HEADER_CAPTURE_STYLE = (
    ".nav{visibility:visible!important;position:relative!important;top:auto!important}"
)
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


def capture_region(
    page: Page,
    selector: str,
    destination: Path,
    width: int,
    *,
    style: str = CAPTURE_STYLE,
) -> None:
    target = page.locator(selector)
    target.wait_for(state="visible")
    # Capture the whole component, independent of the current viewport height.
    # In particular, the architecture heading is not the architecture section.
    target.screenshot(path=str(destination), animations="disabled", style=style)


def capture_mobile_menu(page: Page, destination: Path) -> None:
    page.locator(".menu-toggle").click()
    menu = page.locator("#primary-nav")
    menu.wait_for(state="visible")
    page.evaluate("window.scrollTo(0, 0)")

    header_box = page.locator(".nav").bounding_box()
    menu_box = menu.bounding_box()
    if header_box is None or menu_box is None:
        raise RuntimeError("Could not measure the open mobile navigation.")

    height = max(
        header_box["y"] + header_box["height"],
        menu_box["y"] + menu_box["height"],
    )
    page.screenshot(
        path=str(destination),
        clip={
            "x": 0,
            "y": 0,
            "width": page.viewport_size["width"],
            "height": height,
        },
        animations="disabled",
        style=HEADER_CAPTURE_STYLE,
    )
    page.locator(".menu-toggle").click()
    menu.wait_for(state="hidden")


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
        # Workflow outcomes change independently of this site. Keep badge geometry
        # deterministic in visual captures; browser smoke still tests real images.
        page.route(
            "**/badge.svg",
            lambda route: route.fulfill(
                content_type="image/svg+xml",
                body='<svg xmlns="http://www.w3.org/2000/svg" width="150" height="20">'
                '<rect width="150" height="20" rx="3" fill="#425956"/>'
                '<text x="75" y="14" text-anchor="middle" fill="white" '
                'font-family="sans-serif" font-size="11">Workflow history</text></svg>',
            ),
        )

        # Primary homepage components, including the collapsed role and problem paths.
        for width_name, width in VIEWPORTS:
            for theme in THEMES:
                open_page(page, base_url, "/", width, theme)
                for name, selector in (
                    ("hero", ".hero"),
                    ("role-cards", "#role-explorer"),
                    ("problem-cards", "#focus-explorer"),
                    ("featured-projects", "#projects"),
                    ("dashboard-showcase", "#quality-intelligence"),
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

        # Capture site chrome on its own page so opening the mobile menu cannot
        # affect the established component captures.
        header_page = browser.new_page(reduced_motion="reduce")
        for width_name, width in VIEWPORTS:
            for theme in THEMES:
                open_page(header_page, base_url, "/", width, theme)
                capture_region(
                    header_page,
                    ".nav",
                    output_path(output, "header", width_name, theme),
                    width,
                    style=HEADER_CAPTURE_STYLE,
                )
                if width_name == "mobile":
                    capture_mobile_menu(
                        header_page,
                        output_path(output, "mobile-menu", width_name, theme),
                    )
        header_page.close()

        # Architecture, Related Projects and footer from a generated case study.
        for width_name, width in VIEWPORTS:
            for theme in THEMES:
                open_page(page, base_url, "/projects/enterprise.html", width, theme)
                capture_region(
                    page,
                    'section[aria-labelledby="architecture"]',
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
                # Include every comparison card on mobile, including content that
                # normally scrolls inside the dialog. This affects captures only.
                page.locator("#comparison-dialog").evaluate(
                    "element => { element.style.maxHeight = 'none'; "
                    "element.style.height = 'auto'; element.style.overflow = 'visible'; "
                    "element.style.position = 'relative'; element.style.inset = 'auto'; "
                    "element.style.margin = '0'; }"
                )
                page.locator("#comparison-dialog").screenshot(
                    path=str(output_path(output, "comparison", width_name, theme)),
                    animations="disabled",
                    style=CAPTURE_STYLE,
                )
                page.keyboard.press("Escape")

        browser.close()
    print(f"Visual regression screenshots written to {output}.")


if __name__ == "__main__":
    main()
