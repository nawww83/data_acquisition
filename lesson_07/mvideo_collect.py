from selenium import webdriver as wd

from pymongo import MongoClient
from collections import OrderedDict as od

import json 

client = MongoClient('localhost', 27017)
db = client['electronics']
collection = db['mvideo']

url = 'https://www.mvideo.ru'

options = wd.ChromeOptions()
#options.add_argument('--ignore-certificate-errors')
#options.add_argument('--headless')
options.add_argument('--start-maximized')
driver_path = '/usr/lib/chromium-browser/libs/chromedriver'

driver = wd.Chrome(chrome_options = options, executable_path = driver_path) 

driver.get(url)

title = 'М.Видео - интернет-магазин цифровой и бытовой техники и электроники, низкие цены, большой каталог, отзывы'
assert title in driver.title

script = driver.find_element_by_xpath('//div[@data-init="gtm-push-products"]/script').get_attribute('innerHTML')
index = script.find('[')
if index > -1:
    script = script[index:]
index = script.find(']')
if index > -1:
    script = script[:index+1]
data = json.loads(script)
#print(data)

collection.insert_many(data)

driver.quit()
