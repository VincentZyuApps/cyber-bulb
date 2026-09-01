import unittest

from PyQt5.QtCore import QAbstractAnimation, QDateTime
from PyQt5.QtWidgets import QApplication

from cyber_bulb import DigitalClock as PackageDigitalClock
from cyber_bulb import SegmentStyle as PackageSegmentStyle
from cyber_bulb.app import DigitalClock as AppDigitalClock
from cyber_bulb.effects import (
    COLON_EFFECT_NAMES,
    COLON_EFFECT_ORDER,
    DIGIT_EFFECT_NAMES,
    DIGIT_EFFECT_ORDER,
    ColonEffect,
    DigitEffect,
)
from cyber_bulb.labels import LabelTier, control_label
from cyber_bulb.style import SEGMENT_STYLE_NAMES, SEGMENT_STYLE_ORDER, SegmentStyle
from cyber_bulb.theme import (
    DARK_THEME,
    LIGHT_THEME,
    THEME_MODE_NAMES,
    ThemeMode,
    blend_theme,
)
from cyber_bulb.window import DigitalClock


class DigitalClockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.windows = []

    def tearDown(self):
        for window in self.windows:
            window.close()
        self.app.processEvents()

    def make_clock(self, transition_enabled=True, **kwargs):
        clock = DigitalClock(transition_enabled=transition_enabled, **kwargs)
        clock.timer.stop()
        self.windows.append(clock)
        return clock

    def test_public_imports(self):
        self.assertIs(PackageDigitalClock, DigitalClock)
        self.assertIs(AppDigitalClock, DigitalClock)
        self.assertIs(PackageSegmentStyle, SegmentStyle)

    def test_theme_transition_starts_by_default(self):
        clock = self.make_clock()

        self.assertEqual(
            clock.windowTitle(),
            "💡 数字时钟 - 晶体管显示 / Digital Clock - Transistor Display",
        )
        self.assertEqual(clock.size().width(), 777)
        self.assertEqual(clock.size().height(), 666)
        target_mode = ThemeMode.LIGHT if clock.is_dark_mode else ThemeMode.DARK
        clock.set_mode(target_mode)

        self.assertEqual(clock.theme_mode, target_mode)
        self.assertEqual(clock._theme_animation.state(), QAbstractAnimation.Running)

    def test_rapid_reverse_starts_from_current_frame(self):
        clock = self.make_clock()
        clock.set_mode(ThemeMode.DARK)
        clock._theme_animation.stop()
        midpoint = blend_theme(LIGHT_THEME, DARK_THEME, 0.5)
        clock._current_theme = midpoint
        clock._apply_theme(midpoint)

        clock.set_mode(ThemeMode.LIGHT)

        self.assertFalse(clock.is_dark_mode)
        self.assertEqual(clock._transition_start, midpoint)
        self.assertEqual(clock._transition_end, LIGHT_THEME)

    def test_disabled_transition_switches_immediately_and_stays_stopped(self):
        clock = self.make_clock(transition_enabled=False)
        clock.set_mode(ThemeMode.DARK)

        self.assertTrue(clock.is_dark_mode)
        self.assertEqual(clock._current_theme, DARK_THEME)
        self.assertEqual(clock._theme_animation.state(), QAbstractAnimation.Stopped)

    def test_button_cycles_through_three_bilingual_modes(self):
        clock = self.make_clock(transition_enabled=False)

        self.assertEqual(clock.theme_mode, ThemeMode.SYSTEM)
        self.assertIn("系统", clock.mode_button.accessibleName())

        for expected_mode in (ThemeMode.LIGHT, ThemeMode.DARK, ThemeMode.SYSTEM):
            clock.cycle_mode()
            self.assertEqual(clock.theme_mode, expected_mode)
            self.assertIn(THEME_MODE_NAMES[expected_mode].chinese, clock.mode_button.text())

    def test_initial_mode_can_be_selected(self):
        clock = DigitalClock(initial_mode=ThemeMode.DARK)
        self.windows.append(clock)

        self.assertEqual(clock.theme_mode, ThemeMode.DARK)
        self.assertTrue(clock.is_dark_mode)
        self.assertEqual(clock._current_theme, DARK_THEME)
        self.assertIn("黑夜", clock.mode_button.accessibleName())

    def test_animation_buttons_cycle_and_preview(self):
        clock = self.make_clock()

        self.assertEqual(clock.digit_effect, DigitEffect.AFTERGLOW)
        self.assertEqual(clock.colon_effect, ColonEffect.BLINK)
        for expected in DIGIT_EFFECT_ORDER[1:] + DIGIT_EFFECT_ORDER[:1]:
            clock.cycle_digit_effect()
            self.assertEqual(clock.digit_effect, expected)
            self.assertIn(
                DIGIT_EFFECT_NAMES[expected].chinese,
                clock.digit_button.accessibleName(),
            )
        for expected in COLON_EFFECT_ORDER[1:] + COLON_EFFECT_ORDER[:1]:
            clock.cycle_colon_effect()
            self.assertEqual(clock.colon_effect, expected)
            self.assertIn(
                COLON_EFFECT_NAMES[expected].chinese,
                clock.colon_button.accessibleName(),
            )

        self.assertTrue(clock.date_display.animation_running())
        self.assertTrue(clock.time_display.colon_animation_running(2))
        self.assertTrue(clock.time_display.colon_animation_running(5))

    def test_segment_style_button_cycles_and_previews(self):
        clock = self.make_clock()

        self.assertEqual(clock.segment_style, SegmentStyle.CLASSIC)
        for expected in SEGMENT_STYLE_ORDER[1:] + SEGMENT_STYLE_ORDER[:1]:
            clock.cycle_segment_style()
            self.assertEqual(clock.segment_style, expected)
            self.assertIn(
                SEGMENT_STYLE_NAMES[expected].chinese,
                clock.style_button.accessibleName(),
            )

        self.assertTrue(clock.date_display.style_animation_running())
        self.assertTrue(clock.time_display.style_animation_running())

    def test_disabled_style_transition_switches_immediately(self):
        clock = self.make_clock(style_transition_enabled=False)
        clock.set_segment_style(SegmentStyle.OUTLINE)

        self.assertFalse(clock.date_display.style_animation_running())
        self.assertEqual(
            clock.date_display._style_mix,
            ((SegmentStyle.OUTLINE, 1.0),),
        )

    def test_responsive_buttons_use_all_four_tiers(self):
        clock = self.make_clock()
        specs = clock._control_specs()

        for tier in LabelTier:
            widths = clock._tier_widths(tier)
            required = sum(widths) + clock._button_layout.spacing() * 3
            self.assertEqual(clock._tier_for_width(required), tier)
            if tier is not LabelTier.ICON:
                self.assertLess(
                    clock._tier_for_width(required - 1),
                    tier,
                )

        full_width = (
            sum(clock._tier_widths(LabelTier.FULL))
            + clock._button_layout.spacing() * 3
            + clock._main_layout.contentsMargins().left()
            + clock._main_layout.contentsMargins().right()
        )
        clock.resize(full_width, 666)
        clock._refresh_button_labels()
        self.assertIs(clock._label_tier, LabelTier.FULL)
        for button, names, current, chinese_key, english_key in specs:
            self.assertEqual(
                button.text(),
                control_label(names[current], chinese_key, english_key, LabelTier.FULL),
            )

        clock.resize(210, 666)
        clock._refresh_button_labels()
        self.assertIs(clock._label_tier, LabelTier.ICON)
        self.assertTrue(all(len(button.text()) <= 2 for button, *_ in specs))

    def test_button_widths_do_not_change_when_values_cycle(self):
        clock = self.make_clock()
        margins = clock._main_layout.contentsMargins()
        full_width = (
            sum(clock._tier_widths(LabelTier.FULL))
            + clock._button_layout.spacing() * 3
            + margins.left()
            + margins.right()
        )
        clock.resize(full_width, 666)
        clock._refresh_button_labels()
        before = tuple(button.sizeHint().width() for button, *_ in clock._control_specs())

        clock.cycle_segment_style()
        clock.cycle_digit_effect()
        clock.cycle_colon_effect()
        clock.cycle_mode()
        after = tuple(button.sizeHint().width() for button, *_ in clock._control_specs())

        self.assertEqual(before, after)

    def test_closing_stops_every_animation(self):
        clock = self.make_clock()
        clock.set_mode(ThemeMode.DARK)
        clock.set_segment_style(SegmentStyle.ROUNDED)
        clock.date_display.preview(DigitEffect.GLITCH)
        clock.time_display.preview_colons(ColonEffect.DOUBLE)

        clock.close()

        self.assertFalse(clock.timer.isActive())
        self.assertEqual(clock._theme_animation.state(), QAbstractAnimation.Stopped)
        self.assertFalse(clock.date_display.animation_running())
        self.assertFalse(clock.date_display.style_animation_running())
        self.assertFalse(clock.time_display.colon_animation_running(2))
        self.assertFalse(clock.time_display.colon_animation_running(5))

    def test_second_and_minute_changes_trigger_their_left_colons(self):
        clock = self.make_clock()
        clock._last_datetime = None
        clock._render_datetime(QDateTime.fromString("2026-09-01 12:34:58", "yyyy-MM-dd HH:mm:ss"))
        clock._render_datetime(QDateTime.fromString("2026-09-01 12:34:59", "yyyy-MM-dd HH:mm:ss"))

        self.assertTrue(clock.time_display.colon_animation_running(5))
        self.assertFalse(clock.time_display.colon_animation_running(2))

        clock._render_datetime(QDateTime.fromString("2026-09-01 12:35:00", "yyyy-MM-dd HH:mm:ss"))
        self.assertTrue(clock.time_display.colon_animation_running(2))
        self.assertTrue(clock.time_display.colon_animation_running(5))

    def test_date_change_uses_digit_animation(self):
        clock = self.make_clock()
        clock._last_datetime = None
        clock._render_datetime(QDateTime.fromString("2026-09-01 23:59:59", "yyyy-MM-dd HH:mm:ss"))
        clock._render_datetime(QDateTime.fromString("2026-09-02 00:00:00", "yyyy-MM-dd HH:mm:ss"))

        self.assertTrue(clock.date_display.animation_running())

    def test_initial_dimensions_can_be_selected(self):
        for width, height in (
            (480, 360),
            (600, 450),
            (777, 666),
            (900, 720),
            (1100, 800),
        ):
            with self.subTest(width=width, height=height):
                clock = DigitalClock(width=width, height=height)
                self.windows.append(clock)
                clock.show()
                self.app.processEvents()
                self.assertEqual(clock.size().width(), width)
                self.assertEqual(clock.size().height(), height)


if __name__ == "__main__":
    unittest.main()
