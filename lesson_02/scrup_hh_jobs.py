import sys
import requests as rq
from bs4 import BeautifulSoup as bs
import json as js
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
method = '/search/vacancy?L_is_autosearch=false&area=90&clusters=true&enable_snippets=true&no_magic=true&text='


lp = sys.argv
position = 'Водитель'
npages = 1
if len(lp) > 1:
    position = lp[1]
if len(lp) > 2:
    npages = lp[2]

html = rq.get(main_link_hh, headers = user_agent).text
parsed = bs(html, 'lxml')

query = {'xmlns:b':'http://hhru.github.com/bloko/', 'class':'bloko-columns-wrapper'}
items = parsed.find('div', query).findChildren(recursive = False)

pos_finded = False
pos_id = []
for item in items:
    if item.findChild():
        if item['data-title'] == position:
            pos_id = item['data-id']
            pos_finded = True

if pos_finded:
    pp('Профессия ' + position.lower() + ' найдена! Ее идентификатор ' + pos_id)
else:
    pp('Профессия ' + position.lower() + ' не найдена!')

page = 0
query = {'class':'vacancy-serp'}
while page < npages:
    html = rq.get(main_link_hh + method + position + '&page=' + str(page), headers = user_agent).text
    if html:
        parsed = bs(html, 'lxml')
        items = parsed.find('div', query).findChildren()
        data_pos = 0
        for item in items:
            if item.get('class') == ['g-user-content']:
                a = item.findChild()
                if a:                
                    pp(a.getText())
                    data_pos += 1
        page += 1
    else:
        break

pp('Все закончилось!')

