import sounddevice as sd
import numpy as np
from scipy.io import wavfile

fs, adele_audio = wavfile.read("adele.wav")

if len(adele_audio.shape) > 1:
    adele_audio = adele_audio[:, 0]

duration = len(adele_audio) / fs

print(f"Recording for {round(duration, 1)} seconds... Sing now!")
user_audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()
user_audio = user_audio[:, 0]

chunk_size = fs 
num_chunks = int(len(adele_audio) / chunk_size)

differences = []

for i in range(num_chunks):
    start = i * chunk_size
    end = start + chunk_size
    
    chunk_a = adele_audio[start:end]
    chunk_u = user_audio[start:end]
    
    fft_a = np.fft.fft(chunk_a)
    fft_u = np.fft.fft(chunk_u)
    freqs = np.fft.fftfreq(chunk_size, 1/fs)
    
    idx_a = np.argmax(np.abs(fft_a))
    idx_u = np.argmax(np.abs(fft_u))
    
    hz_a = abs(freqs[idx_a])
    hz_u = abs(freqs[idx_u])
    
    diff = float(hz_u - hz_a)
    differences.append(round(diff, 1))

print("\nResults (Hz difference per second):")
print(differences)
print("\nNegative = Flat. Positive = Sharp.")