import argparse
from collections.abc import Sequence
from dataclasses import dataclass

from .theme import ThemeMode


@dataclass(frozen=True, slots=True)
class RuntimeOptions:
    animation_enabled: bool = True
    theme_mode: ThemeMode = ThemeMode.SYSTEM


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
    args, qt_args = parser.parse_known_args(argv)
    return RuntimeOptions(
        animation_enabled=not args.no_animation,
        theme_mode=ThemeMode(args.theme),
    ), qt_args
