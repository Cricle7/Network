import numpy as np
import wave

def read_hex_file(file_path):
    with open(file_path, 'r') as file:
        hex_data = file.read().strip()
    
    if len(hex_data) % 4 != 0:
        raise ValueError("Hex data length is not a multiple of 4")
    
    int_data = []
    top_count = 0
    bottom_count = 0
    for i in range(0, len(hex_data), 4):
        hex_str = hex_data[i:i+4]
        try:
            # Convert to 16-bit signed integer
            value = int(hex_str, 16)
            if value >= 0x8000:
                value -= 0x10000
            int_data.append(value)
            # Count values close to top and bottom
            if value >= 32760:
                top_count += 1
            elif value <= -32760:
                bottom_count += 1
        except ValueError:
            print(f"Invalid hex value: {hex_str}")
    
    # Print count of values close to top and bottom
    print(f"Number of values close to top (>= 32760): {top_count}")
    print(f"Number of values close to bottom (<= -32760): {bottom_count}")
    # Print total number of read samples
    print(f"Read {len(int_data)} samples from file.")
    
    return np.array(int_data, dtype=np.int16)

def save_to_wav(data, file_path, sample_rate=16000):
    with wave.open(file_path, 'w') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16 bits
        wf.setframerate(sample_rate)
        wf.writeframes(data.tobytes())
    print(f"Saved audio data to {file_path}")

if __name__ == "__main__":
    # Read data.txt file
    audio_data = read_hex_file('data.txt')
    
    if audio_data.size == 0:
        print("No valid data to save.")
    else:
        # Save to WAV file
        save_to_wav(audio_data, 'output.wav')