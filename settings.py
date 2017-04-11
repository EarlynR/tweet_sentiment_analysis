import os
import tweepy

#Variables that contains the user credentials to access Twitter API
access_token = os.environ.get('TWITTER_ACCESS_KEY')
access_token_secret = os.environ.get('TWITTER_SECRET_ACCESS_KEY')
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_SECRET_CONSUMER_KEY')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

connection_string = 'sqlite:///tweets.db'
table_name = 'Lead Score'