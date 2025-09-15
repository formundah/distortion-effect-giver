import os
import tkinter as tk
from tkinter import filedialog
import pygame
import numpy as np
import wave
import tempfile
import threading

# Init pygame
pygame.mixer.init()

# Default hardcoded file (edit as needed)
HARDCODED_FILE = r"C:\Users\formu\Downloads\gamemusick\drunkin_bar.mp3"

# Distortion effect function gain = boost, threshold = crunch
def distort_mp3_to_wav(mp3_path, gain=1.5, threshold=10000):
    sound = pygame.mixer.Sound(mp3_path)
    samples = pygame.sndarray.array(sound).astype(np.int32)

    # Apply gain
    samples = samples * gain

    # Apply clipping
    samples = np.clip(samples, -threshold, threshold).astype(np.int16)

    # Save to temp WAV this saves a temporary file then deletes it after playing cuz it cant play mp3 directly with distortion
    tmp_wav = tempfile.mktemp(suffix=".wav")
    nchannels = samples.shape[1] if samples.ndim > 1 else 1
    framerate = 44100
    with wave.open(tmp_wav, 'wb') as wf:
        wf.setnchannels(nchannels)
        wf.setsampwidth(2)
        wf.setframerate(framerate)
        wf.writeframes(samples.tobytes())
    return tmp_wav

# Play distorted file in background
def play_with_distortion(file):
    try:
        gain = gain_slider.get()
        threshold = threshold_slider.get()
        distorted_file = distort_mp3_to_wav(file, gain=gain, threshold=threshold)
        pygame.mixer.music.load(distorted_file)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error: {e}")

def stop_music():
    pygame.mixer.music.stop()

# GUI setup
root = tk.Tk()
root.title("MP3 Distortion Player")
root.geometry("500x400")

files = []

def add_files():
    new_files = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
    for f in new_files:
        files.append(f)
        listbox.insert(tk.END, os.path.basename(f))

def play_selected():
    selected = listbox.curselection()
    if not selected:
        return
    file = files[selected[0]]
    threading.Thread(target=play_with_distortion, args=(file,), daemon=True).start()

def play_hardcoded():
    if HARDCODED_FILE:
        threading.Thread(target=play_with_distortion, args=(HARDCODED_FILE,), daemon=True).start()


# Widgets
listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

add_btn = tk.Button(btn_frame, text="Add MP3s", command=add_files)
add_btn.grid(row=0, column=0, padx=5)

play_btn = tk.Button(btn_frame, text="Play Selected File", command=play_selected)
play_btn.grid(row=0, column=1, padx=5)

play_hard_btn = tk.Button(btn_frame, text="Play Hardcoded File", command=play_hardcoded)
play_hard_btn.grid(row=0, column=2, padx=5)

stop_btn = tk.Button(root, text="Stop", command=stop_music)
stop_btn.pack(pady=5)

# Sliders ideally should stay like this to work properly and edit in GUI
gain_slider = tk.Scale(root, from_=0.5, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, label="Gain")
gain_slider.set(1.5)
gain_slider.pack(pady=5)

threshold_slider = tk.Scale(root, from_=1000, to=30000, resolution=500, orient=tk.HORIZONTAL, label="Threshold")
threshold_slider.set(10000)
threshold_slider.pack(pady=5)


root.mainloop()

