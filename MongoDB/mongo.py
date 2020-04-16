from pymongo import MongoClient
from hhandspj import search_sj, search_hh
from pprint import pprint

client = MongoClient('localhost',27017)
db = client['GUVacDB']
vacs = db.vacs

def update_db():
    keyword = "python"
    vac_list = search_sj(keyword) + search_hh(keyword)
    for vac in vac_list:
        if not vacs.count_documents(vac):
            vacs.insert_one(vac)
    print(vacs.count_documents({}))

def find_vac_with_sal_gt_then(gt):
    for vac in vacs.find({'sal_min': {'$gt': gt}}):
        pprint(vac)

    print(vacs.count_documents({'sal_min': {'$gt': gt}}))

gt = 100000
find_vac_with_sal_gt_then(gt)



