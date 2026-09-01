from PyQt5.QtCore import QRectF, QSize, Qt, QVariantAnimation
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QSizePolicy, QWidget

from .effects import COLON_EFFECT_DURATIONS, ColonEffect, colon_visual
from .style import SEGMENT_PROFILES, SegmentStyle, colon_paths, segment_paths

SEGMENT_MAP = {
    " ": frozenset(),
    "-": frozenset({6}),
    "0": frozenset({0, 1, 2, 3, 4, 5}),
    "1": frozenset({1, 2}),
    "2": frozenset({0, 1, 3, 4, 6}),
    "3": frozenset({0, 1, 2, 3, 6}),
    "4": frozenset({1, 2, 5, 6}),
    "5": frozenset({0, 2, 3, 5, 6}),
    "6": frozenset({0, 2, 3, 4, 5, 6}),
    "7": frozenset({0, 1, 2}),
    "8": frozenset({0, 1, 2, 3, 4, 5, 6}),
    "9": frozenset({0, 1, 2, 3, 5, 6}),
}


def segment_state(character: str) -> tuple[bool, ...]:
    active = SEGMENT_MAP.get(character, frozenset())
    return tuple(index in active for index in range(7))


def _blend(background: QColor, foreground: QColor, amount: float) -> QColor:
    return QColor(
        round(background.red() + (foreground.red() - background.red()) * amount),
        round(background.green() + (foreground.green() - background.green()) * amount),
        round(background.blue() + (foreground.blue() - background.blue()) * amount),
    )


def _drawing_rect(outer: QRectF, style: SegmentStyle) -> QRectF:
    profile = SEGMENT_PROFILES[style]
    available_width = outer.width()
    if style is SegmentStyle.CLASSIC:
        available_width *= 5.0 / 6.0
    draw_height = min(outer.height(), available_width / profile.ratio)
    draw_width = draw_height * profile.ratio
    return QRectF(
        outer.center().x() - draw_width / 2,
        outer.center().y() - draw_height / 2,
        draw_width,
        draw_height,
    )


class SegmentDigit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._levels = [0.0] * 7
        self._boosts = [0.0] * 7
        self._active = QColor("#00ff00")
        self._background = QColor("#1a1a1a")
        self._style_mix = ((SegmentStyle.CLASSIC, 1.0),)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def sizeHint(self) -> QSize:
        return QSize(52, 96)

    def minimumSizeHint(self) -> QSize:
        return QSize(12, 24)

    def set_colors(self, active: str, background: str) -> None:
        self._active = QColor(active)
        self._background = QColor(background)
        self.update()

    def set_visual(self, levels, boosts=None) -> None:
        self._levels = [max(0.0, min(1.0, float(level))) for level in levels]
        self._boosts = [0.0] * 7 if boosts is None else list(boosts)
        self.update()

    def set_style_mix(self, style_mix) -> None:
        self._style_mix = tuple(style_mix)
        self.update()

    def paintEvent(self, event) -> None:
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for style, opacity in self._style_mix:
            painter.setRenderHint(
                QPainter.Antialiasing, style is not SegmentStyle.CLASSIC
            )
            rect = _drawing_rect(QRectF(self.rect()), style)
            self._draw_profile(painter, style, rect, opacity)

    def _draw_profile(self, painter, style, rect, opacity) -> None:
        profile = SEGMENT_PROFILES[style]
        paths = segment_paths(style, rect)
        inactive = _blend(self._background, self._active, profile.inactive_level)
        pen_width = max(1.0, min(rect.width(), rect.height()) * profile.stroke_ratio)

        for index, path in enumerate(paths):
            if profile.inactive_level:
                painter.setOpacity(opacity)
                if profile.outline:
                    painter.setBrush(Qt.NoBrush)
                    painter.setPen(QPen(inactive, pen_width))
                else:
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(inactive)
                painter.drawPath(path)

            level = self._levels[index]
            if level <= 0:
                continue
            lit = _blend(self._background, self._active, level)
            boost = max(0.0, min(1.0, self._boosts[index]))
            if boost:
                lit = _blend(lit, QColor("#ffffff"), 0.32 * boost)
            painter.setOpacity(opacity)
            if profile.outline:
                painter.setBrush(Qt.NoBrush)
                painter.setPen(QPen(lit, pen_width))
            else:
                painter.setPen(Qt.NoPen)
                painter.setBrush(lit)
            painter.drawPath(path)

        painter.setOpacity(1.0)


class ColonDigit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._levels = [1.0, 1.0]
        self._boosts = [0.0, 0.0]
        self._active = QColor("#00ff00")
        self._background = QColor("#1a1a1a")
        self._style_mix = ((SegmentStyle.CLASSIC, 1.0),)
        self._animation = QVariantAnimation(self)
        self._animation.valueChanged.connect(self._update_animation)
        self._animation.finished.connect(self._finish_animation)
        self._effect = ColonEffect.NONE
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def sizeHint(self) -> QSize:
        return QSize(24, 96)

    def minimumSizeHint(self) -> QSize:
        return QSize(8, 24)

    def set_colors(self, active: str, background: str) -> None:
        self._active = QColor(active)
        self._background = QColor(background)
        self.update()

    def set_style_mix(self, style_mix) -> None:
        self._style_mix = tuple(style_mix)
        self.update()

    def animate(self, effect: ColonEffect) -> None:
        self._animation.stop()
        self._effect = effect
        if effect is ColonEffect.NONE:
            self._finish_animation()
            return
        self._animation.setDuration(COLON_EFFECT_DURATIONS[effect])
        self._animation.setStartValue(0.0)
        self._animation.setEndValue(1.0)
        self._animation.start()

    def _update_animation(self, value) -> None:
        top, bottom = colon_visual(self._effect, float(value))
        self._levels = [top[0], bottom[0]]
        self._boosts = [top[1], bottom[1]]
        self.update()

    def _finish_animation(self) -> None:
        self._levels = [1.0, 1.0]
        self._boosts = [0.0, 0.0]
        self.update()

    def paintEvent(self, event) -> None:
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for style, opacity in self._style_mix:
            painter.setRenderHint(
                QPainter.Antialiasing, style is not SegmentStyle.CLASSIC
            )
            rect = _drawing_rect(QRectF(self.rect()), style)
            profile = SEGMENT_PROFILES[style]
            paths = colon_paths(style, rect)
            inactive = _blend(self._background, self._active, profile.inactive_level)
            pen_width = max(1.0, min(rect.width(), rect.height()) * profile.stroke_ratio)
            for index, path in enumerate(paths):
                if profile.inactive_level:
                    painter.setOpacity(opacity)
                    if profile.outline:
                        painter.setBrush(Qt.NoBrush)
                        painter.setPen(QPen(inactive, pen_width))
                    else:
                        painter.setPen(Qt.NoPen)
                        painter.setBrush(inactive)
                    painter.drawPath(path)
                lit = _blend(self._background, self._active, self._levels[index])
                if self._boosts[index]:
                    lit = _blend(lit, QColor("#ffffff"), 0.32 * self._boosts[index])
                painter.setOpacity(opacity)
                if profile.outline:
                    painter.setBrush(Qt.NoBrush)
                    painter.setPen(QPen(lit, pen_width))
                else:
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(lit)
                painter.drawPath(path)
        painter.setOpacity(1.0)
