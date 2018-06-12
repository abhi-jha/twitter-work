import tweepy
from credentials import cred
import peewee
from peewee import *
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('twitter.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

twitter = MySQLDatabase('twitter', user='root', passwd='root')
last_max = ''
class DATA(peewee.Model):
    id = peewee.BigIntegerField()
    created_at = peewee.DateTimeField()
    user_name = peewee.CharField()
    lang = peewee.CharField()
    text = peewee.CharField()
    class Meta:
        database = twitter
        db_table = 'tweets'

auth = tweepy.OAuthHandler(cred["CONSUMER_KEY"], cred["CONSUMER_SECRET"])
auth.set_access_token(cred["ACCESS_TOKEN"], cred["ACCESS_TOKEN_SECRET"])

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        #print(status.id)
        #print(status.created_at)
        #print(status.user.name)
        #print(status.lang)
        #print(status.text)
        #print("\n\n\n")

        record = DATA(id = status.id, created_at = status.created_at, user_name = status.user.name, lang = status.lang, text = status.text)
        try:
            record.save(force_insert=True)
            #logger.info("successful")
        except Exception as e:
            logger.info( e)



myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['python','data','machine learning','analysis','datsets','papers','computer science'], async=True)
