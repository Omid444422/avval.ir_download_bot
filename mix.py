from glob import glob
from json import loads,dumps

files = glob('./data/*.json')
counter = 0
json_list = list()

for file in files:
    with open(file,'r',encoding='utf-8') as json_file:
        json_list.append(loads(json_file.read()))

files_content_json = dumps(json_list,ensure_ascii=False)

total_file = open('all.json','w',encoding='utf-8')
total_file.write(files_content_json)
total_file.close()



