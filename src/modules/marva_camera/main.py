# Import libraries
from __future__ import annotations
import os
from os import listdir
import time
from dataclasses import dataclass
from typing import List, Tuple

# Have to append root folder in order to import utilities
import sys
sys.path.append(".")
from utilities import retrieve, store

import face_recognition
import cv2
import numpy as np


# Define Face dataclass
@dataclass(eq=False)
class Face:
    first_name: str
    last_name: str
    encoding: any

    def __eq__(self, other):
        return (self.first_name+self.last_name) == (other.first_name+other.last_name)


# Define global variables
known_faces: List[Face]
__location__: str


# Computes known face definitions, or retrieves from cache
def init(ignore_cache: bool = False, detect_batch_size_: int = 1):
    global known_faces, __location__, detect_batch_size

    print("--Initialising face recognition module--")
    
    # initialise known faces
    known_faces = []
    # get location of module
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    detect_batch_size = detect_batch_size_

    known_faces_path = __location__ + "/known_faces"
    cache_path = known_faces_path + "/cache.pkl"

    # ignore this logic if there are no known faces
    if (not os.path.exists(known_faces_path)):
        return

    # retrieve cache if exists
    if (os.path.exists(cache_path) and not ignore_cache):
        known_faces = retrieve(cache_path)
        return

    # process known faces and cache result
    for file_name in listdir(known_faces_path):
        name = file_name.split('.')[0].split('_')
        file_type = file_name.split('.')[1]

        if (file_type == 'png' or file_type == 'jpg'):
            image = face_recognition.load_image_file(known_faces_path + "/" + file_name)
            face_encodings = face_recognition.face_encodings(image)

            known_faces.append(Face(
                name[0],
                name[1],
                face_encodings[0]
            ))

    store(known_faces, cache_path)


# Get faces in current frame of video feed
def get_faces():
    global known_faces, detect_batch_size

    detected_faces: List[Face] = []

    # get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    time.sleep(0.5)

    # grab a single frame of video
    _, frame = video_capture.read()

    # resize frame of video to 1/2 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    small_frame = small_frame[:, :, ::-1]

    # find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    # match faces and annotate them
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces([face.encoding for face in known_faces], face_encoding)
        if (True in matches):
            match_index = matches.index(True)
            face = known_faces[match_index]
        else:
            face = Face(
                "Unknown",
                "",
                face_encoding
            )
        detected_faces.append(face)
        
        # annotate face
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, face.first_name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    video_capture.release()
    return (detected_faces, frame)