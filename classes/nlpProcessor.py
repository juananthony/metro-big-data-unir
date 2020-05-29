import nltk
import pickle
import logging
import os
from .tweet import Tweet
import sys
sys.path.append("..")
import config

logger = logging.getLogger(__name__)


class NlpProcessor():

    def __init__(self):
        logger.info("Initializing NlpProcessor")
        script_dir = os.path.dirname(__file__)
        self.navie_bayes_classifier = config.NAIVE_BAYES_CLASSIFIER
        f = open(script_dir + '/../classifiers/' + self.navie_bayes_classifier + '.classifier.pickle', 'rb')
        self.classifier = pickle.load(f)
        f.close()
        f = open(script_dir + '/../classifiers/' + self.navie_bayes_classifier + '.all_words.pickle', 'rb')
        self.all_words = pickle.load(f)
        f.close()

    def classify(self, tweet):
        try:
            logger.info('classifing tweet: ' + tweet)
            if tweet.isSpanish():
                logger.info('tweet is in spanish')
                created_at = tweet.created_at
                #print out a message to the screen that we have collected a tweet
                logger.info("Tweet collected at " + str(created_at))
                logger.info("Getting tweet features")
                text_features = tweet.getFeatures(self.all_words)
                logger.info("Classifing tweet")
                classification = self.classifier.classify(text_features)
                logger.info('tweet is classified as ' + classification)

                tweet.setClassification(classification, self.navie_bayes_classifier)
        except Exception as e:
            logger.error(e)
