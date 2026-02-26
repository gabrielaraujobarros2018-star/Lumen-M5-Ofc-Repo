#!/usr/bin/env python3
"""
deeplink.py
Simple GNOME-compatible deep link launcher for Lumen project
Opens https://github.com/gabrielaraujobarros2018-star in the default browser

2025–2026 – made to be easy to modify
"""

import sys
import gi

# We only need very basic GTK for showing errors (optional)
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib

# ────────────────────────────────────────────────
#          === EASY TO MODIFY SECTION ===
# ────────────────────────────────────────────────

# Change these three things when you want to point somewhere else

TARGET_URL = "https://github.com/gabrielaraujobarros2018-star"

APP_NAME = "Lumen Deep Link"

APP_ID = "org.lumen.deeplink"          # used for desktop file / notifications

# You can also change the error dialog title / messages if you want
ERROR_TITLE = "Cannot open link"
ERROR_MESSAGE_PREFIX = "Failed to open: "

# ────────────────────────────────────────────────
#         === NO NEED TO TOUCH BELOW HERE ===
#         (unless you want to add features)
# ────────────────────────────────────────────────

def open_url(url):
    """Try to open URL using GLib / xdg-open style methods"""
    try:
        Gio.AppInfo.launch_default_for_uri(url, None)
        return True
    except GLib.Error as e:
        return False, str(e)

def show_error(message):
    """Show a very simple GTK error dialog (non-blocking)"""
    dialog = Gtk.MessageDialog(
        message_type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.OK,
        text=ERROR_TITLE
    )
    dialog.format_secondary_text(f"{ERROR_MESSAGE_PREFIX}{message}")
    dialog.set_title(APP_NAME)
    dialog.run()
    dialog.destroy()

def main():
    success, error = open_url(TARGET_URL)

    if success:
        # Optional: could show a small notification here in the future
        # For now we just exit silently (most common for deeplink launchers)
        return 0

    # If we reach here → opening failed
    print(f"{APP_NAME} error: {error}", file=sys.stderr)

    # Show GUI error only if we are in a graphical session
    if "DISPLAY" in GLib.getenv() or "WAYLAND_DISPLAY" in GLib.getenv():
        show_error(error)

    return 1

if __name__ == "__main__":
    sys.exit(main())
