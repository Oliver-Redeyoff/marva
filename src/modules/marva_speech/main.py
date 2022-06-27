import os
import time

import torch
from pygame import mixer


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
    local_file = 'model.pt'

    if not os.path.isfile(local_file):
        torch.hub.download_url_to_file('https://models.silero.ai/models/tts/en/v3_en.pt',
                                    local_file)  

    speech_model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    speech_model.to(device)


# Text to speech function
# Good voices are [18, 24, 48, 61, 82, 107]
def say(text: str, voice: str = 'en_24'):
    global __location__, speech_model

    # wait for mixer to be done
    while mixer.music.get_busy() == True:
        time.sleep(0.1)

    # speaker='en_1'
    # print(speech_model)
    speech_model.save_wav(text=text,
                        speaker=voice,
                        sample_rate=48000)

    mixer.music.load('test.wav')
    mixer.music.play()