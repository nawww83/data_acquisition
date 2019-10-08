import time
from Crypto.Cipher import AES
from Crypto import Random
import base64

from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys

url =   'https://mail.tusur.ru/'

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

time.sleep(1)

mails = driver.find_elements_by_xpath('//tr[contains(@id, "rcmrow")]')
for mail in mails:
    print(mail.find_element_by_xpath('td[@class="subject"]/a').text.strip())

driver.quit()
