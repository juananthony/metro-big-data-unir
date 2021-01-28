import nltk
import json
import logging
from .database import Database
from nltk.tokenize import word_tokenize


logger = logging.getLogger(__name__)


class Tweet:

    SPANISH = "es"
    ENGLISH = "en"

    def __init__(self, jsonData=None):
        logger.info("init Tweet")
        self.processJson(jsonData)
        self.generateWords()

    def processJson(self, jsonData):
        logger.info("processJson() Tweet")
        self.jsonData = json.loads(jsonData)

        self.text = self.extractText()

        self.created_at = self.jsonData['created_at']
        self.user_id = self.jsonData['user']['id']
        self.lang = self.jsonData['lang']

    def extractText(self):
        logger.info("extractText() Tweet")
        text = ""
        if 'extended_tweet' in self.jsonData:
            text = self.jsonData['extended_tweet']['full_text']
        else:
            text = self.jsonData['text']

        return text

    def generateWords(self):
        logger.info("generateWords() Tweet")
        nltk.download('punkt')
        nltk.download('stopwords')
        tokens = [word for word in nltk.word_tokenize(self.text) if word.isalpha()]
        stopwords = nltk.corpus.stopwords.words("spanish")
        self.words = list(set(tokens) - set(stopwords))
        self.bigrams = nltk.bigrams(tokens)

    def getWords(self):
        logger.info("getWords() Tweet")
        return self.words

    def saveTweet(self):
        logger.info("saveTweet() Tweet")
        database = Database()
        database.insert(collection_name = "tweets", data=self.jsonData)

    def isSpanish(self):
        return self.lang == Tweet.SPANISH

    def isEnglish(self):
        return self.lang == Tweet.ENGLISH

    def getFeatures(self, all_words) :
        logger.info("getFeatures() Tweet")
        return {word.lower(): (word in word_tokenize(self.text.lower())) for word in all_words}

    def setClassification(self, classification, classifier_name):
        self.jsonData['classification'] = {'naive_bayes': {'result' : classification, 'classifier': classifier_name}}