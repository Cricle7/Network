import keyboard
import socket
flag = 0
# 目标 IP 地址和端口
target_ip = '192.168.1.11'
target_port = 8081

local_ip = '192.168.1.105'  # 接收所有网络接口的数据包
local_port = 8081  # 选择一个未被使用的端口

data = b'Hello, UDP!'

# 创建 UDP 套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((local_ip, local_port))

def receive_udp_data():
    try:
        # 接收数据
        data, addr = sock.recvfrom(2048)
        print("从", addr, "收到数据:", data)
    except Exception as e:
        print("接收数据包时出错:", e)


def send_udp_data():
    # 要发送的数据
    data = b'Hello, UDP!'
    
    try:
        # 发送数据到目标地址
        sock.sendto(data, (target_ip, target_port))
        print("数据包发送成功！")
    except Exception as e:
        print("发送数据包时出错:", e)

def on_key_press(event):
  if event.name == 'space':
    flag = 1
    print("Space key pressed")
    send_udp_data()
    receive_udp_data()
  if event.name == 'p':
    print("按键 'q' 被按下，关闭套接字")
    sock.close()

# 监听按键事件
keyboard.on_press(on_key_press)
# 运行程序，直到按下 'q' 键退出
keyboard.wait('q')