import datetime
import subprocess
import time
import string, random, glob, json, signal, os
from sys import exit
from pathlib import Path
from threading import Thread

from alarmclock.server import AlarmController, create_server

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

def play_song(song_path, controller):
    player = subprocess.Popen(
        ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", song_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        while player.poll() is None:
            if controller.consume_skip():
                player.terminate()
                player.wait()
                print("Skip requested")
                break
            time.sleep(0.2)
    finally:
        if player.poll() is None:
            player.terminate()
            player.wait()

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

    controller = AlarmController()
    http_host = data.get("HttpHost", "127.0.0.1")
    http_port = int(data.get("HttpPort", 8765))
    http_server = create_server(http_host, http_port, controller)
    http_thread = Thread(target=http_server.serve_forever, daemon=True)
    http_thread.start()
    print(f"HTTP server listening on http://{http_host}:{http_port}")

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

    print(f"{datetime.datetime.now()}: Sveglia impostata alle {alarmHour}:{alarmMin}")
    start_time = datetime.datetime.now()

    try:
        while (l_times <= l_number_of_songs or controller.has_snooze_pending()) and not controller.is_stopped():
            current_time = datetime.datetime.now()
            snooze_expired = controller.consume_snooze()

            # Controllo orario
            if (
                snooze_expired
                or (
                    not controller.is_snoozed()
                    and current_time.hour == int(alarmHour)
                    and current_time.minute == int(alarmMin)
                )
            ):
                if snooze_expired:
                    l_times = 1
                print(f"{datetime.datetime.now()}: Ora di svegliarsi!")

                # Once triggered, play the requested batch without requiring the
                # clock to remain in the alarm minute.
                while l_times <= l_number_of_songs and not controller.is_stopped():
                    pattern = os.path.join(l_songs_directory, "*/", l_extension)
                    available_songs = glob.glob(pattern)

                    # Filtra già suonate
                    pool = [s for s in available_songs if s not in played.get("songsPlayed", [])]
                    if not pool:
                        pool = available_songs  # Reset se tutte suonate

                    if not pool:
                        print(f"{datetime.datetime.now()}: Nessuna canzone trovata!")
                        break

                    song_to_play = random.choice(pool)
                    if controller.consume_skip():
                        print("Skipping queued song")
                        l_times += 1
                        continue
                    print(f"{datetime.datetime.now()}: Riproduzione: {song_to_play}")

                    # Aggiorna played.json
                    played.setdefault("songsPlayed", []).append(song_to_play)
                    with open(played_file, 'w') as f:
                        json.dump(played, f)

                    # Suona
                    play_song(song_to_play, controller)
                    l_times += 1

                    # Aspetta per evitare che riparta nello stesso minuto
                    time.sleep(8)

            time.sleep(30) # Controllo ogni 30 secondi (salva CPU e Log)
    finally:
        http_server.shutdown()
        http_server.server_close()

if __name__ == "__main__":
    main()

