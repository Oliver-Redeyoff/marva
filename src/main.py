import time
from typing import List

from modules.marva_face_recognition import main as face_recognition
from modules.marva_face_recognition.main import Face
from modules.marva_speech import main as speech
from modules.marva_slack import main as slack

import cv2

speech.say("Hi there, my name is Marva")

face_recognition.init_known_faces(False)

while(True):

    # See what faces are visible
    print("Looking for faces")
    faces: List[Face] = face_recognition.get_faces()
    print("Got faces")

    # Greet them
    for face in faces:
        if (face != None):
            if (not face.appeared):
                speech.say("I can see you, " + face.first_name)
                face.appeared = True
                cv2.imwrite("test.png", face.image)
                slack.send("I saw " + face.first_name)
                slack.send_image("test.png")
        else:
            speech.say("I can see someone I don't know")

    time.sleep(1)