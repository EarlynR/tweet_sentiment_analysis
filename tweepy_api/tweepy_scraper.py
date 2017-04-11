import settings
import tweepy
import dataset
from sqlalchemy.exc import ProgrammingError
import json

db = dataset.connect(settings.connection_string)

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
                
                
        if status.retweeted:
            return
            
        #Included are all of the fields from the twitter api that I think are relevant.     
        user_name= status.user.screen_name
        users_loc = status.user.location
        tweets_coords = status.coordinates
        text = status.text
        symbols_in_text = list(status.entities.hastags.symbols.text)
        hastags_in_text = list(status.entities.hastags.text)
        tweet_created_at = status.created_at
        lead_score = get_score(text)

        #Getting ready to put my inputs into a table
        table = db[settings.table_name]
        try:
            table.insert(dict(
                user_name=user_name
                user_location=users_loc,
                tweet_coordinates=tweets_coords,
                text=text,
                symbols_in_text = symbols_in_text,
                hastags_in_text = hastags_in_text,
                tweet_created_at = tweet_created_at,
                lead_score = sent.lead_score,
            ))
        except ProgrammingError as err:
            print err

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

#Opening a connection to the Twitter api with proper keys. 
auth = tweepy.OAuthHandler(settings.consumer_key, settings.consumer_secret)
auth.set_access_token(settings.access_token, settings.access_token_secret)
api = tweepy.API(auth)

#Start streaming the data.
stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(languages= ['en'], filter_level = ['none'])