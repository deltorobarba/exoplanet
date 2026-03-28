---
name: exoplanet-researcher
description: >
  Use this skill whenever the user wants to explore, research, or visualize exoplanets.
  Triggers include: browsing exoplanets by discovery year or method, selecting a specific
  planet by name (e.g. "Kepler-8", "TRAPPIST-1", "K2-18"), pulling data from the NASA
  Exoplanet Archive, searching for Kepler/TESS/K2 mission observations, loading TESS
  target pixel files, visualizing light curves, plotting periodograms for transit detection,
  or calculating orbital periods. Always use this skill when the user mentions exoplanets,
  NASA exoplanet data, lightkurve, Kepler missions, TESS data, or wants to study or
  visualize any planetary transit data — even if the request seems simple.
---

# Exoplanet Researcher

A full research workflow for discovering, selecting, and visualizing exoplanets using
the NASA Exoplanet Archive and the `lightkurve` library.

## Quick Reference

| Goal | Script |
|------|--------|
| Browse / filter exoplanets | `scripts/explore.py` |
| Pull NASA archive details for a planet | `scripts/details.py` |
| Search available mission data (Kepler/TESS/K2) | `scripts/missions.py` |
| Load TESS pixel file | `scripts/load_tess.py` |
| Visualize Kepler pixel file + light curve | `scripts/visualize_kepler.py` |
| Periodogram + orbital period calculation | `scripts/periodogram.py` |

---

## ⚠️ First-Run Setup (required)

Before running any script, ensure dependencies are installed:
```bash
pip install -r requirements.txt --quiet
```

## Setup

Install dependencies once per environment:

```bash
pip install lightkurve astroquery astropy matplotlib --quiet
```

Or use the bundled requirements file:

```bash
pip install -r requirements.txt --quiet
```

---

## Step-by-Step Workflow

### 1 — Explore Exoplanets

Browse the full confirmed planet list, optionally filtered by year or discovery method.

```bash
# List all confirmed exoplanets (name, host star, discovery year)
python scripts/explore.py

# Filter by year
python scripts/explore.py --year 2016

# Filter by discovery method
python scripts/explore.py --method Transit

# Filter by both
python scripts/explore.py --year 2016 --method Transit

# Search by planet name substring
python scripts/explore.py --search "Kepler"
```

Output: table of `pl_name | hostname | disc_year`, plus total count.

---

### 2 — Pull Planet Details from NASA Archive

```bash
python scripts/details.py --target "Kepler-8 b"
```

Prints: host star temperature, stellar radius, distance (light-years), discovery year,
discovery method, and discovery facility.

---

### 3 — Search Available Mission Data

```bash
python scripts/missions.py --target "Kepler-8 b"
```

Prints a summary table of all available Kepler, TESS, and K2 light curve observations,
including author, cadence/exposure time, and number of results.

---

### 4 — Load TESS Mission Files

TESS Target Pixel Files (TPF) are needed for visualization. Loading requires knowing
what observations are available (Step 3 first).

```bash
# Download the first SPOC 120s TESS pixel file for the target
python scripts/load_tess.py --target "Kepler-8 b"

# Specify a different author or exposure time
python scripts/load_tess.py --target "Kepler-8 b" --author SPOC --exptime 120
```

The script saves the TPF reference to a local cache file (`tpf_cache.pkl`) for use
by downstream visualization scripts.

---

### 5 — Visualize Kepler Pixel File

```bash
python scripts/visualize_kepler.py --target "Kepler-8 b"
```

Produces a side-by-side plot:
- **Left**: pixel flux map (linear scale, aperture mask highlighted)
- **Right**: same map in log scale

Saves to `output/kepler_pixel_{target}.png`.

---

### 6 — Plot Exoplanet Light Curve (outliers removed, normalized)

```bash
python scripts/visualize_kepler.py --target "Kepler-8 b" --lightcurve
```

Plots the PLD (Pixel Level Decorrelation) light curve with outliers removed and
flux normalized. Uses the Kepler 60s cadence pixel file.

Saves to `output/lightcurve_{target}.png`.

---

### 7 — Periodogram for Transit Detection

```bash
python scripts/periodogram.py --target "Kepler-8 b"
```

Computes a Box Least Squares (BLS) periodogram and prints:
- Best-fit orbital period (days) at maximum BLS power
- A folded light curve plot truncated to the transit window

Saves:
- `output/periodogram_{target}.png` — BLS power vs. period
- `output/folded_{target}.png` — phase-folded transit dip

---

## Key Parameters and NASA Archive Tables

| Table | Contents |
|-------|----------|
| `pscomppars` | One row per planet (composite parameters) — use for broad exploration |
| `ps` | All individual measurements per planet — use for detailed queries |

Common column names:
- `pl_name` — planet name
- `hostname` — host star name
- `disc_year` — discovery year
- `discoverymethod` — e.g. Transit, Radial Velocity, Direct Imaging
- `st_teff` — host star effective temperature (K)
- `st_rad` — stellar radius (solar radii)
- `sy_dist` — distance (parsecs; multiply × 3.26 for light-years)
- `disc_facility` — telescope / observatory

---

## Common Targets for Testing

| Target | Distance | Notes |
|--------|----------|-------|
| `Kepler-8 b` | ~3,300 ly | Good Kepler 60s data |
| `K2-18 b` | ~124 ly | Has TESS + K2 |
| `WASP-39 b` | ~700 ly | JWST target |
| `TRAPPIST-1 b` | ~39 ly | Multi-planet system |
| `TOI-1452 b` | ~100 ly | Ocean world candidate |

---

## Gotchas

- **TESS vs. Kepler data availability**: not every planet has both. Always run
  `missions.py` first to see what is available before loading pixel files.
- **SPOC vs. QLP**: SPOC is the primary TESS pipeline (120s cadence); QLP is
  the quick-look pipeline (10-min cadence). Default to SPOC when available.
- **Unit conversions**: `sy_dist` from NASA is in parsecs. Use `× 3.26` for light-years.
- **`lightkurve` quality bitmask**: `"default"` removes most bad cadences and is
  safe for most use cases.
- **Large downloads**: pixel file downloads can take 30–60s for full Kepler quarters.
  Print a status message before calling `.download()`.
- **Periodogram cost**: BLS periodogram computation is CPU-intensive. On large datasets,
  restrict the period range with `minimum_period` / `maximum_period` kwargs.
