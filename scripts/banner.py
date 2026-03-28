# scripts/banner.py

def print_banner():
    # Block-style ASCII art
    banner = [
        "███████╗██╗  ██╗ ██████╗ ██████╗ ██╗      █████╗ ███╗   ██╗███████╗████████╗",
        "██╔════╝╚██╗██╔╝██╔═══██╗██╔══██╗██║     ██╔══██╗████╗  ██║██╔════╝╚══██╔══╝",
        "█████╗   ╚███╔╝ ██║   ██║██████╔╝██║     ███████║██╔██╗ ██║█████╗     ██║   ",
        "██╔══╝   ██╔██╗ ██║   ██║██╔═══╝ ██║     ██╔══██║██║╚██╗██║██╔══╝     ██║   ",
        "███████╗██╔╝ ██╗╚██████╔╝██║     ███████╗██║  ██║██║ ╚████║███████╗   ██║   ",
        "╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   "
    ]

    # Gradient Settings (RGB)
    # Start Color: Gemini Blue
    r1, g1, b1 = 100, 160, 255 
    # End Color: Gemini Pink
    r2, g2, b2 = 255, 120, 200 

    print("") # Empty line for spacing
    
    for line in banner:
        colored_line = ""
        length = len(line)
        
        for i, char in enumerate(line):
            # Calculate the interpolation ratio (0.0 to 1.0)
            ratio = i / max(1, length - 1)
            
            # Blend the RGB values based on the character's position
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            # Apply 24-bit ANSI color escape code for this specific character
            colored_line += f"\033[38;2;{r};{g};{b}m{char}"
        
        # Reset colors at the end of each line and print
        print(colored_line + "\033[0m")
    
    # Subtitle with a soft color
    print(f"\033[38;2;180;180;180m    Exoplanet Research Skill initialized...\033[0m\n")

if __name__ == "__main__":
    # Allows you to test the banner by just running `python scripts/banner.py`
    print_banner()
