from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

ACCESS_TOKEN = '3TYq/22WRBB8DXdAOQ0ymVzfsr+BmvTZhEvVrRlc3lb3sJ/yrpiUQhhPkLMKMx/lTljjidUqm8MVr59nAN1ffNwKLvsySlswx1G+d5hEa+A4PuYKdQ7uP78TiMB7gwTVaHWHkWB9vm0EnKZt2qYzhgdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '35e9177500815f2962713f15edf238f6'


line_bot_api = LineBotApi(ACCESS_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=event.message.text)
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()