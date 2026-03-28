# scripts/banner.py

def print_banner():
    # ANSI color codes (Cyan matches the Gemini aesthetic well)
    CYAN = '\033[96m'
    RESET = '\033[0m'
    
    ascii_art = f"""{CYAN}
  _____  __  __  ____   _____   _         _     _   _  _____  _______ 
 |  ___| \ \/ / / __ \ |  __ \ | |       / \   | \ | ||  ___||__   __|
 | |__    \  / | |  | || |__) || |      / _ \  |  \| || |__     | |   
 |  __|   /  \ | |  | ||  ___/ | |     / ___ \ | . ` ||  __|    | |   
 | |___  / /\ \| |__| || |     | |____/ /   \ \| |\  || |___    | |   
 |_____|/_/  \_\\____/ |_|     |______/_/    \_\_| \_||_____|   |_|   
                                                                      
    Exoplanet Research Skill initialized...{RESET}
"""
    print(ascii_art)