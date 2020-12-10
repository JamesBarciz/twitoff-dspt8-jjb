# from flask_sqlalchemy import SQLAlchemy

# DB = SQLAlchemy()

# class User(DB.Model):
#     id = DB.Column(DB.Integer, primary_key=True)
#     name = DB.Column(DB.String(30), nullable=False)
#     newest_tweet_id = DB.Column(DB.BigInteger)  # Needed to add more tweets (update route)

#     def __repr__(self):
#         return f'<User: {self.name}>'


# class Tweet(DB.Model):
#     id = DB.Column(DB.Integer, primary_key=True)
#     tweet = DB.Column(DB.Unicode(280), nullable=False)  # Tweets are beyond ASCII thus, need Unicode
#     embedding = DB.Column(DB.PickleType, nullable=False)  # Whatever isn't a number or string is a PickleType (embedding)
#     user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
#     user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

#     def __repr__(self):
#         return f'<Tweet: {self.tweet}'

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
	id = DB.Column(DB.BigInteger, primary_key=True)
	name = DB.Column(DB.String(15), nullable=False)
	newest_tweet_id = DB.Column(DB.BigInteger)
	def __repr__(self):
		return f'<User: {self.name}>'


class Tweet(DB.Model):
	id = DB.Column(DB.BigInteger, primary_key=True)
	text = DB.Column(DB.Unicode(300), nullable=False)
	embedding = DB.Column(DB.PickleType, nullable=False)
	user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
	user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

	def __repr__(self):
		return f'<Tweet: {self.text}>'