import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QVBoxLayout, QLabel

class SocketController(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.socket = None

    def init_ui(self):
        # 设置窗口标题
        self.setWindowTitle('Socket Control Example')

        # 创建radio buttons
        self.radio_open = QRadioButton('Open Socket')
        self.radio_close = QRadioButton('Close Socket')
        self.status_label = QLabel('Socket Status: Closed')

        # 连接信号与槽
        self.radio_open.toggled.connect(self.handle_socket)
        self.radio_close.toggled.connect(self.handle_socket)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.radio_open)
        layout.addWidget(self.radio_close)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        # 设置窗口初始大小
        self.resize(300, 150)

    def handle_socket(self, checked):
        if self.radio_open.isChecked():
            # 尝试打开socket
            if not self.socket:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    self.socket.connect(('localhost', 9999))  # 修改为你的服务器地址和端口
                    self.status_label.setText('Socket Status: Opened')
                except socket.error as e:
                    self.status_label.setText(f'Failed to open socket: {e}')
        elif self.radio_close.isChecked():
            # 关闭socket
            if self.socket:
                self.socket.close()
                self.socket = None
                self.status_label.setText('Socket Status: Closed')

app = QApplication(sys.argv)
window = SocketController()
window.show()
sys.exit(app.exec_())
