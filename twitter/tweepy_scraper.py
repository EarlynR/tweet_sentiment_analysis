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


def parse_status(status):
    '''
    Parse through the status and only keep the fields that are relevant to the model.
    This will save hardware space.
    :param status:
    :return: a dictionary of all of the fields that we decided to keep
    '''
    user_name = status.user.screen_name
    users_loc = status.user.location
    tweet_coords = status.coordinates
    text = status.text
    # symbols_in_text = list(status.entities.hastags.symbols.text)
    # hashtags_in_text = list(status.entities.hastags.text)
    created_date = status.created_at

    # TODO: Implement get_score
    # lead_score = get_score(text)

    table_fields = {
        "user_name": user_name,
        "user_location": users_loc,
        "tweet_coordinates": tweet_coords,
        "text": text,
        # "symbols_in_text": symbols_in_text,
        # "hashtags": hashtags_in_text,
        "created_date": created_date,
        #"lead_score": lead_score,
    }


    return table_fields




#Start streaming the data.
# stream_listener = StreamListener()
# stream = Stream(auth=api.auth, listener=stream_listener)
# stream.filter(languages=['en'], filter_level=['none'])


def get_score(tweet_fields):
    pass


def add_user(data):
    """
    Inserts the given data into a table.
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
    user_id = TwitterUser.query.filter_by(user_name=data['user_name']).first().id

    tweet = Tweet(
        user_id=user_id,
        body=data['text'],
        coordinates=data['tweet_coordinates'],
        symbols=data['symbols_in_text'],
        hashtags=data['hashtags'],
        created_date=data['created_date'],
    )
    db.session.add(tweet)
    db.session.commit()
