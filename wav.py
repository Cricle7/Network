import wave
import numpy as np

# 参数配置
sample_rate = 48000
num_channels = 1
sample_width = 2  # 16位

# 读取原始音频数据
with open('data.raw', 'rb') as raw_file:
    raw_data = raw_file.read()

# 将原始数据转换为 numpy 数组
audio_data = np.frombuffer(raw_data, dtype=np.int16)

# 写入 WAV 文件
with wave.open('data.wav', 'wb') as wf:
    wf.setnchannels(num_channels)
    wf.setsampwidth(sample_width)
    wf.setframerate(sample_rate)
    wf.writeframes(audio_data.tobytes())
