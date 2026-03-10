import sounddevice as sd
import numpy as np
from scipy.io import wavfile

def load_reference(filepath):
    fs, audio = wavfile.read(filepath)
    if len(audio.shape) > 1:
        audio = audio[:, 0]
    duration = len(audio) / fs
    return fs, audio, duration

def get_pitch_autocorr(signal, sr):
    if np.max(np.abs(signal)) < 0.01:
        return 0.0
    
    window = np.hanning(len(signal))
    signal = signal * window
    
    corr = np.correlate(signal, signal, mode='full')
    corr = corr[len(corr)//2:]
    
    d_corr = np.diff(corr)
    start_search = np.where(d_corr > 0)[0]
    
    if len(start_search) == 0:
        return 0.0
        
    search_area = corr[start_search[0]:]
    peak_idx = np.argmax(search_area) + start_search[0]
    
    if peak_idx == 0:
        return 0.0
        
    freq = float(sr / peak_idx)
    
    if freq > 1000 or freq < 50:
        return 0.0
        
    return freq

def calculate_final_score(ref_pitches, user_pitches):
    total_points = 0
    correct_points = 0
    for a, u in zip(ref_pitches, user_pitches):
        if a > 0 and u > 0:
            total_points += 1
            if abs(u - a) < 15:
                correct_points += 1
    score = (correct_points / total_points * 100) if total_points > 0 else 0
    return round(score, 1)