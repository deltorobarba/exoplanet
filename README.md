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
Research Kepler-8 b end to end: pull its full NASA details, check what missions are available, then run a BLS periodogram and calculate its orbital period
```


```
 _________________       _________________       _________________
|  NASA Exoplanet
   Archive
Planet facts   |     |  Mission data   |     |   BLS output    |
|  star + method  | --> |  Kepler · TESS  | --> |  period · plots  |
 ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾       ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾       ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```

**🔭 Explore & discover more about exoplanets and their 🛰️ Mission data**

```
Explore 5 confirmed exoplanets with "Kepler" in the name discovered in 2016 using the Transit method
```

```
What Kepler, TESS, and K2 observations are available for Kepler-8 b?
```
```
Search all available mission data for K2-18 b and tell me which pipeline has the best cadence
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
