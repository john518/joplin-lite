"""GTK-specific window cosmetics for pywebview on Linux.

Note: to display an icon, you must put an image file at either:

    - `.local/share/icons/hicolor/256x256/apps/`
    - `.local/share/icons/hicolor/512x512/apps/`

From the path names, the images must be raster.
"""

import gi

# pywebview's Linux backend relies on WebKit2, which uses GTK 3.
# GTK 3 and GTK 4 C-libraries cannot coexist in the same process.
gi.require_version("Gtk", "3.0")
gi.require_version('WebKit2', '4.1') # Falls back to 4.0 if needed on older distros
from gi.repository import Gtk, WebKit2


def enable_native_spellcheck() -> None:
    """Explicitly enables system spell checking on the WebKitGTK web context."""
    try:
        context = WebKit2.WebContext.get_default()
        context.set_spell_checking_enabled(True)
        context.set_spell_checking_languages(["en_US"])
    except Exception as e:
        print(f"Failed to enable WebKit spellcheck: {e}")


def set_custom_header(
        window,
        title,
        bg_color="#2c3e5",
        text_color="#ff00ff",
        icon_name=""
    ) -> None:
    """
    Configures a unique header bar style for a specific window instance.
    """
    # Create GTK header bar
    header_bar = Gtk.HeaderBar()
    header_bar.set_show_close_button(True)

    # Give this specific header bar a unique programmatic name
    header_bar.set_name("isolated-window-header")

    # Set icon - see file docstring for info on locating icon
    if icon_name:
        icon_image = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON)
        icon_image.set_pixel_size(24)
        header_bar.pack_start(icon_image)

    title_label = Gtk.Label(label=title)
    title_label.set_xalign(0.0)
    header_bar.pack_start(title_label)

    # Dynamically build the CSS string from input parameters
    css_data = f"""
        #isolated-window-header {{
            background: {bg_color};
            color: {text_color};
            box-shadow: none;
            border-bottom: 1px solid rgba(0, 0, 0, 0.2);
            font-size: 12pt;
        }}
        #isolated-window-header label {{
            color: {text_color};
            font-size: 10px;
            font-weight: 600;
        }}
        #isolated-window-header button {{
            background-color: rgba(255, 255, 255, 0.1);
            color: #2c3e50;
        }}
    """

    # Load the css provider
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(css_data.encode())

    # Apply the provider strictly to this header bar's context
    context = header_bar.get_style_context()
    context.add_provider(
        css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    # Add headerbar to the window
    window.set_titlebar(header_bar)
    window.show_all()


def set_gtk_features(window, title, bg_color, text_color, icon_name) -> None:
    """Applies GTK native features."""
    enable_native_spellcheck()
    set_custom_header(window, title, bg_color, text_color, icon_name)


def setup_window_features(
        window,
        title: str,
        bg_color: str,
        title_color: str,
        icon_name: str=""
    ) -> None:
    """Hooks native styling to the pywebview window's realize event."""

    # Attach to the before_show event because gtk window is instantiated then
    def _on_before_show():# 1. Turn on WebKit context-level spellchecking globally
        gtk_win = window.native
        if gtk_win:
            gtk_win.connect(
                "realize",
                lambda widget: set_gtk_features(widget, title, bg_color, title_color, icon_name),
            )

    window.events.before_show += _on_before_show
