import pymongo
from pymongo import MongoClient


class Mongo():
    def __init__(self, isOld = False):
        mongo_ip = '10.146.0.2'
        self.client = MongoClient('mongodb://{}:27017'.format(mongo_ip))
