import contextlib
import io
import unittest

from cyber_bulb.cli import parse_runtime_options
from cyber_bulb.effects import ColonEffect, DigitEffect
from cyber_bulb.style import SegmentStyle
from cyber_bulb.theme import ThemeMode


class RuntimeOptionsTests(unittest.TestCase):
    def test_runtime_defaults(self):
        options, qt_args = parse_runtime_options([])

        self.assertTrue(options.transition_enabled)
        self.assertTrue(options.style_transition_enabled)
        self.assertEqual(options.theme_mode, ThemeMode.SYSTEM)
        self.assertEqual(options.digit_effect, DigitEffect.AFTERGLOW)
        self.assertEqual(options.colon_effect, ColonEffect.BLINK)
        self.assertEqual(options.segment_style, SegmentStyle.CLASSIC)
        self.assertEqual(options.width, 777)
        self.assertEqual(options.height, 666)
        self.assertEqual(qt_args, [])

    def test_transition_switches_are_process_only(self):
        disabled, qt_args = parse_runtime_options(
            [
                "--no-theme-transition",
                "--no-style-transition",
                "-platform",
                "offscreen",
            ]
        )
        next_run, _ = parse_runtime_options([])

        self.assertFalse(disabled.transition_enabled)
        self.assertFalse(disabled.style_transition_enabled)
        self.assertEqual(qt_args, ["-platform", "offscreen"])
        self.assertTrue(next_run.transition_enabled)
        self.assertTrue(next_run.style_transition_enabled)
        self.assertEqual(next_run.theme_mode, ThemeMode.SYSTEM)

    def test_old_no_animation_option_is_rejected(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            parse_runtime_options(["--no-animation"])

    def test_old_no_transition_option_is_rejected(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            parse_runtime_options(["--no-transition"])

    def test_each_initial_theme_mode_can_be_selected(self):
        for mode in ThemeMode:
            with self.subTest(mode=mode):
                options, _ = parse_runtime_options(["--theme", mode.value])
                self.assertEqual(options.theme_mode, mode)

    def test_initial_dimensions_can_be_selected(self):
        options, _ = parse_runtime_options(
            ["--width", "1200", "--height", "800"]
        )

        self.assertEqual(options.width, 1200)
        self.assertEqual(options.height, 800)

    def test_each_digit_effect_can_be_selected(self):
        for effect in DigitEffect:
            with self.subTest(effect=effect):
                options, _ = parse_runtime_options(
                    ["--digit-animation", effect.value]
                )
                self.assertEqual(options.digit_effect, effect)

    def test_each_colon_effect_can_be_selected(self):
        for effect in ColonEffect:
            with self.subTest(effect=effect):
                options, _ = parse_runtime_options(
                    ["--colon-animation", effect.value]
                )
                self.assertEqual(options.colon_effect, effect)

    def test_each_segment_style_can_be_selected(self):
        for style in SegmentStyle:
            with self.subTest(style=style):
                options, _ = parse_runtime_options(
                    ["--segment-style", style.value]
                )
                self.assertEqual(options.segment_style, style)

    def test_dimensions_must_be_positive(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            parse_runtime_options(["--width", "0"])


if __name__ == "__main__":
    unittest.main()
