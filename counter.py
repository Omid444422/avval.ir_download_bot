from glob import glob
from json import loads

files = glob('./data/*.json')
counter = 0
json_list = None

for file in files:
    with open(file,'r',encoding='utf-8') as json_file:
        json_list = loads(json_file.read())

        for json in json_list:
            counter += 1


print(counter)