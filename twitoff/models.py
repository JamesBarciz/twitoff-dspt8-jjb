from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(30), nullable=False)


class Tweet(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    tweet = DB.Column(DB.Unicode(280), nullable=False)  # Tweets are beyond ASCII thus, need Unicode
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f'<Tweet: {self.tweet}'