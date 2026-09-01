import unittest

from PyQt5.QtCore import QAbstractAnimation
from PyQt5.QtWidgets import QApplication

from cyber_bulb import DigitalClock as PackageDigitalClock
from cyber_bulb.app import DigitalClock as AppDigitalClock
from cyber_bulb.theme import (
    DARK_THEME,
    LIGHT_THEME,
    THEME_MODE_LABELS,
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

    def make_clock(self, animation_enabled=True):
        clock = DigitalClock(animation_enabled=animation_enabled)
        self.windows.append(clock)
        return clock

    def test_public_imports(self):
        self.assertIs(PackageDigitalClock, DigitalClock)
        self.assertIs(AppDigitalClock, DigitalClock)

    def test_animation_starts_by_default(self):
        clock = self.make_clock()

        self.assertEqual(
            clock.windowTitle(),
            "数字时钟 - 晶体管显示 / Digital Clock - Transistor Display",
        )
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

    def test_disabled_animation_switches_immediately_and_stays_stopped(self):
        clock = self.make_clock(animation_enabled=False)
        clock.set_mode(ThemeMode.DARK)

        self.assertTrue(clock.is_dark_mode)
        self.assertEqual(clock._current_theme, DARK_THEME)
        self.assertEqual(clock._theme_animation.state(), QAbstractAnimation.Stopped)

    def test_button_cycles_through_three_bilingual_modes(self):
        clock = self.make_clock(animation_enabled=False)

        self.assertEqual(clock.theme_mode, ThemeMode.SYSTEM)
        self.assertEqual(clock.mode_button.text(), THEME_MODE_LABELS[ThemeMode.SYSTEM])

        for expected_mode in (ThemeMode.LIGHT, ThemeMode.DARK, ThemeMode.SYSTEM):
            clock.cycle_mode()
            self.assertEqual(clock.theme_mode, expected_mode)
            self.assertEqual(clock.mode_button.text(), THEME_MODE_LABELS[expected_mode])

    def test_initial_mode_can_be_selected(self):
        clock = DigitalClock(initial_mode=ThemeMode.DARK)
        self.windows.append(clock)

        self.assertEqual(clock.theme_mode, ThemeMode.DARK)
        self.assertTrue(clock.is_dark_mode)
        self.assertEqual(clock._current_theme, DARK_THEME)
        self.assertEqual(clock.mode_button.text(), THEME_MODE_LABELS[ThemeMode.DARK])


if __name__ == "__main__":
    unittest.main()
