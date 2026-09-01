from dataclasses import dataclass
from enum import Enum

from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPainterPath, QPolygonF

from .labels import LabelParts


class SegmentStyle(str, Enum):
    CLASSIC = "classic"
    ROUNDED = "rounded"
    OUTLINE = "outline"


SEGMENT_STYLE_ORDER = (
    SegmentStyle.CLASSIC,
    SegmentStyle.ROUNDED,
    SegmentStyle.OUTLINE,
)

SEGMENT_STYLE_NAMES = {
    SegmentStyle.CLASSIC: LabelParts("◆", "经典", "Classic"),
    SegmentStyle.ROUNDED: LabelParts("●", "圆角", "Rounded"),
    SegmentStyle.OUTLINE: LabelParts("◇", "描边", "Outline"),
}


@dataclass(frozen=True, slots=True)
class SegmentProfile:
    ratio: float
    inactive_level: float
    outline: bool = False
    stroke_ratio: float = 0.012


SEGMENT_PROFILES = {
    SegmentStyle.CLASSIC: SegmentProfile(0.50, 0.0),
    SegmentStyle.ROUNDED: SegmentProfile(0.56, 0.055),
    SegmentStyle.OUTLINE: SegmentProfile(0.56, 0.045, True, 0.018),
}


def _path(points: list[QPointF]) -> QPainterPath:
    path = QPainterPath()
    path.addPolygon(QPolygonF(points))
    path.closeSubpath()
    return path


def _point(rect: QRectF, x: float, y: float) -> QPointF:
    return QPointF(rect.x() + x * rect.width(), rect.y() + y * rect.height())


def _hex_segments(
    rect: QRectF,
    horizontal_half: float,
    vertical_half: float,
    left: float,
    right: float,
    top_gap: float,
    middle_gap: float,
) -> list[QPainterPath]:
    def horizontal(center: float) -> QPainterPath:
        tip = horizontal_half * 0.78
        return _path(
            [
                _point(rect, left, center),
                _point(rect, left + tip, center - horizontal_half),
                _point(rect, right - tip, center - horizontal_half),
                _point(rect, right, center),
                _point(rect, right - tip, center + horizontal_half),
                _point(rect, left + tip, center + horizontal_half),
            ]
        )

    def vertical(center: float, top: float, bottom: float) -> QPainterPath:
        tip = vertical_half * 0.72
        return _path(
            [
                _point(rect, center, top),
                _point(rect, center + vertical_half, top + tip),
                _point(rect, center + vertical_half, bottom - tip),
                _point(rect, center, bottom),
                _point(rect, center - vertical_half, bottom - tip),
                _point(rect, center - vertical_half, top + tip),
            ]
        )

    return [
        horizontal(top_gap),
        vertical(right, top_gap + horizontal_half, 0.5 - middle_gap),
        vertical(right, 0.5 + middle_gap, 1.0 - top_gap - horizontal_half),
        horizontal(1.0 - top_gap),
        vertical(left, 0.5 + middle_gap, 1.0 - top_gap - horizontal_half),
        vertical(left, top_gap + horizontal_half, 0.5 - middle_gap),
        horizontal(0.5),
    ]


def _rounded_path(rect: QRectF) -> QPainterPath:
    path = QPainterPath()
    radius = min(rect.width(), rect.height()) * 0.45
    path.addRoundedRect(rect, radius, radius)
    return path


def _rounded_segments(rect: QRectF) -> list[QPainterPath]:
    def scaled(x: float, y: float, width: float, height: float) -> QRectF:
        return QRectF(
            rect.x() + x * rect.width(),
            rect.y() + y * rect.height(),
            width * rect.width(),
            height * rect.height(),
        )

    horizontal = [
        scaled(0.16, 0.025, 0.68, 0.095),
        scaled(0.16, 0.88, 0.68, 0.095),
        scaled(0.16, 0.4525, 0.68, 0.095),
    ]
    vertical = [
        scaled(0.80, 0.10, 0.12, 0.37),
        scaled(0.80, 0.53, 0.12, 0.37),
        scaled(0.08, 0.53, 0.12, 0.37),
        scaled(0.08, 0.10, 0.12, 0.37),
    ]
    paths = [_rounded_path(item) for item in horizontal + vertical]
    return [paths[0], paths[3], paths[4], paths[1], paths[5], paths[6], paths[2]]


def _classic_segments(rect: QRectF) -> list[QPainterPath]:
    seg_len = max(5, round(rect.width()))
    width = seg_len // 5
    half_width = width // 2
    x = round(rect.center().x() - seg_len / 2)
    y = round(rect.center().y() - seg_len)

    def polygon(points: list[tuple[int, int]]) -> QPainterPath:
        return _path([QPointF(x + px, y + py) for px, py in points])

    # Exact integer offsets from Qt 5.15 QLCDNumberPrivate::drawSegment.
    top = polygon(
        [(0, 0), (seg_len - 1, 0), (seg_len - width - 1, width), (width, width)]
    )
    upper_left = polygon(
        [(0, 1), (width, width + 1), (width, seg_len - half_width - 1), (0, seg_len - 1)]
    )
    upper_right = polygon(
        [
            (seg_len - 1, 1),
            (seg_len - 1, seg_len - 1),
            (seg_len - width - 1, seg_len - half_width - 1),
            (seg_len - width - 1, width + 1),
        ]
    )
    if width & 1:
        lower_middle = [
            (seg_len - width - 3, seg_len + half_width + 1),
            (width + 2, seg_len + half_width + 1),
        ]
    else:
        lower_middle = [
            (seg_len - width - 1, seg_len + half_width),
            (width, seg_len + half_width),
        ]
    middle = polygon(
        [
            (0, seg_len),
            (width, seg_len - half_width),
            (seg_len - width - 1, seg_len - half_width),
            (seg_len - 1, seg_len),
            *lower_middle,
        ]
    )
    lower_left = polygon(
        [
            (0, seg_len + 1),
            (width, seg_len + 1 + half_width),
            (width, 2 * seg_len - width - 1),
            (0, 2 * seg_len - 1),
        ]
    )
    lower_right = polygon(
        [
            (seg_len - 1, seg_len + 1),
            (seg_len - 1, 2 * seg_len - 1),
            (seg_len - width - 1, 2 * seg_len - width - 1),
            (seg_len - width - 1, seg_len + 1 + half_width),
        ]
    )
    bottom = polygon(
        [
            (0, 2 * seg_len),
            (width, 2 * seg_len - width),
            (seg_len - width - 1, 2 * seg_len - width),
            (seg_len - 1, 2 * seg_len),
        ]
    )
    return [top, upper_right, lower_right, bottom, lower_left, upper_left, middle]


def segment_paths(style: SegmentStyle, rect: QRectF) -> list[QPainterPath]:
    if style is SegmentStyle.CLASSIC:
        return _classic_segments(rect)
    if style is SegmentStyle.OUTLINE:
        return _hex_segments(rect, 0.045, 0.065, 0.14, 0.86, 0.06, 0.03)
    return _rounded_segments(rect)


def colon_paths(style: SegmentStyle, rect: QRectF) -> list[QPainterPath]:
    if style is SegmentStyle.CLASSIC:
        seg_len = max(5, round(rect.width()))
        diameter = seg_len // 5
        x = round(rect.center().x() - seg_len / 2)
        y = round(rect.center().y() - seg_len)
        left = x + seg_len // 2 - diameter // 2 + 1
        paths = []
        for top in (y + seg_len // 2, y + 3 * seg_len // 2):
            path = QPainterPath()
            path.addRect(QRectF(left, top, diameter, diameter))
            paths.append(path)
        return paths
    else:
        diameter = max(3.0, min(rect.width() * 0.48, rect.height() * 0.11))
        centers = (0.36, 0.64)
    paths = []
    for center_y in centers:
        dot = QRectF(
            rect.center().x() - diameter / 2,
            rect.y() + rect.height() * center_y - diameter / 2,
            diameter,
            diameter,
        )
        path = QPainterPath()
        if style is SegmentStyle.CLASSIC:
            path.addRect(dot)
        else:
            path.addEllipse(dot)
        paths.append(path)
    return paths
