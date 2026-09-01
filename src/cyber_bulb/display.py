from PyQt5.QtCore import QVariantAnimation
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from .digit import ColonDigit, SegmentDigit, segment_state
from .effects import (
    DIGIT_EFFECT_DURATIONS,
    ColonEffect,
    DigitEffect,
    digit_visual,
)
from .style import SegmentStyle

STYLE_TRANSITION_DURATION_MS = 180


class SegmentDisplay(QWidget):
    def __init__(
        self,
        template: str,
        parent=None,
        segment_style: SegmentStyle = SegmentStyle.CLASSIC,
    ):
        super().__init__(parent)
        self._template = template
        self._text = " " * len(template)
        self._initialized = False
        self._seed = 0
        self._effect = DigitEffect.NONE
        self._preview = False
        self._old_text = self._text
        self._changed = set()
        self._segment_style = segment_style
        self._style_mix = ((segment_style, 1.0),)
        self._style_start_mix = self._style_mix
        self._style_target = segment_style

        layout = QHBoxLayout(self)
        self._layout = layout
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        self._cells = []
        self._digits = []
        self._colons = {}
        for index, character in enumerate(template):
            if character == ":":
                cell = ColonDigit(self)
                self._colons[index] = cell
                stretch = 4
            else:
                cell = SegmentDigit(self)
                self._digits.append((index, cell))
                stretch = 10
            self._cells.append(cell)
            cell.set_style_mix(self._style_mix)
            layout.addWidget(cell, stretch)

        self._animation = QVariantAnimation(self)
        self._animation.valueChanged.connect(self._update_animation)
        self._animation.finished.connect(self._finish_animation)

        self._style_animation = QVariantAnimation(self)
        self._style_animation.setDuration(STYLE_TRANSITION_DURATION_MS)
        self._style_animation.valueChanged.connect(self._update_style_animation)
        self._style_animation.finished.connect(self._finish_style_animation)
        self._apply_style_mix()

    def text(self) -> str:
        return self._text

    def set_colors(self, active: str, background: str) -> None:
        for cell in self._cells:
            cell.set_colors(active, background)

    def set_style(self, style: SegmentStyle, animate: bool = True) -> None:
        if style is self._segment_style and not self.style_animation_running():
            return
        self._style_animation.stop()
        self._style_start_mix = self._style_mix
        self._style_target = style
        self._segment_style = style
        if not animate:
            self._finish_style_animation()
            return
        self._style_animation.setStartValue(0.0)
        self._style_animation.setEndValue(1.0)
        self._style_animation.start()

    def set_text(
        self,
        text: str,
        effect: DigitEffect = DigitEffect.NONE,
        animate: bool = True,
    ) -> None:
        if len(text) != len(self._template):
            raise ValueError("display text length does not match its template")

        self._animation.stop()
        if self._initialized:
            self._set_static(self._text)
        old_text = self._text
        self._text = text
        self._seed += 1

        if not self._initialized or not animate or effect is DigitEffect.NONE:
            self._initialized = True
            self._set_static(text)
            return

        changed = {
            index
            for index, cell in self._digits
            if old_text[index] != text[index]
        }
        if not changed:
            self._set_static(text)
            return

        self._start_animation(old_text, changed, effect, preview=False)

    def preview(self, effect: DigitEffect) -> None:
        self._animation.stop()
        self._set_static(self._text)
        if effect is DigitEffect.NONE:
            return
        changed = {index for index, cell in self._digits if self._text[index] != " "}
        self._start_animation(self._text, changed, effect, preview=True)

    def animate_colon(self, index: int, effect: ColonEffect) -> None:
        self._colons[index].animate(effect)

    def preview_colons(self, effect: ColonEffect) -> None:
        for colon in self._colons.values():
            colon.animate(effect)

    def animation_running(self) -> bool:
        return self._animation.state() == QVariantAnimation.Running

    def colon_animation_running(self, index: int) -> bool:
        return self._colons[index]._animation.state() == QVariantAnimation.Running

    def style_animation_running(self) -> bool:
        return self._style_animation.state() == QVariantAnimation.Running

    def stop_animations(self) -> None:
        self._animation.stop()
        self._style_animation.stop()
        for colon in self._colons.values():
            colon._animation.stop()

    def _update_style_animation(self, value) -> None:
        progress = float(value)
        weights = {}
        for style, weight in self._style_start_mix:
            weights[style] = weights.get(style, 0.0) + weight * (1.0 - progress)
        weights[self._style_target] = weights.get(self._style_target, 0.0) + progress
        self._style_mix = tuple(
            (style, weight) for style, weight in weights.items() if weight > 0.001
        )
        self._apply_style_mix()

    def _apply_style_mix(self) -> None:
        for cell in self._cells:
            cell.set_style_mix(self._style_mix)
        classic_weight = sum(
            weight
            for style, weight in self._style_mix
            if style is SegmentStyle.CLASSIC
        )
        self._layout.setSpacing(round(4 * (1.0 - classic_weight)))
        colon_stretch = round(4 + 6 * classic_weight)
        for index in self._colons:
            self._layout.setStretch(index, colon_stretch)

    def _finish_style_animation(self) -> None:
        self._style_mix = ((self._style_target, 1.0),)
        self._apply_style_mix()

    def _start_animation(
        self,
        old_text: str,
        changed: set[int],
        effect: DigitEffect,
        preview: bool,
    ) -> None:
        self._old_text = old_text
        self._changed = changed
        self._effect = effect
        self._preview = preview
        self._animation.setDuration(DIGIT_EFFECT_DURATIONS[effect])
        self._animation.setStartValue(0.0)
        self._animation.setEndValue(1.0)
        self._animation.start()

    def _update_animation(self, value) -> None:
        progress = float(value)
        cell_count = len(self._cells)
        for index, cell in self._digits:
            new_state = segment_state(self._text[index])
            if index not in self._changed:
                cell.set_visual(new_state)
                continue
            old_state = segment_state(self._old_text[index])
            levels = []
            boosts = []
            for segment_index in range(7):
                level, boost = digit_visual(
                    self._effect,
                    progress,
                    old_state[segment_index],
                    new_state[segment_index],
                    index,
                    cell_count,
                    segment_index,
                    self._seed,
                    self._preview,
                )
                levels.append(level)
                boosts.append(boost)
            cell.set_visual(levels, boosts)

    def _finish_animation(self) -> None:
        self._set_static(self._text)

    def _set_static(self, text: str) -> None:
        for index, cell in self._digits:
            cell.set_visual(segment_state(text[index]))
