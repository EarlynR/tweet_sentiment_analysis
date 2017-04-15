from tweepy import StreamListener, Stream

import settings
from settings import api
from app import db
from app.models import TwitterUser, Tweet


class CorpusBuilder(StreamListener):

    def on_status(self, status):
        if status.retweeted:
            return

        tweet_fields = parse_status(status)

        add_user(tweet_fields)
        add_tweet(tweet_fields)

    def on_error(self, status_code):
        if status_code == 420:
            return False


class TwitterScraper(StreamListener):

    def on_status(self, status):
        if status.retweeted:
            return
            
        tweet_fields = parse_status(status)

        get_score(tweet_fields)

        add_user(tweet_fields)
        add_tweet(tweet_fields)


    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

#Start streaming the data.
# stream_listener = StreamListener()
# stream = Stream(auth=api.auth, listener=stream_listener)
# stream.filter(languages=['en'], filter_level=['none'])


def get_score(tweet_fields):
    pass


def parse_status(status):
    pass


def add_user(data):
    """
    Inserts the given data into a table.
    :param table_name: Name of the table to be updated
    :param data: Data dictionary of columns/values
    """
    user = TwitterUser(user_name=data['user_name'], location=data['location'])
    db.session.add(user)
    db.session.commit()


def add_tweet(data):
    """
    Adds tweet to Tweets table
    :param data: tweet_fields from twitter stream listener
    """
    tweet = Tweet(
        body=data['text'],
        coordinates=data['tweet_coordinates'],
        symbols=data['symbols_in_text'],
        hashtags=data['hashtags'],
        created_date=data['created_date'],
    )
    db.session.add(tweet)
    db.session.commit()
