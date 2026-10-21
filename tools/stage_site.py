"""Copy the generated portfolio into a clean, deployable static directory."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "_site"
FILES = (
    "index.html",
    "projects.html",
    "404.html",
    "style.css",
    "theme.js",
    "projects.js",
    "robots.txt",
    "sitemap.xml",
    "Niranjan_Kumar_Agri_CV_Technical_Lead_QA_SDET.pdf",
)


def current_build_id(value: str) -> str:
    if value:
        return value
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "local"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--build-id", default="", help="Commit identifier embedded in the staged site"
    )
    arguments = parser.parse_args()
    build_id = current_build_id(arguments.build_id)
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", build_id):
        raise SystemExit(
            "Build id must contain only letters, digits, period, underscore or hyphen."
        )

    root = ROOT.resolve()
    output = OUTPUT.resolve()
    try:
        output.relative_to(root)
    except ValueError as error:
        raise SystemExit(
            f"Refusing to stage outside the repository: {output}"
        ) from error
    if output.parent != root or output.name != "_site":
        raise SystemExit(f"Refusing to replace unexpected staging path: {output}")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()

    for name in FILES:
        source = root / name
        if not source.is_file():
            raise SystemExit(f"Required generated site file is missing: {name}")
        shutil.copy2(source, output / name)
    for name in ("img", "projects"):
        source = root / name
        if not source.is_dir():
            raise SystemExit(f"Required generated site directory is missing: {name}")
        shutil.copytree(source, output / name)

    asset_match = re.search(
        r"style\.css\?v=([A-Za-z0-9]+)",
        (output / "index.html").read_text(encoding="utf-8"),
    )
    if not asset_match:
        raise SystemExit(
            "The generated home page has no versioned stylesheet reference."
        )
    asset_version = asset_match.group(1)
    for page in output.rglob("*.html"):
        content = page.read_text(encoding="utf-8")
        marker = f'<meta name="portfolio-build" content="{build_id}">'
        if re.search(
            r'<meta\s+name="portfolio-build"\s+content="[^"]*"\s*/?>', content
        ):
            content = re.sub(
                r'<meta\s+name="portfolio-build"\s+content="[^"]*"\s*/?>',
                marker,
                content,
            )
        else:
            content, count = re.subn(
                r"(<meta\s+name=\"viewport\"[^>]*>)", r"\1" + marker, content, count=1
            )
            if count != 1:
                raise SystemExit(
                    f"Could not add the build identifier to {page.relative_to(output)}"
                )
        page.write_text(content, encoding="utf-8", newline="\n")
    (output / "release.json").write_text(
        json.dumps({"build_id": build_id, "asset_version": asset_version}, indent=2)
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Staged site at {output} (build {build_id}, assets {asset_version}).")


if __name__ == "__main__":
    main()
