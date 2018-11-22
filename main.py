from __future__ import print_function
import json
import os
import sys
import logging
import tweepy
from os import environ
from flask import Flask
from classes.StreamListener import StreamListener

WORDS = ['#metro', '#madrid', '#L1', '#L2', '#L3', '#L4', '#L6']

if sys.argv[1] == '-t':
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
elif sys.argv[1] == '-f':
    CONSUMER_KEY = os.environ['CONSUMER_KEY_FOLLOW']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET_FOLLOW']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN_FOLLOW']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET_FOLLOW']
 
logging.info("Starting app")
print("Starting app")
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)


if sys.argv[1] == '-t':
    print("Tracking: " + str(WORDS))
    streamer.filter(track=WORDS)
elif sys.argv[1] == '-f':
    print("user.id: " + os.environ['OFFICIAL_METRO_ACCOUNT'])
    streamer.filter(follow=[os.environ['OFFICIAL_METRO_ACCOUNT']])
