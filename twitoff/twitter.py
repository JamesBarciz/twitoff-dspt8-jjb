from os import getenv
import tweepy
import spacy
# from decouple import config

from .models import DB, User, Tweet


TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = getenv('TWITTER_API_SECRET_KEY')
TWITTER_ACCESS_KEY = getenv('TWITTER_ACCESS_KEY')
TWITTER_ACCESS_KEY_SECRET = getenv('TWITTER_ACCESS_KEY_SECRET')


TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
TWITTER_AUTH.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)


spacy_model_name = "en_core_web_sm"
if not spacy.util.is_package(spacy_model_name):
	spacy.cli.download(spacy_model_name)

nlp = spacy.load(spacy_model_name)
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(name):
	"""
	Add or update a user and their tweets.
	Throw an error if user doesn't exist or is private
	"""
	try:
		twitter_user = TWITTER.get_user(name)
		db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id, name=name)
		tweets = twitter_user.timeline(count=200, 
			exclude_replies=True, 
			include_rts=False,
			since_id=db_user.newest_tweet_id)

		if tweets:
			db_user.newest_tweet_id = tweets[0].id

		for tweet in tweets:
			embedding = list(nlp(tweet.text).vector)
			db_tweet = Tweet(id=tweet.id, text=tweet.text, embedding=embedding)
			db_user.tweets.append(db_tweet)

		DB.session.add(db_user)
		DB.session.commit()
	except Exception as e:
		print(f'Unable to process user {name}: {str(e)}')


def update_all_users():
	"""	Update all Tweets for existing users."""
	for user in User.query.all():
		add_or_update_user(user.name)



# >>> from twitoff.twitter import *
# >>> from twitoff.models import *
# >>> import spacy
# >>> DB.drop_all()
# >>> DB.create_all()
# >>> username = 'elonmusk'
# >>> twitter_user = TWITTER.get_user(username)
# >>> tweets = twitter_user.timeline(count=200, exclude_replies=True, exclude_rts=True)
# >>> nlp = spacy.load('en_core_web_md')
# >>> db_user = User(name=username)
# >>> for tweet in tweets:
# ...   text = tweet.text
# ...   embedding = list(nlp(text).vector)
# ...   db_tweet = Tweet(id=tweet.id, tweet=text, embedding=embedding)
# ...   db_user.tweets.append(db_tweet)
# >>> DB.session.add(db_user)
# >>> DB.session.commit()