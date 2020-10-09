from transformers import pipeline
from sentence_transformers import SentenceTransformer
import pickle
from bson.binary import Binary
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utils.preprocess_data_utils import split_txt_into_sentences
from database.db_connection import make_db_connection


embedding_model = SentenceTransformer('bert-base-nli-mean-tokens')

mongo_collection = make_db_connection()
number_docs = mongo_collection.count_documents({})

## bit of a hack to circumvent the 100 document batch size problem with mongodb
start_index = 0
for iteration in range(1+number_docs//99):
    cursor = mongo_collection.find({"abstract":{'$exists':True}},no_cursor_timeout=True)
    # iterate through each document in the collection, vectorize each sentence in its abstract, save the vectors
    for element in cursor[start_index:start_index+99]:
        start_index+=1
        abstract_txt = split_txt_into_sentences(element['abstract'])
        if "abstract_embeddings" not in element.keys():
            object_id = element["_id"]
            sentence_embeddings = embedding_model.encode(abstract_txt)
            mongo_collection.update_one({'_id':object_id},
                                    {'$set': {'abstract_embeddings': Binary(pickle.dumps(sentence_embeddings, protocol=2))}}
                                    )