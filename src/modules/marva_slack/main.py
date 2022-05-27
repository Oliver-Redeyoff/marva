import os
from slack import WebClient
from slack.errors import SlackApiError

client = WebClient(token='xoxb-3587969578531-3611836213232-WnXIo2F2WUC5mZxEBzjI0ANZ')
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def send(message: str):
    try:
        response = client.chat_postMessage(
            channel = '#general',
            text = message
        )
        assert response["message"]["text"] == message
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")

def send_image(filepath: str):
    try:
        response = client.files_upload(
            channels='#general',
            file=filepath)
        assert response["file"]  # the uploaded file
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")