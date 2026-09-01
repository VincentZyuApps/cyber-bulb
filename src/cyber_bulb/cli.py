import argparse
from collections.abc import Sequence
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as distribution_version

from .dimensions import DEFAULT_HEIGHT, DEFAULT_WIDTH
from .effects import ColonEffect, DigitEffect
from .style import SegmentStyle
from .theme import ThemeMode

PACKAGE_NAME = "cyber-bulb"


class BilingualHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None) -> None:
        super().add_usage(
            usage,
            actions,
            groups,
            prefix="用法 / Usage: " if prefix is None else prefix,
        )


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


def _package_version() -> str:
    try:
        return distribution_version(PACKAGE_NAME)
    except PackageNotFoundError:
        return "unknown"


def parse_runtime_options(
    argv: Sequence[str],
) -> tuple[RuntimeOptions, list[str]]:
    parser = argparse.ArgumentParser(
        prog="cyber-bulb",
        description="💡 赛博灯泡 / Cyber Bulb",
        add_help=False,
        formatter_class=BilingualHelpFormatter,
    )
    options = parser.add_argument_group("⚙️ 选项 / Options")
    options.add_argument(
        "-h",
        "--help",
        action="help",
        help="📖 显示帮助并退出。 / Show help and exit.",
    )
    options.add_argument(
        "-V",
        "--V",
        "--version",
        action="version",
        version=f"%(prog)s {_package_version()}",
        help="🏷️ 显示版本并退出。 / Show version and exit.",
    )
    options.add_argument(
        "--no-theme-transition",
        action="store_true",
        help="🌓 禁用明暗主题渐变。 / Disable the light/dark theme transition.",
    )
    options.add_argument(
        "--no-style-transition",
        action="store_true",
        help="🎨 禁用数码管外观渐变。 / Disable the segment style transition.",
    )
    options.add_argument(
        "--theme",
        choices=[mode.value for mode in ThemeMode],
        default=ThemeMode.SYSTEM.value,
        help="🌓 设置初始主题（默认：system）。 / Set the initial theme (default: system).",
    )
    options.add_argument(
        "--digit-animation",
        choices=[effect.value for effect in DigitEffect],
        default=DigitEffect.AFTERGLOW.value,
        help="✨ 设置数字动画（默认：afterglow）。 / Set the digit animation (default: afterglow).",
    )
    options.add_argument(
        "--colon-animation",
        choices=[effect.value for effect in ColonEffect],
        default=ColonEffect.BLINK.value,
        help="⏱️ 设置冒号动画（默认：blink）。 / Set the colon animation (default: blink).",
    )
    options.add_argument(
        "--segment-style",
        choices=[style.value for style in SegmentStyle],
        default=SegmentStyle.CLASSIC.value,
        help="💡 设置初始数码管外观（默认：classic）。 / Set the initial segment style (default: classic).",
    )
    options.add_argument(
        "--width",
        type=positive_dimension,
        default=DEFAULT_WIDTH,
        help=f"↔️ 设置初始窗口宽度（默认：{DEFAULT_WIDTH}）。 / Set the initial window width (default: {DEFAULT_WIDTH}).",
    )
    options.add_argument(
        "--height",
        type=positive_dimension,
        default=DEFAULT_HEIGHT,
        help=f"↕️ 设置初始窗口高度（默认：{DEFAULT_HEIGHT}）。 / Set the initial window height (default: {DEFAULT_HEIGHT}).",
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
