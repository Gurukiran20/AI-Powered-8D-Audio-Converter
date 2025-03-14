
"""AI 8D song converter.py"""

import numpy as np
import librosa
import soundfile as sf
from scipy.signal import convolve
from google.colab import files
import matplotlib.pyplot as plt

print("Upload your audio file:")
uploaded = files.upload()
input_path = list(uploaded.keys())[0]

def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None, mono=False)
    print(f"Loaded audio with sample rate: {sr} Hz")
    return y, sr

def apply_8d_effects(y, sr):
    if len(y.shape) == 1:
        y = np.array([y, y])

    duration = y.shape[1] / sr
    t = np.linspace(0, duration, y.shape[1])

    left_pan = 0.5 * (1 + np.sin(2 * np.pi * 0.08 * t))
    right_pan = 1 - left_pan

    y_stereo = np.array([y[0] * left_pan, y[1] * right_pan])

    reverb_kernel = np.random.randn(5000) * 0.01
    y_stereo[0] = convolve(y_stereo[0], reverb_kernel, mode='same')
    y_stereo[1] = convolve(y_stereo[1], reverb_kernel, mode='same')

    max_val = np.max(np.abs(y_stereo))
    y_stereo /= max_val

    return y_stereo

def plot_waveform(y, sr):
    plt.figure(figsize=(14, 5))
    librosa.display.waveshow(y[0], sr=sr, alpha=0.6, color='blue', label='Left Channel')
    librosa.display.waveshow(y[1], sr=sr, alpha=0.6, color='orange', label='Right Channel')
    plt.title("8D Audio Waveform")
    plt.legend()
    plt.show()

def export_audio(y, sr, output_path):
    sf.write(output_path, y.T, sr)
    print("8D Audio version exported successfully!")
    files.download(output_path)

y, sr = load_audio(input_path)
y_8d = apply_8d_effects(y, sr)
plot_waveform(y_8d, sr)
output_path = "8d_audio_version.wav"
export_audio(y_8d, sr, output_path)
