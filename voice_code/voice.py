import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import os
import numpy as np
import queue
import noisereduce as nr

def process_audio():
    filename = "output.wav"
    duration = 10  # seconds
    fs = 44100  # Sample rate

    def update_status_start():
        status_label.config(text="Recording...")
    root.after(0, update_status_start)

    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  

    # data = myrecording.flatten()
    # noise_sample = data[:int(0.5 * fs)]
    # reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noise_sample, verbose=False)

    sf.write(filename, myrecording, fs)

    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text = "[Could not understand audio]"
    except sr.RequestError as e:
        text = f"[Could not request results; {e}]"

    text_queue.put(text)

    os.remove(filename)

    def update_status_end():
        status_label.config(text="Press Space to start recording.")
    root.after(0, update_status_end)

def update_gui():
    try:
        while True:
            text = text_queue.get_nowait()
            text_display.insert(tk.END, text + '\n')
            text_display.see(tk.END)
    except queue.Empty:
        pass
    root.after(100, update_gui)

def on_space_bar(event):
    threading.Thread(target=process_audio).start()

root = tk.Tk()
root.title("Speech to Text Display")

text_display = ScrolledText(root, wrap=tk.WORD, width=80, height=20)
text_display.pack(padx=10, pady=10)

status_label = tk.Label(root, text="Press Space to start recording.")
status_label.pack(pady=5)

text_queue = queue.Queue()

root.bind('<space>', on_space_bar)

root.after(100, update_gui)

root.mainloop()
