import sys
from dataclasses import dataclass, fields
from enum import Enum

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication

from .labels import LabelParts


class ThemeMode(str, Enum):
    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"


THEME_MODE_NAMES = {
    ThemeMode.SYSTEM: LabelParts("🖥️", "系统", "System"),
    ThemeMode.LIGHT: LabelParts("☀️", "白天", "Light"),
    ThemeMode.DARK: LabelParts("🌙", "黑夜", "Dark"),
}


@dataclass(frozen=True, slots=True)
class ThemePalette:
    window: str
    date: str
    time: str
    button: str
    button_hover: str
    button_text: str
    button_border: str


LIGHT_THEME = ThemePalette(
    window="#ffffff",
    date="#0000ff",
    time="#000000",
    button="#f0f0f0",
    button_hover="#e0e0e0",
    button_text="#000000",
    button_border="#dcdcdc",
)

DARK_THEME = ThemePalette(
    window="#1a1a1a",
    date="#00ff00",
    time="#00ff00",
    button="#2e2e2e",
    button_hover="#3b3b3b",
    button_text="#ffffff",
    button_border="#4d4d4d",
)


def theme_for_mode(is_dark_mode: bool) -> ThemePalette:
    return DARK_THEME if is_dark_mode else LIGHT_THEME


def system_prefers_dark() -> bool:
    if sys.platform == "win32":
        try:
            import winreg

            path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as key:
                apps_use_light_theme, _ = winreg.QueryValueEx(
                    key, "AppsUseLightTheme"
                )
            return not bool(apps_use_light_theme)
        except OSError:
            pass

    app = QApplication.instance()
    return bool(app and app.palette().window().color().lightness() < 128)


def blend_color(start: str, end: str, progress: float) -> str:
    progress = max(0.0, min(1.0, progress))
    start_color = QColor(start)
    end_color = QColor(end)
    return QColor(
        round(start_color.red() + (end_color.red() - start_color.red()) * progress),
        round(
            start_color.green()
            + (end_color.green() - start_color.green()) * progress
        ),
        round(start_color.blue() + (end_color.blue() - start_color.blue()) * progress),
    ).name()


def blend_theme(
    start: ThemePalette, end: ThemePalette, progress: float
) -> ThemePalette:
    return ThemePalette(
        **{
            field.name: blend_color(
                getattr(start, field.name), getattr(end, field.name), progress
            )
            for field in fields(ThemePalette)
        }
    )


def contrasting_text_color(background: str) -> str:
    color = QColor(background)

    def linear(channel: int) -> float:
        value = channel / 255
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    luminance = (
        0.2126 * linear(color.red())
        + 0.7152 * linear(color.green())
        + 0.0722 * linear(color.blue())
    )
    return "#000000" if luminance > 0.179 else "#ffffff"
