import time

from modules.marva_face_recognition import main as face_recognition
from modules.marva_speech import main as speech
from modules.marva_slack import main as slack

import cv2


# Main loop
def main():
    while(True):

        # see what faces are visible
        (faces, image) = face_recognition.get_faces()
        
        # send update via slack
        slack.send("I can see " + ", ".join([face.first_name for face in faces]))
        cv2.imwrite("test.png", image)
        slack.send_file("./test.png")

        time.sleep(5)


# Driver code
if __name__ == "__main__":
    print('''
    ___      ___       __        _______  ___      ___  __      
    |"  \    /"  |     /""\      /"      \|"  \    /"  |/""\     
    \   \  //   |    /    \    |:        |\   \  //  //    \    
    /\\  \/.    |   /' /\  \   |_____/   ) \\  \/. .//' /\  \   
    |: \.        |  //  __'  \   //      /   \.    ////  __'  \  
    |.  \    /:  | /   /  \\  \ |:  __   \    \\   //   /  \\  \ 
    |___|\__/|___|(___/    \___)|__|  \___)    \__/(___/    \___)
                                                                
    ''')
    face_recognition.init()
    speech.init()
    slack.init()

    speech.say("Hi there, my name is Marva")