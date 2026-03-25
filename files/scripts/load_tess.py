"""
load_tess.py — Download a TESS Target Pixel File (TPF) and cache it locally.

Usage:
    python scripts/load_tess.py --target "Kepler-8 b"
    python scripts/load_tess.py --target "Kepler-8 b" --author SPOC --exptime 120
    python scripts/load_tess.py --target "K2-18 b" --exptime 120

The downloaded TPF is cached to tpf_cache.pkl so downstream scripts
(visualize_kepler.py, periodogram.py) can load it without re-downloading.
"""

import argparse
import os
import pickle
import lightkurve as lk
from astropy import units as u


CACHE_FILE = "tpf_cache.pkl"


def main():
    parser = argparse.ArgumentParser(description="Download TESS pixel file for an exoplanet")
    parser.add_argument("--target",  required=True, help="Planet/star name, e.g. 'Kepler-8 b'")
    parser.add_argument("--author",  default="SPOC", help="Pipeline author (default: SPOC)")
    parser.add_argument("--exptime", type=int, default=120,
                        help="Exposure time in seconds (default: 120 for SPOC 2-min cadence)")
    args = parser.parse_args()

    target  = args.target
    author  = args.author
    exptime = args.exptime * u.second

    print(f"Searching TESS pixel files for: {target}")
    print(f"  Author: {author}  |  Exposure: {args.exptime}s")

    results = lk.search_targetpixelfile(target)

    if results is None or len(results) == 0:
        print(f"\nNo TESS pixel files found for '{target}'.")
        print("Run missions.py first to check what is available.")
        return

    # Filter by author and exposure time
    try:
        mask = (results.author == author)
        filtered = results[mask]
        # Further filter by exptime if possible
        exp_mask = [abs(float(r.exptime.value) - args.exptime) < 1 for r in filtered]
        filtered = filtered[exp_mask]
    except Exception:
        filtered = results  # Fall back to all results

    if len(filtered) == 0:
        print(f"\nNo results matched author='{author}' + exptime={args.exptime}s.")
        print("Available files:")
        for i, r in enumerate(results):
            try:
                print(f"  [{i}] {r.author}  exptime={r.exptime}  mission={r.mission}")
            except Exception:
                print(f"  [{i}] {r}")
        print("\nTry adjusting --author or --exptime, or run missions.py for full listing.")
        return

    print(f"\nFound {len(filtered)} matching file(s). Downloading first entry...")
    tpf = filtered[0].download()

    print(f"Downloaded: {tpf}")
    print(f"  Shape: {tpf.shape}")
    print(f"  Time: {len(tpf.time)} cadences")

    # Save cache
    with open(CACHE_FILE, "wb") as f:
        pickle.dump({"target": target, "tpf": tpf}, f)

    print(f"\nCached to: {CACHE_FILE}")
    print("Next step: run  python scripts/visualize_kepler.py --target <name>")


if __name__ == "__main__":
    main()
