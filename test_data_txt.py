import wave
import numpy as np
import pyaudio

def hex_to_raw(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    with open(output_file, 'wb') as raw_file:
        for line in lines:
            hex_str = line.strip()
            raw_data = bytes.fromhex(hex_str)
            raw_file.write(raw_data)

def raw_to_wav(input_file, output_file, sample_rate=44100):
    with open(input_file, 'rb') as raw_file:
        raw_data = raw_file.read()
    
    audio_data = np.frombuffer(raw_data, dtype=np.int16)
    
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)  # 单声道
        wf.setsampwidth(2)  # 16位 (2 bytes)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

def play_audio(file_path):
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    hex_to_raw('data.txt', 'data.raw')
    raw_to_wav('data.raw', 'data.wav')
    play_audio('data.wav')
