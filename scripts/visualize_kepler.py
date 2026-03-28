"""
visualize_kepler.py — Visualize Kepler pixel data and light curves for an exoplanet.

Modes:
  Default   : Plot 2-panel pixel map (linear + log scale)
  --lightcurve : Plot PLD light curve (outliers removed, normalized flux)

Usage:
    python scripts/visualize_kepler.py --target "Kepler-8 b"
    python scripts/visualize_kepler.py --target "Kepler-8 b" --lightcurve
    python scripts/visualize_kepler.py --target "Kepler-8 b" --author SPOC --exptime 120
"""

import argparse
import os
import lightkurve as lk
import matplotlib.pyplot as plt
from astropy import units as u


OUTPUT_DIR = "output"


def slug(name):
    return name.replace(" ", "_").replace("/", "-")


def get_tpf(target, author, exptime_s):
    """Download TPF filtered by author + exptime."""
    print(f"Searching pixel files: target={target}, author={author}, exptime={exptime_s}s")
    results = lk.search_targetpixelfile(target)
    if results is None or len(results) == 0:
        raise RuntimeError(f"No pixel files found for '{target}'.")

    def _exptime_s(r):
    val = r.exptime.value
    return float(val.flat[0] if hasattr(val, 'flat') else val)

    mask = [
      str(r.author) == author and abs(_exptime_s(r) - exptime_s) < 5
      for r in results
    ]
    filtered = results[mask]
    if len(filtered) == 0:
        # Try author only
        mask2 = [str(r.author) == author for r in results]
        filtered = results[mask2]
    if len(filtered) == 0:
        filtered = results  # fallback to all

    print(f"  Downloading first of {len(filtered)} matches...")
    return filtered[0].download(quality_bitmask="default")


def plot_pixel_map(tpf, target):
    """2-panel: linear + log scale pixel map."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    tpf.plot(ax=axes[0], aperture_mask=tpf.pipeline_mask,
             title=f"Exoplanet {target} — Linear")
    tpf.plot(ax=axes[1], aperture_mask=tpf.pipeline_mask,
             scale="log", title=f"Exoplanet {target} — Log Scale")

    fig.tight_layout()
    out = os.path.join(OUTPUT_DIR, f"kepler_pixel_{slug(target)}.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved pixel map → {out}")
    return out


def plot_lightcurve(tpf, target):
    """PLD light curve, outliers removed, normalized."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    lc = tpf.to_lightcurve(method="pld").remove_outliers().flatten()

    fig, ax = plt.subplots(figsize=(13, 4))
    lc.plot(ax=ax, c="green", alpha=0.8)
    ax.set_xlabel(ax.get_xlabel(), fontsize=10)
    ax.set_ylabel(ax.get_ylabel(), fontsize=10)
    ax.set_title(f"Exoplanet {target} — Light Curve (PLD, normalized)", fontsize=12)
    ax.tick_params(axis="both", labelsize=8)

    fig.tight_layout()
    out = os.path.join(OUTPUT_DIR, f"lightcurve_{slug(target)}.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved light curve → {out}")
    return out


def main():
    parser = argparse.ArgumentParser(description="Visualize Kepler pixel data")
    parser.add_argument("--target",     required=True, help="Planet/star name, e.g. 'Kepler-8 b'")
    parser.add_argument("--author",     default="Kepler", help="Pipeline author (default: Kepler)")
    parser.add_argument("--exptime",    type=int, default=60,
                        help="Exposure time in seconds (default: 60 for Kepler 1-min cadence)")
    parser.add_argument("--lightcurve", action="store_true",
                        help="Plot PLD light curve instead of pixel map")
    args = parser.parse_args()

    tpf = get_tpf(args.target, args.author, args.exptime)

    if args.lightcurve:
        out = plot_lightcurve(tpf, args.target)
    else:
        out = plot_pixel_map(tpf, args.target)

    print(f"\nDone. Output: {out}")


if __name__ == "__main__":
    main()
