import keyboard
import socket
import threading
import wave
import numpy as np

# 全局变量
receiver_thread = None
stop_event = threading.Event()

# 目标 IP 地址和端口
target_ip = '192.168.1.11'
target_port = 8081

local_ip = '192.168.1.105'  # 接收所有网络接口的数据包
local_port = 8081  # 选择一个未被使用的端口

# 创建 UDP 套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((local_ip, local_port))

def receive_udp_data():
    while not stop_event.is_set():
        try:
            # 设置超时时间以便能够及时响应停止事件
            sock.settimeout(1.0)
            data, addr = sock.recvfrom(2048)
            print("从", addr, "收到数据:", data)

            # Extract payload (skip first 12 bytes)
            payload = data[12:]
            
            # Write the raw payload to a binary file
            with open('data.raw', 'ab') as file:
                file.write(payload)
            hex_pairs = [f'{payload[i]:02x}{payload[i+1]:02x}' for i in range(0, len(payload)-1, 2)]
            print("从", addr, "收到数据:", hex_pairs)

            # 追加写入文件
            with open('data.txt', 'a') as file:
                for hex_pair in hex_pairs:
                    file.write(hex_pair)
        except socket.timeout:
            continue
        except Exception as e:
            print("接收数据包时出错:", e)

def play():
    global receiver_thread, stop_event
    if receiver_thread is None or not receiver_thread.is_alive():
        stop_event.clear()
        receiver_thread = threading.Thread(target=receive_udp_data)
        receiver_thread.start()
        print("Started data reception...")

def pause():
    global stop_event
    print('Pausing...')
    stop_event.set()

def on_key_press(event):
    global receiver_thread
    if event.name == 's':
        if receiver_thread is None or not receiver_thread.is_alive():
            print("Starting data reception...")
            play()
    elif event.name == 'p':
        if receiver_thread is not None and receiver_thread.is_alive():
            print("Pausing data reception...")
            pause()
            receiver_thread.join()

# 监听按键事件
keyboard.on_press(on_key_press)
print("Press 's' to start receiving data and 'p' to pause receiving data. Press 'q' to quit.")
# 运行程序，直到按下 'q' 键退出
keyboard.wait('q')

# 程序退出时关闭套接字
sock.close()
print("Program exited.")
