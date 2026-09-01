import unittest
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from cyber_bulb.cli import parse_runtime_options
from cyber_bulb.window import DigitalClock


class DefaultConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_code_cli_ui_and_readme_defaults_agree(self):
        options, _ = parse_runtime_options([])
        clock = DigitalClock(
            transition_enabled=options.transition_enabled,
            style_transition_enabled=options.style_transition_enabled,
            initial_mode=options.theme_mode,
            digit_effect=options.digit_effect,
            colon_effect=options.colon_effect,
            segment_style=options.segment_style,
            width=options.width,
            height=options.height,
        )
        clock.timer.stop()
        self.addCleanup(clock.close)

        self.assertEqual(clock.segment_style, options.segment_style)
        self.assertEqual(clock.digit_effect, options.digit_effect)
        self.assertEqual(clock.colon_effect, options.colon_effect)
        self.assertEqual(clock.theme_mode, options.theme_mode)
        self.assertTrue(clock.transition_enabled)
        self.assertTrue(clock.style_transition_enabled)
        self.assertIn("晶体管：经典 / Segment: Classic", clock.style_button.accessibleName())
        self.assertIn("动画：余辉 / Animation: Glow", clock.digit_button.accessibleName())
        self.assertIn("冒号：熄闪 / Colon: Blink", clock.colon_button.accessibleName())
        self.assertIn("黑白：系统 / Light-Dark: System", clock.mode_button.accessibleName())

        readme = (Path(__file__).parents[1] / "README.md").read_text(encoding="utf-8")
        for fragment in (
            "| `--theme {system,light,dark}` | `system` |",
            "| `--segment-style {classic,rounded,outline}` | `classic` |",
            "| `--digit-animation {none,afterglow,pulse,scan,wave,glitch}` | `afterglow` |",
            "| `--colon-animation {none,blink,pulse,double,alternate}` | `blink` |",
            "| `--no-theme-transition`, `--no-style-transition` | 关闭 / Off |",
            "| `--width`, `--height <像素 / pixels>` | `777 × 666` |",
            "`-V`, `--V`, `--version`",
        ):
            self.assertIn(fragment, readme)


if __name__ == "__main__":
    unittest.main()
