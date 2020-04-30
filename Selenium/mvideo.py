from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pymongo import MongoClient
import time
import json

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)

driver.get('https://www.mvideo.ru/')

assert "М.Видео -" in driver.title

time.sleep(2)
driver.execute_script("window.scrollTo(0, 2500)")
time.sleep(2)

hits = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sel-hits-block')))[1]

data = []
while True:
    products = WebDriverWait(hits, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sel-product-tile-title')))

    for pr in products:
        dict_items = {}
        
        dict_items['link'] = pr.get_attribute('href')
        description = json.loads(pr.get_attribute('data-product-info'))
    
        dict_items['name'] = description['productName']
        description.pop('productName')

        dict_items['id'] = description['productId']
        description.pop('productId')

        dict_items['desr'] = description

        data.append(dict_items)

    button = hits.find_element_by_xpath(".//a[contains(@class, 'sel-hits-button-next')]")
    time.sleep(3)
    if 'disabled' in button.get_attribute('class'):
        break
    else:
        button.click()

client = MongoClient('localhost',27017)
db = client['MVideo']
db_letters = db.mvideo

for dat in data:
    if not db_letters.count_documents(dat):
        db_letters.insert_one(dat)