import os
from subprocess import list2cmdline
import time
from queue import Queue, Empty
from threading import Thread

from slack import WebClient
from slack.errors import SlackApiError


# Define global variables
client: WebClient
__location__: str
command_queue: Queue
listen_thread: Thread
last_updated: str


# Initialise module
def init():
    global client, __location__, command_queue, listen_thread, last_updated

    print("--Initialising Slack module--")
    
    # Setup global variables
    client = WebClient(token=os.environ['SLACK_TOKEN'])
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    command_queue = Queue(maxsize = 100)
    last_updated = time.time()
    listen_thread = Thread(target=listen)
    listen_thread.start()


# Thread for listening for new commands
def listen():
    global client, command_queue, last_updated

    # get data about general channel
    general_channel = get_channel("")

    while True:
        print("Checking for new commands")

        new_time = time.time()
        response = client.conversations_history(
            channel = general_channel['id'],
            oldest = str(last_updated)
        )

        # check if there was an issue with the response
        if (response['ok'] == False):
            continue
        
        if (len(response['messages']) > 0):
            # Update last checked time
            last_updated = new_time

            # Add messages to command queue
            response['messages'].reverse()
            for message in response['messages']:
                print("Putting message {} on the queue".format(message['text']))
                command_queue.put(message['text'])

        time.sleep(5)


# Retrieve new command
def get_new_command():
    try:
        new_command = command_queue.get(False)
    except Empty:
        new_command = None

    return new_command


# Returns dictionary with information about a channel
def get_channel(channel: str):
    global client

    response = client.conversations_list()
    if (response['ok'] == False):
        return []
    
    for channel in response['channels']:
        if channel['is_general']:
            return channel

    return None


# Send text message
def send(message: str):
    global client

    try:
        response = client.chat_postMessage(
            channel = '#general',
            text = message
        )
        assert response["message"]["text"] == message
    except SlackApiError as e:
        # will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")


# Send file
def send_file(filepath: str):
    global client

    try:
        response = client.files_upload(
            channels='#general',
            file=filepath)
        assert response["file"]  # the uploaded file
    except SlackApiError as e:
        # will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")