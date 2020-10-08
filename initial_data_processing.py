client = MongoClient('localhost', 27017)
db = client.db_world_bank
reports_coll = db["reports"]

coll_knowledge_notes = reports_coll.find({'collection':'Knowledge Notes'})

# from pdf metadata, download and store text
for element in coll_knowledge_notes[start_index:]:
    url = element["pdf_link"]
    object_id = element['_id']
    storage_dir = 'tempstorage'
    title = element["title"]
    if url:
        if 'full_text' not in element.keys():
            for attempt in range(5):
                try:
                    #download pdf
                    pdf_path = download_pdf(url,storage_dir,title)
                    #split pdf into iamges (one per page)
                    pdf_to_images(pdf_path,storage_dir,object_id,reports_coll)
                    #OCR to turn all images into text
                    master_text = images_to_text(storage_dir)
                    #upload text to mongodb
                    upload_text_to_mongodb(reports_coll,object_id,master_text)
                    #clean up temporary storage folder where images and pdf are stored
                    delete_temp_content(storage_dir)
                    time.sleep(60)
                    break
                except:
                    print('ERROR - trying again')
                    time.sleep(60)

# from text, count country mentions and store the information
coll_knowledge_notes = reports_coll.find({'collection':'Knowledge Notes','full_text': {'$exists':True}})                                         
for elem in coll_knowledge_notes[:1]:
    object_id = elem["_id"]
    txt = elem['full_text']
    txt = split_txt_into_sentences(txt)
    country_mentions = search_through_text(txt,list_search_terms)
    reports_coll.update_one({'_id':object_id},
                            {'$set': {'country_mentions': country_mentions}}
                            )

# from abstract, create vector and store it 
