import tweepy
import random
import time
from textblob import TextBlob

# Twitter APIの認証情報
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

# TweepyでTwitter APIに接続
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# 初期気分を喜怒哀楽でランダムに設定
moods = ['happy', 'angry', 'sad', 'joyful']
current_mood = random.choice(moods)

# 初期ツイート頻度を設定
tweet_frequency = 30  # seconds

while True:
    # ツイート内容と頻度を現在の気分に応じて変更
    if current_mood == 'happy':
        tweet_text = "I'm feeling happy! 😄"
    elif current_mood == 'angry':
        tweet_text = "I'm feeling angry! 😠"
    elif current_mood == 'sad':
        tweet_text = "I'm feeling sad... 😞"
    else:
        tweet_text = "I'm feeling joyful! 🎉"
    
    # ツイートする
    api.update_status(tweet_text)
    
    # ユーザーからの最新のツイートを取得
    mentions = api.mentions_timeline(count=1)
    for mention in mentions:
        # ツイートの感情分析
        analysis = TextBlob(mention.text)
        polarity = analysis.sentiment.polarity

        # ポジティブな反応であれば、ツイート頻度を上げる
        if polarity > 0:
            tweet_frequency -= 5
            current_mood = 'happy'  # 気分を良くする
        # ネガティブな反応であれば、ツイート頻度を下げる
        elif polarity < 0:
            tweet_frequency += 5
            current_mood = 'sad'  # 気分を悪くする
    
    # ツイート頻度が極端にならないように制限
    tweet_frequency = max(10, min(tweet_frequency, 60))
    
    # 次のツイートまでの待機時間
    time.sleep(tweet_frequency)
