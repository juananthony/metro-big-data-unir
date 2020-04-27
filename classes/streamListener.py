import logging
import tweepy
from .tweet import Tweet
from .nlpProcessor import NlpProcessor

class StreamListener(tweepy.StreamListener):
    #This is a class provided by tweepy to access the Twitter Streaming API.

    def __init__(self, classify, api):
        self.nlpProcessor = NlpProcessor()
        self.classify = classify
        super().__init__(api)

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
            # Decode the JSON from Twitter
            tweet = Tweet(data)
            if self.classify:
                self.nlpProcessor.classify(tweet)
            tweet.saveTweet()

        except Exception as e:
            print(" ########### ERROR in StreamListener:")
            print(e)
