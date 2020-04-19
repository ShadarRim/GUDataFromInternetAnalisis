from pymongo import MongoClient
from xpath import req_to_mail, req_to_yandex, req_to_lenta
from pprint import pprint

client = MongoClient('localhost',27017)
db = client['GUNewsDB']
vacs = db.vacs

def update_db():
    vac_list = req_to_lenta() + req_to_yandex() + req_to_mail()
    for vac in vac_list:
        if not vacs.count_documents(vac):
            vacs.insert_one(vac)
    print(vacs.count_documents({}))

update_db()




