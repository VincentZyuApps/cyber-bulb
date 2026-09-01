import unittest

from PyQt5.QtCore import QRectF

from cyber_bulb.style import (
    SEGMENT_PROFILES,
    SEGMENT_STYLE_ORDER,
    SegmentStyle,
    colon_paths,
    segment_paths,
)


class SegmentStyleTests(unittest.TestCase):
    def test_three_styles_have_profiles_and_stable_cycle_order(self):
        self.assertEqual(tuple(SegmentStyle), SEGMENT_STYLE_ORDER)
        self.assertEqual(len(SEGMENT_PROFILES), 3)
        self.assertIs(SEGMENT_STYLE_ORDER[0], SegmentStyle.CLASSIC)

    def test_every_style_has_seven_segments_and_two_colon_parts(self):
        rect = QRectF(0, 0, 100, 200)
        for style in SegmentStyle:
            with self.subTest(style=style):
                segments = segment_paths(style, rect)
                colons = colon_paths(style, rect)
                self.assertEqual(len(segments), 7)
                self.assertEqual(len(colons), 2)
                self.assertTrue(all(not path.isEmpty() for path in segments))
                self.assertTrue(all(not path.isEmpty() for path in colons))

    def test_classic_hides_unlit_segments(self):
        self.assertEqual(SEGMENT_PROFILES[SegmentStyle.CLASSIC].inactive_level, 0.0)
        self.assertGreater(SEGMENT_PROFILES[SegmentStyle.ROUNDED].inactive_level, 0.0)

    def test_classic_matches_qt_flat_segment_proportions(self):
        rect = QRectF(0, 0, 100, 200)
        segments = segment_paths(SegmentStyle.CLASSIC, rect)

        self.assertEqual(segments[0].boundingRect(), QRectF(0, 0, 99, 20))
        self.assertEqual(segments[5].boundingRect(), QRectF(0, 1, 20, 98))
        self.assertEqual(segments[6].boundingRect(), QRectF(0, 90, 99, 20))
        self.assertEqual(segments[3].boundingRect(), QRectF(0, 180, 99, 20))
        self.assertEqual(segments[0].elementAt(1).y, 0)
        self.assertEqual(segments[1].elementAt(0).y, 1)

    def test_classic_colon_uses_qt_flat_square_positions(self):
        dots = colon_paths(SegmentStyle.CLASSIC, QRectF(0, 0, 100, 200))

        self.assertEqual(dots[0].boundingRect(), QRectF(41, 50, 20, 20))
        self.assertEqual(dots[1].boundingRect(), QRectF(41, 150, 20, 20))


if __name__ == "__main__":
    unittest.main()
