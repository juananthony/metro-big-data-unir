import nltk
import pickle
import logging
import os
from .tweet import Tweet
import sys
sys.path.append("..")
import config

class NlpProcessor():

    def __init__(self):
        script_dir = os.path.dirname(__file__)
        self.navie_bayes_classifier = config.NAIVE_BAYES_CLASSIFIER
        f = open(script_dir + '/../classifiers/' + self.navie_bayes_classifier + '.classifier.pickle', 'rb')
        self.classifier = pickle.load(f)
        f.close()
        f = open(script_dir + '/../classifiers/' + self.navie_bayes_classifier + '.all_words.pickle', 'rb')
        self.all_words = pickle.load(f)
        f.close()

    def classify(self, tweet):
        if tweet.isSpanish():
            print("tweet:")
            print(tweet.words)
            created_at = tweet.created_at
            #print out a message to the screen that we have collected a tweet
            logging.debug("Tweet collected at " + str(created_at))
            print("Tweet collected at " + str(created_at))

            text_features = tweet.getFeatures(self.all_words)

            classification = self.classifier.classify(text_features)
            print("classification: " + classification)

            tweet.setClassification(classification, self.navie_bayes_classifier)

            tweet.saveTweet()
