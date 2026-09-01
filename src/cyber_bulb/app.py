import sys
from collections.abc import Sequence

from PyQt5.QtWidgets import QApplication

from .cli import parse_runtime_options
from .window import DigitalClock

__all__ = ["DigitalClock", "main"]


def main(argv: Sequence[str] | None = None) -> int:
    runtime_args = list(sys.argv[1:] if argv is None else argv)
    options, qt_args = parse_runtime_options(runtime_args)
    app = QApplication([sys.argv[0], *qt_args])
    clock = DigitalClock(
        transition_enabled=options.transition_enabled,
        initial_mode=options.theme_mode,
        digit_effect=options.digit_effect,
        colon_effect=options.colon_effect,
        segment_style=options.segment_style,
        style_transition_enabled=options.style_transition_enabled,
        width=options.width,
        height=options.height,
    )
    clock.show()
    return app.exec_()
