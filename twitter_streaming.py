from __future__ import print_function
import tweepy
import json
import os
import logging
from pymongo import MongoClient
from os import environ
from flask import Flask

MONGO_HOST = 'mongodb+srv://' + os.environ['MONGO_USER'] + ':' + os.environ['MONGO_PASS'] + '@cluster0-2bfcj.mongodb.net/test?retryWrites=true'

WORDS = ['#metro', '#madrid', '#L1', '#L2', '#L3', '#L4', '#L6']

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
 
logging.info("Starting app")
print("Starting app")

class StreamListener(tweepy.StreamListener):    
    #This is a class provided by tweepy to access the Twitter Streaming API. 
 
    def on_connect(self):
        # Called initially to connect to the Streaming API
        logging.info("You are now connected to the streaming API.")
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        logging.error('An Error has occured: ' + repr(status_code))
        print('An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            client = MongoClient(MONGO_HOST)
            
            # Use metrotwitterdb database. If it doesn't exist, it will be created.
            db = client.metrotwitterdb
    
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            
            if datajson['lang'] == 'es':
                #grab the 'created_at' data from the Tweet to use for display
                created_at = datajson['created_at']
    
                #print out a message to the screen that we have collected a tweet
                logging.debug("Tweet collected at " + str(created_at))
                print("Tweet collected at " + str(created_at))
                
                #insert the data into the mongoDB into a collection called tweets
                #if tweets doesn't exist, it will be created.
                db.tweets.insert(datajson)
        except Exception as e:
           print(e)
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
streamerSearch = tweepy.Stream(auth=auth, listener=listener)
streamerOfficial = tweepy.Stream(auth=auth, listener=listener)
logging.info("Tracking: " + str(WORDS))
print("Tracking: " + str(WORDS))
streamerSearch.filter(track=WORDS)
streamerOfficial.filter(follow=None, track=os.environ['OFFICIAL_METRO_ACCOUNT'])

app = Flask(__name__)
app.run(host= '0.0.0.0', port=environ.get('PORT'))