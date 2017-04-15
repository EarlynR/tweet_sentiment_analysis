from tweepy import StreamListener, Stream

import settings
from settings import api
from app import db
from app.models import TwitterUser, Tweet


class TwitterScraper(StreamListener):

    def on_status(self, status):
        if status.retweeted:
            return
            
        user_name = status.user.screen_name
        users_loc = status.user.location
        tweet_coords = status.coordinates
        text = status.text
        symbols_in_text = list(status.entities.hastags.symbols.text)
        hashtags_in_text = list(status.entities.hastags.text)
        created_date = status.created_at

        # TODO: Implement get_score
        # lead_score = get_score(text)

        table = db[settings.table_name]

        table_fields = {
            "user_location": users_loc,
            "tweet_coordinates": tweet_coords,
            "text": text,
            "symbols_in_text": symbols_in_text,
            "hashtags": hashtags_in_text,
            "created_date": created_date,
        }

        table.insert(table_fields)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

#Start streaming the data.
# stream_listener = StreamListener()
# stream = Stream(auth=api.auth, listener=stream_listener)
# stream.filter(languages=['en'], filter_level=['none'])


def add_user(data):
    """
    Inserts the given data into a table.
    :param table_name: Name of the table to be updated
    :param data: Data dictionary of columns/values
    """
    user = TwitterUser(user_name=data['user_name'], location=data['location'])
    db.session.add(user)
    db.session.commit()
