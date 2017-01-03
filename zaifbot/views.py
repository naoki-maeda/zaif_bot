# from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, URITemplateAction, PostbackTemplateAction,PostbackEvent,
)

from zaifapi import impl


ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
CHANNEL_SECRET = 'YOUR_CHANNEL_SECRET'

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
                text = event.message.text
                if text == 'zaif':
                    zaif = impl.ZaifPublicApi()
                    btc = str(zaif.last_price('btc_jpy')['last_price'])
                    xem = str(zaif.last_price('xem_jpy')['last_price'])
                    mona = str(zaif.last_price('mona_jpy')['last_price'])
                    mona_btc = str(zaif.last_price('mona_btc')['last_price'])
                    buttons_template = ButtonsTemplate(
                        title = 'Zaif button', text = '好きな通貨ペアを選択してください。', actions=[
                            MessageTemplateAction(label='BTC_JPY', text=btc),
                            MessageTemplateAction(label='XEM_JPY', text=xem),
                            MessageTemplateAction(label='MONA_JPY', text=mona),
                            MessageTemplateAction(label='MONA_BTC', text=mona_btc),
                    ])
                    template_message = TemplateSendMessage(
                        alt_text='BTC価格をお知らせします', template=buttons_template
                    )
                    line_bot_api.reply_message(event.reply_token,template_message)
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                       TextSendMessage(text=event.message.text)
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
