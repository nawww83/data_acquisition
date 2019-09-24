import sys
import requests as rq
from bs4 import BeautifulSoup as bs
import json as js
from pprint import pprint as pp
import math
import re
import pandas as pd
from collections import OrderedDict as od

'''
1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайта
 superjob.ru и hh.ru. Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы). 
 Получившийся список должен содержать в себе минимум:

    *Наименование вакансии
    *Предлагаемую зарплату (отдельно мин. и и отдельно макс.)
    *Ссылку на саму вакансию        
    *Сайт откуда собрана вакансия
'''

def separate_salaries(s): # Разделяет зарплату на "от и до"
    _tt_min = ''
    _tt_max = ''
    _ttl = s.split('-')
    if len(_ttl) == 1:
        if _ttl[0].find('от') > -1:
            _tt_min = re.sub('\D', '',  _ttl[0])
        if _ttl[0].find('до') > -1:
            _tt_max = re.sub('\D', '',  _ttl[0])
    if len(_ttl) == 2:
        _tt_min = re.sub('\D', '',  _ttl[0])
        _tt_max = re.sub('\D', '',  _ttl[1])
    return [_tt_min, _tt_max]

main_link_hh = 'https://tomsk.hh.ru'
main_link_superjob = 'https://www.superjob.ru'
user_agent = {'User-agent': 'Mozilla/5.0'}
method = '/search/vacancy?L_is_autosearch=false&area=90&clusters=true&enable_snippets=true&no_magic=true&text='


lp = sys.argv
position = 'Водитель' # позиция по умолчанию
npages = math.inf     # по умолчанию обрабатывать все страницы
if len(lp) > 1:
    position = lp[1]
if len(lp) > 2:
    npages = int(lp[2])

html = rq.get(main_link_hh, headers = user_agent).text
parsed = bs(html, 'lxml')

query = {'xmlns:b':'http://hhru.github.com/bloko/', 'class':'bloko-columns-wrapper'}
items = parsed.find('div', query).findChildren(recursive = False)

pos_finded = False
pos_id = []
for item in items: # ищем требуемую позицию среди всех позиций (по самому верху иерархии)
    if item.findChild():
        if item['data-title'] == position:
            pos_id = item['data-id']
            pos_finded = True

if pos_finded:
    pp('Профессия ' + position.lower() + ' найдена! Ее идентификатор ' + pos_id)
else:
    pp('Профессия ' + position.lower() + ' не найдена!')

pp('')

page = 0
query = {'class':'vacancy-serp'}
data = []
while page < npages: # перебираем все страницы по найденной позиции; для этого используем линк строки поиска сайта
    html = rq.get(main_link_hh + method + position + '&page=' + str(page), headers = user_agent).text
    if html:
        parsed = bs(html, 'lxml')
        items = parsed.find('div', query).findChildren()
        out_of_range = parsed.find('div', {'data-qa':'pager-block'}).findChildren()
        b_out = True # если Истина, то эта страница последняя и в конце цикла будет выход
        for out in out_of_range:
            if out.get('data-qa') == 'pager-next':
                b_out = False
                break
        tmp = od()
        _filled = 0
        for item in items:
            if item.get('data-qa') == 'vacancy-serp__vacancy-title':
                _tt = item.getText().strip()
                if _tt:
                    tmp['title'] = _tt
                    _filled += 1
            if item.get('data-qa') == 'vacancy-serp__vacancy-employer':
                _tt = item.getText().strip()
                if _tt:
                    tmp['employeer'] = _tt
                    _filled += 1
            if item.get('data-qa') == 'vacancy-serp__vacancy-compensation':
                _tt = item.getText().strip().replace('\xa0', '')
                if _tt:
                    _tt_salar = separate_salaries(_tt)
                    tmp['compensation_min'] = int(_tt_salar[0]) if _tt_salar[0] else None
                    tmp['compensation_max'] = int(_tt_salar[1]) if _tt_salar[1] else None
                    _filled += 1
            if item.get('data-qa') == 'vacancy-serp__vacancy-address':
                _tt = item.getText().strip()
                if _tt:
                    tmp['address'] = _tt
                    _filled += 1
            if item.get('class') == ['g-user-content']:
                if item.findChildren()[0].get('href'):
                    tmp['link'] = item.findChildren()[0].get('href')
                    _filled += 1
            if _filled == 5:
                data.append(tmp)
                _filled = 0
                tmp = od()
        page += 1
        pp(page)
        if b_out:
            break
# pp(data)
df = pd.DataFrame(data)
pp(df)

pp('Обработано ' + str(page) + ' страниц')

with open('hh.json', 'w') as f:
    js.dump(data, f)

