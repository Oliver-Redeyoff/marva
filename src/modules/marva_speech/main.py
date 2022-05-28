import time
import os
from gtts import gTTS
from pygame import mixer


# Define global variables
__location__: str


# Init module
def init():
    global __location__

    print("--Initialising speech module--")
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    mixer.init()


# Say a given string
def say(text: str):
    global __location__

    # wait for mixer to be done
    while mixer.music.get_busy() == True:
        time.sleep(0.1)

    tts = gTTS(text=text, tld='com', lang='en')
    tts.save(__location__ + '/speach.mp3')
    mixer.music.load(__location__ + '/speach.mp3')
    mixer.music.play()
