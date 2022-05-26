# Import libraries
from __future__ import annotations
import os
from os import listdir
from dataclasses import dataclass
from typing import List

# Have to append root folder in order to import utilities
import sys
sys.path.append(".")
from utilities import create_dir, retrieve, store

import face_recognition
import cv2


# Define Face dataclass
@dataclass
class Face:
    first_name: str
    last_name: str
    encoding: any
    appeared: bool

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialise known faces
known_faces: List[Face] = []


# Computes known face definitions, or retrieves from cache
def init_known_faces(ignore_cache: bool = False):
    global known_faces

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    known_faces_path = __location__ + "/known_faces"
    cache_path = known_faces_path + "/cache.pkl"

    # Ignore this logic if there are no known faces
    if (not os.path.exists(known_faces_path)):
        return

    # Retrieve cache if exists
    if (os.path.exists(cache_path) and not ignore_cache):
        known_faces = retrieve(cache_path)
        return

    # Process known faces and cache result
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
    # Release handle to the webcam
    video_capture.release()


# Get faces in current frame of video feed
def get_faces() -> List[Face]:
    face_locations = []
    face_encodings = []

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    faces = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces([face.encoding for face in known_faces], face_encoding)

        if True in matches:
            match_index = matches.index(True)
            face = known_faces[match_index]
            faces.append(face)
        
        else:
            faces.append(None)

    return faces