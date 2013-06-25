import os
import io
BASE_PATH = "I:\\WebCrawer\\"
keyword = "郑江滨"

file2url = dict();
relation_file = open(BASE_PATH + 'relation.conf', 'r')
pairs = relation_file.read().split('\n')
relation_file.close()
for pair in pairs:
    if(len(pair)!=0):
        pair_split = pair.split('\t')
        file2url[pair_split[0]]=pair_split[1]

files = os.listdir(BASE_PATH)
files.remove('relation.conf')
for file in files:
    fileobj = open(BASE_PATH + file,'r', encoding='UTF-8')
    file_content = fileobj.read()
    if(file_content.find(keyword) >= 0):
        print(file2url[file[:-5]])
    fileobj.close()
