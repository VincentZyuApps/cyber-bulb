from PyQt5.QtCore import QDateTime, QEasingCurve, QTimer, QVariantAnimation
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLCDNumber,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .titlebar import NativeTitleBar
from .theme import (
    THEME_MODE_LABELS,
    ThemeMode,
    ThemePalette,
    blend_theme,
    system_prefers_dark,
    theme_for_mode,
)

TRANSITION_DURATION_MS = 350
THEME_MODE_ORDER = (ThemeMode.SYSTEM, ThemeMode.LIGHT, ThemeMode.DARK)


class DigitalClock(QWidget):
    def __init__(
        self,
        animation_enabled: bool = True,
        initial_mode: ThemeMode = ThemeMode.SYSTEM,
    ):
        super().__init__()
        self.animation_enabled = animation_enabled
        self.theme_mode = initial_mode
        self.is_dark_mode = (
            system_prefers_dark()
            if initial_mode is ThemeMode.SYSTEM
            else initial_mode is ThemeMode.DARK
        )
        self._current_theme = theme_for_mode(self.is_dark_mode)
        self._transition_start = self._current_theme
        self._transition_end = self._current_theme
        self._native_title_bar = NativeTitleBar(self)

        self._init_ui()
        self._theme_animation = QVariantAnimation(self)
        self._theme_animation.setDuration(TRANSITION_DURATION_MS)
        self._theme_animation.setEasingCurve(QEasingCurve.InOutCubic)
        self._theme_animation.valueChanged.connect(self._update_transition)
        self._theme_animation.finished.connect(self._finish_transition)
        self.update_style()

    def _init_ui(self) -> None:
        self.setWindowTitle(
            "数字时钟 - 晶体管显示 / Digital Clock - Transistor Display"
        )
        self.resize(400, 250)

        main_layout = QVBoxLayout()

        self.date_display = QLCDNumber(self)
        self.date_display.setDigitCount(10)
        self.date_display.setSegmentStyle(QLCDNumber.Flat)
        main_layout.addWidget(self.date_display)

        self.time_display = QLCDNumber(self)
        self.time_display.setDigitCount(8)
        self.time_display.setSegmentStyle(QLCDNumber.Flat)
        main_layout.addWidget(self.time_display)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        self.mode_button = QPushButton(THEME_MODE_LABELS[self.theme_mode])
        self.mode_button.setToolTip(
            "循环切换主题模式 / Cycle through theme modes"
        )
        self.mode_button.clicked.connect(self.cycle_mode)
        button_layout.addWidget(self.mode_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)
        self.update_display()

    def update_style(self) -> None:
        self._theme_animation.stop()
        self._current_theme = theme_for_mode(self.is_dark_mode)
        self._apply_theme(self._current_theme)

    def toggle_mode(self) -> None:
        self.cycle_mode()

    def cycle_mode(self) -> None:
        current_index = THEME_MODE_ORDER.index(self.theme_mode)
        next_index = (current_index + 1) % len(THEME_MODE_ORDER)
        self.set_mode(THEME_MODE_ORDER[next_index])

    def set_mode(self, mode: ThemeMode) -> None:
        self.theme_mode = mode
        self.mode_button.setText(THEME_MODE_LABELS[mode])
        is_dark_mode = (
            system_prefers_dark() if mode is ThemeMode.SYSTEM else mode is ThemeMode.DARK
        )
        self._transition_to(is_dark_mode)

    def _transition_to(self, is_dark_mode: bool) -> None:
        self._theme_animation.stop()
        self.is_dark_mode = is_dark_mode
        target_theme = theme_for_mode(is_dark_mode)

        if not self.animation_enabled or self._current_theme == target_theme:
            self.update_style()
            return

        self._transition_start = self._current_theme
        self._transition_end = target_theme
        self._theme_animation.setStartValue(0.0)
        self._theme_animation.setEndValue(1.0)
        self._theme_animation.start()

    def _update_transition(self, value) -> None:
        self._current_theme = blend_theme(
            self._transition_start, self._transition_end, float(value)
        )
        self._apply_theme(self._current_theme)

    def _finish_transition(self) -> None:
        self._current_theme = self._transition_end
        self._apply_theme(self._current_theme)

    def _apply_theme(self, theme: ThemePalette) -> None:
        self.setStyleSheet(f"background-color: {theme.window};")

        date_palette = self.date_display.palette()
        date_palette.setColor(QPalette.WindowText, QColor(theme.date))
        self.date_display.setPalette(date_palette)

        time_palette = self.time_display.palette()
        time_palette.setColor(QPalette.WindowText, QColor(theme.time))
        self.time_display.setPalette(time_palette)

        self.mode_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {theme.button};
                color: {theme.button_text};
                border: 1px solid {theme.button_border};
                border-radius: 5px;
                padding: 5px 10px;
            }}
            QPushButton:hover {{
                background-color: {theme.button_hover};
            }}
            """
        )
        self._native_title_bar.apply(theme.window, theme.button_border)

    def update_display(self) -> None:
        self._sync_system_theme()
        current_datetime = QDateTime.currentDateTime()
        self.date_display.display(current_datetime.toString("yyyy-MM-dd"))
        self.time_display.display(current_datetime.toString("HH:mm:ss"))

    def _sync_system_theme(self) -> None:
        if self.theme_mode is not ThemeMode.SYSTEM:
            return

        is_dark_mode = system_prefers_dark()
        if is_dark_mode != self.is_dark_mode:
            self._transition_to(is_dark_mode)
