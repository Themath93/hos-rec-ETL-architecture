from jpype.types import *
import json
from konlpy.tag import Okt
import asyncio
import os
import datetime as dt
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk
from hdfs import InsecureClient
import time
import requests

class QuestionTransformer:
    
    today=str(dt.datetime.today().date())
    hdfs_path = "/data/naver_crawl/"
    data_path = "/home/worker/python_crawling/app/data/"
    
    

    hdfs_client = InsecureClient('http://namenode:9870', user='worker')
    # # 크롤링한 json 파일 불러오기

    # 불용어 리스트 불러오기
    with open(f"{data_path}stopword.txt","r") as f:
        str_stopword= f.read().replace("\n"," ")
    

    try:
        yesterday = dt.date.today() - dt.timedelta(days=1)
        yesterday = str(yesterday.date())
        with hdfs_client.read(f"{hdfs_path}subjective_questions_{yesterday}.json") as f :
            docids = list(json.load(f)['data'])
    except: docids=['70101', '70102', '70106', '70113', '70111', '70112', '70114']
    empty_list = [[]]*len(docids)
    result_dict = dict(zip(docids,empty_list))
    okt = Okt()
    
    
    
    @classmethod
    def transform(self):
        os.system('echo "QuestionTransformer is working"')
        # asnyc tasks
        self.__async_transforming()
        # Bulk API To OpenSearch Data 전처리
        bulk_data = self.__create_Bulk_API_data()
        # 
        QuestionTransformer.__to_opensearch(self,bulk_data)

    @classmethod
    def __create_Bulk_API_data(self):
        tmp_json=json.dumps(self.result_dict,ensure_ascii=False)
        docids = ['70101', '70102', '70106', '70111', '70112', '70113', '70114']
        dict_json = json.loads(tmp_json)
        index_name = "alias1"
        index_dict = { "index" : { "_index" : index_name } }
        index_json = json.dumps(index_dict,ensure_ascii=False)
        result = []
        for id in docids:
            tmp_dict = json.dumps({"major":id,"words":dict_json[id]},ensure_ascii=False)
            result.append(index_json)
            result.append(tmp_dict)
        
        bulk_data = " \n ".join(result)
        return bulk_data

    @classmethod
    def __async_transforming(self):
        tasks = [QuestionTransformer.__okt_konlpy(self,id) for id in self.docids]

        loop = asyncio.get_event_loop()
        # 비동기 tasks ready
        cors = asyncio.wait(tasks)
        loop.run_until_complete(cors)
        loop.close()
    

    def __to_opensearch(self,bulk_data=str):
        
        ## Bulk API 적재전 Rollover API 전송
        QuestionTransformer.__rollover_index(self)
        
        hosts=[{"host":"osingest","port":9200}]
        os_client = OpenSearch(hosts=hosts)
        os_client.bulk(bulk_data)

    def __rollover_index(self):
        
        # POST API CURL TO OPENSEARCH
        res_json = self.__execute_rollover_API()
        
        # bool
        is_rollover = res_json["acknowledged"]
        
        # rollover 된경우 index 생성시간을 기다려준다.
        self.__waiting_until_new_index_created(res_json, is_rollover)

    def __waiting_until_new_index_created(self, res_json, is_rollover):
        if is_rollover : 
            os.system(f'echo "alias1 is rollovered \n New index name : {res_json["new_index"]}" \n Waiting New index')
            for i in range(1,20):
                os.system(f"echo {str(i)}")
                time.sleep(1)

    def __execute_rollover_API(self):
        headers = {
            "Content-Type": "application/json",
        }

        params = {
            "pretty": "true",
        }

        data = '{\"conditions\":{\"max_age\":\"1d\",\"max_docs\":7}}'

        res = requests.post('http://osingest:9200/alias1/_rollover', params=params, headers=headers, data=data)
        res_json = json.loads(res.text.replace("\n",""))
        return res_json
    
    async def __okt_konlpy(self,docId=str):
        with self.hdfs_client.read(f"{self.hdfs_path}subjective_questions_{self.today}.json") as f :
            json_file = json.load(f)
        # 각과 데이터
        each_major_data = json_file['data'][docId]

        # 텍스트 어절 추출
        filter_list = [ "Noun", "Adjective", "Verb" ]
        # 질문 항목만 추출
        pos_list = list(map(lambda e: self.okt.pos(e['qus_content']),each_major_data))
        pos_list = list(filter(lambda e: e[1] in filter_list,pos_list[1]))
        pos_list = list(map(lambda e: e[0],pos_list))
        result = []
        
        # 특정 어미 제거 리스트
        specific_word = ["고요", "니다", "세요", "네요", "어요", "까요", "니고" ,"는데" , "케", "지고", "나요", "구요"]
        
        # 불용어 제거 및 특정 어미로 끝나는 말 제거
        for pos in pos_list:
            await asyncio.sleep(0.1)
            if pos not in self.str_stopword:
                result.append(pos)
                if len(result[-1]) >= 3 :
                    for word in specific_word:
                        if word in pos: result.pop()
        
        # 결과물 result_dict 에 저장
        self.result_dict[docId] = self.result_dict[docId] + list(set(result))