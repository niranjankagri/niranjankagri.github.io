"""Serve a staged site locally and run the Playwright browser smoke suite."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", default="_site")
    parser.add_argument("--build-id", required=True)
    parser.add_argument("--asset-version", required=True)
    parser.add_argument("--axe-script", default="")
    parser.add_argument(
        "--browser", choices=("chromium", "firefox", "webkit", "all"), default="all"
    )
    parser.add_argument("--artifacts", default="artifacts/browser-smoke")
    parser.add_argument(
        "--capture-review",
        default="",
        help="Capture section screenshots after smoke passes",
    )
    arguments = parser.parse_args()

    site = (ROOT / arguments.directory).resolve()
    artifacts = (ROOT / arguments.artifacts).resolve()
    try:
        site.relative_to(ROOT.resolve())
        artifacts.relative_to(ROOT.resolve())
    except ValueError as error:
        raise SystemExit(
            "Site and smoke artifacts must stay inside the repository."
        ) from error
    if not (site / "index.html").is_file() or not (site / "release.json").is_file():
        raise SystemExit(f"Staged site is incomplete: {site}")
    artifacts.mkdir(parents=True, exist_ok=True)
    server_log_path = artifacts / "server.log"
    smoke_log_path = artifacts / "run.log"
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    server_log = server_log_path.open("w", encoding="utf-8")
    server = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "http.server",
            str(port),
            "--bind",
            "127.0.0.1",
            "--directory",
            str(site),
        ],
        cwd=ROOT,
        stdout=server_log,
        stderr=subprocess.STDOUT,
    )
    base_url = f"http://127.0.0.1:{port}"
    try:
        ready = False
        for _ in range(50):
            if server.poll() is not None:
                break
            try:
                with urlopen(base_url + "/release.json", timeout=1) as response:
                    if response.status == 200:
                        ready = True
                        break
            except (OSError, URLError):
                time.sleep(0.1)
        if not ready:
            raise SystemExit(
                f"Local static server did not become ready. See {server_log_path}"
            )

        command = [
            sys.executable,
            str(ROOT / "tools" / "browser_smoke.py"),
            "--base-url",
            base_url,
            "--browser",
            arguments.browser,
            "--expected-build-id",
            arguments.build_id,
            "--expected-asset-version",
            arguments.asset_version,
        ]
        if arguments.axe_script:
            command.extend(
                ("--axe-script", str((ROOT / arguments.axe_script).resolve()))
            )
        smoke_environment = os.environ.copy()
        smoke_environment["PORTFOLIO_SMOKE_ARTIFACTS"] = str(artifacts)
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=smoke_environment,
            capture_output=True,
            text=True,
            check=False,
        )
        smoke_log_path.write_text(result.stdout + result.stderr, encoding="utf-8")
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        if result.returncode:
            print(
                f"Browser smoke failed; logs and failure screenshots are in {artifacts}.",
                file=sys.stderr,
            )
            raise SystemExit(result.returncode)
        if arguments.capture_review:
            screenshot_command = [
                sys.executable,
                str(ROOT / "tools" / "capture_review_screenshots.py"),
                "--base-url",
                base_url,
                "--output",
                arguments.capture_review,
            ]
            screenshots = subprocess.run(
                screenshot_command,
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            smoke_log_path.write_text(
                smoke_log_path.read_text(encoding="utf-8")
                + screenshots.stdout
                + screenshots.stderr,
                encoding="utf-8",
            )
            print(screenshots.stdout, end="")
            if screenshots.stderr:
                print(screenshots.stderr, end="", file=sys.stderr)
            if screenshots.returncode:
                raise SystemExit(screenshots.returncode)
        print(f"Browser smoke passed on {base_url}. Logs: {smoke_log_path}")
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=5)
        server_log.close()


if __name__ == "__main__":
    main()
