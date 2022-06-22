import requests, datetime
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


area = ["001","005","009","013","017","021","025","029","033","037","041","045","049","053","057","061","065","069","073","077","081","085"]
information_list = []
for i in area:
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-{}?Authorization=CWB-40C73C51-9AF7-4B8B-A5BE-8635FB67523F&format=JSON'.format(i)
    data = requests.get(url).json()
    information_list.append(data)

cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

for y in information_list:
    doc_ref = db.collection(str(datetime.date.today())).document(y["records"]["locations"][0]["locationsName"])
    doc_ref.set({"地區":y["records"]["locations"][0]["location"]})
    for z in y["records"]["locations"][0]["location"]:
        try:
            doc_ref.update(({z["locationName"]:z["weatherElement"]}))
            print("新增成功")
        except:
            print("新增失敗")
                
        break
