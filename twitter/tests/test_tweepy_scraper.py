import os
import datetime
from unittest import TestCase

from app import app, db
from settings import BASE_DIR
from twitter import tweepy_scraper
from app.models import TwitterUser, Tweet


class TestTweepyScraper(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_user(self):
        data = {
            "user_name": "@TestUser",
            "location": "test_coords",
        }

        self.assertIsNone(TwitterUser.query.filter_by(user_name='@TestUser').first())

        tweepy_scraper.add_user(data)

        test_user = TwitterUser.query.filter_by(user_name="@TestUser").first()
        self.assertEqual(test_user.user_name, data['user_name'])
        self.assertEqual(test_user.location, data['location'])

    def test_add_tweet(self):
        data = {
            "user_name": "@TestlyTestaverde",
            "location": "Testfordshire Abbey",
            "text": "lol this is like totally a tweet and stuff lol",
            "tweet_coordinates": "123.456, 789.000",
            "symbols_in_text": "!@#$%",
            "hashtags": "loltwitter",
            "created_date": datetime.datetime.now(),
        }

        tweepy_scraper.add_user(data)
        test_user = TwitterUser.query.filter_by(user_name='@TestlyTestaverde').first()
        self.assertIsNone(Tweet.query.filter_by(user_id=test_user.id).first())

        tweepy_scraper.add_tweet(data)
        print test_user.id
        test_tweet = Tweet.query.filter_by(user_id=test_user.id).first()

        self.assertEqual(test_tweet.body, data['text'])
        self.assertEqual(test_tweet.coordinates, data['tweet_coordinates'])
        self.assertEqual(test_tweet.symbols, data['symbols_in_text'])
        self.assertEqual(test_tweet.hashtags, data['hashtags'])
        self.assertEqual(test_tweet.created_date, data['created_date'])
