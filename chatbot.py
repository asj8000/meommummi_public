# -*- coding: utf-8 -*-
import os
from flask import Flask, request, Response
import slack
import requests

from skills.weather import weather
from skills.help import help_command
from skills.lunch_search import lunch_search
#from skills.lunch_search import lunch_search
#잠깐 사용 X

app = Flask(__name__)
SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_OUTGOING_WEBHOOKS')
SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
slack_client = slack.WebClient(token=SLACK_TOKEN)



def send_message_block(channel_id, message):
    slack_client.chat_postMessage(
        channel=channel_id,
        blocks=message,
        username='멈뭄미',
        icon_emoji=':profile_meommummi:'
    )

def send_message(channel_id, message):
    slack_client.chat_postMessage(
        channel=channel_id,
        text=message,
        username='멈뭄미',
        icon_emoji=':profile_meommummi:'
    )


@app.route('/webhook', methods=['POST'])

def inbound():
    meommummi_curse = 0
    username = request.form.get('user_name')
    if request.form.get('token') == SLACK_WEBHOOK_SECRET and username != 'slackbot':
        channel_name = request.form.get('channel_name')
        channel_id = request.form.get('channel_id')
        username = request.form.get('user_name')
        text = request.form.get('text')
        defalt_message = '아직 개발중인 기능이에요!'

        if '도움말' in text or 'help' in text or '명령어' in text or '사용법' in text:
            send_message_block(channel_id, help_command(text))
        elif '날씨' in text:
            message = weather(text)
            send_message_block(channel_id, message)
        elif '메뉴' in text or '점심' in text or '배고파' in text:
            message = lunch_search(text)
            send_message_block(channel_id,message)
        elif '테스트' in text:
            message = str([
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": 'message'
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Average Rating*\n1.0"
                        }
                    ]
                }
            ])
            send_message_block(channel_id, message)
        elif '접속' in text:
            send_message(channel_id, defalt_message)
        elif '문서' in text or '찾기' in text:
            message = file_search(text)
            send_message_block(channel_id,message)
        elif '안녕' in text or '반가워' in text:
            hello_message = '반가워요!!'
            send_message(channel_id, hello_message)
        else:
            message = '명령어를 보시려면 "멈뭄미 명령어" 를 입력해주세요!'
            send_message(channel_id,message)




    return Response(), 200






@app.route('/', methods=['GET'])
def test():
    return Response('It works!')

if __name__ == "__main__":
    app.run(debug=True)