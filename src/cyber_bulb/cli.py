import argparse
from collections.abc import Sequence
from dataclasses import dataclass

from .dimensions import DEFAULT_HEIGHT, DEFAULT_WIDTH
from .theme import ThemeMode


@dataclass(frozen=True, slots=True)
class RuntimeOptions:
    animation_enabled: bool = True
    theme_mode: ThemeMode = ThemeMode.SYSTEM
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
        "--no-animation",
        action="store_true",
        help="disable the light/dark theme transition",
    )
    parser.add_argument(
        "--theme",
        choices=[mode.value for mode in ThemeMode],
        default=ThemeMode.SYSTEM.value,
        help="set the initial theme mode (default: system)",
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
    args, qt_args = parser.parse_known_args(argv)
    return RuntimeOptions(
        animation_enabled=not args.no_animation,
        theme_mode=ThemeMode(args.theme),
        width=args.width,
        height=args.height,
    ), qt_args
