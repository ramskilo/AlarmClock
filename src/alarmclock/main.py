import datetime
import time
from playsound3 import playsound
import string, random, glob, json, signal, os
from sys import exit
from pathlib import Path

# Pipe per comunicazione tra handler e main
rfd, wfd = os.pipe()
l_times = 1 # Ora è globale davvero

def handler(signal_received, frame):
    print('Exiting gracefully')
    exit(0)

def handlerNext(signal_received, frame):
    global l_times
    l_times += 1
    print('Next signal received')
    try:
        os.write(wfd, b"\x00") # Sblocca il main
    except OSError:
        pass

def load_json_data(file_ptr):
    try:
        return json.load(file_ptr)
    except Exception as exc:
        print(f"Errore lettura JSON: {exc}")
        return {}

def main():
    global l_times
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGUSR1, handlerNext) # SIGUSR1 (10) o SIGUSR2 (12) sono meglio di 20

    BASE_DIR = Path(__file__).resolve().parent
    settings_file = BASE_DIR / 'settings.json'
    played_file = BASE_DIR / 'played.json'

    # Caricamento dati con gestione file mancanti
    if not played_file.exists():
        played_file.write_text('{"songsPlayed": []}')
    
    with open(settings_file) as s, open(played_file) as p:
        data = load_json_data(s)
        played = load_json_data(p)

    l_songs_directory = data.get('SongsDirectory', './')
    l_extension = data.get('MediaFileExtension', '*.mp3')
    l_number_of_songs = data.get('NumberOfSongsToPlay', 1)
    current_time = datetime.datetime.now()
    alarmHour = data.get('DefaultHour', "") 
    if alarmHour == "":
        alarmHour = str(current_time.hour)
    alarmMin = data.get('DefaultMinutes', "")
    if alarmMin == "":
        alarmMin = str(current_time.minute)

    print(f"Sveglia impostata alle {alarmHour}:{alarmMin}")
    start_time = datetime.datetime.now()

    while l_times <= l_number_of_songs or (start_time > current_time - datetime.timedelta(minutes=30)):
                
        # Controllo orario
        if current_time.hour == int(alarmHour) and current_time.minute == int(alarmMin):
            print("Ora di svegliarsi!")
            
            # Costruzione lista canzoni (spostata fuori dal loop scelta per efficienza)
            pattern = os.path.join(l_songs_directory, l_extension)
            available_songs = glob.glob(pattern)
            
            # Filtra già suonate
            pool = [s for s in available_songs if s not in played.get("songsPlayed", [])]
            if not pool: pool = available_songs # Reset se tutte suonate

            if pool:
                song_to_play = random.choice(pool)
                print(f"Riproduzione: {song_to_play}")
                
                # Aggiorna played.json
                played.setdefault("songsPlayed", []).append(song_to_play)
                with open(played_file, 'w') as f:
                    json.dump(played, f)
                
                # Suona
                playsound(song_to_play)
                l_times += 1
                
                # Aspetta un minuto per evitare che riparta nello stesso minuto
                time.sleep(60) 
            else:
                print("Nessuna canzone trovata!")
                break
        
        time.sleep(30) # Controllo ogni 30 secondi (salva CPU e Log)

if __name__ == "__main__":
    main()
