import json
import datetime as dt

today=str(dt.datetime.today().date())
# local_loc ="../../data/"
container_loc = "/home/worker/python_crawling/app/data/"
doc_id_list=["70101","70102","70106","70111","70112","70113","70114"]

datas = {}

for id in doc_id_list:
    json_name = f"{container_loc}_crawl_{id}_{today}.json"
    
    with open(json_name,'r') as f:
        crawld_json = json.load(f)
    datas[id] = crawld_json["items"]

result = {
    "metadata": "Crawling subjective questsions and answers from NAVER Jiskik In",
    "date" : today,
    "data" : datas
}

with open(f'{container_loc}subjective_questions_{today}.json', 'w', encoding='utf-8') as make_file:

    json.dump(result, make_file, indent="\t",ensure_ascii=False)
    
from hdfs import InsecureClient
client = InsecureClient('http://namenode:9870', user='worker')
