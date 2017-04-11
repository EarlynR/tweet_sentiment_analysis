from app import db


class TwitterUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), index=True, unique=True)
    location = db.Column(db.String(40))  # TODO: is db.String(40) right?
    tweets = db.relationship('Tweet', backref='author', lazy='dynamic')


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('twitteruser.id'))
    body = db.Column(db.String(140))

    # TODO: Verify data types for these columns
    coordinates = db.Column(db.String(40))
    symbols = db.Column(db.String(40))
    hashtags = db.Column(db.string(140))
    created_date = db.Column(db.DateTime)

