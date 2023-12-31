import json
import requests
from bs4 import BeautifulSoup
import time
import datetime as dt
import os

class QuestionExtractor:

    today=str(dt.datetime.today().date())
    container_loc = "/home/worker/python_crawling/app/data/"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
    base_url = "https://kin.naver.com"
    docIds_file_loc = f"{container_loc}docIds_{today}.json"

    
    # crawl 된 dirID.json으로 crawling 진행
    @classmethod
    def extract(self,dirId=int):
        
        dirId = str(dirId)
        with open(self.docIds_file_loc,'r') as f:
            js_docIds = json.load(f)
        mj_docids = list(js_docIds[dirId].values())

        items = []
        for docid in mj_docids:

            url = f"{self.base_url}/qna/detail.naver?d1id=7&dirId={dirId}&docId={docid}"
            try : 
                res = requests.get(url,headers=self.headers)
            except :
                print("Raised 429 Error")
                time.sleep(10)
                res = requests.get(url,headers=self.headers)
            bs = BeautifulSoup(res.text, 'html.parser')

            # 지식인 제목
            bs_title=bs.title
            title_text = "deleted" if bs_title == None else bs_title.text.replace("\n","").replace("\t","")

            # 질문자 내용
            bs_qus_content = bs.find("div",{"class","c-heading__content"})
            qus_content = '' if bs_qus_content == None else bs_qus_content.text
            qus_content

            # 의사답변 내용
            bs_ans = bs.find("div",{"class":"se-module se-module-text"})
            ans = '' if bs_ans == None else bs_ans.text

            tmp_json = {
                "dirId": dirId,
                "url": url,
                "title":title_text,
                "qus_content": qus_content,
                "answer":ans
            }
            items.append(tmp_json)

            # 너무 빠른 요청으로 인한 429 Error 로 타임슬립
            os.system(f'echo "STATUS_CODE : {res.status_code}"')
            time.sleep(2)

        fin_data = {
        "description":"네이버 지식iN에서 건강상담중 7개 관련하여 전문가가 답변한 글만 크롤링",
        "crawling_date" : self.today,
        "items":items
        }
        
        with open(f'{self.container_loc}_crawl_{dirId}_{self.today}.json', 'w', encoding='utf-8') as make_file:

            json.dump(fin_data, make_file, indent="\t",ensure_ascii=False)

