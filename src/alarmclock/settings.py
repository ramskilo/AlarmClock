import os

from dotenv import load_dotenv

load_dotenv()

SONGS_DIRECTORY = os.getenv("SONGS_DIRECTORY", "./songs")
MEDIA_FILE_EXTENSION = os.getenv("MEDIA_FILE_EXTENSION", "mp3")
NUMBER_OF_SONGS_TO_PLAY = 1
