import argparse
from collections.abc import Sequence
from dataclasses import dataclass

from .dimensions import DEFAULT_HEIGHT, DEFAULT_WIDTH
from .effects import ColonEffect, DigitEffect
from .style import SegmentStyle
from .theme import ThemeMode


@dataclass(frozen=True, slots=True)
class RuntimeOptions:
    transition_enabled: bool = True
    style_transition_enabled: bool = True
    theme_mode: ThemeMode = ThemeMode.SYSTEM
    digit_effect: DigitEffect = DigitEffect.AFTERGLOW
    colon_effect: ColonEffect = ColonEffect.BLINK
    segment_style: SegmentStyle = SegmentStyle.CLASSIC
    width: int = DEFAULT_WIDTH
    height: int = DEFAULT_HEIGHT


def positive_dimension(value: str) -> int:
    dimension = int(value)
    if dimension <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return dimension


def parse_runtime_options(
    argv: Sequence[str],
) -> tuple[RuntimeOptions, list[str]]:
    parser = argparse.ArgumentParser(prog="cyber-bulb")
    parser.add_argument(
        "--no-theme-transition",
        action="store_true",
        help="disable the light/dark theme transition",
    )
    parser.add_argument(
        "--no-style-transition",
        action="store_true",
        help="disable the segment style transition",
    )
    parser.add_argument(
        "--theme",
        choices=[mode.value for mode in ThemeMode],
        default=ThemeMode.SYSTEM.value,
        help="set the initial theme mode (default: system)",
    )
    parser.add_argument(
        "--digit-animation",
        choices=[effect.value for effect in DigitEffect],
        default=DigitEffect.AFTERGLOW.value,
        help="set the digit animation (default: afterglow)",
    )
    parser.add_argument(
        "--colon-animation",
        choices=[effect.value for effect in ColonEffect],
        default=ColonEffect.BLINK.value,
        help="set the colon animation (default: blink)",
    )
    parser.add_argument(
        "--segment-style",
        choices=[style.value for style in SegmentStyle],
        default=SegmentStyle.CLASSIC.value,
        help="set the initial segment style (default: classic)",
    )
    parser.add_argument(
        "--width",
        type=positive_dimension,
        default=DEFAULT_WIDTH,
        help=f"set the initial window width (default: {DEFAULT_WIDTH})",
    )
    parser.add_argument(
        "--height",
        type=positive_dimension,
        default=DEFAULT_HEIGHT,
        help=f"set the initial window height (default: {DEFAULT_HEIGHT})",
    )
    if "--no-animation" in argv:
        parser.error("--no-animation is unsupported")
    if "--no-transition" in argv:
        parser.error("--no-transition was replaced by --no-theme-transition")

    args, qt_args = parser.parse_known_args(argv)
    return RuntimeOptions(
        transition_enabled=not args.no_theme_transition,
        style_transition_enabled=not args.no_style_transition,
        theme_mode=ThemeMode(args.theme),
        digit_effect=DigitEffect(args.digit_animation),
        colon_effect=ColonEffect(args.colon_animation),
        segment_style=SegmentStyle(args.segment_style),
        width=args.width,
        height=args.height,
    ), qt_args
