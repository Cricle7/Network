import keyboard
import numpy as np
import pyaudio

# 设置一个标志变量来控制循环
running = True


def end_loop():
    global running
    running = False


# 监听P键，按下时调用end_loop函数
keyboard.add_hotkey('p', end_loop)


# 生成1 kHz正弦波的函数
def generate_sine_wave(frequency, sample_rate, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    note = np.sin(2 * np.pi * frequency * t)
    # 将正弦波信号转换为int16格式
    audio_data = (note * 32767).astype(np.int16)
    return audio_data

# 音频流参数
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024  # 从数组中一次读取的样本数

# 生成音频数据
duration = 1  # 持续1秒
frequency = 1000  # 1 kHz
audio_data = generate_sine_wave(frequency, RATE, duration)

# 初始化PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

print("Playing audio...")

index = 0

while running:
    # 如果当前读取的数据块将超出数组末尾，则重新开始
    end_index = index + CHUNK
    if end_index > len(audio_data):
        end_index = CHUNK - (len(audio_data) - index)
        data = np.concatenate((audio_data[index:], audio_data[:end_index])).tobytes()
        index = end_index
    else:
        data = audio_data[index:end_index].tobytes()
        index = end_index

    # 播放音频数据
    stream.write(data)

    # 如果到达数据末尾，从头开始
    if index >= len(audio_data):
        index = 0


# 关闭流
stream.stop_stream()
stream.close()
audio.terminate()

