# scripts/banner.py
def print_banner():
    banner = [
        "███████╗██╗  ██╗ ██████╗ ██████╗ ██╗      █████╗ ███╗   ██╗███████╗████████╗",
        "██╔════╝╚██╗██╔╝██╔═══██╗██╔══██╗██║     ██╔══██╗████╗  ██║██╔════╝╚══██╔══╝",
        "█████╗   ╚███╔╝ ██║   ██║██████╔╝██║     ███████║██╔██╗ ██║█████╗     ██║   ",
        "██╔══╝   ██╔██╗ ██║   ██║██╔═══╝ ██║     ██╔══██║██║╚██╗██║██╔══╝     ██║   ",
        "███████╗██╔╝ ██╗╚██████╔╝██║     ███████╗██║  ██║██║ ╚████║███████╗   ██║   ",
        "╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝  ",
    ]

    # 256-color gradient stops: blue → purple → pink
    gradient = [33, 63, 99, 135, 171, 207]

    import sys
    sys.stdout.write("\n")
    for line in banner:
        colored = ""
        length = max(1, len(line) - 1)
        for i, char in enumerate(line):
            ratio = i / length
            # Pick gradient stop
            idx = ratio * (len(gradient) - 1)
            lo, hi = int(idx), min(int(idx) + 1, len(gradient) - 1)
            # Blend between two stops (pick nearest)
            color = gradient[round(ratio * (len(gradient) - 1))]
            colored += f"\033[38;5;{color}m{char}"
        sys.stdout.write(colored + "\033[0m\n")
        sys.stdout.flush()

    sys.stdout.write("\033[38;5;245m    Exoplanet Research Skill initialized...\033[0m\n\n")
    sys.stdout.flush()

if __name__ == "__main__":
    print_banner()
