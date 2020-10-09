from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re
import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from database.db_connection import make_db_connection
from utils.scrape_utils import get_all_elements_on_page

mongo_collection = make_db_connection()

start_urls_list = {
    'Journals' : 'https://openknowledge.worldbank.org/handle/10986/2210/discover?filtertype=supportedlanguage&filter_relational_operator=equals&filter=en',
    'Serial Publications': 'https://openknowledge.worldbank.org/handle/10986/11863/discover?filtertype=supportedlanguage&filter_relational_operator=equals&filter=en',
    'Technical Papers':'https://openknowledge.worldbank.org/handle/10986/18022/discover?filtertype=supportedlanguage&filter_relational_operator=equals&filter=en',
    'Economic and Sector Work':'https://openknowledge.worldbank.org/handle/10986/6/discover?filtertype=supportedlanguage&filter_relational_operator=equals&filter=en',
    'Working papers':'https://openknowledge.worldbank.org/handle/10986/8/discover?rpp=10&etal=0&group_by=none&page=1&filtertype_0=supportedlanguage&filter_relational_operator_0=equals&filter_0=en',
    'Knowledge Notes':'https://openknowledge.worldbank.org/handle/10986/9387/discover?filtertype=supportedlanguage&filter_relational_operator=equals&filter=en'
}

options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)

# start scraping from each document category's home url
for doc_category in start_urls_list.keys():
    driver.get(start_urls_list[doc_category])
    time.sleep(3)

    ## Find number pages in collection
    last_page_link = driver.find_element_by_xpath("//*[@class='last-page-link']")
    child_element_split_url = last_page_link.find_elements_by_xpath(".//*")[0].get_attribute('href').split('&')
    for element in child_element_split_url:
        if 'page' in element:
            total_pages_numb = int(element.split("=")[1])
    
    #iterate through all pages
    n=0
    for results_page in range(total_pages_numb-1):
        n+=1
        button_next_page = driver.find_element_by_xpath("//*[@class='next-page-link']").get_attribute('href')
        # get list of all links to document information
        items_on_page = driver.find_elements_by_xpath("//*[@class='item-wrapper']")
        root_url = 'https://openknowledge.worldbank.org/'
        lst_links_documents = [root_url + element.get_attribute('data-href') for element in items_on_page]

        #iterate through each document information page, collect data and upload it to mongodb 
        for document_link in lst_links_documents:
            driver.get(document_link)
            time.sleep(3)
            dict_infos = get_all_elements_on_page(driver)
            dict_infos['collection'] = doc_category
            mongo_collection.insert_one(dict_infos)

        # move to next page
        driver.get(button_next_page)
        time.sleep(3)