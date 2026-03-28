"""
periodogram.py — BLS periodogram and orbital period for an exoplanet transit.

Computes a Box Least Squares (BLS) periodogram from pixel data,
identifies the period at maximum power, and produces a phase-folded light curve.

Auto-detects the best available mission data (Kepler → K2 → SPOC/TESS).
Use --author to override.

Usage:
    python scripts/periodogram.py --target "Kepler-8 b"
    python scripts/periodogram.py --target "TRAPPIST-1 b"
    python scripts/periodogram.py --target "K2-18 b" --min-period 30 --max-period 40
    python scripts/periodogram.py --target "Kepler-8 b" --author Kepler --exptime 60
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
            # Prefer matching exptime within filtered
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


def main():
    parser = argparse.ArgumentParser(description="Compute BLS periodogram for exoplanet transit")
    parser.add_argument("--target",     required=True,
                        help="Planet/star name, e.g. 'Kepler-8 b'")
    parser.add_argument("--author",     default=None,
                        help="Override data author (e.g. Kepler, K2, SPOC). "
                             "Default: auto-detect best available source.")
    parser.add_argument("--exptime",    type=int, default=60,
                        help="Preferred exposure time in seconds (default: 60). "
                             "Used as a hint when --author is also set.")
    parser.add_argument("--min-period", type=float, default=None,
                        help="Minimum period in days for BLS search (optional)")
    parser.add_argument("--max-period", type=float, default=None,
                        help="Maximum period in days for BLS search (optional)")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    target = args.target

    # 1 — Download pixel data (auto or manual author)
    tpf, used_author = get_tpf(target, args.author, args.exptime)

    # 2 — Build flat light curve
    print("Building PLD light curve...")
    lc = tpf.to_lightcurve(method="pld").remove_outliers().flatten()

    # 3 — BLS periodogram
    print("Computing BLS periodogram (this may take ~30–60 seconds)...")
    pg_kwargs = {"method": "bls"}
    if args.min_period:
        pg_kwargs["minimum_period"] = args.min_period
    if args.max_period:
        pg_kwargs["maximum_period"] = args.max_period

    periodogram = lc.to_periodogram(**pg_kwargs)

    # 4 — Find best period
    period = periodogram.period_at_max_power
    print(f"\n  Best-fit orbital period: {period.value:.4f} days")
    print(f"  (at maximum BLS power)")

    # 5 — Plot BLS periodogram
    fig1, ax1 = plt.subplots(figsize=(13, 4))
    periodogram.plot(ax=ax1, color="green")
    ax1.set_title(
        f"Periodogram — Transit Detection for {target} ({used_author})", fontsize=12
    )
    ax1.set_xlabel("Period (days)", fontsize=10)
    ax1.set_ylabel("BLS Power", fontsize=10)
    ax1.tick_params(axis="both", labelsize=10)
    fig1.tight_layout()
    out_pg = os.path.join(OUTPUT_DIR, f"periodogram_{slug(target)}.png")
    fig1.savefig(out_pg, dpi=150, bbox_inches="tight")
    plt.close(fig1)
    print(f"Saved periodogram → {out_pg}")

    # 6 — Phase-folded transit plot
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    lc.fold(period).truncate(-2.0, -1.0).plot(ax=ax2, color="green")
    ax2.set_title(
        f"Orbital Period = {period.value:.2f} days — {target} ({used_author})", fontsize=12
    )
    ax2.set_xlabel("Phase (JD)", fontsize=10)
    ax2.set_ylabel("Normalized Flux", fontsize=10)
    ax2.tick_params(axis="both", labelsize=10)
    fig2.tight_layout()
    out_fold = os.path.join(OUTPUT_DIR, f"folded_{slug(target)}.png")
    fig2.savefig(out_fold, dpi=150, bbox_inches="tight")
    plt.close(fig2)
    print(f"Saved folded curve → {out_fold}")

    print(f"\nSummary:")
    print(f"  Target  : {target}")
    print(f"  Author  : {used_author}")
    print(f"  Period  : {period.value:.4f} days = {period.value * 24:.1f} hours")
    print(f"  Outputs : {out_pg}")
    print(f"            {out_fold}")


if __name__ == "__main__":
    main()
