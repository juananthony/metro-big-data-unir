import logging
import tweepy
from tweet import Tweet
from nlpProcessor import NlpProcessor

class StreamListener(tweepy.StreamListener):    
    #This is a class provided by tweepy to access the Twitter Streaming API. 

    def __init__(self):
        self.nlpProcessor = NlpProcessor()
 
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

            self.nlpProcessor.classify(tweet)
            
            if tweet.isSpanish():
                #grab the 'created_at' data from the Tweet to use for display
                created_at = tweet.created_at
    
                #print out a message to the screen that we have collected a tweet
                logging.debug("Tweet collected at " + str(created_at))
                print("Tweet collected at " + str(created_at))
                
                #insert the data into the mongoDB into a collection called tweets
                #if tweets doesn't exist, it will be created.
                db.tweets.insert(tweet.jsonData)
        except Exception as e:
           print(e)