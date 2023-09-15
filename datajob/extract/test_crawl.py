import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import asyncio
import datetime as dt
import os

class DocIdExtractor:
    container_loc = "/home/worker/python_crawling/app/data/"
    df = pd.read_csv(f"{container_loc}major_list.csv",encoding="utf-8",index_col=0)
    mj_codes=list(map(str,list(df['0'])))
    res_json = dict(zip(mj_codes,[[]]*len(mj_codes)))
    today=str(dt.datetime.today().date())
    def __init__(self):
        print("""
              네이버 지식인에서 건강관련 질문 크롤링에 필요한 각 게시판의 고유번호를 크롤링해온다. 
              page_num는 crawling 하고 싶은 page 의 개수이며 1 개의 page 당 20개의 게시물을 크롤링할 수 있다.
              """)

    @classmethod
    def extract(self,page_num=10):
        os.system('echo "DocId extract begin"')
        
        loop = asyncio.get_event_loop()
        for id in self.mj_codes:
            tasks = DocIdExtractor.get_tasks(page_num,id)
            cors = asyncio.wait(tasks)
            loop.run_until_complete(cors)
        loop.close()

        df_json = pd.DataFrame(DocIdExtractor.res_json)
        df_json.to_json(f"{self.container_loc}docIds_{self.today}.json")

    @classmethod
    def get_tasks(self,page_num,major_code):
        tasks = [DocIdExtractor.get_docid(None,major_code,i) for i in range(1,page_num + 1)]
        return tasks
        

    
    async def get_docid(self,major_code,num):
        tmp_list=[]
        page_url = "https://kin.naver.com" + "/qna/expertAnswerList.naver?dirId=" + major_code +"&page="
        loop= asyncio.get_event_loop()
        res = await loop.run_in_executor(None,requests.get, page_url+str(num))
        bs = BeautifulSoup(res.text, 'html.parser')
        trs = bs.find('tbody',{'id':'au_board_list'}).findAll("tr")
        tmp_list.append(list(map(lambda e:e.find("a")['href'].split("&")[-1].split("=")[1] ,trs)))
        time.sleep(1)
    
        DocIdExtractor.res_json[major_code] = DocIdExtractor.res_json[major_code] + sum(tmp_list,[])
