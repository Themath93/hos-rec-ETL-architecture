# Import module
import jpype
# Enable Java imports
import jpype.imports
# Pull in types
from jpype.types import *
# Launch the JVM
# jpype.startJVM()
import json
from konlpy.tag import Kkma

with open("../../data/subjective_questions_2023-09-11.json","r") as f :
    json_file = json.load(f)

docids=list(json_file['data'])
doc_70101 = json_file['data'][docids[0]]
sample = doc_70101[0]['answer']




kkma = Kkma()
print(kkma.nouns(sample))


jpype.shutdownJVM()