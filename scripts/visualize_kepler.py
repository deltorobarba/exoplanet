"""
visualize_kepler.py — Visualize pixel data and light curves for an exoplanet.

Auto-detects the best available mission data (Kepler → K2 → SPOC/TESS).
Use --author to override.

Modes:
  Default      : Plot 2-panel pixel map (linear + log scale)
  --lightcurve : Plot PLD light curve (outliers removed, normalized flux)

Usage:
    python scripts/visualize_kepler.py --target "Kepler-8 b"
    python scripts/visualize_kepler.py --target "TRAPPIST-1 b"
    python scripts/visualize_kepler.py --target "Kepler-8 b" --lightcurve
    python scripts/visualize_kepler.py --target "K2-18 b" --author SPOC --exptime 120
"""

import argparse
import os
import lightkurve as lk
import matplotlib.pyplot as plt
from astropy import units as u


OUTPUT_DIR = "output"

# Priority order for auto-detection: best cadence / most reliable first
AUTHOR_PRIORITY = ["Kepler", "K2", "SPOC", "TESS-SPOC", "QLP"]


def slug(name):
    return name.replace(" ", "_").replace("/", "-")


def _exptime_s(r):
    val = r.exptime.value
    return float(val.flat[0] if hasattr(val, "flat") else val)


def get_tpf(target, author_override, exptime_s):
    """
    Download TPF for target. If author_override is None, auto-detect the best
    available source using AUTHOR_PRIORITY. Falls back to any available data.
    """
    print(f"Searching pixel files for: {target}")
    results = lk.search_targetpixelfile(target)

    if results is None or len(results) == 0:
        raise RuntimeError(f"No pixel files found for '{target}'.")

    print(f"  Found {len(results)} total file(s) across all missions.")

    # --- Manual override ---
    if author_override is not None:
        print(f"  Using specified author: {author_override}")
        mask = [str(r.author) == author_override for r in results]
        filtered = results[mask]
        if len(filtered) == 0:
            print(f"  ⚠️  No files found for author='{author_override}'. "
                  f"Available: {sorted(set(str(r.author) for r in results))}")
            print("  Falling back to auto-detection.")
        else:
            exp_mask = [abs(_exptime_s(r) - exptime_s) < 5 for r in filtered]
            best = filtered[exp_mask] if any(exp_mask) else filtered
            print(f"  Downloading first of {len(best)} match(es)...")
            return filtered[0].download(quality_bitmask="default"), author_override

    # --- Auto-detection by priority ---
    available_authors = set(str(r.author) for r in results)
    print(f"  Available authors: {sorted(available_authors)}")

    for preferred in AUTHOR_PRIORITY:
        if preferred not in available_authors:
            continue
        mask = [str(r.author) == preferred for r in results]
        filtered = results[mask]
        if len(filtered) == 0:
            continue

        # Within this author, prefer shortest exptime (best cadence)
        filtered_sorted = sorted(filtered, key=_exptime_s)
        chosen = filtered_sorted[0]
        chosen_exp = _exptime_s(chosen)

        print(f"  ✓ Auto-selected: author={preferred}, exptime={chosen_exp:.0f}s")
        return chosen.download(quality_bitmask="default"), preferred

    # Last-resort: just take the first result
    print("  ⚠️  No priority author matched. Using first available file.")
    first = results[0]
    print(f"  Using: author={first.author}, exptime={_exptime_s(first):.0f}s")
    return first.download(quality_bitmask="default"), str(first.author)


def plot_pixel_map(tpf, target, used_author):
    """2-panel: linear + log scale pixel map."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    tpf.plot(ax=axes[0], aperture_mask=tpf.pipeline_mask,
             title=f"Exoplanet {target} — Linear ({used_author})")
    tpf.plot(ax=axes[1], aperture_mask=tpf.pipeline_mask,
             scale="log", title=f"Exoplanet {target} — Log Scale ({used_author})")

    fig.tight_layout()
    out = os.path.join(OUTPUT_DIR, f"kepler_pixel_{slug(target)}.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved pixel map → {out}")
    return out


def plot_lightcurve(tpf, target, used_author):
    """PLD light curve, outliers removed, normalized."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    lc = tpf.to_lightcurve(method="pld").remove_outliers().flatten()

    fig, ax = plt.subplots(figsize=(13, 4))
    lc.plot(ax=ax, c="green", alpha=0.8)
    ax.set_xlabel(ax.get_xlabel(), fontsize=10)
    ax.set_ylabel(ax.get_ylabel(), fontsize=10)
    ax.set_title(
        f"Exoplanet {target} — Light Curve (PLD, normalized) [{used_author}]", fontsize=12
    )
    ax.tick_params(axis="both", labelsize=8)

    fig.tight_layout()
    out = os.path.join(OUTPUT_DIR, f"lightcurve_{slug(target)}.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved light curve → {out}")
    return out


def main():
    parser = argparse.ArgumentParser(description="Visualize exoplanet pixel data and light curves")
    parser.add_argument("--target",     required=True,
                        help="Planet/star name, e.g. 'Kepler-8 b'")
    parser.add_argument("--author",     default=None,
                        help="Override data author (e.g. Kepler, K2, SPOC). "
                             "Default: auto-detect best available source.")
    parser.add_argument("--exptime",    type=int, default=60,
                        help="Preferred exposure time in seconds (default: 60). "
                             "Used as a hint when --author is also set.")
    parser.add_argument("--lightcurve", action="store_true",
                        help="Plot PLD light curve instead of pixel map")
    args = parser.parse_args()

    tpf, used_author = get_tpf(args.target, args.author, args.exptime)

    if args.lightcurve:
        out = plot_lightcurve(tpf, args.target, used_author)
    else:
        out = plot_pixel_map(tpf, args.target, used_author)

    print(f"\nDone. Output: {out}")


if __name__ == "__main__":
    main()
