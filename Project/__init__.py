from flask import Flask, request, abort
import requests
import json
from Project.Config import *
from uncleengineer import thaistock
app = Flask(__name__)


keyword01 = ['คือใคร','เป็นใคร']
AnimeZone = 'https://www.anime-sugoi.com/tag/{}.html'
name = ['konosuba','date-a-live','to-love-ru']


def GET_BTC_PRICE():
    data = requests.get('https://bx.in.th/api/')
    BTC_PRICE = data.text.split('BTC')[1].split('last_price":')[1].split(',"volume_24hours')[0]
    return BTC_PRICE

API_URL = 'https://api.bitkub.com'

endpoint = {
    'status':'/api/status',
    'timestamp':'/api/servertime',
    'symbols':'/api/market/symbols',
    'ticker':'/api/market/ticker',
    'trades':'/api/market/trades'

}

def GET_BTC_PRICE_02(COIN = 'THB_BTC'):
    url = API_URL + endpoint['ticker']
    r = requests.get(url,params = {'sym':COIN})
    data = r.json()
    PRICE_BTC = data[COIN]['last']
    return PRICE_BTC





@app.route('/webhook', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        payload = request.json

        Reply_token = payload['events'][0]['replyToken']
        print(Reply_token)
        message = payload['events'][0]['message']['text']
        print(message)
        if 'หุ้น' in message :
            ITD = thaistock('ITD')
            Reply_messasge = 'คำตอบ: ราคาหุ้น อิตาเลียนไทย ขณะนี้ : {}'.format(ITD)
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        
        elif 'btc' in message :
            Reply_messasge = 'คำตอบ: ราคา BITCOIN ขณะนี้ : {}'.format(GET_BTC_PRICE_02())
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        
        elif 'เป็นใคร' in message:
            Reply_messasge = 'แนะนำตัว: ยูซูรุเองค่ะ'
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        
        elif 'คือใคร' in message:
            Reply_messasge = 'แนะนำตัว: ยูซูรุเองค่ะ'
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        
        elif '55' in message:
            Reply_messasge = 'งุนงง: หัวเราะหาพ่อมึงหรอ'
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        
        elif 'คำสั่ง' in message:
            Reply_messasge = 'ชี้แจง: เช็คหุ้น พิมพ์ อะไรก็ได้ตามด้วย หุ้น หรือให้มีคำว่าหุ้นอยู่ในประโยค\n\n\nค้นหาอนิเมะ พิมพ์ ชื่อเรื่อง\n\n\nถามราคา BTC พิมพ์ btc'
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)

        elif name[0] in message:
            Reply_messasge = AnimeZone.format(name[0])
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)

        elif name[1] in message:
            Reply_messasge = AnimeZone.format(name[1])
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        
        elif name[2] in message:
            Reply_messasge = AnimeZone.format(name[2])
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)

        

        return request.json, 200

    elif request.method == 'GET' :
        return 'this is method GET!!!' , 200

    else:
        abort(400)

@app.route('/')
def hello():
    return 'hello world book',200

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = {
        "replyToken":Reply_token,
        "messages":[{
            "type":"text",
            "text":TextMessage
        }]
    }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data) 
    return 200