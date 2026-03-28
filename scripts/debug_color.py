# scripts/debug_color.py
import os, sys

# Check what Gemini CLI sets in the environment
print(f"TERM={os.environ.get('TERM', 'NOT SET')}")
print(f"COLORTERM={os.environ.get('COLORTERM', 'NOT SET')}")
print(f"NO_COLOR={os.environ.get('NO_COLOR', 'NOT SET')}")
print(f"FORCE_COLOR={os.environ.get('FORCE_COLOR', 'NOT SET')}")
print(f"stdout.isatty()={sys.stdout.isatty()}")
print(f"stderr.isatty()={sys.stderr.isatty()}")

# Raw ANSI directly to stdout
sys.stdout.write("\033[38;2;255;100;100mRED stdout\033[0m\n")
sys.stdout.flush()

# Raw bytes directly to stderr fd
os.write(2, b"\033[38;2;100;255;100mGREEN stderr raw\033[0m\n")

# Raw bytes to /dev/tty
try:
    with open('/dev/tty', 'wb') as tty:
        tty.write(b"\033[38;2;100;160;255mBLUE /dev/tty\033[0m\n")
    print("/dev/tty: worked")
except Exception as e:
    print(f"/dev/tty: {e}")