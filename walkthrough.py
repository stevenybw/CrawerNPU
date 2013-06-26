import os
import io
import bs4;

BASE_PATH = "I:\\WebCrawer1\\"
keyword = "郑江滨"

counter = 0;
guess_list = ["utf-8","gbk"]

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
    if counter % 100 ==0:
        print(counter)
    counter = counter+1;
    for guess in guess_list:
        try:
            fileobj = open(BASE_PATH + file,'r', encoding=guess)
            file_content = fileobj.read()
        except:
            pass
    if(file_content.find(keyword) >= 0):
        print(file2url[file[:-5]])
    fileobj.close()
