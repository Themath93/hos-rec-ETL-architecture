from jpype.types import *
import json
from konlpy.tag import Okt
import asyncio
import os
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from collections import Counter
class Transform:
    # 크롤링한 json 파일 불러오기
    with open("../../data/subjective_questions_2023-09-11.json","r") as f :
        json_file = json.load(f)
    # 불용어 리스트 불러오기
    with open("../../data/stopword.txt","r") as f:
        str_stopword= f.read().replace("\n"," ")
        
    docids=list(json_file['data'])
    empty_list = [[]]*len(docids)
    result_dict = dict(zip(docids,empty_list))
    okt = Okt()
    
    
    
    @classmethod
    def transform(self):
        os.system('echo "Transform is working"')
            # asnyc tasks
        tasks = [Transform.__okt_konlpy(self,id) for id in self.docids]

        loop = asyncio.get_event_loop()
        # 비동기 tasks ready
        cors = asyncio.wait(tasks)
        loop.run_until_complete(cors)
        loop.close()

        print(self.result_dict)
        # for id in docids:
        #     tmp_dict = {id:dict(Counter(result_dict[id]))}
    
    async def __okt_konlpy(self,docId=str):
        # 각과 데이터
        each_major_data = self.json_file['data'][docId]

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

Transform.transform()