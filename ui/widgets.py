import math
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QTimer, QPointF, Signal
from PySide6.QtGui import QColor, QPainter, QBrush

from core.config import _c


class PulseDot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._color = QColor(_c("text_dim"))
        self._is_active = False
        self._phase = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self.setFixedSize(22, 22)

    def set_active(self, color_hex: str, active: bool):
        self._color = QColor(color_hex)
        self._is_active = active
        if active:
            self._timer.start(30)
        else:
            self._timer.stop()
        self.update()

    def _tick(self):
        self._phase = (self._phase + 0.05) % (2 * math.pi)
        self.update()

    def paintEvent(self, _e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        c = self.width() / 2.0
        if self._is_active:
            pulse = 0.5 + 0.5 * math.sin(self._phase)
            halo = QColor(self._color)
            halo.setAlphaF(0.2 * pulse)
            p.setBrush(QBrush(halo))
            p.setPen(Qt.NoPen)
            p.drawEllipse(QPointF(c, c), 7, 7)
        p.setBrush(QBrush(self._color))
        p.setPen(Qt.NoPen)
        p.drawEllipse(QPointF(c, c), 3.5, 3.5)


class Card(QFrame):
    def __init__(self, parent=None, radius=12, pad=16, accent=False):
        super().__init__(parent)
        bg = _c("accent_bg") if accent else _c("surface")
        border_col = _c("accent") if accent else _c("border")
        self.setStyleSheet(
            f"QFrame{{background:{bg};border-radius:{radius}px;border:1px solid {border_col};}}"
        )
        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(pad, pad, pad, pad)
        self._lay.setSpacing(10)

    def layout(self):
        return self._lay


class Sep(QFrame):
    def __init__(self, vertical=False, parent=None):
        super().__init__(parent)
        if vertical:
            self.setFrameShape(QFrame.VLine)
            self.setFixedWidth(1)
        else:
            self.setFrameShape(QFrame.HLine)
            self.setFixedHeight(1)
        self.setStyleSheet(f"background:{_c('line')};border:none;")


class SidebarBtn(QPushButton):
    def __init__(self, text, icon="", parent=None):
        super().__init__(parent)
        self._text = text
        self._icon = icon
        self._on = False
        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        self._refresh()

    def set_active(self, v):
        self._on = v
        self._refresh()

    def _refresh(self):
        if self._on:
            self.setStyleSheet(
                f"QPushButton{{ background: {_c('surface_hover')}; border-radius: 8px; "
                f"color: {_c('text_pri')}; text-align: left; padding-left: 12px; "
                f"font-size: 13px; font-weight: 500; border: 1px solid {_c('border')}; }}"
            )
        else:
            self.setStyleSheet(
                f"QPushButton{{ background: transparent; border-radius: 8px; "
                f"color: {_c('text_mut')}; text-align: left; padding-left: 12px; "
                f"font-size: 13px; font-weight: 400; border: 1px solid transparent; }} "
                f"QPushButton:hover{{ background: {_c('surface')}; color: {_c('text_pri')}; }}"
            )
        self.setText(f"  {self._icon}  {self._text}" if self._icon else self._text)


class PBtn(QPushButton):
    def __init__(self, text, color=None, parent=None):
        super().__init__(text, parent)
        self._c_text = color or _c("text_pri")
        self._bg = _c("surface_hover") if color else "transparent"
        self._b = color or _c("border")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(38)
        self.setStyleSheet(
            f"QPushButton{{ background: {self._bg}; color: {self._c_text}; border-radius: 8px; "
            f"font-size: 12px; font-weight: 500; border: 1px solid {self._b}; padding: 0 16px; }} "
            f"QPushButton:hover{{ border-color: {_c('text_mut')}; color: {_c('text_pri')}; background: {_c('surface')}; }} "
            f"QPushButton:pressed{{ background: rgba(0,0,0,0.05); }} "
            f"QPushButton:disabled{{ background: {_c('bg')}; color: {_c('text_dim')}; border-color: {_c('line')}; }}"
        )


class GBtn(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(34)
        self.setStyleSheet(
            f"QPushButton{{ background: transparent; color: {_c('text_mut')}; border-radius: 8px; "
            f"font-size: 12px; border: 1px solid {_c('border')}; padding: 0 14px; }} "
            f"QPushButton:hover{{ background: {_c('surface')}; color: {_c('text_pri')}; border-color: {_c('text_mut')}; }}"
        )


class TogBtn(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(34)
        self.toggled.connect(self._s)
        self._s(False)

    def _s(self, on):
        if on:
            self.setStyleSheet(
                f"QPushButton{{background:{_c('surface_hover')};color:{_c('text_pri')};border-radius:8px;font-size:12px;font-weight:500;border:1px solid {_c('accent')};padding:0 16px;}}"
            )
        else:
            self.setStyleSheet(
                f"QPushButton{{background:transparent;color:{_c('text_mut')};border-radius:8px;font-size:12px;border:1px solid {_c('border')};padding:0 16px;}} QPushButton:hover{{background:{_c('surface')};color:{_c('text_pri')};}}"
            )


class OptBtn(QPushButton):
    def __init__(self, text, idx, parent=None):
        super().__init__(parent)
        self.idx = idx
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(48)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self._st = "default"
        self._apply()
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(12)
        self.badge = QLabel("ABCD"[idx] if idx < 4 else str(idx + 1))
        self.badge.setFixedSize(24, 24)
        self.badge.setAlignment(Qt.AlignCenter)
        self.badge.setStyleSheet(
            f"background:{_c('bg')};color:{_c('text_mut')};border-radius:6px;font-size:11px;font-weight:600;border:1px solid {_c('border')};"
        )
        lay.addWidget(self.badge)
        self.tlbl = QLabel(text)
        self.tlbl.setWordWrap(True)
        self.tlbl.setStyleSheet(
            f"color:{_c('text_pri')};font-size:13px;background:transparent;border:none;"
        )
        lay.addWidget(self.tlbl, 1)
        self.ric = QLabel("")
        self.ric.setFixedWidth(16)
        self.ric.setStyleSheet("background:transparent;font-size:13px;border:none;")
        lay.addWidget(self.ric)

    def _apply(self):
        c_green, c_red = _c("green"), _c("red")
        S = {
            "default": f"QPushButton{{background:{_c('surface')};border:1px solid {_c('border')};border-radius:10px;}}QPushButton:hover{{background:{_c('surface_hover')};border:1px solid {_c('text_mut')};}}",
            "correct": f"QPushButton{{background:transparent;border:1px solid {c_green};border-radius:10px;}}",
            "wrong": f"QPushButton{{background:transparent;border:1px solid {_c('border')};border-radius:10px;}}",
            "disabled": f"QPushButton{{background:{_c('bg')};border:1px solid {_c('line')};border-radius:10px;}}",
        }
        self.setStyleSheet(S.get(self._st, S["default"]))

    def set_state(self, state):
        self._st = state
        self._apply()
        self.tlbl.setStyleSheet(
            f"color:{_c('text_pri')};font-size:13px;background:transparent;border:none;"
        )
        self.badge.setStyleSheet(
            f"background:{_c('bg')};color:{_c('text_mut')};border-radius:6px;font-size:11px;font-weight:600;border:1px solid {_c('border')};"
        )
        self.ric.setText("")
        if state == "correct":
            self.ric.setText("✓")
            self.ric.setStyleSheet(
                f"background:transparent;font-size:14px;font-weight:700;color:{_c('green')};border:none;"
            )
            self.badge.setStyleSheet(
                f"background:transparent;color:{_c('green')};border-radius:6px;font-size:11px;font-weight:700;border:1px solid {_c('green')};"
            )
        elif state == "wrong":
            self.ric.setText("✗")
            self.ric.setStyleSheet(
                f"background:transparent;font-size:14px;font-weight:700;color:{_c('red')};border:none;"
            )
            self.tlbl.setStyleSheet(
                f"color:{_c('red')};font-size:13px;background:transparent;border:none;"
            )
            self.badge.setStyleSheet(
                f"background:transparent;color:{_c('red')};border-radius:6px;font-size:11px;font-weight:700;border:1px solid {_c('red')};"
            )


class PBar(QWidget):
    def __init__(self, total=1, current=0, parent=None):
        super().__init__(parent)
        self.total = max(total, 1)
        self._current = current
        self.setFixedHeight(2)

    def set_progress(self, v):
        self._current = v
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(_c("line"))))
        p.drawRect(0, 0, self.width(), 2)
        w = int(self.width() * self._current / self.total)
        if w > 0:
            p.setBrush(QBrush(QColor(_c("accent"))))
            p.drawRect(0, 0, w, 2)


class Sidebar(QWidget):
    page_changed = Signal(str)
    NAV = [
        ("dashboard", "Dashboard", "⊞"),
        ("simulado", "Simulado Local", "📝"),
        ("simulado_ia", "Simulado IA", "✦"),
        ("config", "Configurações", "⚙"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.btns: dict[str, SidebarBtn] = {}
        self._build()

    def _build(self):
        self.setStyleSheet(
            f"QWidget{{background:{_c('bg')};border-right:1px solid {_c('border')};}}"
        )
        if self.layout():
            while self.layout().count():
                item = self.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        else:
            QVBoxLayout(self)
        lay = self.layout()
        lay.setContentsMargins(14, 24, 14, 24)
        lay.setSpacing(4)
        row = QHBoxLayout()
        tl = QLabel("CNH Simulated")
        tl.setStyleSheet(
            f"font-size:15px;font-weight:600;color:{_c('text_pri')};background:transparent;border:none;letter-spacing:-0.3px;"
        )
        row.addWidget(tl)
        row.addStretch()
        lay.addLayout(row)
        lay.addSpacing(24)
        ml = QLabel("MENU")
        ml.setStyleSheet(
            f"font-size:10px;font-weight:600;color:{_c('text_dim')};letter-spacing:1px;background:transparent;border:none;"
        )
        lay.addWidget(ml)
        lay.addSpacing(6)
        self.btns = {}
        for key, label, icon in self.NAV:
            b = SidebarBtn(label, icon)
            b.clicked.connect(lambda _, k=key: self._click(k))
            lay.addWidget(b)
            self.btns[key] = b
        lay.addStretch()
        self.ai_container = QWidget()
        ai_lay = QHBoxLayout(self.ai_container)
        ai_lay.setContentsMargins(4, 0, 4, 8)
        ai_lay.setSpacing(8)
        self.ai_dot = PulseDot()
        self.ai_dot.setFixedSize(16, 16)
        ai_lay.addWidget(self.ai_dot)
        self.ai_lbl = QLabel("IA Operando...")
        self.ai_lbl.setStyleSheet(
            f"font-size: 11px; color: {_c('accent')}; font-weight: 500;"
        )
        ai_lay.addWidget(self.ai_lbl)
        ai_lay.addStretch()
        self.ai_container.hide()
        lay.addWidget(self.ai_container)
        lay.addWidget(Sep())
        lay.addSpacing(12)
        vl = QLabel("v1.0 Edição")
        vl.setStyleSheet(
            f"font-size:10px;color:{_c('text_dim')};background:transparent;border:none;"
        )
        lay.addWidget(vl)
        self._set_active("dashboard")

    def show_ai_running(self):
        self.ai_container.show()
        self.ai_dot.set_active(_c("accent"), True)

    def hide_ai_running(self):
        self.ai_container.hide()
        self.ai_dot.set_active(_c("accent"), False)

    def rebuild(self):
        self._build()

    def _click(self, key):
        self._set_active(key)
        self.page_changed.emit(key)

    def _set_active(self, key):
        for k, b in self.btns.items():
            b.set_active(k == key)
