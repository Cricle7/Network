import socket
import pyaudio
import keyboard

# 音频配置
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 474  # 960 字节的包 - 12 字节的 RTP 头部 = 948 字节，948 字节 / 2 字节（每个采样） = 474 个采样

# 目标 IP 地址和端口
target_ip = '192.168.1.11'
target_port = 8081

# 本地 IP 地址和端口
local_ip = '192.168.1.105'  # 接收所有网络接口的数据包
local_port = 8081  # 选择一个未被使用的端口

# 创建 UDP 套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定到本地地址和端口
sock.bind((local_ip, local_port))

# 初始化 pyaudio
audio = pyaudio.PyAudio()

# 打开音频流
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

# 打开文件用于写入去掉 RTP 头部的音频数据
file = open('data.txt', 'wb')

def send_udp_data():
  # 生成一些音频数据（这里用 silence 替代，可以替换为实际音频数据）
  rtp_header = b'\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 12 字节的 RTP 头部
  payload = b'\x00' * (960 - len(rtp_header))  # 960 字节总包长减去 12 字节的头部
  data = rtp_header + payload
  
  try:
      # 发送数据到目标地址
      sock.sendto(data, (target_ip, target_port))
  except Exception as e:
      print("发送数据包时出错:", e)

def receive_udp_data():
  try:
    # 检查套接字是否已关闭
    if not sock._closed:
      # 接收数据
      data, addr = sock.recvfrom(1500)  # 接收 960 字节的数据包
      # 去掉 RTP 头部（前 12 字节）
      audio_data = data[12:]
      # 播放接收到的音频数据
      # stream.write(audio_data)
      # 将去掉 RTP 头部的音频数据写入文件
      file.write(audio_data)
  except Exception as e:
    print("接收数据包时出错:", e)

def on_key_press(event):
  if event.name == 'space':
    flag = 1
    print("Space key pressed")
    send_udp_data()
    receive_udp_data()
  if event.name == 'p':
    print("按键 'q' 被按下，关闭套接字")
    sock.close()


  if (event.name == 'q'):
    print("按键 'q' 被按下，关闭套接字")
    sock.close()
    stream.stop_stream()
    stream.close()
    audio.terminate()
    file.close()
    exit()

# 监听按键事件
keyboard.on_press(on_key_press)
keyboard.wait('q')