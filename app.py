from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('faWlPkEFhmsXKWmyGr6Gzxs763PvibrK3P8i2C/7zR5GLaW9wTvSrBvBgZmniJ/8+NmQ4h729d3kT/98GhYeVowqau0fQEJgyl60cU/9HyteThr/b+y1RdjXXjYIgn7C7E0/HI1Jhl+28y+wNULZ1QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('696414cef3aaa6169735468569a6c67f')


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

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
