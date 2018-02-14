__author__ = 'yyb'

#real-time tweets flows

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import datetime


consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth=OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)

class MyListener(StreamListener):
    def on_data(self,data):
        n=1
        try:
            with open('/Users/yyb/Desktop/tweets_API_test.json','a')as f:
                print()
                f.write(data)
                n+=1
                print(n)
                return True
        except BaseException as e:
            print('Error on_data:%S'%str(e))

        return True

    def on_error(self,status):
        print(status)
        return True


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#python'])



