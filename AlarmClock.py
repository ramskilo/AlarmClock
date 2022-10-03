import datetime
import time
from playsound import playsound
import string
import random
import glob
import json

from signal import signal, SIGINT
from sys import exit

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)
    l_song_to_play = ""
    l_song = []
    l_times = 1
    timeout = 60 #seconds
    
    f = open('settings.json')
    data = json.load(f)
    
    l_number_of_songs = data['NumberOfSongsToPlay']
    l_songs_directory = data['SongsDirectory']
    l_extension = data['MediaFileExtension']
    
    alarmHour = data['DefaultHour']
    alarmMin = data['DefaultMinutes']
    
    if alarmHour is None  or alarmMin is None:  
        alarmHour = int(input("Which time do you wanna wake up? (Hour)"))
        alarmMin = int(input("minutes:")) 
    
    print('Running. Press CTRL-C to exit.')
    while True:
        time.sleep(0.2)
        if alarmHour==datetime.datetime.now().hour and alarmMin==datetime.datetime.now().minute or ( l_times <= l_number_of_songs and l_times > 1 ):
            print("Playing...")
            while l_song_to_play == "":
                start = time.time()
                l_letter = random.choice(string.ascii_letters + string.digits)
                l_letter2 = random.choice(string.ascii_letters)
                l_glob = l_songs_directory + l_letter2 + "*/" + l_letter + l_extension
                l_song = glob.glob(l_glob) 
                if len(l_song) > 0:
                    l_song_to_play = l_song[0]
                if time.time() - start >= timeout:
                    break
            print(l_song_to_play)
            if not len(l_song_to_play) == 0:
                playsound(l_song_to_play)
                l_song_to_play = ""
                l_times += 1
            if l_times > l_number_of_songs:
                break
        
