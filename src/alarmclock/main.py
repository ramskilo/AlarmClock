import sys
import tkinter
from pathlib import Path

import settings

root = tkinter.Tk()
root.title("Alarm Clock")
root.geometry("600x400")

alarm_is_on = True


def find_files(dirfiles, extension):
    path = Path(dirfiles)
    return list(path.rglob("*.{}".format(extension)))


def on_key_press(event):
    if event.keysym == "Escape":
        print("Escape key pressed, exiting...")
        root.quit()
    else:
        print(f"Key pressed: {event.keysym}")


music_files = find_files(settings.SONGS_DIRECTORY, settings.MEDIA_FILE_EXTENSION)
print(f"{len(music_files)} files found")
for mp3 in music_files:
    print(mp3)

root.bind("<KeyPress>", on_key_press)
root.mainloop()
# for event in pygame.event.get():
#     if event.type == pygame.QUIT:  # exit the program
#         alarm_is_on = False
#     if event.type == pygame.KEYDOWN:  # key pressed
#         if event.key == pygame.K_LEFT:  # left arrow key
#             print("Previous")
#         if event.key == pygame.K_RIGHT:  # right arrow key
#             print("Next")
# pygame.display.flip()
