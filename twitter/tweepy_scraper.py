from tweepy import StreamListener, Stream

import settings
from settings import api
from app import db

# TODO: Create local db & settings module
# db = dataset.connect(settings.connection_string)


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.retweeted:
            return
            
        user_name= status.user.screen_name
        users_loc = status.user.location
        tweets_coords = status.coordinates
        text = status.text
        symbols_in_text = list(status.entities.hastags.symbols.text)
        hastags_in_text = list(status.entities.hastags.text)
        tweet_created_at = status.created_at

        # TODO: Implement get_score
        # lead_score = get_score(text)

        #Getting ready to put my inputs into a table
        # TODO: Implement db
        table = db[settings.table_name]

        table.insert(dict(
            user_name=user_name
            user_location=users_loc,
            tweet_coordinates=tweets_coords,
            text=text,
            symbols_in_text = symbols_in_text,
            hastags_in_text = hastags_in_text,
            tweet_created_at = tweet_created_at,
            # lead_score = sent.lead_score,
        ))

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

#Start streaming the data.
stream_listener = StreamListener()
stream = Stream(auth=api.auth, listener=stream_listener)
stream.filter(languages=['en'], filter_level=['none'])
