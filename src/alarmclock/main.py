import sys
from pathlib import Path

import pygame
import settings

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Alarm Clock")
alarm_is_on = True


def find_files(dirfiles, extension):
    path = Path(dirfiles)
    return list(path.rglob("*.{}".format(extension)))


music_files = find_files(settings.SONGS_DIRECTORY, settings.MEDIA_FILE_EXTENSION)
print(f"{len(music_files)} files found")
for mp3 in music_files:
    print(mp3)

while alarm_is_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # exit the program
            alarm_is_on = False
        if event.type == pygame.KEYDOWN:  # key pressed
            if event.key == pygame.K_LEFT:  # left arrow key
                print("Previous")
            if event.key == pygame.K_RIGHT:  # right arrow key
                print("Next")
    screen.fill((0, 0, 0))
    pygame.display.update()

pygame.quit()
sys.exit()
