import os
from slack import WebClient
from slack.errors import SlackApiError


# Define global variables
client: WebClient
__location__: str


# Initialise module
def init():
    global client, __location__

    print("--Initialising Slack module--")
    
    client = WebClient(token=os.environ['SLACK_TOKEN'])
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


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