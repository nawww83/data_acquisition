import time
from Crypto.Cipher import AES
from Crypto import Random
import base64

from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pymongo import MongoClient
from collections import OrderedDict as od

def get_mails(mails):
    items = []
    for mail in mails:
        item = od()
        fromTo = mail.find_element_by_xpath('td[@class = "fromto"]').text.strip()
        item['От кого'] = fromTo
        date = mail.find_element_by_xpath('td[@class = "date"]').text.strip()
        item['Дата'] = date
        sba = mail.find_element_by_xpath('td[@class = "subject"]/a')
        subject = sba.text.strip()
        item['Тема'] = subject
        href = sba.get_attribute('href').strip()
        item['href'] = href
        items.append(item)
    return items


client = MongoClient('localhost', 27017)
db = client['mails']
collection = db['tusur']

url = 'https://mail.tusur.ru/'

options = wd.ChromeOptions()
#options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
driver_path = '/usr/lib/chromium-browser/libs/chromedriver'

driver = wd.Chrome(chrome_options = options, executable_path = driver_path) 

driver.get(url)

title = 'TUSUR Webmail :: Добро пожаловать в TUSUR Webmail!'
assert title in driver.title

login = driver.find_element_by_id('rcmloginuser')
login.send_keys('anatolii.v.novikov@tusur.ru')

with open('key.txt', 'rb') as f:
    key = f.read()
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)

with open('pass.txt', 'rb') as f:
    enc = f.read()
    decoded = cipher.decrypt(base64.b64decode(enc))
    passwd = decoded[-12:].decode('utf-8')
    pwd = driver.find_element_by_id('rcmloginpwd')
    pwd.send_keys(passwd)
    pwd.send_keys(Keys.RETURN)

title = 'TUSUR Webmail :: Входящие'
assert title in driver.title

items = []

wait = WebDriverWait(driver, 5) 
mails = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//tr[contains(@id, "rcmrow")]')))
mails_count = len(mails)
items.extend(get_mails(mails))
pages = 1 if mails_count > 0 else 0
if pages > 0:
    print('Обработана страница номер ' + str(pages))
while True:
    try:
        button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="button nextpage"]')))
        button.click()
        mails = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//tr[contains(@id, "rcmrow")]')))
        items.extend(get_mails(mails))
        cnt = len(mails)
        mails_count += cnt
        pages = (pages + 1) if cnt > 0 else pages
        print('Обработана страница номер ' + str(pages))
    except:
        print('Обработка закончена')
        break

print('Обработано ' + str(pages) + ' страниц и ' + str(mails_count) + ' ссылок на письма')

print('Получение текста писем и запись всего в базу данных MongoDB')
docs = 0
for item in items:
    print('Получаем из ' + item['href'])
    driver.get(item['href'])
    msg = driver.find_element_by_id('messagebody').text.strip()
    _ii = item
    _ii.pop('href')
    _ii['Сообщение'] = msg
    try:
        collection.insert_one(_ii)
        docs += 1
    except:
        pass

print('Работа закончена')
print('В базу вставлено ' + str(docs) + ' документов')
driver.quit()

