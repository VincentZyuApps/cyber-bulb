import sys

from PyQt5.QtCore import QDateTime, QTimer
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLCDNumber,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_mode = False
        self.init_ui()
        self.update_style()

    def init_ui(self):
        self.setWindowTitle("数字时钟 - 晶体管显示")
        self.resize(400, 250)

        main_layout = QVBoxLayout()

        self.date_display = QLCDNumber(self)
        self.date_display.setDigitCount(10)
        self.date_display.setSegmentStyle(QLCDNumber.Flat)
        main_layout.addWidget(self.date_display)

        self.time_display = QLCDNumber(self)
        self.time_display.setDigitCount(8)
        self.time_display.setSegmentStyle(QLCDNumber.Flat)
        main_layout.addWidget(self.time_display)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        self.mode_button = QPushButton("切换模式")
        self.mode_button.setToolTip("点击切换白天/夜晚模式")
        self.mode_button.clicked.connect(self.toggle_mode)
        button_layout.addWidget(self.mode_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)
        self.update_display()

    def update_style(self):
        if self.is_dark_mode:
            self.setStyleSheet("background-color: #1a1a1a;")

            date_palette = self.date_display.palette()
            date_palette.setColor(QPalette.WindowText, QColor("#00ff00"))
            self.date_display.setPalette(date_palette)

            time_palette = self.time_display.palette()
            time_palette.setColor(QPalette.WindowText, QColor("#00ff00"))
            self.time_display.setPalette(time_palette)

            self.mode_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #2e2e2e;
                    color: white;
                    border: 1px solid #4d4d4d;
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #3b3b3b;
                }
                """
            )
        else:
            self.setStyleSheet("background-color: #ffffff;")

            date_palette = self.date_display.palette()
            date_palette.setColor(QPalette.WindowText, QColor("blue"))
            self.date_display.setPalette(date_palette)

            time_palette = self.time_display.palette()
            time_palette.setColor(QPalette.WindowText, QColor("black"))
            self.time_display.setPalette(time_palette)

            self.mode_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #f0f0f0;
                    color: black;
                    border: 1px solid #dcdcdc;
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                """
            )

    def toggle_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_style()

    def update_display(self):
        current_datetime = QDateTime.currentDateTime()
        self.date_display.display(current_datetime.toString("yyyy-MM-dd"))
        self.time_display.display(current_datetime.toString("HH:mm:ss"))


def main() -> int:
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    return app.exec_()
