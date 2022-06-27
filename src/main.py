import time
from queue import Queue

from modules.marva_camera import main as camera
from modules.marva_speech import main as speech
from modules.marva_slack import main as slack


# Define global variables
command_queue: Queue


# Main loop
def main():
    global command_queue

    while(True):

        speech.say('Froliver. My name is Marva.')
        speech.say('''At least two people have been confirmed dead and 20 injured in a missile strike at a crowded retail area in Kremenchuk in the Poltava region of Ukraine. President Zelensky posted this footage on his social media showing a badly damaged, collapsing building on fire. The Ukrainian president said Russia carried out the missile strike while more than 1,000 people were in the building.''')
        
        # Check command queue
        # print(slack.get_new_command())

        # new_messages = slack.get_new_messages()
        # if ('Get faces' in new_messages):
        #     # see what faces are visible
        #     (faces, image) = camera.get_faces()
        
        #     # send update via slack
        #     slack.send("I can see " + ", ".join([face.first_name for face in faces]))
        #     cv2.imwrite("test.png", image)
        #     slack.send_file("./test.png")

        # time.sleep(2)


# Process command messaged through slack
def process_command(command: str):
    print(command)


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

    # initialise modules
    camera.init(ignore_cache=True)
    speech.init()
    # slack.init()

    speech.say('Hi there, Oliver. My name is Marva.')
    speech.say('I can currently see the faces of: Oliver, Tilly, and Jade.')

    # start main loop
    main()