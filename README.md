# AlarmClock
This is an alarm clock to wake you up with your mp3 songs 

Settings are in settings.json in this format:

{
	"SongsDirectory" : "/home/skilo/Musica/mp3/",   --> the dir where you store your song files
	"MediaFileExtension" : "*.mp3",                 --> the extension of your media files
	"NumberOfSongsToPlay" : 10,                     --> When you alarm triggers, this number of songs will be played. 
	"DefaultHour" : 21,				--> Hour (24-hour format) on which the alarm triggers  - it can be null
	"DefaultMinutes" : 26				--> Minutes (24-hour format) on which the alarm triggers - it can be null 
}


If time is not fully defined in this file, you will be asked about that upon lauch of the script
NOTE: the keys in the settings.json must appear in any case
