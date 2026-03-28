"""
explore.py — Browse the NASA Exoplanet Archive.

Usage:
    python scripts/explore.py                          # All confirmed planets
    python scripts/explore.py --year 2016              # Filter by discovery year
    python scripts/explore.py --method Transit         # Filter by discovery method
    python scripts/explore.py --year 2016 --method Transit
    python scripts/explore.py --search "Kepler"        # Substring search on planet name
    python scripts/explore.py --limit 20               # Max rows to print (default 20)
"""

# scripts/explore.py
import sys
from banner import print_banner

# Print the banner right when the script starts
print_banner()

import argparse
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive


def main():
    parser = argparse.ArgumentParser(description="Explore NASA Exoplanet Archive")
    parser.add_argument("--year",   type=int,   help="Filter by discovery year")
    parser.add_argument("--method", type=str,   help="Filter by discovery method (e.g. Transit, 'Radial Velocity')")
    parser.add_argument("--search", type=str,   help="Substring search on planet name")
    parser.add_argument("--limit",  type=int,   default=20, help="Max rows to display (default 20)")
    args = parser.parse_args()

    # Build WHERE clause
    conditions = []
    if args.year:
        conditions.append(f"disc_year={args.year}")
    if args.method:
        conditions.append(f"discoverymethod='{args.method}'")

    where = " and ".join(conditions) if conditions else None

    print("Querying NASA Exoplanet Archive (pscomppars table)...")
    query_kwargs = dict(
        table="pscomppars",
        select="pl_name, hostname, disc_year, discoverymethod",
    )
    if where:
        query_kwargs["where"] = where

    planets = NasaExoplanetArchive.query_criteria(**query_kwargs)

    # Optional name substring filter (client-side)
    if args.search:
        mask = [args.search.lower() in str(row["pl_name"]).lower() for row in planets]
        planets = planets[mask]

    total = len(planets)
    display = planets[:args.limit]

    # Pretty-print
    header = f"{'Planet':<30} {'Host Star':<25} {'Year':>6}  {'Method'}"
    sep = "-" * 90
    print(sep)
    print(header)
    print(sep)
    for row in display:
        print(f"{str(row['pl_name']):<30} {str(row['hostname']):<25} "
              f"{str(row['disc_year']):>6}  {str(row['discoverymethod'])}")

    print(sep)
    shown = min(args.limit, total)
    print(f"Showing {shown} of {total} confirmed exoplanets")
    if args.year or args.method or args.search:
        filters = []
        if args.year:   filters.append(f"year={args.year}")
        if args.method: filters.append(f"method={args.method}")
        if args.search: filters.append(f"name contains '{args.search}'")
        print(f"Filters applied: {', '.join(filters)}")


if __name__ == "__main__":
    main()
