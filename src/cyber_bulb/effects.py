import math
from enum import Enum

from .labels import LabelParts


class DigitEffect(str, Enum):
    NONE = "none"
    AFTERGLOW = "afterglow"
    PULSE = "pulse"
    SCAN = "scan"
    WAVE = "wave"
    GLITCH = "glitch"


class ColonEffect(str, Enum):
    NONE = "none"
    BLINK = "blink"
    PULSE = "pulse"
    DOUBLE = "double"
    ALTERNATE = "alternate"


DIGIT_EFFECT_ORDER = (
    DigitEffect.AFTERGLOW,
    DigitEffect.PULSE,
    DigitEffect.SCAN,
    DigitEffect.WAVE,
    DigitEffect.GLITCH,
    DigitEffect.NONE,
)

COLON_EFFECT_ORDER = (
    ColonEffect.BLINK,
    ColonEffect.PULSE,
    ColonEffect.DOUBLE,
    ColonEffect.ALTERNATE,
    ColonEffect.NONE,
)

DIGIT_EFFECT_NAMES = {
    DigitEffect.NONE: LabelParts("⏹️", "无", "None"),
    DigitEffect.AFTERGLOW: LabelParts("🌫️", "余辉", "Glow"),
    DigitEffect.PULSE: LabelParts("💡", "脉冲", "Pulse"),
    DigitEffect.SCAN: LabelParts("📡", "扫描", "Scan"),
    DigitEffect.WAVE: LabelParts("🌊", "波浪", "Wave"),
    DigitEffect.GLITCH: LabelParts("⚡", "故障", "Glitch"),
}

COLON_EFFECT_NAMES = {
    ColonEffect.NONE: LabelParts("⏹️", "无", "None"),
    ColonEffect.BLINK: LabelParts("⏱️", "熄闪", "Blink"),
    ColonEffect.PULSE: LabelParts("✨", "脉冲", "Pulse"),
    ColonEffect.DOUBLE: LabelParts("⚡", "双闪", "Double"),
    ColonEffect.ALTERNATE: LabelParts("🔁", "交替", "Alternate"),
}

DIGIT_EFFECT_DURATIONS = {
    DigitEffect.NONE: 0,
    DigitEffect.AFTERGLOW: 260,
    DigitEffect.PULSE: 220,
    DigitEffect.SCAN: 320,
    DigitEffect.WAVE: 360,
    DigitEffect.GLITCH: 240,
}

COLON_EFFECT_DURATIONS = {
    ColonEffect.NONE: 0,
    ColonEffect.BLINK: 180,
    ColonEffect.PULSE: 180,
    ColonEffect.DOUBLE: 260,
    ColonEffect.ALTERNATE: 240,
}


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _local_progress(progress: float, delay: float, span: float) -> float:
    return _clamp((progress - delay) / span)


def digit_visual(
    effect: DigitEffect,
    progress: float,
    old_on: bool,
    new_on: bool,
    cell_index: int,
    cell_count: int,
    segment_index: int,
    seed: int,
    preview: bool,
) -> tuple[float, float]:
    progress = _clamp(progress)
    if effect is DigitEffect.NONE or progress >= 1.0:
        return (1.0 if new_on else 0.0, 0.0)

    if preview:
        if not new_on:
            return 0.0, 0.0
        if effect is DigitEffect.AFTERGLOW:
            return 1.0 - 0.58 * math.sin(math.pi * progress), 0.0
        if effect is DigitEffect.PULSE:
            return 0.62 + 0.38 * progress, math.sin(math.pi * progress)
        if effect is DigitEffect.SCAN:
            local = _local_progress(progress, segment_index * 0.065, 0.55)
            return local, 0.15 * math.sin(math.pi * local)
        if effect is DigitEffect.WAVE:
            delay = 0.35 * cell_index / max(1, cell_count - 1)
            local = _local_progress(progress, delay, 0.65)
            return 0.45 + 0.55 * local, 0.25 * math.sin(math.pi * local)

    if effect is DigitEffect.AFTERGLOW:
        if old_on and not new_on:
            return 1.0 - _local_progress(progress, 0.0, 0.72), 0.0
        if new_on and not old_on:
            local = _local_progress(progress, 0.18, 0.82)
            return local, 0.18 * math.sin(math.pi * local)
        return (1.0 if new_on else 0.0, 0.0)

    if effect is DigitEffect.PULSE:
        if not new_on:
            return (1.0 - _local_progress(progress, 0.0, 0.42)) if old_on else 0.0, 0.0
        local = _local_progress(progress, 0.08, 0.92)
        return 0.48 + 0.52 * local, math.sin(math.pi * local)

    if effect is DigitEffect.SCAN:
        local = _local_progress(progress, segment_index * 0.065, 0.55)
        if new_on:
            return local, 0.12 * math.sin(math.pi * local)
        return (1.0 - local) if old_on else 0.0, 0.0

    if effect is DigitEffect.WAVE:
        delay = 0.35 * cell_index / max(1, cell_count - 1)
        local = _local_progress(progress, delay, 0.65)
        if new_on:
            return local, 0.2 * math.sin(math.pi * local)
        return (1.0 - local) if old_on else 0.0, 0.0

    if effect is DigitEffect.GLITCH:
        if progress >= 0.82:
            local = _local_progress(progress, 0.82, 0.18)
            return (local if new_on else 0.0), 0.0
        phase = int(progress * 18)
        noise = (seed * 31 + cell_index * 17 + segment_index * 13 + phase * 7) % 19
        base_on = new_on if progress >= 0.34 else old_on
        if noise in (0, 5) and base_on:
            return 0.08, 0.0
        if noise == 9 and not base_on:
            return 0.42, 0.22
        return (0.82 if base_on else 0.0), (0.16 if noise == 3 else 0.0)

    return (1.0 if new_on else 0.0, 0.0)


def colon_visual(
    effect: ColonEffect, progress: float
) -> tuple[tuple[float, float], tuple[float, float]]:
    progress = _clamp(progress)
    if effect is ColonEffect.NONE or progress >= 1.0:
        return (1.0, 0.0), (1.0, 0.0)

    if effect is ColonEffect.BLINK:
        level = abs(2.0 * progress - 1.0)
        return (level, 0.0), (level, 0.0)

    if effect is ColonEffect.PULSE:
        boost = math.sin(math.pi * progress)
        return (1.0, boost), (1.0, boost)

    if effect is ColonEffect.DOUBLE:
        level = 0.12 if math.sin(4.0 * math.pi * progress) < 0 else 1.0
        return (level, 0.0), (level, 0.0)

    if effect is ColonEffect.ALTERNATE:
        top = 0.15 + 0.85 * abs(math.cos(math.pi * progress))
        bottom = 0.15 + 0.85 * abs(math.sin(math.pi * progress))
        return (top, 0.0), (bottom, 0.0)

    return (1.0, 0.0), (1.0, 0.0)
