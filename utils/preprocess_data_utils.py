from nltk import sent_tokenize 
import nltk 
nltk.download('punkt')

def search_through_text(txt,list_search_terms,reference_dict):
    dict_occurrences= {}
    for sentence in txt:
        for country_name in list_search_terms:
            if country_name in sentence:
                if country_name in dict_occurrences:
                    dict_occurrences[reference_dict[country_name]] += 1
                elif country_name not in dict_occurrences:
                    dict_occurrences[reference_dict[country_name]] = 1        
    return dict_occurrences

def split_txt_into_sentences(txt):
    temp_txt = txt.replace('-\n','').replace('\n',' ').lower()
    return sent_tokenize(temp_txt)