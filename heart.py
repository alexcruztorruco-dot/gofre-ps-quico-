#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
heart.py

This script draws a parametric heart. It supports two modes:
- turtle (interactive window using the turtle/tkinter GUI)
- matplotlib (headless-friendly; can save to PNG)

Usage:
  python heart.py           # auto mode: uses turtle if available, otherwise saves PNG
  python heart.py --mode turtle
  python heart.py --mode matplotlib --output heart.png
  python heart.py --mode save --output heart.png   # alias for matplotlib+save

The matplotlib mode makes the script reproducible in headless environments (CI, servers)
by saving an image instead of requiring a display.
"""

import sys
import os
import math
import argparse

try:
    import turtle
    _HAS_TURTLE = True
except Exception:
    _HAS_TURTLE = False

# matplotlib is optional but used for headless reproducible output
try:
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    _HAS_MPL = True
except Exception:
    _HAS_MPL = False


def compute_heart(scale=1.0, step_deg=2):
    """Return lists of x,y coordinates for one heart scaled by `scale`.
    step_deg controls sampling density (degrees per step).
    """
    xs = []
    ys = []
    for deg in range(0, 360, step_deg):
        angle = math.radians(deg)
        x = 16 * (math.sin(angle) ** 3) * scale
        y = (13 * math.cos(angle)
             - 5 * math.cos(2 * angle)
             - 2 * math.cos(3 * angle)
             - math.cos(4 * angle)) * scale
        xs.append(x)
        ys.append(y)
    return xs, ys


def draw_with_turtle(scales, message="¿QUIERES SER MI NOVIA?"):
    """Draw hearts using turtle (interactive)."""
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.setup(width=800, height=600)
    screen.title("Corazón")

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.color("#ffb6c1")
    t.pensize(2)

    for scale in scales:
        t.penup()
        first_point = True
        xs, ys = compute_heart(scale=scale, step_deg=2)
        for x, y in zip(xs, ys):
            if first_point:
                t.goto(x, y)
                t.pendown()
                first_point = False
            else:
                t.goto(x, y)
        t.penup()

    t.goto(0, -30)
    t.color("white")
    t.write(message, align="center", font=("Arial", 24, "bold"))
    t.hideturtle()
    turtle.done()


def draw_with_matplotlib(scales, output_path=None, message="¿QUIERES SER MI NOVIA?", dpi=150):
    """Draw hearts with matplotlib. If output_path is provided, saves to PNG; otherwise shows the plot."""
    if not _HAS_MPL:
        raise RuntimeError("matplotlib is required for matplotlib/save mode but is not available")

    # Styling
    fig = plt.figure(figsize=(8, 6), facecolor="black")
    ax = fig.add_subplot(111)
    ax.set_facecolor("black")

    # Plot each scaled heart with slight alpha so layered effect appears
    colors = ["#ffb6c1"] * len(scales)
    for scale, color in zip(scales, colors):
        xs, ys = compute_heart(scale=scale, step_deg=1)
        ax.plot(xs, ys, color=color, linewidth=1.6, alpha=0.9)

    # Text
    ax.text(0, -30, message, color="white", fontsize=20, fontweight="bold",
            horizontalalignment="center")

    ax.set_aspect('equal', adjustable='datalim')
    ax.axis('off')

    # Adjust limits so the heart is nicely framed
    all_x = []
    all_y = []
    for scale in scales:
        xs, ys = compute_heart(scale=scale, step_deg=4)
        all_x.extend(xs)
        all_y.extend(ys)
    margin = 10
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin - 40, max(all_y) + margin)

    plt.tight_layout(pad=0)

    if output_path:
        # Create output directory if needed
        outdir = os.path.dirname(os.path.abspath(output_path))
        if outdir and not os.path.exists(outdir):
            os.makedirs(outdir, exist_ok=True)
        fig.savefig(output_path, dpi=dpi, facecolor=fig.get_facecolor())
        print(f"Saved image to: {output_path}")
    else:
        plt.show()


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Draw a heart (turtle or matplotlib).")
    p.add_argument('--mode', choices=['auto', 'turtle', 'matplotlib', 'save'], default='auto',
                   help='Drawing mode: turtle (GUI) or matplotlib (headless). "save" is alias for matplotlib with saving.')
    p.add_argument('--output', '-o', default='heart.png', help='Output filename for save/matplotlib modes')
    p.add_argument('--scales', default='11-16', help='Scale range as start-end (integers), default 11-16')
    p.add_argument('--message', default='¿QUIERES SER MI NOVIA?', help='Message to write on the image')
    return p.parse_args(argv)


def parse_scales(s: str):
    if '-' in s:
        a, b = s.split('-')
        try:
            a_i = int(a)
            b_i = int(b)
            if a_i <= b_i:
                return list(range(a_i, b_i + 1))
        except Exception:
            pass
    # fallback: single integer
    try:
        v = int(s)
        return [v]
    except Exception:
        return list(range(11, 17))


def main(argv=None):
    args = parse_args(argv)
    scales = parse_scales(args.scales)

    # Decide mode
    mode = args.mode
    if mode == 'auto':
        # prefer turtle if available and a display is present
        has_display = True
        # On Unix-like systems, DISPLAY must be set for tkinter to create windows
        if sys.platform != 'win32' and 'DISPLAY' not in os.environ:
            has_display = False
        if _HAS_TURTLE and has_display:
            mode = 'turtle'
        else:
            mode = 'matplotlib'

    if mode == 'turtle':
        if not _HAS_TURTLE:
            print('turtle is not available in this environment. Falling back to matplotlib (saved image).')
            if not _HAS_MPL:
                raise RuntimeError('Neither turtle nor matplotlib are available.')
            draw_with_matplotlib(scales, output_path=args.output, message=args.message)
            return
        # If we reach here, turtle is available; run interactive draw
        draw_with_turtle(scales, message=args.message)

    elif mode in ('matplotlib', 'save'):
        if not _HAS_MPL:
            raise RuntimeError('matplotlib is required for this mode but is not installed.')
        draw_with_matplotlib(scales, output_path=(args.output if args.mode != 'matplotlib' or args.output else None),
                             message=args.message)
    else:
        raise ValueError('Unknown mode: ' + str(mode))


if __name__ == '__main__':
    main()
