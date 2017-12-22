from pymongo import MongoClient


def get_mongo_collection():
    client = MongoClient()
    db = client['twitter_tweet']
    collection = db['tweets']
    return collection