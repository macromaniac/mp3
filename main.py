#%%
from time import sleep
print(f"starting vlc")
import vlc
Instance = vlc.Instance("--no-video")

#create our playlist
import glob, random
playlist = glob.glob("music/*.mp4") + glob.glob("music/*.webm") +  glob.glob("music/*.mkv")
random.shuffle(playlist)
idx=0
def getSong(num):
    return Instance.media_new(playlist[idx % len(playlist)])

p = Instance.media_player_new()
p.set_media(getSong(idx))
p.pause()

#%%
print(f"starting alsa mixer interface")
import alsaaudio
m = alsaaudio.Mixer('PCM')

#%%
def playPause():
    print(f"play/pause button pressed")
    if(p.is_playing()):
        p.pause()
        print("pausing")
    else:
        p.play()
        print("playing")


def volUp():
    print(f"vol up button pressed")
    vol=m.getvolume()[0]
    vol+=5
    if(vol>90):
        vol=90
    print(f"set vol to {vol}")
    m.setvolume(vol)

def volDown():
    print(f"vol down button pressed")
    vol=m.getvolume()[0]
    vol-=5
    if(vol<0):
        vol=0
    print(f"set vol to {vol}")
    m.setvolume(vol)

def nextSong():
    global idx
    print(f"next song button pressed")
    idx=idx+1
    song = getSong(idx)
    print(f"playing {song.get_mrl()}")
    p.stop()
    p.set_media(song)
    p.play()

def prevSong():
    global idx
    print(f"prev song button pressed")
    idx=idx-1
    song = getSong(idx)
    print(f"playing {song.get_mrl()}")
    p.stop()
    p.set_media(song)
    p.play()

#%%
print(f"hooking up our buttons to our functions")
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

def onVoltageIncrease(pin, fun):
    print(f"added listener to BCN pin {pin}")
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.remove_event_detect(pin)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=lambda a:fun(), bouncetime=200)

onVoltageIncrease(5, playPause)
onVoltageIncrease(6, volUp)
onVoltageIncrease(13, volDown)
onVoltageIncrease(19, nextSong)
onVoltageIncrease(26, prevSong)

#%%

print("starting main loop")
while(True):
    sleep(.100)
    if(p.get_state()==vlc.State.Ended):
        print("song ended going to next song")
        nextSong()