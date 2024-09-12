import random
import time
import tkinter as tk
from pathlib import Path

import settings


class Debounce:
    def __init__(self, root):
        self.root = root
        self.last_trigger_time = 0
        self.debounce_delay = settings.DEBOUNCE_DELAY
        self.root.bind("<Key>", self.on_key_press)

    def on_key_press(self, event):
        current_time = time.time() * 1000
        if current_time - self.last_trigger_time > self.debounce_delay:
            self.last_trigger_time = current_time
            process_key(event)


class Radio:
    def __init__(self, playlist):
        self.playlist = playlist
        self.history = []
        self.current = random.randint(0, len(playlist) - 1)

    def play(self):
        print(f"Playing: {self.playlist[self.current]}")

    def stop(self):
        print("Stopping song")

    def next(self):
        valid_numbers = [i for i in range(len(self.playlist)) if i not in self.history]
        if not valid_numbers:
            print("No more songs to play")
            return
        self.history.append(self.current)
        self.current = random.choice(valid_numbers)
        self.play()

    def previous(self):
        if not self.history:
            print("No previous songs")
            return
        self.current = self.history.pop()
        self.play()


def find_files(dirfiles, extension):
    return list(Path(dirfiles).rglob(f"*.{extension}"))


def process_key(event):
    if event.keysym == "Escape":
        app.quit()
    elif event.keysym == "Left":
        radio.previous()
    elif event.keysym == "Right":
        radio.next()


def main():
    print("Starting Radio!")
    radio.play()


filelist = find_files(settings.SONGS_DIRECTORY, settings.MEDIA_FILE_EXTENSION)

app = tk.Tk()
app.title("Alarm Clock")
app.geometry("600x400")

radio = Radio(playlist=filelist)
debounce = Debounce(app)

app.after(200, main)
app.mainloop()
