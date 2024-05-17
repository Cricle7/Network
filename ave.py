import socket
import pyaudio
import keyboard

# 设置音频流参数
FORMAT = pyaudio.paInt16  # 与FPGA发送的数据格式匹配
CHANNELS = 1              # 单声道
RATE = 48000             # 样本频率，与FPGA设置匹配
CHUNK = 474  # 960 字节的包 - 12 字节的 RTP 头部 = 948 字节，948 字节 / 2 字节（每个采样） = 474 个采样

# 初始化PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

# 设置UDP监听
UDP_IP = "192.168.1.105"        # 监听所有的IP
UDP_PORT = 8081          # 监听的端口号
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 使用IPv4和UDP
sock.bind((UDP_IP, UDP_PORT))

print("Listening for audio samples...")

try:
    while True:
        data, addr = sock.recvfrom(4096)  # 缓冲区大小为4096
        print(data)
        stream.write(data)                # 播放接收到的音频数据
except KeyboardInterrupt:
    print("Stopped by User")

# 关闭流
def on_key_press(event):
  if event.name == 'p':
    print("按键 'q' 被按下，关闭套接字")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()

# 监听按键事件
keyboard.on_press(on_key_press)
# 运行程序，直到按下 'q' 键退出
keyboard.wait('q')
