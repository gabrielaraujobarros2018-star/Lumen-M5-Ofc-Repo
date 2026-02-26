Lumen Project – deeplink.py
===============================================================================

Purpose
-------
Small, standalone Python script that opens a predefined URL (your GitHub profile)
in the default browser using GNOME/GTK-friendly APIs.

Designed specifically for:
- Environments with GNOME / PyGObject (no Android dependencies)
- Very easy modification (all important values are at the top)
- Future extension for Lumen OS deep linking / URI handling

Currently used for:
https://github.com/gabrielaraujobarros2018-star

Features
--------
- Uses only GLib + Gio → no heavy browser-specific code
- Opens link via launch_default_for_uri() (xdg-open style)
- Falls back to console error if graphical session is missing
- Shows simple GTK error dialog when launch fails in GUI session
- Single-file, no external dependencies beyond python3-gi
- All configurable parts are clearly marked and grouped at the top

Requirements
------------
- Python 3.6+
- PyGObject (python3-gi package on Debian/Ubuntu derivatives)
  → sudo apt install python3-gi gir1.2-gtk-3.0
- Running in a graphical session with Gio-supporting backend
  (GNOME, most Wayland/X11 desktops)

Installation (typical usage on desktop Linux)
---------------------------------------------
1. Place the file somewhere, e.g. /usr/local/bin/deeplink.py
   or \~/lumen/tools/deeplink.py

2. Make executable:
   chmod +x deeplink.py

3. Optional – create .desktop file for menu / URI association
   \~/.local/share/applications/lumen-github.desktop

   Example content:
   [Desktop Entry]
   Name=Lumen GitHub Profile
   Exec=/path/to/deeplink.py
   Type=Application
   Terminal=false
   Icon=system-users              # or github icon if you have one
   Categories=Utility;Development;

Quick Modification Examples
---------------------------
Change target URL:
    TARGET_URL = "https://github.com/gabrielaraujobarros2018-star/releases"

Add command-line argument support (example):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--releases", action="store_true")
    args = parser.parse_args()
    if args.releases:
        TARGET_URL = "https://github.com/gabrielaraujobarros2018-star/releases"

Future / planned extensions for Lumen OS
----------------------------------------
- Support custom URI scheme (lumen://open/profile, lumen://open/releases, etc.)
- Parse sys.argv[1] as URI and dispatch accordingly
- Desktop file with MimeType=x-scheme-handler/lumen;
- Small system tray / indicator support (optional)
- Notification on success/failure using Notify
- Logging to \~/.cache/lumen/deeplink.log for debugging

License
-------
Public domain / Unlicense – do whatever you want with it.
Feel free to include it directly in Lumen OS flashable zips or tools.

Author / Maintainer
-------------------
Lumen (gabrielaraujobarros2018-star)
For questions / improvements → GitHub issues or direct message

Last updated: February 2026
