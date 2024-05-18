import pyaudio
import wave

def play_audio(file_path):
    # 打开音频文件
    wf = wave.open(file_path, 'rb')

    # 创建 PyAudio 对象
    p = pyaudio.PyAudio()

    # 打开音频流
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # 读取音频数据并播放
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # 停止音频流
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    play_audio('data.wav')
