from bson import ObjectId
from bson.binary import Binary
from transformers import pipeline
import re
import json
import scipy
import numpy as np
import pickle
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utils.preprocess_data_utils import split_txt_into_sentences,search_through_text
from database.db_connection import make_db_connection

with open('./initial_database_creation/country_name_variations.json') as json_file:
    dict_countries = json.load(json_file)
list_search_terms = [key.lower() for key in dict_countries.keys()]    

mongo_collection = make_db_connection()
number_docs = mongo_collection.count_documents({})

## bit of a hack to circumvent the 100 document batch size problem with mongodb
start_index = 0
for iteration in range(1+number_docs//99):
    cursor = mongo_collection.find({"full_text":{'$exists':True}},no_cursor_timeout=True)
    
    # iterate through each document's raw text, split it into sentences, extract number of country mentions inside the document
    for elem in cursor[start_index:start_index+99]:
        start_index += 1
        object_id = elem["_id"]
        txt = elem['full_text']
        txt = split_txt_into_sentences(txt)
        country_mentions = search_through_text(txt,list_search_terms,dict_countries)
        mongo_collection.update_one({'_id':object_id},
                                {'$set': {'country_mentions': country_mentions}}
                                )