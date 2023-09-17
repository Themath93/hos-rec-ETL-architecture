import os
import sys

from datajob.extract.crawl_docIds import DocIdExtractor
from datajob.extract.crawl_questions import QuestionExtractor
from datajob.transform.transform import QuestionTransformer
from datajob.extract import reducer

def test() :
    print("called")

def main():
    """ Main entry point of the app """
    works = {
        "extract":{
            "doc_ids": DocIdExtractor.extract,
            "quetions": QuestionExtractor.extract,
            "reducer": reducer.reducer
        },
        "transform":{
            "questions":QuestionTransformer.transform
        }
        
    }

    return works
works = main()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    args = sys.argv
    
    if args[1] not in works.keys() :
        raise Exception("첫번째 전달인자가 이상함 >> " +str(works.keys()))
    if args[2] not in works[args[1]].keys() :
        raise Exception("두번째 전달인자가 이상함 >> " +str(works[args[1]].keys()))
    
    print(len(args))
    
    if len(args) == 3 :
        work = works[args[1]][args[2]]
        work()
    else :
        work = works[args[1]][args[2]]
        work(int(args[3]))