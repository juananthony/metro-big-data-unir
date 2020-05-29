from pymongo import MongoClient
import os
import sys
sys.path.append("..")
import config
import logging

logger = logging.getLogger(__name__)

class Database():

    MONGO_HOST = 'mongodb+srv://' + config.MONGO_USER + ':' + config.MONGO_PASS + '@' + config.MONGO_SERVER + '/test?retryWrites=true'

    def __init__(self):
        # Creating MongoDB client connected to configured host by system properties
        self.client = MongoClient(Database.MONGO_HOST)
        # Use metrotwitterdb database. If it doesn't exist, it will be created.
        self.db = self.client.metrotwitterdb

    def insert(self, collection_name, data):
        logger.info('Insert document into <' + collection_name + '>')
        return self.db[collection_name].insert(data)
