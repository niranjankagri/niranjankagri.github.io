# Visual regression workflow

The Chromium visual review captures hero, role cards, problem-led cards, featured
projects, architecture, comparison, Related Projects and the case-study footer.
Every region includes desktop and mobile layouts in light and dark themes; role
and problem cards also include collapsed and expanded states.

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
