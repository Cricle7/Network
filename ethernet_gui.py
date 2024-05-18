import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import Ui_gui
import socket
from audio_play import play_audio



class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        # 目标 IP 地址和端口
        self.target_ip = '192.168.1.11'
        self.target_port = 8081
        self.local_ip = '192.168.1.105'  # 接收所有网络接口的数据包
        self.local_port = 8081  # 选择一个未被使用的端口
        self.socket = None

        self.ui = Ui_gui.Ui_MainWindow()
        self.ui.setupUi(self)

        # 连接按钮的信号
        self.ui.pushButton_2.clicked.connect(self.ethernet_transmitt)
        self.ui.pushButton.clicked.connect(self.retrieve_file)
        self.ui.radioButton.toggled.connect(self.ethernet_on_off)
        self.ui.radioButton_2.toggled.connect(self.ethernet_on_off)


        
        # 初始化定时器
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.progress = 0

        self.delay = QtCore.QTimer(self)
        self.delay.timeout.connect(self.delay_done)

    def ethernet_on_off(self, checked):
        if self.ui.radioButton.isChecked():
            # 尝试打开socket
            if not self.socket:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    self.socket.bind((self.local_ip, self.local_port))  # 修改为你的服务器地址和端口
                    self.ui.textBrowser.append('Socket Status: Opened')
                except socket.error as e:
                    self.ui.textBrowser.append(f'Failed to open socket: {e}')
        elif self.ui.radioButton_2.isChecked():
            # 关闭socket
            if self.socket:
                self.socket.close()
                self.socket = None
                self.ui.textBrowser.append('Socket Status: Closed')


    def ethernet_transmitt(self):
        if not self.socket == None:
            self.socket.sendto('xxx'.encode(), (self.target_ip, self.target_port))
            self.ui.textBrowser.append('开始发送')
            self.progress = 0  # 重置进度条
            self.ui.textBrowser.clear()  # 清空文本浏览器
            self.timer.start(40)  # 设置定时器100毫秒更新一次
        else:
            self.ui.textBrowser.append('发送失败,udp端口未打开')

    def update_progress(self):
        self.progress += 1
        # 直接设置文本框的内容，而不是追加
        self.ui.textBrowser.setText('正在推理: \n' + '■' * self.progress + ' ' * (20 - self.progress) + str(self.progress/0.2) + '%')
        if self.progress >= 20:  # 假设进度条最大值为20
            self.ui.textBrowser.append('推理完毕,等待FPGA返回数据')
            self.timer.stop()  # 停止定时器
            self.delay.start(500)

    def delay_done(self):
        self.delay.stop()
        self.ui.textBrowser.append('接收完毕，开始解析')
        self.ui.textBrowser.append('解析完毕，判断结果为 第26号')

    def retrieve_file(self):
        filename = self.ui.filename_lineEdit.text()
        self.ui.textBrowser.append(filename + ' has been found')
        play_audio(filename)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
