"""UI platform abstraction layer for window features."""

import sys


def setup_window_features(
        window,
        title,
        bg_color: str,
        title_color: str,
        icon_name: str=""
    ) -> None:

    """Applies native window cosmetics if running on a supported platform."""

    # print(f"{sys.platform=}")
    if sys.platform.startswith("linux"):
        try:
            from .gtk import setup_window_features as apply_gtk_features

            apply_gtk_features(window, title, bg_color, title_color, icon_name)
        except (ImportError, ValueError) as e:
            # GTK or PyGObject bindings not installed; pass silently
            print(f"[UI] GTK features bypassed: {e}")
    else:
        # On Windows (win32) / macOS (darwin), pywebview handles titlebars natively
        pass
