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
        animation_enabled=options.animation_enabled,
        initial_mode=options.theme_mode,
        width=options.width,
        height=options.height,
    )
    clock.show()
    return app.exec_()
