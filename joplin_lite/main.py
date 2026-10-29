"""Main entry point for the pywebview desktop application.

Initializes the application window and points it toward the local UI server
or static production build files.
"""

# /// script
# dependencies = [
#     "pywebview",
# ]
# ///

import argparse
import logging
import sys
from pathlib import Path

import webview

from joplin_lite.api import Api
from joplin_lite.platforms import setup_window_features

from joplin_lite.joplin_server import (
    start_server, wait_for_server, stop_server, get_api_credentials
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")



def get_target_window_size(scale=0.8):
    """Calculates window size as a percentage of the primary monitor resolution."""
    screen = webview.screens[0]
    width = int(screen.width * scale)
    height = int(screen.height * scale)

    return width, height


def main() -> int:
    """Initialize and start the joplin data/api server and pywebview desktop window."""
    parser = argparse.ArgumentParser(description="Starts the application")
    parser.add_argument("-d", "--debug", action="store_true", help="Open inspection panel.")
    args = parser.parse_args()

    # Start the joplin data/api server
    _proc = start_server()
    ok = wait_for_server()
    if not ok:
        sys.exit(1)

    # Initialize pywebview API instance
    api = Api()

    win_width, win_height = get_target_window_size(scale=0.8)

    # Get absolute path to the built in dex.html
    dist_path = Path("ui/dist/index.html").resolve().as_uri()

    print(f"Starting desktop window pointing to {dist_path}...")

    title = "Joplin Lite"
    window = webview.create_window(
        title=title,
        url=dist_path,
        width=win_width,
        height=win_height,
        js_api=api,
    )

    # Apply window styling
    # See platform-specific file to see how to register icon_name
    slate_teal_gray = "#8c969b"
    setup_window_features(
        window, title, bg_color=slate_teal_gray, title_color="white", icon_name="")

    webview.start(debug=args.debug)


if __name__ == "__main__":
  main()
