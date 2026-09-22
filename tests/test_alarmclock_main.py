from alarmclock import main as alarm_main
from alarmclock.server import AlarmController


class RunningPlayer:
    def __init__(self):
        self.terminated = False

    def poll(self):
        return None if not self.terminated else 0

    def terminate(self):
        self.terminated = True

    def wait(self):
        return 0


def run_interrupted_playback(monkeypatch, command):
    player = RunningPlayer()
    monkeypatch.setattr(alarm_main.subprocess, "Popen", lambda *args, **kwargs: player)

    controller = AlarmController()
    command(controller)

    return player, alarm_main.play_song("song.mp3", controller)


def test_play_song_stops_immediately(monkeypatch):
    player, result = run_interrupted_playback(monkeypatch, lambda controller: controller.stop())

    assert result == "stop"
    assert player.terminated


def test_play_song_snoozes_immediately(monkeypatch):
    player, result = run_interrupted_playback(monkeypatch, lambda controller: controller.snooze())

    assert result == "snooze"
    assert player.terminated


def test_play_song_skips_immediately(monkeypatch):
    player, result = run_interrupted_playback(monkeypatch, lambda controller: controller.skip())

    assert result == "skip"
    assert player.terminated