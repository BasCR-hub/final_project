import pymongo
from pymongo import MongoClient,ReturnDocument
from bson import ObjectId
import requests
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path,pdfinfo_from_path
from pdf2image.exceptions import PDFSyntaxError,PDFPageCountError
import os
import glob
import time


def download_pdf(url,storage_dir,title):
    r = requests.get(url, allow_redirects=True)
    pdf_path = f"./{storage_dir}/{title}.pdf"
    open(f"./{storage_dir}/{title}.pdf", 'wb').write(r.content)
    return pdf_path
    
def pdf_to_images(pdf_path,storage_dir,object_id,mongodb_collection):
    info = pdfinfo_from_path(pdf_path)
    maxPages = info["Pages"]
    mongodb_collection.update_one({'_id':object_id},
                                {"$set": {"numb_pages": maxPages}},
                                )    
    image_counter = 0
    for page in range(1, maxPages+1, 10): 
        pages = convert_from_path(pdf_path, dpi=200, first_page=page, last_page = min(page+10-1,maxPages))
        
        for individual_page in pages:
            filename = f"./{storage_dir}/page_{image_counter}.jpg"
            individual_page.save(filename, 'JPEG')
            image_counter += 1

def images_to_text(storage_dir):
    allfiles = os.listdir(storage_dir)
    images = [filename for filename in allfiles if filename.endswith('.jpg')]
    
    master_text = ''
    for img_number in range(0,len(images)): 
        filename = f"./{storage_dir}/page_{img_number}.jpg"
        master_text += pytesseract.image_to_string(Image.open(filename))
        
    return master_text

def upload_text_to_mongodb(mongodb_collection,object_id,master_text):
    mongodb_collection.update_one({'_id':object_id},
                                {'$set': {'full_text': master_text}},
                                )
def delete_temp_content(storage_dir):
    files = glob.glob(f'./{storage_dir}/*')
    for f in files:
        os.remove(f)

def search_through_text(txt,list_search_terms):
    dict_occurrences= {}
    for sentence in txt:
        for country_name in list_search_terms:
            if country_name in sentence:
                if country_name in dict_occurrences:
                    dict_occurrences[dict_countries[country_name]] += 1
                elif country_name not in dict_occurrences:
                    dict_occurrences[dict_countries[country_name]] = 1        
    return dict_occurrences

def split_txt_into_sentences(txt):
    temp_txt = txt.replace('-\n','').replace('\n',' ').lower()
    return sent_tokenize(temp_txt)
