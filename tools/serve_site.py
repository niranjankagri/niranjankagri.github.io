"""Serve a static site with GitHub Pages-style 404 handling for browser smoke."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class PagesHandler(SimpleHTTPRequestHandler):
    """Return the site's 404 document with the original missing-route status."""

    def send_error(self, code: int, message: str | None = None, explain: str | None = None) -> None:
        if code == 404:
            not_found = Path(self.directory or ".") / "404.html"
            if not_found.is_file():
                body = not_found.read_bytes()
                self.send_response(404, "File not found")
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(body)
                return
        super().send_error(code, message, explain)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", required=True, type=Path)
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument("--bind", default="127.0.0.1")
    arguments = parser.parse_args()
    directory = arguments.directory.resolve()
    handler = partial(PagesHandler, directory=str(directory))
    with ThreadingHTTPServer((arguments.bind, arguments.port), handler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
