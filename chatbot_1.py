# -*- coding: utf-8 -*-
import os
from flask import Flask, request, Response
import slack
app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_OUTGOING_WEBHOOKS')
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
slack_client = slack.RTMClient(SLACK_TOKEN)


print(os.environ.get('SLACK_OUTGOING_WEBHOOKS'))

def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='abcdBot',
        icon_emoji=':monkey_face:'
    )
@app.route('/webhook', methods=['POST'])
def inbound():
    username = request.form.get('user_name')
    if request.form.get('token') == SLACK_WEBHOOK_SECRET and username != 'slackbot':
        channel_name = request.form.get('channel_name')
        channel_id = request.form.get('channel_id')
        username = request.form.get('user_name')
        text = request.form.get('text')
        inbound_message = username + " in " + channel_name + " says: " + text
        send_message(channel_id, unicode("alalal ", 'utf-8') + " " + text)
    return Response(), 200
@app.route('/', methods=['GET'])
def test():
    return Response('It works!')
    if __name__ == "__main__":
        app.run(debug=True)
