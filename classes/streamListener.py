import logging
import tweepy
from .tweet import Tweet
from .nlpProcessor import NlpProcessor

logger = logging.getLogger(__name__)


class StreamListener(tweepy.StreamListener):
    #This is a class provided by tweepy to access the Twitter Streaming API.

    def __init__(self, classify, api):
        logger.info("init StreamListener")
        self.nlpProcessor = NlpProcessor()
        self.classify = classify
        super().__init__(api)

    def on_connect(self):
        # Called initially to connect to the Streaming API
        logger.info("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        logger.error('An Error has occured: ' + repr(status_code))
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
            logger.error(e)
