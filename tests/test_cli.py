import unittest

from cyber_bulb.cli import parse_runtime_options
from cyber_bulb.theme import ThemeMode


class RuntimeOptionsTests(unittest.TestCase):
    def test_animation_is_enabled_by_default(self):
        options, qt_args = parse_runtime_options([])

        self.assertTrue(options.animation_enabled)
        self.assertEqual(options.theme_mode, ThemeMode.SYSTEM)
        self.assertEqual(qt_args, [])

    def test_no_animation_is_process_only(self):
        disabled, qt_args = parse_runtime_options(
            ["--no-animation", "-platform", "offscreen"]
        )
        next_run, _ = parse_runtime_options([])

        self.assertFalse(disabled.animation_enabled)
        self.assertEqual(qt_args, ["-platform", "offscreen"])
        self.assertTrue(next_run.animation_enabled)
        self.assertEqual(next_run.theme_mode, ThemeMode.SYSTEM)

    def test_each_initial_theme_mode_can_be_selected(self):
        for mode in ThemeMode:
            with self.subTest(mode=mode):
                options, _ = parse_runtime_options(["--theme", mode.value])
                self.assertEqual(options.theme_mode, mode)


if __name__ == "__main__":
    unittest.main()
