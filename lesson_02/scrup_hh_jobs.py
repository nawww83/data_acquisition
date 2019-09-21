import json as js
from bs4 import BeautifulSoup as bs
import requests as rq
import sys
from pprint import pprint as pp

'''
1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайта
 superjob.ru и hh.ru. Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы). 
 Получившийся список должен содержать в себе минимум:

    *Наименование вакансии
    *Предлагаемую зарплату (отдельно мин. и и отдельно макс.)
    *Ссылку на саму вакансию        
    *Сайт откуда собрана вакансия
'''

main_link_hh = 'https://tomsk.hh.ru'
main_link_superjob = 'https://www.superjob.ru'

user_agent = {'User-agent': 'Mozilla/5.0'}

lp = sys.argv
position = 'Водитель'
npages = 1
if len(lp) > 1:
    positon = lp[1]
elif len(lp) > 2:
    npages = lp[2]

html = rq.get(main_link_hh, headers = user_agent).text
parsed = bs(html, 'lxml')

items = parsed.find('div', {'xmlns:b':'http://hhru.github.com/bloko/', 'class':'bloko-columns-wrapper'}).findChildren(recursive = False)

for item in items:
    if item.findChild():
        pp(item['data-title'])
