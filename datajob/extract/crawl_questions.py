import json
import requests
from bs4 import BeautifulSoup
import time
import asyncio
import datetime as dt

today=str(dt.datetime.today().date())
local_loc ="../../data/"
container_loc = "/home/worker/python_crawling/app/data/"


docIds_file_loc = f"{container_loc}docIds_{today}.json"

# crawl 된 dirID.json으로 crawling 진행
def crawl_jisik(dirId=int):
    global items
    dirId = str(dirId)
    base_url = "https://kin.naver.com"
    header= "{'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}"

    with open(docIds_file_loc,'r') as f:
        js_docIds = json.load(f)
    mj_docids = list(js_docIds[dirId].values())

    contents_list=[]

    for docid in mj_docids:

        url = f"{base_url}/qna/detail.naver?d1id=7&dirId={dirId}&docId={docid}"
        res = requests.get(url)
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
        contents_list.append(tmp_json)

        # 너무 빠른 요청으로 인한 429 Error 로 타임슬립
        time.sleep(1)

    items += contents_list


async def call_crawl_func(dirId=int):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None,crawl_jisik,dirId)


async def run_crawl_func():
    await asyncio.gather(
        call_crawl_func(70101),
        call_crawl_func(70102),
        call_crawl_func(70106),
        call_crawl_func(70113),
        call_crawl_func(70111),
        call_crawl_func(70112),
        call_crawl_func(70114)
    )

items = []
asyncio.run(run_crawl_func())

fin_data = {
    "description":"네이버 지식iN에서 건강상담중 7개 관련하여 전문가가 답변한 글만 크롤링",
    "crawling_date" : today,
    "items":items
}


with open(f'{container_loc}crawling_data_{today}.json', 'w', encoding='utf-8') as make_file:

    json.dump(fin_data, make_file, indent="\t",ensure_ascii=False)
