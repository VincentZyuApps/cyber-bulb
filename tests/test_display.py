import unittest

from PyQt5.QtWidgets import QApplication

from cyber_bulb.digit import segment_state
from cyber_bulb.display import SegmentDisplay
from cyber_bulb.effects import DigitEffect
from cyber_bulb.style import SegmentStyle


class SegmentDisplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_initial_text_is_applied_without_animation(self):
        display = SegmentDisplay("00")
        display.set_text("12", DigitEffect.AFTERGLOW)

        self.assertEqual(display.text(), "12")
        self.assertFalse(display.animation_running())

    def test_interrupted_animation_settles_on_latest_text(self):
        display = SegmentDisplay("00")
        display.set_text("12")
        display.set_text("13", DigitEffect.GLITCH)
        display.set_text("14", DigitEffect.AFTERGLOW)
        display._finish_animation()

        self.assertEqual(display.text(), "14")
        for index, cell in display._digits:
            self.assertEqual(tuple(cell._levels), segment_state("14"[index]))

    def test_text_length_must_match_template(self):
        display = SegmentDisplay("00")
        with self.assertRaises(ValueError):
            display.set_text("123")

    def test_style_transition_preserves_current_mix_when_interrupted(self):
        display = SegmentDisplay("00")
        display.set_style(SegmentStyle.ROUNDED)
        display._update_style_animation(0.4)
        current_mix = display._style_mix

        display.set_style(SegmentStyle.OUTLINE)

        self.assertEqual(display._style_start_mix, current_mix)
        self.assertTrue(display.style_animation_running())

    def test_style_can_switch_immediately(self):
        display = SegmentDisplay("00")
        display.set_style(SegmentStyle.ROUNDED, animate=False)

        self.assertFalse(display.style_animation_running())
        self.assertEqual(display._style_mix, ((SegmentStyle.ROUNDED, 1.0),))

    def test_classic_uses_qt_equal_width_colon_slots(self):
        display = SegmentDisplay("00:00")

        self.assertEqual(display._layout.spacing(), 0)
        self.assertEqual(display._layout.stretch(2), 10)

        display.set_style(SegmentStyle.ROUNDED, animate=False)
        self.assertEqual(display._layout.spacing(), 4)
        self.assertEqual(display._layout.stretch(2), 4)


if __name__ == "__main__":
    unittest.main()
