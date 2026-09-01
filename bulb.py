"""Backward-compatible source launcher for Cyber Bulb."""

from cyber_bulb.app import DigitalClock, main

__all__ = ["DigitalClock", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
