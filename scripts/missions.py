"""
missions.py — Search available Kepler, TESS, and K2 mission data for an exoplanet.

Usage:
    python scripts/missions.py --target "Kepler-8 b"
    python scripts/missions.py --target "K2-18 b"
"""

import argparse
import lightkurve as lk


def search_and_print(label, emoji, results):
    print(f"\n{'=' * 70}")
    print(f"  {emoji}  {label}")
    print(f"{'=' * 70}")
    if results is None or len(results) == 0:
        print("  No data available.")
        return

    # Print table header
    print(f"  {'#':<4} {'Author':<20} {'Exp/Cadence':<20} {'Year':<8} {'Mission'}")
    print(f"  {'-'*64}")
    for i, row in enumerate(results):
        try:
            val = row.exptime.value
            val = float(val.flat[0]) if hasattr(val, 'flat') else float(val)
            exptime = f"{val:.0f}s" if
        except Exception:
            exptime = "?"
        try:
            year = str(row.year) if hasattr(row, 'year') else "?"
        except Exception:
            year = "?"
        try:
            author = str(row.author)
        except Exception:
            author = "?"
        try:
            mission = str(row.mission)
        except Exception:
            mission = "?"
        print(f"  {i:<4} {author:<20} {exptime:<20} {year:<8} {mission}")

    print(f"\n  Total: {len(results)} observation(s)")


def main():
    parser = argparse.ArgumentParser(description="Search mission data for an exoplanet")
    parser.add_argument("--target", required=True, help="Planet or star name, e.g. 'Kepler-8 b'")
    args = parser.parse_args()

    target = args.target
    print(f"\nSearching all available mission data for: {target}")

    # Light curve searches
    try:
        kepler_lc = lk.search_lightcurve(target, mission="Kepler")
    except Exception as e:
        kepler_lc = None
        print(f"  Kepler LC search error: {e}")

    try:
        tess_lc = lk.search_lightcurve(target, mission="TESS")
    except Exception as e:
        tess_lc = None
        print(f"  TESS LC search error: {e}")

    try:
        k2_lc = lk.search_lightcurve(target, mission="K2")
    except Exception as e:
        k2_lc = None
        print(f"  K2 LC search error: {e}")

    # Target pixel file search (all missions)
    try:
        tpf_all = lk.search_targetpixelfile(target)
    except Exception as e:
        tpf_all = None
        print(f"  TPF search error: {e}")

    search_and_print(f"Kepler Light Curves — {target}", "🔭", kepler_lc)
    search_and_print(f"TESS Light Curves — {target}", "🛰️", tess_lc)
    search_and_print(f"K2 Light Curves — {target}", "🛰️", k2_lc)
    search_and_print(f"Target Pixel Files (all missions) — {target}", "📦", tpf_all)

    print()
    print("Tip: Use load_tess.py to download a specific TESS pixel file.")
    print("     Use visualize_kepler.py to download and plot Kepler data.")


if __name__ == "__main__":
    main()
