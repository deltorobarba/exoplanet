"""
details.py — Pull detailed parameters for a specific exoplanet from NASA archive.

Usage:
    python scripts/details.py --target "Kepler-8 b"
    python scripts/details.py --target "TRAPPIST-1 b" --table ps
"""

import argparse
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive


def fmt(value, unit="", precision=None):
    """Format a potentially masked/None value for display."""
    try:
        if hasattr(value, 'unmasked'):
            value = float(value)
        v = float(value)
        if precision is not None:
            return f"{v:.{precision}f} {unit}".strip()
        return f"{v} {unit}".strip()
    except Exception:
        return "N/A"


def main():
    parser = argparse.ArgumentParser(description="Pull exoplanet details from NASA archive")
    parser.add_argument("--target", required=True, help="Planet name, e.g. 'Kepler-8 b'")
    parser.add_argument("--table", default="ps", choices=["ps", "pscomppars"],
                        help="NASA table to query: ps (all measurements) or pscomppars (composite)")
    args = parser.parse_args()

    print(f"Querying NASA Exoplanet Archive for: {args.target}")
    data = NasaExoplanetArchive.query_object(args.target, table=args.table)

    if len(data) == 0:
        print(f"No results found for '{args.target}'. Check the planet name spelling.")
        return

    row = data[0]
    print()
    print("=" * 55)
    print(f"  🪐  {args.target}")
    print("=" * 55)

    # Host star
    print(f"\n  HOST STAR")
    print(f"    Name:              {row.get('hostname', 'N/A')}")
    print(f"    Temperature:       {fmt(row['st_teff'], 'K')} (effective temp)")
    print(f"    Radius:            {fmt(row['st_rad'], 'R☉')} (solar radii)")

    # Planet
    dist_ly = None
    try:
        dist_pc = float(row['sy_dist'])
        dist_ly = dist_pc * 3.26156
    except Exception:
        pass

    print(f"\n  PLANET")
    print(f"    Discovery Year:    {row.get('disc_year', 'N/A')}")
    print(f"    Discovery Method:  {row.get('discoverymethod', 'N/A')}")
    print(f"    Discovery Facility:{row.get('disc_facility', 'N/A')}")
    if dist_ly:
        print(f"    Distance:          {dist_ly:,.0f} light-years  ({float(row['sy_dist']):.1f} parsecs)")
    else:
        print(f"    Distance:          N/A")

    # Orbital
    print(f"\n  ORBITAL PARAMETERS")
    print(f"    Orbital Period:    {fmt(row.get('pl_orbper', None), 'days')}")
    print(f"    Planet Radius:     {fmt(row.get('pl_rade', None), 'R⊕')} (Earth radii)")
    print(f"    Planet Mass:       {fmt(row.get('pl_bmasse', None), 'M⊕')} (Earth masses)")

    print()
    print(f"  Total measurements in archive: {len(data)}")
    print("=" * 55)


if __name__ == "__main__":
    main()
