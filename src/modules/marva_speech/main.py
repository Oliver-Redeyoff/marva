import os
import time
import re

import torch
from pygame import mixer
from num2words import num2words


# Define global variables
__location__: str
speech_model: any


# Download TTS model if not already downloaded, and set up mixer
def init():
    global __location__, speech_model

    print("--Initialising speech module--")
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    mixer.init()

    device = torch.device('cpu')
    torch.set_num_threads(4)
    model_path = __location__ + '/model.pt'

    if not os.path.isfile(model_path):
        torch.hub.download_url_to_file('https://models.silero.ai/models/tts/en/v3_en.pt', model_path)  

    speech_model = torch.package.PackageImporter(model_path).load_pickle("tts_models", "model")
    speech_model.to(device)


# Text to speech function
# Good voices are [18, 24, 48, 61, 82, 107]
def say(text: str, voice: str = 'en_24'):
    global __location__, speech_model

    # wait for mixer to be done
    while mixer.music.get_busy() == True:
        time.sleep(0.1)

    # replace numbers with text
    text = re.sub(r"(\d+)", lambda x: num2words(int(x.group(0))), text)

    # generate audio file
    speech_model.save_wav(text=text,
                        speaker=voice,
                        sample_rate=48000,
                        audio_path= __location__ + '/speech.wav')

    # play audio file
    mixer.music.load(__location__ + '/speech.wav')
    mixer.music.play()