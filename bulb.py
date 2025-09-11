import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLCDNumber, QPushButton, QHBoxLayout
from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QPalette, QColor

class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        # 初始模式为白天模式
        self.is_dark_mode = False
        self.initUI()
        self.update_style()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle("数字时钟 - 晶体管显示")
        self.resize(400, 250)

        # 创建主垂直布局
        main_layout = QVBoxLayout()

        # 添加日期显示 (数码管样式)
        self.date_display = QLCDNumber(self)
        self.date_display.setDigitCount(10)  # yyyy-MM-dd 共10个字符
        self.date_display.setSegmentStyle(QLCDNumber.Flat)
        main_layout.addWidget(self.date_display)

        # 添加时间显示 (数码管样式)
        self.time_display = QLCDNumber(self)
        self.time_display.setDigitCount(8)  # HH:mm:ss 共8个字符
        self.time_display.setSegmentStyle(QLCDNumber.Flat)
        main_layout.addWidget(self.time_display)

        # 创建一个水平布局来放置按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)  # 添加一个伸缩空间，将按钮推向右侧

        # 创建切换模式的按钮
        self.mode_button = QPushButton("切换模式")
        self.mode_button.setToolTip("点击切换白天/夜晚模式")
        self.mode_button.clicked.connect(self.toggle_mode)
        self.mode_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        button_layout.addWidget(self.mode_button)

        # 将按钮布局添加到主布局
        main_layout.addLayout(button_layout)

        # 将布局应用到窗口
        self.setLayout(main_layout)

        # 设置计时器，每秒更新一次时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)  # 每1000毫秒更新一次

        # 初始化显示
        self.update_display()

    def update_style(self):
        # 根据当前模式更新样式
        if self.is_dark_mode:
            # 夜晚模式
            self.setStyleSheet("background-color: #1a1a1a;")
            
            date_palette = self.date_display.palette()
            date_palette.setColor(QPalette.WindowText, QColor("#00ff00"))  # 日期绿色
            self.date_display.setPalette(date_palette)

            time_palette = self.time_display.palette()
            time_palette.setColor(QPalette.WindowText, QColor("#00ff00"))  # 时间绿色
            self.time_display.setPalette(time_palette)

            self.mode_button.setStyleSheet("""
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
            """)
        else:
            # 白天模式
            self.setStyleSheet("background-color: #ffffff;")
            
            date_palette = self.date_display.palette()
            date_palette.setColor(QPalette.WindowText, QColor("blue")) # 日期蓝色
            self.date_display.setPalette(date_palette)

            time_palette = self.time_display.palette()
            time_palette.setColor(QPalette.WindowText, QColor("black")) # 时间黑色
            self.time_display.setPalette(time_palette)

            self.mode_button.setStyleSheet("""
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
            """)

    def toggle_mode(self):
        # 切换模式状态并更新样式
        self.is_dark_mode = not self.is_dark_mode
        self.update_style()

    def update_display(self):
        # 获取当前时间和日期
        current_datetime = QDateTime.currentDateTime()
        current_date = current_datetime.toString("yyyy-MM-dd")
        current_time = current_datetime.toString("HH:mm:ss")

        # 更新日期和时间显示
        self.date_display.display(current_date)
        self.time_display.display(current_time)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())
