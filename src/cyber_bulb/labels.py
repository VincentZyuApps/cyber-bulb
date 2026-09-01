from dataclasses import dataclass
from enum import IntEnum


class LabelTier(IntEnum):
    ICON = 0
    KEY = 1
    VALUE = 2
    FULL = 3


@dataclass(frozen=True, slots=True)
class LabelParts:
    icon: str
    chinese: str
    english: str


def control_label(
    parts: LabelParts,
    chinese_key: str,
    english_key: str,
    tier: LabelTier,
) -> str:
    if tier is LabelTier.ICON:
        return parts.icon
    if tier is LabelTier.KEY:
        return f"{parts.icon} {chinese_key}"
    if tier is LabelTier.VALUE:
        return f"{parts.icon} {chinese_key}：{parts.chinese}"
    return (
        f"{parts.icon} {chinese_key}：{parts.chinese} / "
        f"{english_key}: {parts.english}"
    )


def control_tooltip(
    parts: LabelParts,
    chinese_key: str,
    english_key: str,
) -> str:
    label = control_label(parts, chinese_key, english_key, LabelTier.FULL)
    return f"{label}\n点击循环切换 / Click to cycle"
