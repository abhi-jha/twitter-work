import tweepy
from credentials import cred

auth = tweepy.OAuthHandler(cred["CONSUMER_KEY"], cred["CONSUMER_SECRET"])
auth.set_access_token(cred["ACCESS_TOKEN"], cred["ACCESS_TOKEN_SECRET"])

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)