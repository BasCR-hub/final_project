import pymongo
from pymongo import MongoClient,ReturnDocument
from bson import ObjectId

def make_db_connection():
    client = MongoClient('localhost', 27017)
    db = client.db_world_bank
    reports_coll = db["reports"]
    return reports_coll

def return_query(mongo_collection,query_terms):
    mongo_collection.find()
    return 
