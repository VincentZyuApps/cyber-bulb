import unittest

from cyber_bulb.digit import segment_state
from cyber_bulb.effects import (
    COLON_EFFECT_DURATIONS,
    DIGIT_EFFECT_DURATIONS,
    ColonEffect,
    DigitEffect,
    colon_visual,
    digit_visual,
)


class SegmentMappingTests(unittest.TestCase):
    def test_digits_use_expected_segment_counts(self):
        expected_counts = (6, 2, 5, 5, 4, 5, 6, 3, 7, 6)

        for digit, expected_count in enumerate(expected_counts):
            with self.subTest(digit=digit):
                self.assertEqual(sum(segment_state(str(digit))), expected_count)

    def test_hyphen_uses_only_middle_segment(self):
        self.assertEqual(segment_state("-"), (False,) * 6 + (True,))


class EffectCurveTests(unittest.TestCase):
    def test_every_digit_effect_finishes_at_target_state(self):
        for effect in DigitEffect:
            with self.subTest(effect=effect):
                on_level, on_boost = digit_visual(
                    effect, 1.0, False, True, 0, 8, 0, 1, False
                )
                off_level, off_boost = digit_visual(
                    effect, 1.0, True, False, 0, 8, 0, 1, False
                )
                self.assertEqual((on_level, on_boost), (1.0, 0.0))
                self.assertEqual((off_level, off_boost), (0.0, 0.0))

    def test_glitch_frames_are_deterministic(self):
        arguments = (DigitEffect.GLITCH, 0.4, True, True, 3, 8, 4, 17, False)
        self.assertEqual(digit_visual(*arguments), digit_visual(*arguments))

    def test_every_colon_effect_finishes_fully_lit(self):
        for effect in ColonEffect:
            with self.subTest(effect=effect):
                self.assertEqual(
                    colon_visual(effect, 1.0),
                    ((1.0, 0.0), (1.0, 0.0)),
                )

    def test_effect_durations_match_the_design(self):
        self.assertEqual(DIGIT_EFFECT_DURATIONS[DigitEffect.AFTERGLOW], 260)
        self.assertEqual(DIGIT_EFFECT_DURATIONS[DigitEffect.PULSE], 220)
        self.assertEqual(DIGIT_EFFECT_DURATIONS[DigitEffect.SCAN], 320)
        self.assertEqual(DIGIT_EFFECT_DURATIONS[DigitEffect.WAVE], 360)
        self.assertEqual(DIGIT_EFFECT_DURATIONS[DigitEffect.GLITCH], 240)
        self.assertEqual(COLON_EFFECT_DURATIONS[ColonEffect.BLINK], 180)
        self.assertEqual(COLON_EFFECT_DURATIONS[ColonEffect.PULSE], 180)
        self.assertEqual(COLON_EFFECT_DURATIONS[ColonEffect.DOUBLE], 260)
        self.assertEqual(COLON_EFFECT_DURATIONS[ColonEffect.ALTERNATE], 240)


if __name__ == "__main__":
    unittest.main()
