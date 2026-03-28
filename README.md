# Exoplanet Research Skill

*Author: Alexander Del Toro Barba, PhD*

Explore exoplanets in a variety of ways directly in natural language and without astronomy coding knowledge - this is your expert who does the heavy work in the background.


Install skill on Gemini CLI:
```
git clone https://github.com/deltorobarba/exoplanet.git
gemini skills install ./exoplanet
```
```
  _____  __  __  ____   _____   _         _     _   _  _____  _______ 
 |  ___| \ \/ / / __ \ |  __ \ | |       / \   | \ | ||  ___||__   __|
 | |__    \  / | |  | || |__) || |      / _ \  |  \| || |__     | |   
 |  __|   /  \ | |  | ||  ___/ | |     / ___ \ | . ` ||  __|    | |   
 | |___  / /\ \| |__| || |     | |____/ /   \ \| |\  || |___    | |   
 |_____|/_/  \_\\____/ |_|     |______/_/    \_\_| \_||_____|   |_|   
                                                                      
    Exoplanet Research Skill initialized..
```

**The power of Agent Skills is to run expert in procedual knowledge. Try to run this multi-step, fully automated astronomy workflow:**
```
Research Kepler-8 b end to end: pull its NASA details, check what missions are available, then run a BLS periodogram and calculate its orbital period
```


```
 _________________       _________________       _________________
|  Planet facts   |     |  Mission data   |     |   BLS output    |
|  star + method  | --> |  Kepler · TESS  | --> |  period · plots  |
 ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾       ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾       ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```

Ask questions about exoplanets:

```
Explore 5 confirmed exoplanets discovered in 2016 using the Transit method
```

**🔭 Explore & discover**

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



That prompt triggers the skill and walk through `details.py → missions.py → periodogram.py` in sequence 🪐


**Structure of this Skill**

```
exoplanet-researcher/
├── SKILL.md              ← skill descriptor + full workflow guide
├── requirements.txt      ← lightkurve, astroquery, astropy, matplotlib
└── scripts/
    ├── explore.py        ← browse planets by year/method/name
    ├── details.py        ← pull NASA archive details for one planet
    ├── missions.py       ← list all Kepler/TESS/K2 observations
    ├── load_tess.py      ← download + cache a TESS pixel file
    ├── visualize_kepler.py  ← pixel map (linear+log) + PLD light curve
    └── periodogram.py    ← BLS periodogram + folded transit + orbital period
```
