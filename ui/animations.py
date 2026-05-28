from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsOpacityEffect
from PySide6.QtCore import (
    QPropertyAnimation,
    QEasingCurve,
    QPoint,
    QParallelAnimationGroup,
)


def fade_in_widget(widget, duration=250):
    if not widget:
        return
    if widget.graphicsEffect():
        widget.setGraphicsEffect(None)
    eff = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(eff)
    anim = QPropertyAnimation(eff, b"opacity", widget)
    anim.setDuration(duration)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.OutCubic)
    anim.finished.connect(lambda: widget.setGraphicsEffect(None))
    anim.start(QPropertyAnimation.DeleteWhenStopped)
    widget._fade_anim = anim


class AnimatedPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.wrapper = QWidget(self)
        self.wrapper.setStyleSheet("background:transparent;")
        self.lay = QVBoxLayout(self.wrapper)
        self.lay.setContentsMargins(0, 0, 0, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if (
            not hasattr(self, "anim_group")
            or self.anim_group.state() != QPropertyAnimation.Running
        ):
            self.wrapper.resize(self.size())
            self.wrapper.move(0, 0)
        else:
            self.wrapper.resize(self.size())

    def slide_in(self, direction_up=True):
        if self.wrapper.graphicsEffect():
            self.wrapper.setGraphicsEffect(None)
        eff = QGraphicsOpacityEffect(self.wrapper)
        self.wrapper.setGraphicsEffect(eff)
        self.anim_group = QParallelAnimationGroup(self)
        fade = QPropertyAnimation(eff, b"opacity")
        fade.setDuration(350)
        fade.setStartValue(0.0)
        fade.setEndValue(1.0)
        fade.setEasingCurve(QEasingCurve.OutCubic)
        slide = QPropertyAnimation(self.wrapper, b"pos")
        slide.setDuration(400)
        start_y = 30 if direction_up else -30
        slide.setStartValue(QPoint(0, start_y))
        slide.setEndValue(QPoint(0, 0))
        slide.setEasingCurve(QEasingCurve.OutQuart)
        self.anim_group.addAnimation(fade)
        self.anim_group.addAnimation(slide)
        self.anim_group.finished.connect(lambda: self.wrapper.setGraphicsEffect(None))
        self.anim_group.start(QPropertyAnimation.DeleteWhenStopped)
