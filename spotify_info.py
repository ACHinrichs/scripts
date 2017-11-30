'''
Script to output the Song & artist currently playd on spotify. 

Intended for usage in my Polybar
Should work with both python3 and python2, but I develop it under python3

WORKS ON LINUX ONLY

Partially stolen from https://stackoverflow.com/questions/33883360/get-spotify-currently-playing-track
'''

import dbus
try:
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                         "/org/mpris/MediaPlayer2")
    spotify_properties = dbus.Interface(spotify_bus,
                                        "org.freedesktop.DBus.Properties")
    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
    
    
    artist = ""
    for key in metadata['xesam:artist']:
        if not artist=="":
            artist=artist+", "
            artist=artist + key
            
    print(metadata['xesam:title']+" - "+artist)
except Exception as e:
    print("not playing")
    print(e)
