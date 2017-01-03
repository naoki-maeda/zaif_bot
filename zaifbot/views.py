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


ACCESS_TOKEN = '3TYq/22WRBB8DXdAOQ0ymVzfsr+BmvTZhEvVrRlc3lb3sJ/yrpiUQhhPkLMKMx/lTljjidUqm8MVr59nAN1ffNwKLvsySlswx1G+d5hEa+A4PuYKdQ7uP78TiMB7gwTVaHWHkWB9vm0EnKZt2qYzhgdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '35e9177500815f2962713f15edf238f6'


line_bot_api = LineBotApi(ACCESS_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)

zaif = impl.ZaifPublicApi()
btc = str(zaif.last_price('btc_jpy')['last_price'])


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

        # for event in events:
        #     if isinstance(event, MessageEvent):
        #         if isinstance(event.message, TextMessage):
        #             line_bot_api.reply_message(
        #                 event.reply_token,
        #                 TextSendMessage(text=event.message.text)
        #             )
        for event in events:
            if isinstance(event, MessageEvent):
                text = event.message.text
                if text == 'confirm':
                    confirm_template = ConfirmTemplate(text='Do it?', actions=[
                        MessageTemplateAction(label='Yes', text='Yes!'),
                        MessageTemplateAction(label='No', text='No!'),
                    ])
                    template_message = TemplateSendMessage(
                       alt_text='Confirm alt text', template=confirm_template)
                    line_bot_api.reply_message(
                       event.reply_token,
                       template_message
                    )
                elif text == 'buttons':
                    buttons_template = ButtonsTemplate(
                        title='My buttons sample', text='Hello, my buttons', actions=[
                            URITemplateAction(
                                label='Go to line.me', uri='https://line.me'),
                            PostbackTemplateAction(label='ping', data='ping'),
                            PostbackTemplateAction(
                                label='ping with text', data='ping',
                                text='ping'),
                            MessageTemplateAction(label='Translate Rice', text='米')
                        ])
                    template_message = TemplateSendMessage(
                        alt_text='Buttons alt text', template=buttons_template)
                    line_bot_api.reply_message(event.reply_token, template_message)

                elif text == 'zaif':
                    buttons_template = ButtonsTemplate(
                        title = 'Zaif button', text = 'zaifのBTC価格を表示します。', actions=[
                            PostbackTemplateAction(
                                label='btc_jpy', text=btc
                            ),
                            MessageTemplateAction(label='XEM_jpy', text='XEM')
                        ]
                    )

                elif isinstance(event, PostbackEvent):
                    data = event.postback.data
                    if data == 'ping':
                        line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='ping postback received!')
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                       TextSendMessage(text=event.message.text)
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
