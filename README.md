# Exoplanet Research Skill 🪐

*Author: Alexander Del Toro Barba, PhD*

Become a citizen exoplanet researcher. No need for you to know how to load the exoplanet-research specific libraries, how to connect to NASA databases, decide which mission data to choose, write functions fo calculuate periods and plot periograms - this agent skill does this all for you!

**Just install and run this multi-step, fully automated astronomy workflow to explore & discover exoplanets:**

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


```
 _____________________        _________________        _________________
| Connect to NASA 🔭  |      | Load Mission 🛰️ |      | Plot and  🪐    |
| Exoplanet Archive   |  --> | TESS & Kepler.  |  --> | Calculate Period |
|  'details.py'       |      | 'missions.py'   |      | 'periodogram.py' |
 ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾       ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```

Sample questions to analyse exoplanets:

```
Research Kepler-8 b end to end: pull its full NASA details, check what missions are available, then run a BLS periodogram and calculate its orbital period
```

```
Explore 5 confirmed exoplanets with "Kepler" in the name discovered in 2016 using the Transit method
```

```
What Kepler, TESS, and K2 observations are available for Kepler-8 b? And tell me which pipeline has the best cadence?
```

---



**Understand Structure of this Skill**

```
exoplanet-researcher/
├── SKILL.md                 ← skill descriptor + full workflow guide
├── requirements.txt         ← lightkurve, astroquery, astropy, matplotlib
└── scripts/
    ├── explore.py           ← browse planets by year/method/name
    ├── details.py           ← pull NASA archive details for one planet
    ├── missions.py          ← list all Kepler/TESS/K2 observations
    ├── load_tess.py         ← download + cache a TESS pixel file
    ├── visualize_kepler.py  ← pixel map (linear+log) + PLD light curve
    └── periodogram.py       ← BLS periodogram + folded transit + orbital period
```
