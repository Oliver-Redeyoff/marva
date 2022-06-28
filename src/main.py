import time
from queue import Queue
import weakref

from modules.marva_camera import main as camera
from modules.marva_speech import main as speech
from modules.marva_slack import main as slack
from modules.marva_weather import main as weather


# Define global variables
command_queue: Queue


# Main loop
def main():
    global command_queue

    while(True):
        
        # Check command queue
        print(slack.get_new_command())

        # Get weather
        weather_data = weather.get_current_weather()
        speech.say("It is currently {} degrees, with {}".format(round(weather_data['temp']), weather_data['weather'][0]['description']))

        # new_messages = slack.get_new_messages()
        # if ('Get faces' in new_messages):
        #     # see what faces are visible
        #     (faces, image) = camera.get_faces()
        
        #     # send update via slack
        #     slack.send("I can see " + ", ".join([face.first_name for face in faces]))
        #     cv2.imwrite("test.png", image)
        #     slack.send_file("./test.png")

        time.sleep(2)


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
    slack.init()
    weather.init()

    speech.say('Hi there, Oliver. My name is Marva.')

    # start main loop
    main()