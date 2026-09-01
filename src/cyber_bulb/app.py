import signal
import sys
from collections.abc import Sequence
from types import FrameType

from PyQt5.QtWidgets import QApplication

from .cli import parse_runtime_options
from .window import DigitalClock

__all__ = ["DigitalClock", "main"]

INTERRUPT_EXIT_CODE = 130
INTERRUPT_MESSAGE = "👋 收到 Ctrl+C，正在退出。 / Ctrl+C received, exiting."


def _run_event_loop(app: QApplication) -> int:
    interrupted = False

    def handle_interrupt(_signum: int, _frame: FrameType | None) -> None:
        nonlocal interrupted
        if interrupted:
            return
        interrupted = True
        print(INTERRUPT_MESSAGE, flush=True)
        app.exit(INTERRUPT_EXIT_CODE)

    previous_handler = signal.signal(signal.SIGINT, handle_interrupt)
    try:
        return app.exec_()
    finally:
        signal.signal(signal.SIGINT, previous_handler)


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
    return _run_event_loop(app)
