from PyQt5.QtCore import QDateTime, QEasingCurve, QSize, QTimer, QVariantAnimation
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .dimensions import DEFAULT_HEIGHT, DEFAULT_WIDTH
from .display import SegmentDisplay
from .effects import (
    COLON_EFFECT_NAMES,
    COLON_EFFECT_ORDER,
    DIGIT_EFFECT_NAMES,
    DIGIT_EFFECT_ORDER,
    ColonEffect,
    DigitEffect,
)
from .labels import LabelTier, control_label, control_tooltip
from .style import SEGMENT_STYLE_NAMES, SEGMENT_STYLE_ORDER, SegmentStyle
from .theme import (
    THEME_MODE_NAMES,
    ThemeMode,
    ThemePalette,
    blend_theme,
    system_prefers_dark,
    theme_for_mode,
)
from .titlebar import NativeTitleBar

TRANSITION_DURATION_MS = 350
THEME_MODE_ORDER = (ThemeMode.SYSTEM, ThemeMode.LIGHT, ThemeMode.DARK)
BUTTON_HORIZONTAL_PADDING = 14
BUTTON_MINIMUM_WIDTH = 36


class _StableButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._preferred_width = BUTTON_MINIMUM_WIDTH

    def set_preferred_width(self, width: int) -> None:
        self._preferred_width = max(BUTTON_MINIMUM_WIDTH, width)
        self.updateGeometry()

    def sizeHint(self) -> QSize:
        hint = super().sizeHint()
        return QSize(self._preferred_width, hint.height())

    def minimumSizeHint(self) -> QSize:
        hint = super().minimumSizeHint()
        return QSize(BUTTON_MINIMUM_WIDTH, hint.height())


class DigitalClock(QWidget):
    def __init__(
        self,
        transition_enabled: bool = True,
        initial_mode: ThemeMode = ThemeMode.SYSTEM,
        digit_effect: DigitEffect = DigitEffect.AFTERGLOW,
        colon_effect: ColonEffect = ColonEffect.BLINK,
        segment_style: SegmentStyle = SegmentStyle.CLASSIC,
        style_transition_enabled: bool = True,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__()
        self.transition_enabled = transition_enabled
        self.digit_effect = digit_effect
        self.colon_effect = colon_effect
        self.segment_style = segment_style
        self.style_transition_enabled = style_transition_enabled
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
        self._last_datetime = None
        self._label_tier = LabelTier.FULL

        self._theme_animation = QVariantAnimation(self)
        self._theme_animation.setDuration(TRANSITION_DURATION_MS)
        self._theme_animation.setEasingCurve(QEasingCurve.InOutCubic)
        self._theme_animation.valueChanged.connect(self._update_transition)
        self._theme_animation.finished.connect(self._finish_transition)

        self._init_ui(width, height)
        self.update_style()

    def _init_ui(self, width: int, height: int) -> None:
        self.setWindowTitle(
            "💡 数字时钟 - 晶体管显示 / Digital Clock - Transistor Display"
        )
        self.resize(width, height)

        main_layout = QVBoxLayout()
        self._main_layout = main_layout

        self.date_display = SegmentDisplay(
            "0000-00-00", self, segment_style=self.segment_style
        )
        main_layout.addWidget(self.date_display)

        self.time_display = SegmentDisplay(
            "00:00:00", self, segment_style=self.segment_style
        )
        main_layout.addWidget(self.time_display)

        button_layout = QHBoxLayout()
        self._button_layout = button_layout
        button_layout.addStretch(1)

        self.style_button = _StableButton(self)
        self.style_button.clicked.connect(self.cycle_segment_style)
        self.style_button.setMinimumWidth(BUTTON_MINIMUM_WIDTH)
        self.style_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        button_layout.addWidget(self.style_button)

        self.digit_button = _StableButton(self)
        self.digit_button.clicked.connect(self.cycle_digit_effect)
        self.digit_button.setMinimumWidth(BUTTON_MINIMUM_WIDTH)
        self.digit_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        button_layout.addWidget(self.digit_button)

        self.colon_button = _StableButton(self)
        self.colon_button.clicked.connect(self.cycle_colon_effect)
        self.colon_button.setMinimumWidth(BUTTON_MINIMUM_WIDTH)
        self.colon_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        button_layout.addWidget(self.colon_button)

        self.mode_button = _StableButton(self)
        self.mode_button.clicked.connect(self.cycle_mode)
        self.mode_button.setMinimumWidth(BUTTON_MINIMUM_WIDTH)
        self.mode_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        button_layout.addWidget(self.mode_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        self._refresh_button_labels()

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
        self._refresh_button_labels()
        is_dark_mode = (
            system_prefers_dark() if mode is ThemeMode.SYSTEM else mode is ThemeMode.DARK
        )
        self._transition_to(is_dark_mode)

    def cycle_digit_effect(self) -> None:
        current_index = DIGIT_EFFECT_ORDER.index(self.digit_effect)
        next_index = (current_index + 1) % len(DIGIT_EFFECT_ORDER)
        self.set_digit_effect(DIGIT_EFFECT_ORDER[next_index])

    def set_digit_effect(self, effect: DigitEffect) -> None:
        self.digit_effect = effect
        self._refresh_button_labels()
        self.date_display.preview(effect)
        self.time_display.preview(effect)

    def cycle_colon_effect(self) -> None:
        current_index = COLON_EFFECT_ORDER.index(self.colon_effect)
        next_index = (current_index + 1) % len(COLON_EFFECT_ORDER)
        self.set_colon_effect(COLON_EFFECT_ORDER[next_index])

    def set_colon_effect(self, effect: ColonEffect) -> None:
        self.colon_effect = effect
        self._refresh_button_labels()
        self.time_display.preview_colons(effect)

    def cycle_segment_style(self) -> None:
        current_index = SEGMENT_STYLE_ORDER.index(self.segment_style)
        next_index = (current_index + 1) % len(SEGMENT_STYLE_ORDER)
        self.set_segment_style(SEGMENT_STYLE_ORDER[next_index])

    def set_segment_style(self, style: SegmentStyle) -> None:
        self.segment_style = style
        self._refresh_button_labels()
        self.date_display.set_style(style, animate=self.style_transition_enabled)
        self.time_display.set_style(style, animate=self.style_transition_enabled)

    def _transition_to(self, is_dark_mode: bool) -> None:
        self._theme_animation.stop()
        self.is_dark_mode = is_dark_mode
        target_theme = theme_for_mode(is_dark_mode)

        if not self.transition_enabled or self._current_theme == target_theme:
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

        self.date_display.set_colors(theme.date, theme.window)
        self.time_display.set_colors(theme.time, theme.window)

        button_style = (
            f"""
            QPushButton {{
                background-color: {theme.button};
                color: {theme.button_text};
                border: 1px solid {theme.button_border};
                border-radius: 5px;
                padding: 5px 6px;
            }}
            QPushButton:hover {{
                background-color: {theme.button_hover};
            }}
            """
        )
        for button in (
            self.style_button,
            self.digit_button,
            self.colon_button,
            self.mode_button,
        ):
            button.setStyleSheet(button_style)
        self._native_title_bar.apply(theme.window, theme.button_border)

    def update_display(self) -> None:
        self._sync_system_theme()
        current_datetime = QDateTime.currentDateTime()
        self._render_datetime(current_datetime)

    def _render_datetime(self, current_datetime: QDateTime) -> None:
        animate = self._last_datetime is not None
        self.date_display.set_text(
            current_datetime.toString("yyyy-MM-dd"),
            self.digit_effect,
            animate=animate,
        )
        self.time_display.set_text(
            current_datetime.toString("HH:mm:ss"),
            self.digit_effect,
            animate=animate,
        )

        if self._last_datetime is not None:
            if self._last_datetime.toString("ss") != current_datetime.toString("ss"):
                self.time_display.animate_colon(5, self.colon_effect)
            if self._last_datetime.toString("mm") != current_datetime.toString("mm"):
                self.time_display.animate_colon(2, self.colon_effect)

        self._last_datetime = current_datetime

    def _sync_system_theme(self) -> None:
        if self.theme_mode is not ThemeMode.SYSTEM:
            return

        is_dark_mode = system_prefers_dark()
        if is_dark_mode != self.is_dark_mode:
            self._transition_to(is_dark_mode)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if hasattr(self, "style_button"):
            self._refresh_button_labels()

    def closeEvent(self, event) -> None:
        self.timer.stop()
        self._theme_animation.stop()
        self.date_display.stop_animations()
        self.time_display.stop_animations()
        super().closeEvent(event)

    def _control_specs(self):
        return (
            (
                self.style_button,
                SEGMENT_STYLE_NAMES,
                self.segment_style,
                "晶体管",
                "Segment",
            ),
            (
                self.digit_button,
                DIGIT_EFFECT_NAMES,
                self.digit_effect,
                "动画",
                "Animation",
            ),
            (
                self.colon_button,
                COLON_EFFECT_NAMES,
                self.colon_effect,
                "冒号",
                "Colon",
            ),
            (
                self.mode_button,
                THEME_MODE_NAMES,
                self.theme_mode,
                "黑白",
                "Light-Dark",
            ),
        )

    def _tier_widths(self, tier: LabelTier) -> tuple[int, ...]:
        widths = []
        for button, names, _, chinese_key, english_key in self._control_specs():
            metrics = button.fontMetrics()
            width = max(
                metrics.horizontalAdvance(
                    control_label(parts, chinese_key, english_key, tier)
                )
                for parts in names.values()
            )
            widths.append(max(BUTTON_MINIMUM_WIDTH, width + BUTTON_HORIZONTAL_PADDING))
        return tuple(widths)

    def _tier_for_width(self, available_width: int) -> LabelTier:
        spacing = self._button_layout.spacing()
        for tier in reversed(tuple(LabelTier)):
            required = sum(self._tier_widths(tier)) + spacing * 3
            if required <= available_width:
                return tier
        return LabelTier.ICON

    def _refresh_button_labels(self) -> None:
        margins = self._main_layout.contentsMargins()
        available = max(0, self.width() - margins.left() - margins.right())
        tier = self._tier_for_width(available)
        self._label_tier = tier
        widths = self._tier_widths(tier)
        for width, spec in zip(widths, self._control_specs()):
            button, names, current, chinese_key, english_key = spec
            parts = names[current]
            button.setText(control_label(parts, chinese_key, english_key, tier))
            tooltip = control_tooltip(parts, chinese_key, english_key)
            button.setToolTip(tooltip)
            button.setAccessibleName(
                control_label(parts, chinese_key, english_key, LabelTier.FULL)
            )
            button.set_preferred_width(width)
