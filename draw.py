import numpy as np
import matplotlib.pyplot as plt

def read_hex_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # 将每行的十六进制字符串转换为整数
    int_data = []
    for line in lines:
        hex_str = line.strip()
        # 转换为 16 位有符号整数
        value = int(hex_str, 16)
        if value >= 0x8000:
            value -= 0x10000
        int_data.append(value)
    
    return np.array(int_data)

def plot_waveform(data, sample_rate=44100):
    # 创建时间数组
    time = np.arange(len(data)) / sample_rate

    plt.figure(figsize=(12, 6))
    plt.plot(time, data)
    plt.title('Audio Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # 读取 data.txt 文件
    audio_data = read_hex_file('data.txt')
    
    # 将数据缩放到合理范围内（根据需要调整缩放比例）
    audio_data = np.clip(audio_data, -32768, 32767)

    # 描绘波形
    plot_waveform(audio_data)
