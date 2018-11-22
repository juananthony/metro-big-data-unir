import nltk
import logging
from tweet import Tweet

class NlpProcessor():

    def classify(self, tweet):
        if tweet.isSpanish():
            created_at = tweet.created_at
            #print out a message to the screen that we have collected a tweet
            logging.debug("Tweet collected at " + str(created_at))
            print("Tweet collected at " + str(created_at))

            tweet.saveTweet()