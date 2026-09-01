import unittest

from cyber_bulb.theme import (
    DARK_THEME,
    LIGHT_THEME,
    blend_color,
    blend_theme,
    contrasting_text_color,
)
from cyber_bulb.titlebar import colorref


class ThemeTests(unittest.TestCase):
    def test_blend_color_clamps_to_endpoints(self):
        self.assertEqual(blend_color("#000000", "#ffffff", -1), "#000000")
        self.assertEqual(blend_color("#000000", "#ffffff", 2), "#ffffff")

    def test_blend_theme_interpolates_midpoint(self):
        midpoint = blend_theme(LIGHT_THEME, DARK_THEME, 0.5)

        self.assertEqual(midpoint.window, "#8c8c8c")
        self.assertEqual(midpoint.button_text, "#808080")

    def test_contrasting_text_color(self):
        self.assertEqual(contrasting_text_color("#ffffff"), "#000000")
        self.assertEqual(contrasting_text_color("#1a1a1a"), "#ffffff")

    def test_colorref_uses_windows_byte_order(self):
        self.assertEqual(colorref("#123456"), 0x563412)


if __name__ == "__main__":
    unittest.main()
