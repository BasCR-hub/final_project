import scipy
import numpy as np
import pickle

def embed_query(embedding_model,query):
    return embedding_model.encode(query)

def find_high_cos_similarity(mongo_collection,embedded_query):
    all_vectors = mongo_collection.find(
                                        {'abstract_embeddings': {'$exists':True}},
                                        {"abstract_embeddings": 1},
                                        )
    ids_of_interest = []
    super_ids = []
    all_vectors_list = []
    for element in all_vectors:
        vector_set = pickle.loads(element["abstract_embeddings"])
        cossimil_abstract_query = [scipy.spatial.distance.cosine(embedded_query,vector) for vector in vector_set]
        if np.mean(cossimil_abstract_query) > 0.85 and max(cossimil_abstract_query)>.9:
            ids_of_interest.append(element['_id'])
            if np.mean(cossimil_abstract_query) > 0.92:
                super_ids.append(element['_id'])
    return ids_of_interest,super_ids

def extract_country_info(mongo_collection,lst_ids_of_interest):
    interesting_documents = mongo_collection.find({"_id":{'$in':lst_ids_of_interest}})
    dict_mentions = {}
    for elem in interesting_documents:
        if 'country_mentions' in elem.keys():
            for key,value in elem['country_mentions'].items():
                if key in dict_mentions.keys():
                    dict_mentions[key]+=value
                elif key not in dict_mentions.keys():
                    dict_mentions[key] = value

    lst_most_mentioned = sorted(dict_mentions, key=dict_mentions.get,reverse=True)
    dict_most_mentioned = {k: v for k, v in sorted(dict_mentions.items(), key=lambda item: item[1],reverse=True)}

    return lst_most_mentioned, dict_most_mentioned

def extract_document_info(mongo_collection,lst_super_ids):
    interesting_documents = mongo_collection.find({"_id":{'$in':lst_super_ids}})
    results_dict = {}
    for element in interesting_documents:
        results_dict[element["title"]] = {"abstract":element['abstract'],"url":element['pdf_link']}
    return results_dict
        
