import tweepy
from decouple import config



TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_API_KEY'), config('TWITTER_API_SECRET_KEY'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_KEY'), config('TWITTER_ACCESS_KEY_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

# >>> from twitoff.twitter import *
# >>> from twitoff.models import *
# >>> import spacy
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
# >>> DB.drop_all()
# >>> DB.create_all()
# >>> DB.session.add(db_user)
# >>> DB.session.commit()