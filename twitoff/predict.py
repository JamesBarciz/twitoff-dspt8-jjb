import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import spacy

from .models import User
from .twitter import vectorize_tweet


def predict_user(user1_name, user2_name, tweet_text):
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()

    user1_emb = np.array([tweet.embedding for tweet in user1.tweets])
    user2_emb = np.array([tweet.embedding for tweet in user2.tweets])

    embeddings = np.vstack([user1_emb, user2_emb])  # create a Numpy matrix - first User1, second User2 (X)
    labels = np.concatenate([np.ones(len(user1.tweets)), np.zeros(len(user2.tweets))])  # y

    knnc = KNeighborsClassifier(weights='distance', metric='cosine').fit(embeddings, labels)
    
    tweet_embedding = vectorize_tweet(tweet_text)
    
    pred = knnc.predict(np.array(tweet_embedding).reshape(1,-1))

    return pred