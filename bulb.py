import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLCDNumber
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QPalette, QColor

class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle("数字时钟 - 晶体管显示")
        self.resize(400, 250)

        # 创建一个垂直布局
        layout = QVBoxLayout()

        # 添加日期显示 (蓝色，数码管样式)
        self.date_display = QLCDNumber(self)
        self.date_display.setDigitCount(10)  # yyyy-MM-dd 共10个字符
        self.date_display.setSegmentStyle(QLCDNumber.Flat)
        
        # 设置日期显示为蓝色
        date_palette = self.date_display.palette()
        date_palette.setColor(QPalette.WindowText, QColor("blue"))
        self.date_display.setPalette(date_palette)
        
        layout.addWidget(self.date_display)

        # 添加时间显示 (黑色，数码管样式)
        self.time_display = QLCDNumber(self)
        self.time_display.setDigitCount(8)  # HH:MM:SS共8个字符
        self.time_display.setSegmentStyle(QLCDNumber.Flat)
        
        # 设置时间显示为黑色
        time_palette = self.time_display.palette()
        time_palette.setColor(QPalette.WindowText, QColor("black"))
        self.time_display.setPalette(time_palette)
        
        layout.addWidget(self.time_display)

        # 将布局应用到窗口
        self.setLayout(layout)

        # 设置计时器，每秒更新一次时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)  # 每1000毫秒更新一次

        # 初始化显示
        self.update_display()

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
