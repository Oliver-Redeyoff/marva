# Import libraries
from __future__ import annotations

from pathlib import Path
from os import listdir
from dataclasses import dataclass
from typing import Any, AnyStr, List, Tuple, Dict
import time

import src.modules.speech.main as main

import face_recognition
import cv2
import numpy as np

@dataclass
class Face:
    first_name: str
    last_name: str
    encoding: any
    appeared: bool

known_faces: List[Face] = []

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

for file_name in listdir("./known_faces"):
    name = file_name.split('.')[0].split('_')
    image = face_recognition.load_image_file("./known_faces/" + file_name)
    face_encodings = face_recognition.face_encodings(image)

    known_faces.append(Face(
        name[0],
        name[1],
        face_encodings[0],
        False
    ))

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

print("Starting loop")
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces([face.encoding for face in known_faces], face_encoding)

            if True in matches:
                match_index = matches.index(True)
                face = known_faces[match_index]
                if not face.appeared:
                    main.say("Hi there " + face.first_name)
                    face.appeared = True

                face_names.append(face.first_name)
            
            else:
                face_names.append("Unknown")
                main.say("I don't know you")

    process_this_frame = not process_this_frame

#     # Display the results
#     # for (top, right, bottom, left), name in zip(face_locations, face_names):
#     #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
#     #     top *= 4
#     #     right *= 4
#     #     bottom *= 4
#     #     left *= 4

#     #     # Draw a box around the face
#     #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

#     #     # Draw a label with a name below the face
#     #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#     #     font = cv2.FONT_HERSHEY_DUPLEX
#     #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

#     # Display the resulting image
#     # cv2.imshow('Video', frame)

#     # Hit 'q' on the keyboard to quit!
#     # if cv2.waitKey(1) & 0xFF == ord('q'):
#     #     break

time.sleep(10)

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()