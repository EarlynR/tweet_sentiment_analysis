from tweepy.streaming import Stream

from twitter.tweepy_scraper import CorpusBuilder
from settings import api

corpus_builder = CorpusBuilder()
stream = Stream(api.auth, listener=corpus_builder)
stream.filter(languages=['en'], track=['buy'])
