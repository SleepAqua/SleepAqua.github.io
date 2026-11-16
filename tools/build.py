#!/usr/bin/env python3
"""Build index.html from tools/index.template.html.

The two chart figures are generated here rather than checked in as images, so the
numbers in them come straight from the tool output they describe. Everything the
script needs is in this file; it writes index.html next to the repo root.

    python3 tools/build.py

Chart data, from actual runs (see each project's README):
  mahjong-mc  --games 2000 --policies greedy,defensive,defensive,defensive --seed 7
  GapFiller   ./run.sh --rounds 2000 --workers 2   (2,000 per strategy, 10,000 games)
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INK = "#c9c5be"
DIM = "#8a867f"
GRID = "rgba(255,255,255,0.08)"
SAGE = "#8fb8a0"
CLAY = "#c98a5e"
MONO = "ui-monospace,monospace"


def mahjong():
    """Win rate and deal-in rate per seat, 2,000 games, seed 7."""
    rows = [
        ("0 greedy", 16.65, 14.40),
        ("1 defensive", 19.00, 13.75),
        ("2 defensive", 17.25, 14.10),
        ("3 defensive", 20.35, 12.90),
    ]
    W, LEFT, LABEL_W = 440, 78, 70
    TOP, ROW_H = 30, 27
    plot_w = W - LEFT - 42
    vmax = 22.0
    px = lambda v: v / vmax * plot_w
    body_h = ROW_H * len(rows)
    h = TOP + body_h + 20
    out = [f'<svg viewBox="0 0 {W} {h}" role="img" aria-label="Win rate and deal-in rate by policy, 2,000 games">']
    ly = 6
    out.append(f'<rect x="{LEFT}" y="{ly}" width="7" height="7" rx="1.5" fill="{SAGE}"/>')
    out.append(f'<text x="{LEFT+11}" y="{ly+6}" fill="{DIM}" font-size="8" font-family="{MONO}">win %</text>')
    out.append(f'<rect x="{LEFT+58}" y="{ly}" width="7" height="7" rx="1.5" fill="{CLAY}"/>')
    out.append(f'<text x="{LEFT+69}" y="{ly+6}" fill="{DIM}" font-size="8" font-family="{MONO}">deal-in %</text>')
    for v in (0, 5, 10, 15, 20):
        x = LEFT + px(v)
        out.append(f'<line x1="{x:.1f}" y1="{TOP-8}" x2="{x:.1f}" y2="{TOP+body_h-8}" stroke="{GRID}"/>')
        out.append(f'<text x="{x:.1f}" y="{TOP+body_h+8}" fill="{DIM}" font-size="8.5" '
                   f'font-family="{MONO}" text-anchor="middle">{v}%</text>')
    for i, (name, win, deal) in enumerate(rows):
        y = TOP + i * ROW_H
        out.append(f'<text x="{LABEL_W}" y="{y+11}" fill="{INK}" font-size="9.5" '
                   f'font-family="{MONO}" text-anchor="end">{name}</text>')
        out.append(f'<rect x="{LEFT}" y="{y}" width="{px(win):.1f}" height="7" rx="1.5" fill="{SAGE}"/>')
        out.append(f'<text x="{LEFT+px(win)+5:.1f}" y="{y+6.5}" fill="{DIM}" font-size="8" '
                   f'font-family="{MONO}">{win:.2f}</text>')
        out.append(f'<rect x="{LEFT}" y="{y+10}" width="{px(deal):.1f}" height="7" rx="1.5" fill="{CLAY}"/>')
        out.append(f'<text x="{LEFT+px(deal)+5:.1f}" y="{y+16.5}" fill="{DIM}" font-size="8" '
                   f'font-family="{MONO}">{deal:.2f}</text>')
    out.append("</svg>")
    return "\n".join(out)


def gapfiller():
    """Mean score with one standard error, 2,000 games per strategy."""
    rows = [
        ("upper_plan", 155.44, 1.28),
        ("high_faces", 138.21, 0.94),
        ("heuristic", 130.06, 1.38),
        ("chase_yahtzee", 118.74, 0.86),
        ("random", 110.49, 0.64),
    ]
    W, LEFT, LABEL_W, TOP, ROW_H, RIGHT_PAD = 440, 70, 76, 16, 24, 106
    plot_w = W - LEFT - RIGHT_PAD
    vmin, vmax = 100.0, 160.0
    px = lambda v: (v - vmin) / (vmax - vmin) * plot_w
    body_h = ROW_H * len(rows)
    h = TOP + body_h + 20
    out = [f'<svg viewBox="0 0 {W} {h}" role="img" aria-label="Mean score with one standard error, 2,000 games per strategy">']
    for v in (100, 120, 140, 160):
        x = LEFT + px(v)
        out.append(f'<line x1="{x:.1f}" y1="{TOP-6}" x2="{x:.1f}" y2="{TOP+body_h-10}" stroke="{GRID}"/>')
        out.append(f'<text x="{x:.1f}" y="{TOP+body_h+8}" fill="{DIM}" font-size="8.5" '
                   f'font-family="{MONO}" text-anchor="middle">{v}</text>')
    for i, (name, mean, se) in enumerate(rows):
        y = TOP + i * ROW_H + 6
        x = LEFT + px(mean)
        out.append(f'<text x="{LABEL_W}" y="{y+3}" fill="{INK}" font-size="9.5" '
                   f'font-family="{MONO}" text-anchor="end">{name}</text>')
        out.append(f'<line x1="{x-px(se):.1f}" y1="{y}" x2="{x+px(se):.1f}" y2="{y}" '
                   f'stroke="{CLAY}" stroke-width="3" opacity="0.55"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y}" r="3" fill="{SAGE}"/>')
        out.append(f'<text x="{W-2}" y="{y+3}" fill="{DIM}" font-size="8.5" '
                   f'font-family="{MONO}" text-anchor="end">{mean:.2f} ± {se:.2f}</text>')
    out.append("</svg>")
    return "\n".join(out)


def main():
    tpl = (ROOT / "tools" / "index.template.html").read_text()
    html = tpl.replace("{{SVG_MAHJONG}}", mahjong()).replace("{{SVG_GAPFILLER}}", gapfiller())
    if "{{" in html:
        raise SystemExit("unreplaced placeholder left in template")
    (ROOT / "index.html").write_text(html)
    print(f"wrote index.html ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
