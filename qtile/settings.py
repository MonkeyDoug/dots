import re
import subprocess


def get_dpi_from_xresources():
    try:
        # Use subprocess to run the 'xrdb -query' command and capture the output
        xrdb_output = subprocess.check_output(["xrdb", "-query"], text=True)

        # Use a regular expression to find the 'Xft.dpi' value
        match = re.search(r"Xft\.dpi:\s*(\d+)", xrdb_output)
        if match:
            return float(match.group(1))

        # Return None if 'Xft.dpi' is not found in the output
        return 96
    except Exception:
        return 96


def set_font_size(dpi):
    if dpi >= 192:
        return 32
    elif dpi >= 144:
        return 28
    elif dpi >= 120:
        return 24
    elif dpi >= 96:
        return 10
    elif dpi >= 72:
        return 8
    else:
        return 6


settings = {"font_size": set_font_size(get_dpi_from_xresources())}
