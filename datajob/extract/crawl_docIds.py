import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import asyncio
import datetime as dt

async def get_docid(major_code=str,num=int):
    global tmp_list
    page_url = "https://kin.naver.com" + "/qna/expertAnswerList.naver?dirId=" + major_code +"&page="
    loop = asyncio.get_event_loop()
    res = await loop.run_in_executor(None,requests.get, page_url+str(num))
    bs = BeautifulSoup(res.text, 'html.parser')
    trs = bs.find('tbody',{'id':'au_board_list'}).findAll("tr")
    tmp_list.append(list(map(lambda e:e.find("a")['href'].split("&")[-1].split("=")[1] ,trs)))
    time.sleep(0.3)

async def get_list_doc_ids(major_code=str):
    await asyncio.gather(
        get_docid(major_code,1),
        get_docid(major_code,2),
        get_docid(major_code,3),
        get_docid(major_code,4),
        get_docid(major_code,5),
        get_docid(major_code,6),
        get_docid(major_code,7),
        get_docid(major_code,8),
        get_docid(major_code,9),
        get_docid(major_code,10)
    )

local_loc ="../../data/"
container_loc = "/home/worker/python_crawling/app/data/"

today=str(dt.datetime.today().date())
# 각 과별로 url df 만들기.
df = pd.read_csv(container_loc+"major_list.csv",encoding="utf-8",index_col=0)
mj_codes=list(map(str,list(df['0'])))
tmp_list = []
for code in mj_codes:
    asyncio.run(get_list_doc_ids(code))
    
res_json = dict()
for i in range(0,7):
    res_json[mj_codes[i]] = sum(tmp_list[i*10:(i+1)*10],[])
df_json = pd.DataFrame(res_json)
df_json.to_json(f"{container_loc}docIds_{today}.json")