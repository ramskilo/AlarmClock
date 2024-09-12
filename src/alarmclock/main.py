import time
import tkinter
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
        self.current = 0

    def play(self):
        print("Playing song")

    def stop(self):
        print("Stopping song")

    def next(self):
        print("Next song")

    def previous(self):
        print("Previous song")

    def current_song(self):
        return self.playlist[self.current]


def find_files(dirfiles, extension):
    path = Path(dirfiles)
    return list(path.rglob("*.{}".format(extension)))


def process_key(event):
    if event.keysym == "Escape":
        app.quit()
    else:
        print(f"Key pressed: {event.keysym}")
        if event.keysym == "Left":
            radio.previous()
        if event.keysym == "Right":
            radio.next()


def main():
    print("Starting Radio!")
    # root.after(1000, say_hello)


# Load songs
filelist = find_files(settings.SONGS_DIRECTORY, settings.MEDIA_FILE_EXTENSION)
for mp3 in filelist:
    print(mp3)

# Start GUI
app = tkinter.Tk()
app.title("Alarm Clock")
app.geometry("600x400")
# Start radio istance
radio = Radio(playlist=filelist)
# Debounce click events
debounce = Debounce(app)
# Start main loop
app.after(200, main)
app.mainloop()
