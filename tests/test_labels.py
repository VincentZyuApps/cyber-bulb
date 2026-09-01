import unittest

from cyber_bulb.labels import LabelParts, LabelTier, control_label, control_tooltip


class LabelTests(unittest.TestCase):
    def test_all_four_responsive_tiers(self):
        parts = LabelParts("◆", "经典", "Classic")

        self.assertEqual(control_label(parts, "晶体管", "Segment", LabelTier.ICON), "◆")
        self.assertEqual(
            control_label(parts, "晶体管", "Segment", LabelTier.KEY),
            "◆ 晶体管",
        )
        self.assertEqual(
            control_label(parts, "晶体管", "Segment", LabelTier.VALUE),
            "◆ 晶体管：经典",
        )
        self.assertEqual(
            control_label(parts, "晶体管", "Segment", LabelTier.FULL),
            "◆ 晶体管：经典 / Segment: Classic",
        )

    def test_tooltip_is_always_complete_and_bilingual(self):
        tooltip = control_tooltip(
            LabelParts("◆", "经典", "Classic"), "晶体管", "Segment"
        )

        self.assertIn("晶体管：经典", tooltip)
        self.assertIn("Segment: Classic", tooltip)
        self.assertIn("点击循环切换 / Click to cycle", tooltip)


if __name__ == "__main__":
    unittest.main()
