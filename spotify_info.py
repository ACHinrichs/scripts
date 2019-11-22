'''
Script to output the Song & artist currently playd on spotify. 

Intended for usage in my Polybar
Should work with both python3 and python2, but I develop it under python3

WORKS ON LINUX ONLY

Partially stolen from https://stackoverflow.com/questions/33883360/get-spotify-currently-playing-track
'''
import dbus

MAX_LEN = 32
MAX_SONG_LEN = 22
try:
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                         "/org/mpris/MediaPlayer2")
    spotify_properties = dbus.Interface(spotify_bus,
                                        "org.freedesktop.DBus.Properties")
    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
    
    #print(metadata)
    artist = ""
    for key in metadata['xesam:artist']:
        if not artist=="":
            artist=artist+", "
        artist=artist + key

    title = str(metadata['xesam:title']).partition(" - ")[0]
    if len(title + artist) + 3 > MAX_LEN:
        if len(title) > MAX_SONG_LEN:
           title = title[0:(MAX_SONG_LEN - 1)]+"…"
    output = title +" - "+artist
    if len(output) > MAX_LEN:
        output = output[0:(MAX_LEN-1)]+"…"
    print(output)
except Exception as e:
    print("not playing")
    print(e)
