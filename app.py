import os
from os import environ
from dotenv import load_dotenv
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent, LocationMessageContent
from linebot.v3.messaging.models.location_action import LocationAction
from linebot.v3.messaging import (
    ReplyMessageRequest,
    TextMessage,
    QuickReply,
    QuickReplyItem,    
)

# original file import area


# ----------------------------
app = Flask(__name__)

# setting enviroment variable
# for local
if os.path.exists('.env'):
    load_dotenv('.env', verbose=True)
    channel_secret = os.getenv('LINE_CHANNEL_SECRET')
    access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    
# for heroku
else:
    channel_secret = os.environ.get('LINE_CHANNEL_SECRET')
    access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')

# check if the environment variable is set
if not channel_secret:
    raise Exception("LINE_CHANNEL_SECRET is not set")
if not access_token:
    raise Exception("LINE_CHANNEL_ACCESS_TOKEN is not set")

configuration = Configuration(access_token=access_token)
handler = WebhookHandler(channel_secret)


# root directory
@app.route('/')
def index():
    return 'emergency service!'

# response to LINE API callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        print(e)
        abort(500)
    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    print('?'*10)
    if event.message.text == "location":
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            items = [
                QuickReplyItem(
                    action=LocationAction(
                        label="Location",
                        text="位置情報を送信する"
                    
                    )
                )
            ]
            quick_reply = QuickReply(items=items)

            message=TextMessage(text='返信メッセージ', quickReply=quick_reply)

            line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[message]
                        )
                    )
                
    else:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    # messages=[TextMessage(text=f"your position is {event.message.latitude} {event.message.longitude}")]
                    messages=[TextMessage(text=f"hoge")]  
                )
            )
            
# location message
@handler.add(MessageEvent, message=LocationMessageContent)
def handle_location(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        user_latitude = event.message.latitude
        user_longitude = event.message.longitude

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=f"緯度：{user_latitude}\n経度 : {user_longitude}")] 
                )
        )       


if __name__ == '__main__':
    app.run(port=3131, debug=True)
    