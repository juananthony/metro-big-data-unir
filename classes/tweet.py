import nltk
import json
from .database import Database

class Tweet:

    SPANISH = "es"
    ENGLISH = "en"

    def __init__(self, jsonData=None):
        self.processJson(jsonData)
        self.generateWords()

    def processJson(self, jsonData):
        self.jsonData = json.loads(jsonData)

        self.text = self.extractText()

        self.created_at = self.jsonData['created_at']
        self.user_id = self.jsonData['user']['id']
        self.lang = self.jsonData['lang']

    def extractText(self):
        text = ""
        if 'extended_tweet' in self.jsonData:
            text = self.jsonData['extended_tweet']['full_text']
        else:
            text = self.jsonData['text']

        return text

    def generateWords(self):
        tokens = [word for word in nltk.word_tokenize(self.text) if word.isalpha()]
        stopwords = nltk.corpus.stopwords.words("spanish")
        self.words = list(set(tokens) - set(stopwords))

    def getWords(self):
        return self.words

    def saveTweet(self):
        database = Database()
        database.insert(collection_name = "tweets", data=self.jsonData)

    def isSpanish(self):
        return self.lang == Tweet.SPANISH

    def isEnglish(self):
        return self.lang == Tweet.ENGLISH
