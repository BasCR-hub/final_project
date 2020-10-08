from sentence_transformers import SentenceTransformer
import scipy
import numpy as np

model = SentenceTransformer('bert-base-nli-mean-tokens')
sentence_embeddings = model.encode(temp_txt)

query = "tax measures covid"
query_embedding = model.encode(query)

