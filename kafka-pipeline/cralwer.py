import requests
from bs4 import BeautifulSoup
import datetime as dt
import time
import os,json
import producer


def crawler(dir_id,sleep_second=3600):
    page_url=f"https://kin.naver.com/qna/expertAnswerList.naver?dirId={dir_id}&page="
    i=1
    content_num_list=[]
    docids_loc = f"./each-save-point/id-{dir_id}"
    
    # print(last_point.readline())
    while True:
        last_point = open(docids_loc,'r')
        last_point = str(last_point.readline())
        res = requests.get(url=page_url+str(i))
        bs = BeautifulSoup(res.text, 'html.parser')
        trs = bs.find('tbody',{'id':'au_board_list'}).findAll("tr")
        for tr in trs:
            content_num = tr.find("a")['href'].split("&")[-1].split("=")[1]
            if content_num != last_point:
                content_num_list.append(content_num)
            else :
                i = 1
                # Data to Kafka Broker
                extract(dir_id=dir_id,content_num_list=content_num_list)
                #save_last_point
                save_last_point(content_num_list, docids_loc)
                print(f"Nothing to crawl This app going to sleep about {str(sleep_second)} seconds")
                time.sleep(sleep_second)
        time.sleep(1)
        i += 1

def save_last_point(content_num_list, docids_loc):
    last_point = open(docids_loc,'w')
    last_point.write(content_num_list[0])
    last_point.close()
        


def extract(dir_id,content_num_list):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
    base_url = "https://kin.naver.com"
    
    content_num_list

    for doc_id in content_num_list:

        url = f"{base_url}/qna/detail.naver?d1id=7&dirId={dir_id}&docId={doc_id}"
        try : 
            res = requests.get(url,headers=headers)
        except :
            print("Raised 429 Error")
            time.sleep(10)
            res = requests.get(url,headers=headers)
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
            "dirId": dir_id,
            "url": url,
            "title":title_text,
            "qus_content": qus_content,
            "answer":ans,
            "timestamp":str(time.time())
        }
        
        broker = ["localhost:19092","localhost:19093","localhost:19094"]
        topic = f"question-{dir_id}"
        producer.MessageProducer(broker=broker,topic=topic).send_message(tmp_json)

        # 너무 빠른 요청으로 인한 429 Error 로 타임슬립
        os.system(f'echo "STATUS_CODE : {res.status_code}"')
        time.sleep(2)
        
        
crawler("70101")