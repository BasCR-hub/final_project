import streamlit as st
from search import embed_query,find_high_cos_similarity,extract_country_info,extract_document_info
from database.db_connection import make_db_connection
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('bert-base-nli-mean-tokens')
mongocollection = make_db_connection()

st.title('Which country is the best at what')

query = st.text_input("what are you interested in ?")
if query:
    embedded_query = embed_query(embedding_model,query)
    lst_ids_of_interest,lst_super_ids = find_high_cos_similarity(mongocollection,embedded_query)
    lst_most_mentioned, dict_most_mentioned = extract_country_info(mongocollection,lst_ids_of_interest)
    st.write("Very interesting topic indeed !  Check out what the following countries have done:")
    for country in lst_most_mentioned[:5]:
        st.write(country.capitalize())
    
    super_documents = extract_document_info(mongocollection,lst_super_ids)
    st.write(' ')
    st.write('In particular, the following documents might be of interest to you')
    st.write(super_documents)



        