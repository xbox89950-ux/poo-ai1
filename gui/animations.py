"""Custom animated widgets for Poo UI"""
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QPainter, QColor, QRadialGradient
import math

class AIOrb(QWidget):
    def __init__(self, parent=None, size=120):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self._phase = 0
        self._active = False
        self._color = QColor(100, 200, 255)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(30)

    def set_active(self, active: bool):
        self._active = active
        self.update()

    def _animate(self):
        self._phase += 0.1
        if self._phase > 2 * math.pi:
            self._phase = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        cx, cy = self.width() / 2, self.height() / 2
        base_radius = min(cx, cy) * 0.7
        if self._active:
            pulse = math.sin(self._phase) * 8
            radius = base_radius + pulse
            alpha = 180 + int(math.sin(self._phase) * 40)
        else:
            radius = base_radius
            alpha = 120
        gradient = QRadialGradient(cx, cy, radius)
        gradient.setColorAt(0, QColor(self._color.red(), self._color.green(), self._color.blue(), alpha))
        gradient.setColorAt(0.7, QColor(self._color.red(), self._color.green(), self._color.blue(), alpha // 2))
        gradient.setColorAt(1, QColor(self._color.red(), self._color.green(), self._color.blue(), 0))
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(cx - radius), int(cy - radius), int(radius * 2), int(radius * 2))


class VoiceWave(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self._bars = 20
        self._values = [0.2] * self._bars
        self._active = False
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_bars)
        self._timer.start(50)

    def set_active(self, active: bool):
        self._active = active
        if not active:
            self._values = [0.2] * self._bars

    def _update_bars(self):
        import random
        if self._active:
            self._values = [random.uniform(0.3, 1.0) for _ in range(self._bars)]
        else:
            self._values = [max(0.1, v - 0.05) for v in self._values]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        bar_width = self.width() / self._bars
        color = QColor(100, 200, 255)
        for i, val in enumerate(self._values):
            h = val * self.height()
            x = i * bar_width + bar_width * 0.2
            w = bar_width * 0.6
            y = (self.height() - h) / 2
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(int(x), int(y), int(w), int(h), 4, 4)


class TypingIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self._dots = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(300)

    def _animate(self):
        self._dots = (self._dots + 1) % 4
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(150, 150, 150))
        painter.setPen(Qt.PenStyle.NoPen)
        for i in range(3):
            x = 10 + i * 18
            y = self.height() / 2
            radius = 4 if i < self._dots else 2
            painter.drawEllipse(int(x - radius), int(y - radius), radius * 2, radius * 2)
