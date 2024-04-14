import os
from os import environ
from dotenv import load_dotenv
from flask import Flask, request, abort
import pandas as pd
import requests

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

from functions.store_aed_data import aed_data_to_pandas, fetch_aed_data

def convert_to_dict(data):
    return [
        {
            'DIST': data['DIST'],
            'LocationName': data['LocationName'],
            'ADRESS': f"{data['Perfecture']}{data['City']}{data['AddressArea']} {data['FacilityName']}",
            'FacilityPlace': data['FacilityPlace'],
            'Lat': data['Latitude'],
            'Lng': data['Longitude']
        }
    ]

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
    if event.message.text == "emergency":
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            items = [
                QuickReplyItem(
                    action=LocationAction(
                        label="位置情報を送信する",
                        text="location"
                    
                    )
                )
            ]
            # set quick reply
            quick_reply = QuickReply(items=items)
            message=TextMessage(text='近くのAEDを調査するため現在地を送信してください', quickReply=quick_reply)

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
    user_lat = event.message.latitude
    user_lng = event.message.longitude
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        url = f"https://aed.azure-mobile.net/api/NearAED?lat={user_lat}&lng={user_lng}"
        response = requests.get(url)
        
        aed_data = response.json()
        select_data = convert_to_dict(aed_data[0])
        
        destination_lat = select_data[0]['Lat']
        destination_lng = select_data[0]['Lng']
        
        user_lat = event.message.latitude
        user_lng = event.message.longitude
        
        url = f"https://www.google.com/maps/dir/?api=1&origin={user_lat},{user_lng}&destination={destination_lat},{destination_lng}&travelmode=walking"

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text="直近のAEDの情報です"),
                    TextMessage(text=url),
                    TextMessage(text="AEDを取りに行っている間に、以下の応急処置を行ってください。\n\n1. 呼吸確認: 意識がない場合は気道の確保と人工呼吸を行います。脈拍も確認し、心肺蘇生を開始します。\n\n2. 出血コントロール: 大きな出血がある部位は、清潔なタオルやガーゼで強く押さえつけて止血を図ります。\n\n3. ショック予防: 寒冷化を防ぐため、毛布などで体を覆い保温します。必要に応じて四肢を挙上します。\n\n4. 緊急連絡: 状況を家族や救急隊に随時連絡し、迅速な対応を要請します。\n\n5 .安静保持: 意識のある方の場合は、動かずに安静を保つよう指示します。\n\n6. その他: 状況に応じて、骨折の固定、熱傷の冷却など、必要な応急処置を行います。")
                    ]
                )
        )


if __name__ == '__main__':
    app.run(port=3131, debug=True)
    