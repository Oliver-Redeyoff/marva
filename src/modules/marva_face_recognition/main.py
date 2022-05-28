# Import libraries
from __future__ import annotations
import os
from os import listdir
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
@dataclass
class Face:
    first_name: str
    last_name: str
    image: any
    encoding: any
    appeared: bool


# Define global variables
known_faces: List[Face]
video_capture: any
__location__: str


# Computes known face definitions, or retrieves from cache
def init(ignore_cache: bool = False):
    global known_faces, video_capture, __location__

    print("--Initialising face recognition module--")
    
    # initialise known faces
    known_faces = []
    # get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    # get location of module
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

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

        if (file_type != 'pkl'):
            image = face_recognition.load_image_file(known_faces_path + "/" + file_name)
            face_encodings = face_recognition.face_encodings(image)

            known_faces.append(Face(
                name[0],
                name[1],
                face_encodings[0],
                False
            ))

    store(known_faces, cache_path)


# Closes video capture
def close():
    global video_capture

    # release handle to the webcam
    video_capture.release()


# Get faces in current frame of video feed
def get_faces() -> Tuple[List[Face], any]:
    global known_faces, video_capture

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)s
        matches = face_recognition.compare_faces([face.encoding for face in known_faces], face_encoding)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            known_face_names = [face.first_name for face in known_faces]
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        # face_distances = face_recognition.face_distance([face.encoding for face in known_faces], face_encoding)
        # best_match_index = np.argmin(face_distances)
        # if matches[best_match_index]:
        #     known_face_names = [face.first_name for face in known_faces]
        #     name = known_face_names[best_match_index]

        face_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    return ([], frame)