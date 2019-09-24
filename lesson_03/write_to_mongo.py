'''
1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД
2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы
'''

from pymongo import MongoClient
from pprint import pprint as pp
import json as js

# выводит вакансии с минимальной зарплатой выше min_salary
def show_vac_gt(min_salary, coll):
    ob = coll.find({'compensation_min':{'$gt':min_salary}})
    for o in ob:
        pp(o)

client = MongoClient('localhost', 27017)
db = client['vacancies']

with open('../lesson_02/hh.json') as f:
    data = js.load(f)

db.hh.drop()

hh = db.hh

hh.insert_many(data)

#ob = hh.find({})
#for o in ob:
#    pp(o)

show_vac_gt(70000, hh)

