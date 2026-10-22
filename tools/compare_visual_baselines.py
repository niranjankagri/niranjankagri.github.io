"""Compare captured portfolio screenshots with explicitly reviewed baselines."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import shutil

from PIL import Image, ImageChops, ImageDraw, ImageStat

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASELINES = "screenshots/portfolio-ux-review/baselines"
DEFAULT_ACTUAL = "artifacts/visual-review/actual"
DEFAULT_FAILURES = "artifacts/visual-review/failures"


def in_root(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as error:
        raise SystemExit(f"Path must stay inside the repository: {relative}") from error
    return path


def write_difference(
    expected_path: Path, actual_path: Path, difference_path: Path
) -> None:
    if not expected_path.exists():
        actual = Image.open(actual_path).convert("RGB")
        placeholder = Image.new("RGB", actual.size, "#fff2f2")
        draw = ImageDraw.Draw(placeholder)
        draw.text((24, 24), "MISSING REVIEWED BASELINE", fill="#a40000")
        placeholder.save(difference_path)
        return

    expected = Image.open(expected_path).convert("RGB")
    actual = Image.open(actual_path).convert("RGB")
    if expected.size != actual.size:
        canvas = Image.new(
            "RGB",
            (max(expected.width, actual.width), max(expected.height, actual.height)),
            "#ffffff",
        )
        canvas.paste(actual, (0, 0))
        overlay = Image.new("RGB", expected.size, "#ff00ff")
        canvas.paste(overlay, (0, 0))
        canvas.save(difference_path)
        return

    difference = ImageChops.difference(expected, actual)
    # Amplify all changed pixels in red so even small layout shifts are visible.
    red = difference.getchannel("R")
    green = difference.getchannel("G")
    blue = difference.getchannel("B")
    amplified = Image.merge(
        "RGB",
        (red.point(lambda value: min(255, value * 4 + 48)), green, blue),
    )
    amplified.save(difference_path)


def write_missing_baseline(actual_path: Path, destination: Path) -> None:
    actual = Image.open(actual_path).convert("RGB")
    placeholder = Image.new("RGB", actual.size, "#fff2f2")
    ImageDraw.Draw(placeholder).text(
        (24, 24), "MISSING REVIEWED BASELINE", fill="#a40000"
    )
    placeholder.save(destination)


def differs(expected_path: Path, actual_path: Path, threshold: int) -> tuple[bool, str]:
    if not expected_path.exists():
        return True, "missing baseline"
    expected = Image.open(expected_path).convert("RGB")
    actual = Image.open(actual_path).convert("RGB")
    if expected.size != actual.size:
        return True, f"dimensions differ: expected {expected.size}, got {actual.size}"
    difference = ImageChops.difference(expected, actual)
    extrema = difference.getextrema()
    max_channel_delta = max(channel[1] for channel in extrema)
    if max_channel_delta > threshold:
        mean_delta = sum(ImageStat.Stat(difference).mean) / 3
        return (
            True,
            f"pixel delta {max_channel_delta} > {threshold} (mean {mean_delta:.3f})",
        )
    return False, "matches"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baselines", default=DEFAULT_BASELINES)
    parser.add_argument("--actual", default=DEFAULT_ACTUAL)
    parser.add_argument("--failures", default=DEFAULT_FAILURES)
    parser.add_argument("--pixel-threshold", type=int, default=0)
    parser.add_argument(
        "--accept-reviewed-baselines",
        action="store_true",
        help="Replace baselines only after the screenshot changes were reviewed.",
    )
    parser.add_argument(
        "--review-note",
        default="",
        help="Required review record when accepting new or changed baselines.",
    )
    arguments = parser.parse_args()
    if not 0 <= arguments.pixel_threshold <= 255:
        parser.error("--pixel-threshold must be between 0 and 255")

    baselines = in_root(arguments.baselines)
    actual = in_root(arguments.actual)
    failures = in_root(arguments.failures)
    images = sorted(actual.glob("*.png"))
    if not images:
        raise SystemExit(f"No screenshots found in {actual}")

    if arguments.accept_reviewed_baselines:
        if not arguments.review_note.strip():
            parser.error("--review-note is required when accepting baselines")
        baselines.mkdir(parents=True, exist_ok=True)
        for image in images:
            shutil.copy2(image, baselines / image.name)
        record = ROOT / "screenshots" / "portfolio-ux-review" / "baseline-review.md"
        record.parent.mkdir(parents=True, exist_ok=True)
        with record.open("a", encoding="utf-8") as stream:
            stream.write(
                f"\n- {date.today().isoformat()}: {arguments.review_note.strip()}\n"
            )
        print(f"Accepted {len(images)} reviewed baselines in {baselines}.")
        return

    failures.mkdir(parents=True, exist_ok=True)
    issues: list[str] = []
    expected_missing = 0
    for image in images:
        expected = baselines / image.name
        is_different, reason = differs(expected, image, arguments.pixel_threshold)
        if not is_different:
            continue
        expected_missing += not expected.exists()
        issues.append(f"{image.name}: {reason}")
        shutil.copy2(image, failures / f"{image.stem}-actual.png")
        if expected.exists():
            shutil.copy2(expected, failures / f"{image.stem}-expected.png")
        else:
            write_missing_baseline(image, failures / f"{image.stem}-expected.png")
        write_difference(expected, image, failures / f"{image.stem}-difference.png")

    unexpected = sorted(
        baseline.name
        for baseline in baselines.glob("*.png")
        if not (actual / baseline.name).exists()
    )
    if unexpected:
        issues.extend(
            f"{name}: baseline has no captured screenshot" for name in unexpected
        )

    if issues:
        print("Visual regression differences:")
        print("\n".join(f"- {issue}" for issue in issues))
        if expected_missing:
            print(
                f"{expected_missing} reviewed baselines are missing. Review the capture "
                "diffs, then accept updates with --accept-reviewed-baselines and --review-note."
            )
        raise SystemExit(1)
    print(f"All {len(images)} screenshots match reviewed baselines.")


if __name__ == "__main__":
    main()
