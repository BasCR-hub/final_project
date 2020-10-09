from selenium.common.exceptions import NoSuchElementException

def get_all_elements_on_page(driver):
    try:
        title = driver.find_element_by_xpath("//*[@class='ds-div-head']").text
    except NoSuchElementException:
        title = ''
        pass
    try:
        abstract = driver.find_element_by_xpath("//*[@class='okr-item-page-field-wrapper abstract']").text
    except NoSuchElementException:
        abstract = ''
        pass
    try:   
        abstract_views = driver.find_element_by_xpath("//*[@class='item-stat abstract-views']").text.split("\n")[1]
    except NoSuchElementException:
        abstract_views = ''
        pass
    try:
        file_downloads = driver.find_element_by_xpath("//*[@class='item-stat file-downloads']").text.split("\n")[1]
    except NoSuchElementException:
        file_downloads = ''
        pass
    try:
        published_date = driver.find_element_by_xpath("//*[@class='simple-item-view-other word-break']").text
    except NoSuchElementException:
        published_date = ''
        pass
    try:
        pdf_link = driver.find_element_by_xpath("//*[@class='bitstream-link']").get_attribute('href')
    except NoSuchElementException:
        pdf_link = ''
        pass
    
    dict_document = {'title':title,'abstract':abstract,'abstract_views':abstract_views,
                     'file_downloads':file_downloads, 'published_date' : published_date, 'pdf_link':pdf_link,
                     'collection':''}
    return dict_document
