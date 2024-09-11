# import datetime
# import time
# from playsound3 import playsound
# import string
# import random
# import glob
# import json
# # import keyboard
# import signal
# from sys import exit
# from _signal import SIGINT

from pathlib import Path

import settings


def find_files(dirfiles, extension):
    path = Path(dirfiles)
    return list(path.rglob("*.{}".format(extension)))


music_files = find_files(settings.SONGS_DIRECTORY, settings.MEDIA_FILE_EXTENSION)
print(f"{len(music_files)} files found")

for mp3 in music_files:
    print(mp3)


def handler(signal_received, frame):
    pass
    # # Handle any cleanup here
    # print('SIGINT or CTRL-C detected. Exiting gracefully')
    # exit(0)


def handler_next(signal_received, frame):
    pass
    # # Handle any cleanup here
    # l_times += 1
    # print('Next')
    # os.write(wfd, b"\x00")


def load_json_data(json_data):
    pass
    # try:
    #     # Attempt to decode the JSON data
    #     data = json.load(json_data)
    #     return data
    # except json.JSONDecodeError:
    #     # Handle the JSONDecodeError by printing an error message
    #     return {"songsPlayed": []}


def ciclo_base(l_song_to_play, alarmMin, alarmHour):
    pass
    # current_time = datetime.datetime.now()
    # time.sleep(0.2)
    # print("...")
    # if (alarmHour == current_time.hour and alarmMin == current_time.minute) or (l_times <= l_number_of_songs and l_times > 1):
    #     print("Playing...")
    #     while not l_song_to_play:
    #         start = time.time()
    #         l_letter = random.choice('LM' + string.digits)
    #         l_letter2 = random.choice(string.ascii_letters)
    #         l_constr_pattern = f"{l_songs_directory}{l_letter2}*/{l_letter}{l_extension}"
    #         l_song = glob.glob(l_constr_pattern)
    #         if l_song:
    #             l_song_to_play = l_song[0]
    #         if time.time() - start >= timeout:
    #             break
    #         if l_song_to_play in played.get("songsPlayed", []):
    #             l_song_to_play = ""
    #         print(l_song_to_play)
    #         if l_song_to_play:
    #             played.get("songsPlayed").append(l_song_to_play)
    #             with open("played.json", 'w') as filehandle:
    #                 json.dump(played, filehandle)
    #         print(l_song_to_play)
    #         playsound(l_song_to_play)
    #         l_song_to_play = ""
    #         os.read(rfd, 1)
    #         l_times += 1


if __name__ == "__main__":
    pass
    # Tell Python to run the handler() function when SIGINT is received
    # signal.signal(SIGINT, handler)
    # signal.signal(20, handlerNext)  #
    #
    # l_song_to_play = ""
    # l_times = 1
    # timeout = 60  # seconds
    # played = {"songsPlayed": []}
    #
    #
    # # with open('settings.json') as f:
    # #     data = load_json_data(f)
    # #
    # # with open('played.json') as f:
    # #     played = load_json_data(f)
    #
    # l_number_of_songs = data.get('NumberOfSongsToPlay', 0)
    # l_songs_directory = data.get('SongsDirectory', '')
    # l_extension = data.get('MediaFileExtension', '')
    #
    # alarmHour = data.get('DefaultHour')
    # alarmMin = data.get('DefaultMinutes')
    #
    # if alarmHour is None or alarmMin is None:
    #     alarmHour = int(input("What time do you want to wake up? (Hour)"))
    #     alarmMin = int(input("Minutes:"))
    #
    # print(f"{alarmHour}:{alarmMin}")
    # print('Running. Press CTRL-C to exit.')
    #
    # while True:
    #     current_time = datetime.datetime.now()
    #     time.sleep(0.2)
    #     print("...")
    #     if (alarmHour == current_time.hour and alarmMin == current_time.minute) or (l_times <= l_number_of_songs and l_times > 1):
    #         print("Playing...")
    #         while not l_song_to_play:
    #             start = time.time()
    #             l_letter = random.choice('LM' + string.digits)
    #             l_letter2 = random.choice(string.ascii_letters)
    #             l_constr_pattern = f"{l_songs_directory}{l_letter2}*/{l_letter}{l_extension}"
    #             l_song = glob.glob(l_constr_pattern)
    #             if l_song:
    #                 l_song_to_play = l_song[0]
    #             if time.time() - start >= timeout:
    #                 break
    #             if l_song_to_play in played.get("songsPlayed", []):
    #                 l_song_to_play = ""
    #             print(l_song_to_play)
    #             if l_song_to_play:
    #                 played.get("songsPlayed").append(l_song_to_play)
    #                 with open("played.json", 'w') as filehandle:
    #                     json.dump(played, filehandle)
    #             print(l_song_to_play)
    #             playsound(l_song_to_play)
    #             l_song_to_play = ""
    #             os.read(rfd, 1)
    #             l_times += 1
    #     if l_times > l_number_of_songs:
    #        break
