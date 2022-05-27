
import time
import os
from gtts import gTTS
from pygame import mixer

print("Initialising speech module")

mixer.init()

# Say a given string
def say(text: str):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    while mixer.music.get_busy() == True:
        time.sleep(0.1)

    tts = gTTS(text=text, tld='com', lang='en')
    tts.save(__location__ + '/speach.mp3')
    mixer.music.load(__location__ + '/speach.mp3')
    mixer.music.play()
