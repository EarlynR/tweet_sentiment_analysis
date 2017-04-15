import os
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
        test_user = TwitterUser(user_name="@TestUser", location="test_coords")

        self.assertIsNone(db.session.query(test_user))

        db.session.add(test_user)
        db.session.commit()

        print db.session.query(test_user)
        assert False

