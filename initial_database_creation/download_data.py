import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import glob
from utils.download_data_utils import delete_temp_content, upload_text_to_mongodb, images_to_text, pdf_to_images,download_pdf
import time
from database.db_connection import make_db_connection

mongo_collection = make_db_connection()
number_docs = mongo_collection.count_documents({})

## bit of a hack to circumvent the 100 document batch size problem with mongodb
start_index = 0
for iteration in range(1+number_docs//99):
    cursor = mongo_collection.find({},no_cursor_timeout=True)

    # iterate through each document in the collection, download the pdf, scan it and store the raw text in mongodb
    for element in cursor[start_index:start_index+99]:
        url = element["pdf_link"]
        object_id = element['_id']
        storage_dir = 'initial_database_creation/temp_storage'
        title = element["title"]
        start_index+=1
        print(start_index)
        if url:
            if 'full_text' not in element.keys():
                for attempt in range(5):
                    try:
                        #download pdf
                        pdf_path = download_pdf(url,storage_dir,title)
                        #split pdf into images (one per page)
                        pdf_to_images(pdf_path,storage_dir,object_id,mongo_collection)
                        #OCR to turn all images into text
                        master_text = images_to_text(storage_dir)
                        #upload text to mongodb
                        upload_text_to_mongodb(mongo_collection,object_id,master_text)
                        #clean up temporary storage folder where images and pdf are stored
                        delete_temp_content(storage_dir)
                        time.sleep(60)
                        break
                    except Exception as e:
                        print(e)
                        time.sleep(60)