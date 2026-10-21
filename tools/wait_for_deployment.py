"""Wait a bounded period for GitHub Pages to serve the expected release."""

from __future__ import annotations

import argparse
import json
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import urlopen


def fetch(url: str) -> tuple[int, bytes]:
    with urlopen(url, timeout=10) as response:
        return response.status, response.read()


def verify(url: str, build_id: str, asset_version: str) -> tuple[bool, str]:
    try:
        release_status, release_body = fetch(urljoin(url, "release.json"))
        if release_status != 200:
            return False, f"release.json returned {release_status}"
        release = json.loads(release_body)
        if release.get("build_id") != build_id:
            return (
                False,
                f"release.json has build {release.get('build_id')!r}, expected {build_id!r}",
            )
        if release.get("asset_version") != asset_version:
            return (
                False,
                f"release.json has asset version {release.get('asset_version')!r}, expected {asset_version!r}",
            )

        home_status, home_body = fetch(urljoin(url, ""))
        home = home_body.decode("utf-8", errors="replace")
        if home_status != 200:
            return False, f"homepage returned {home_status}"
        if f'<meta name="portfolio-build" content="{build_id}">' not in home:
            return False, "homepage build identifier does not match"
        if f"style.css?v={asset_version}" not in home:
            return False, "homepage does not reference the expected stylesheet version"
        if f"theme.js?v={asset_version}" not in home:
            return False, "homepage does not reference the expected script version"
        for name in ("style.css", "theme.js", "projects.js"):
            asset_status, _ = fetch(urljoin(url, f"{name}?v={asset_version}"))
            if asset_status != 200:
                return False, f"{name} returned {asset_status}"
        return True, f"release {build_id} with assets {asset_version} is live"
    except (OSError, ValueError, HTTPError, URLError) as error:
        return False, str(error)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--build-id", required=True)
    parser.add_argument("--asset-version", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--interval-seconds", type=int, default=10)
    arguments = parser.parse_args()
    url = arguments.url.rstrip("/") + "/"
    attempts = max(
        1, arguments.timeout_seconds // max(1, arguments.interval_seconds) + 1
    )
    latest = "not checked"
    for attempt in range(1, attempts + 1):
        ready, latest = verify(url, arguments.build_id, arguments.asset_version)
        if ready:
            print(latest)
            return
        print(f"Deployment check {attempt}/{attempts}: {latest}")
        if attempt < attempts:
            time.sleep(max(1, arguments.interval_seconds))
    raise SystemExit(
        f"Deployment was not ready with the expected build after {attempts} checks: {latest}"
    )


if __name__ == "__main__":
    main()
