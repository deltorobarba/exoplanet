# Exoplanet Research

Exoplanet Research Skill for Starters

*Author: Alexander Del Toro Barba*

Install skill on Gemini CLI:
```
git clone https://github.com/deltorobarba/exoplanet.git
gemini skills install ./exoplanet
```

Explore exoplanets 

**🔭 Explore & discover**
```
Explore 5 confirmed exoplanets discovered in 2016 using the Transit method
```
```
Search for all confirmed exoplanets with "Kepler" in the name
```
```
How many total confirmed exoplanets are in the NASA archive right now?
```

**🪐 Planet details**
```
Pull full details for Kepler-8 b from the NASA Exoplanet Archive
```
```
How far away is TRAPPIST-1 b and who discovered it?
```
```
Compare the host star properties of K2-18 b and WASP-39 b
```

**🛰️ Mission data**
```
What Kepler, TESS, and K2 observations are available for Kepler-8 b?
```
```
Search all available mission data for K2-18 b and tell me which pipeline has the best cadence
```

**Visualize Infrared Data Plots**
```
Download the Kepler pixel file for Kepler-8 b and plot the pixel map
```
```
Plot the normalized PLD light curve for Kepler-8 b with outliers removed
```
```
Load the TESS SPOC 120s data for K2-18 b and visualize it
```

**Calculate Periodogram & Orbital Period**
```
Run a BLS periodogram on Kepler-8 b and find its orbital period
```
```
Calculate the orbital period of Kepler-8 b and show me the phase-folded transit dip
```

---

**For full astronomy workflow in one prompt:**
```
Research Kepler-8 b end to end: pull its NASA details, check what missions are available, then run a BLS periodogram and calculate its orbital period
```

That prompt triggers the skill and walk through `details.py → missions.py → periodogram.py` in sequence 🪐
