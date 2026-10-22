# Visual regression workflow

The Chromium visual review captures the homepage hero, role cards, problem-led
cards, featured projects and site header; the case-study architecture, Related
Projects and footer; the project comparison dialog; and the mobile menu.
Component captures include the full architecture section and all comparison
cards, even when the live dialog scrolls. They hide the sticky site header so it
cannot obscure the component. Dedicated header captures show the header at
desktop and mobile widths, and mobile-menu captures show the expanded navigation
in its real overlay state. Dialog headers are static during capture so they
cannot obscure the comparison. Live workflow badges use a neutral, fixed-size
SVG during capture because their results can change without a site change;
functional browser smoke still loads the real badges.

Every region is captured in light and dark themes. Component captures include
desktop and mobile layouts; role and problem cards also include collapsed and
expanded states. Header captures include the closed desktop and mobile header;
mobile-menu captures include the expanded menu at mobile width.

CI compares every captured PNG with
`screenshots/portfolio-ux-review/baselines/`. A difference fails the job and
uploads the expected image, actual image and highlighted difference image under
the visual-review artifact.

## Reviewing baseline changes

Never refresh snapshots just to make CI green. Review each expected, actual and
difference image first, confirm the layout change is intentional, then run:

```powershell
python tools/compare_visual_baselines.py --accept-reviewed-baselines --review-note "Reviewed the hero, role, problem, featured, architecture, comparison, related-project and footer captures for this change."
```

Commit the updated PNGs and the appended `baseline-review.md` record with the
layout change. CI never accepts or rewrites baselines. The initial baseline set
must be populated from the same pinned Chromium workflow used by CI.
