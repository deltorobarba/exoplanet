# scripts/banner.py
def print_banner():
    try:
        from rich.console import Console
        from rich.text import Text
        import sys

        # Write to /dev/tty to bypass Gemini CLI's stdout pipe
        try:
            tty = open('/dev/tty', 'w')
            console = Console(file=tty, color_system="truecolor", width=200)
        except OSError:
            # Fallback to stderr (also usually not piped)
            console = Console(file=sys.stderr, force_terminal=True,
                              color_system="truecolor", width=200)

        banner = [
            "███████╗██╗  ██╗ ██████╗ ██████╗ ██╗      █████╗ ███╗   ██╗███████╗████████╗",
            "██╔════╝╚██╗██╔╝██╔═══██╗██╔══██╗██║     ██╔══██╗████╗  ██║██╔════╝╚══██╔══╝",
            "█████╗   ╚███╔╝ ██║   ██║██████╔╝██║     ███████║██╔██╗ ██║█████╗     ██║   ",
            "██╔══╝   ██╔██╗ ██║   ██║██╔═══╝ ██║     ██╔══██║██║╚██╗██║██╔══╝     ██║   ",
            "███████╗██╔╝ ██╗╚██████╔╝██║     ███████╗██║  ██║██║ ╚████║███████╗   ██║   ",
            "╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝  ",
        ]

        r1, g1, b1 = 100, 160, 255
        r2, g2, b2 = 255, 120, 200

        console.print("")
        for line in banner:
            text = Text()
            length = max(1, len(line) - 1)
            for i, char in enumerate(line):
                ratio = i / length
                r = int(r1 + (r2 - r1) * ratio)
                g = int(g1 + (g2 - g1) * ratio)
                b = int(b1 + (b2 - b1) * ratio)
                text.append(char, style=f"rgb({r},{g},{b})")
            console.print(text)

        console.print("\n    [rgb(180,180,180)]Exoplanet Research Skill initialized...[/]\n")

    except ImportError:
        print("\n  [ EXOPLANET RESEARCHER ]\n  Exoplanet Research Skill initialized...\n")


if __name__ == "__main__":
    print_banner()
