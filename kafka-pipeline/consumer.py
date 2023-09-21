import get_kafka
import json
import asyncio
from konlpy.tag import Okt

broker = ["kafka1:9092","kafka2:9092","kafka3:9092"]

def process_data(docId):
    okt= Okt()
    # 불용어 리스트 불러오기
    data_path = "/home/worker/volume/kakfa_python/"
    with open(f"{data_path}stopword.txt","r") as f:
        str_stopword= f.read().replace("\n"," ")
    
    consumer = get_kafka.Consumer(broker,f'question-{docId}',"question_consumer").consumer
    
    while True:
        for msg in consumer:
            msg_dict = json.loads(msg.value)
            print(msg_dict)
    
            # 텍스트 어절 추출
            filter_list = [ "Noun", "Adjective", "Verb" ]
            # 질문 항목만 추출
            
            pos_str = okt.pos(msg_dict['qus_content'])
            pos_str = list(filter(lambda e: e[1] in filter_list,pos_str))
            pos_list = list(map(lambda e: e[0],pos_str))
            result = []
            
            # 특정 어미 제거 리스트
            specific_word = ["고요", "니다", "세요", "네요", "어요", "까요", "니고" ,"는데" , "케", "지고", "나요", "구요"]
            
            # 불용어 제거 및 특정 어미로 끝나는 말 제거
            for pos in pos_list:
                if pos not in str_stopword:
                    result.append(pos)
                    if len(result[-1]) >= 3 :
                        for word in specific_word:
                            if word in pos: result.pop()
            
            # 결과물 result_dict 에 저장
            fin = list(set(result))
            print(fin)

process_data("70101")