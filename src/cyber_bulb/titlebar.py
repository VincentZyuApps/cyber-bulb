import ctypes
import sys
from ctypes import wintypes

from .theme import contrasting_text_color

DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19
DWMWA_USE_IMMERSIVE_DARK_MODE = 20
DWMWA_BORDER_COLOR = 34
DWMWA_CAPTION_COLOR = 35
DWMWA_TEXT_COLOR = 36


def colorref(color: str) -> int:
    value = int(color.removeprefix("#"), 16)
    red = (value >> 16) & 0xFF
    green = (value >> 8) & 0xFF
    blue = value & 0xFF
    return red | (green << 8) | (blue << 16)


class NativeTitleBar:
    def __init__(self, widget):
        self._widget = widget
        self._last_style = None

    def apply(self, background: str, border: str) -> None:
        if sys.platform != "win32":
            return

        text = contrasting_text_color(background)
        style = (background, border, text)
        if style == self._last_style:
            return

        hwnd = int(self._widget.winId())
        if not hwnd:
            return

        try:
            dwm_set = ctypes.windll.dwmapi.DwmSetWindowAttribute
        except (AttributeError, OSError):
            return

        dwm_set.argtypes = [
            wintypes.HWND,
            wintypes.DWORD,
            ctypes.c_void_p,
            wintypes.DWORD,
        ]
        dwm_set.restype = ctypes.c_long

        dark_mode = ctypes.c_int(text == "#ffffff")
        result = dwm_set(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(dark_mode),
            ctypes.sizeof(dark_mode),
        )
        if result != 0:
            dwm_set(
                hwnd,
                DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1,
                ctypes.byref(dark_mode),
                ctypes.sizeof(dark_mode),
            )

        for attribute, color in (
            (DWMWA_BORDER_COLOR, border),
            (DWMWA_CAPTION_COLOR, background),
            (DWMWA_TEXT_COLOR, text),
        ):
            color_value = ctypes.c_uint32(colorref(color))
            dwm_set(
                hwnd,
                attribute,
                ctypes.byref(color_value),
                ctypes.sizeof(color_value),
            )

        self._last_style = style
