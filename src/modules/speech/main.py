from gtts import gTTS
from pygame import mixer
import time

mixer.init()

def say(text: str):
    while mixer.music.get_busy() == True:
        time.sleep(0.1)
    tts = gTTS(text=text, tld='com', lang='en')
    tts.save('speach.mp3')
    mixer.music.load('speach.mp3')
    mixer.music.play()
