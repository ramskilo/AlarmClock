# AlarmClock
This is an alarm clock to wake you up with your mp3 songs 

Settings are in settings.json in this format:

```json
{
	"SongsDirectory" : "/home/skilo/Musica/mp3/",   --> the dir where you store your song files
	"MediaFileExtension" : "*.mp3",                 --> the extension of your media files
	"NumberOfSongsToPlay" : 10,                     --> When you alarm triggers, this number of songs will be played. 
	"DefaultHour" : 21,				--> Hour (24-hour format) on which the alarm triggers  - it can be null
	"DefaultMinutes" : 26,				--> Minutes (24-hour format) on which the alarm triggers - it can be null
	"HttpHost" : "0.0.0.0",				--> Listen on all network interfaces
	"HttpPort" : 8765					--> HTTP port
}
```



If time is not fully defined in this file, you will be asked about that upon lauch of the script
**NOTE**: the key names in the settings.json are mandatory

## HTTP control

The alarm starts an HTTP server using the `HttpHost` and `HttpPort` values in
`src/alarmclock/settings.json`. Use `0.0.0.0` as `HttpHost` to accept
connections from other devices on the same network. From those devices, open
the alarm computer's LAN address, for example:

```text
http://192.168.1.25:8765/
```

Do not use `0.0.0.0` in the browser address bar. Find the alarm computer's LAN
address with `hostname -I`. Binding to all interfaces exposes the control API
to the local network, so restrict the port with your firewall if needed.

Send a `POST` request to one of these endpoints from a client whose address is
in `192.168.0.0/16`:

```text
POST /snooze  # snooze for five minutes
POST /stop    # stop after the current song finishes
POST /skip    # advance after the current song, or skip the queued song
GET  /status  # inspect stopped and snoozed state
```

Commands from loopback, public addresses, and other private networks are
rejected with `403 Forbidden`. For example, from a device on the allowed LAN:

```bash
curl -X POST http://192.168.1.25:8765/snooze
curl -X POST http://192.168.1.25:8765/stop
curl -X POST http://192.168.1.25:8765/skip
```
