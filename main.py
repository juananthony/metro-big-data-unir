from __future__ import print_function
import json
import os
import sys
import logging
import tweepy
from os import environ
from flask import Flask
from logging.handlers import TimedRotatingFileHandler


WORDS = ['metro_madrid']

logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = TimedRotatingFileHandler(
                filename=os.path.join('./logs', 'metrodata' + sys.argv[1] + '.log'),
                when="midnight",
                interval=1,
                backupCount=7)
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


from classes.streamListener import StreamListener
import config

if sys.argv[1] == '-t':
    CONSUMER_KEY = config.CONSUMER_KEY
    CONSUMER_SECRET = config.CONSUMER_SECRET
    ACCESS_TOKEN = config.ACCESS_TOKEN
    ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET
elif sys.argv[1] == '-f':
    CONSUMER_KEY = config.CONSUMER_KEY_FOLLOW
    CONSUMER_SECRET = config.CONSUMER_SECRET_FOLLOW
    ACCESS_TOKEN = config.ACCESS_TOKEN_FOLLOW
    ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET_FOLLOW

logger.info("Starting app")



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
has_to_classify = True if sys.argv[1] == '-t' else False
listener = StreamListener(classify=has_to_classify, api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)


if sys.argv[1] == '-t':
    logger.info("Tracking: " + str(WORDS))
    streamer.filter(track=WORDS)
elif sys.argv[1] == '-f':
    logger.info("user.id: " + config.OFFICIAL_METRO_ACCOUNT)
    streamer.filter(follow=[config.OFFICIAL_METRO_ACCOUNT])
