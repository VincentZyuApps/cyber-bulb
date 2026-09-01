import contextlib
import io
import signal
import unittest

from cyber_bulb.app import INTERRUPT_EXIT_CODE, INTERRUPT_MESSAGE, _run_event_loop


class InterruptibleApplication:
    def __init__(self):
        self.exit_code = 0

    def exit(self, exit_code: int) -> None:
        self.exit_code = exit_code

    def exec_(self) -> int:
        signal.raise_signal(signal.SIGINT)
        signal.raise_signal(signal.SIGINT)
        return self.exit_code


class FailingApplication:
    def exec_(self) -> int:
        raise RuntimeError("event loop failed")


class EventLoopTests(unittest.TestCase):
    def test_sigint_prints_once_exits_130_and_restores_handler(self):
        previous_handler = signal.getsignal(signal.SIGINT)
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            exit_code = _run_event_loop(InterruptibleApplication())

        self.assertEqual(exit_code, INTERRUPT_EXIT_CODE)
        self.assertEqual(output.getvalue().strip(), INTERRUPT_MESSAGE)
        self.assertIs(signal.getsignal(signal.SIGINT), previous_handler)

    def test_other_exceptions_propagate_and_restore_handler(self):
        previous_handler = signal.getsignal(signal.SIGINT)

        with self.assertRaisesRegex(RuntimeError, "event loop failed"):
            _run_event_loop(FailingApplication())

        self.assertIs(signal.getsignal(signal.SIGINT), previous_handler)


if __name__ == "__main__":
    unittest.main()
