import pymongo
from pymongo import MongoClient,ReturnDocument
from bson import ObjectId
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import config

def make_db_connection(host=config.host,port=config.port,db_name=config.db_name,collection_name=config.collection_name):
    client = MongoClient(host, port)
    db = client[db_name]
    reports_coll = db[collection_name]
    return reports_coll

def return_query(mongo_collection,query_terms):
    mongo_collection.find()
    return 'hello'