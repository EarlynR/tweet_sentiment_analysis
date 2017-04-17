import os
import datetime
from unittest import TestCase

from app import app, db
from settings import BASE_DIR
from twitter import tweepy_scraper
from app.models import TwitterUser, Tweet
from mock import Mock


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

    def test_parse_status(self):
        self.maxDiff = None
        status = Mock(
            user_name='@fake_user_name',
            user_location='fake_location',
            coordinates='fake_coordinates',
            text='fake_test',
            # symbols_in_text='fake_symbols_in_fake_text',
            # hashtags='fake_hashtags',
            created_at='fake_created_date',
            #lead_score=3,
        )
        status.user = Mock(
            screen_name='@fake_user_name',
            location='fake_location'
        )

        expected_result = {
                "user_name": status.user_name,
                "user_location": status.user_location,
                "tweet_coordinates": status.coordinates,
                "text": status.text,
                # "symbols_in_text": status.symbols_in_text,
                # "hashtags": status.hashtags,
                "created_date": status.created_at,
                # "lead_score": lead_score,
        }

        test_fields = tweepy_scraper.parse_status(status)
        self.assertEqual(test_fields, expected_result)

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
        test_tweet = Tweet.query.filter_by(user_id=test_user.id).first()

        self.assertEqual(test_tweet.body, data['text'])
        self.assertEqual(test_tweet.coordinates, data['tweet_coordinates'])
        self.assertEqual(test_tweet.symbols, data['symbols_in_text'])
        self.assertEqual(test_tweet.hashtags, data['hashtags'])
        self.assertEqual(test_tweet.created_date, data['created_date'])
