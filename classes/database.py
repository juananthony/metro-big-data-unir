from pymongo import MongoClient
import os

class Database():

    MONGO_HOST = 'mongodb+srv://' + os.environ['MONGO_USER'] + ':' + os.environ['MONGO_PASS'] + '@' + os.environ['MONGO_SERVER'] + '/test?retryWrites=true'

    def __init__(self):
        # Creating MongoDB client connected to configured host by system properties
        self.client = MongoClient(Database.MONGO_HOST)
        # Use metrotwitterdb database. If it doesn't exist, it will be created.
        self.db = self.client.metrotwitterdb

    def insert(self, collection_name, data):
        return self.db[collection_name].insert(data)
