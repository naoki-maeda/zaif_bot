# zaif_bot
暗号通貨取引所Zaifのビットコイン価格などを返すLINE botです。非公式です。

# 環境構成
* Python3.5.1
* Django 1.10.1
* line-bot-sdk 1.0.2
* zaifapi 1.0.1
* サーバーはHerokuを使用しています。

# 使い方
* 以下のQRコードを読み取り、LINEで友達追加してください。

![](images/line_qr.png)

* zaifと入力すれば通貨ペアを表示するので選択してください。
* 通貨ペアはbtc_jpy、xem_jpy、mona_jpy、mona_btcの4つです。
* 現時点では返してくる値はzaifで取引されている最終取引価格のみです。
