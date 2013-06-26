import os
import io
import bs4;

BASE_PATH = "I:\\WebCrawer\\"
OUTPUT = "I:\\"
keyword = "台炳龙"

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
outputfile = open(OUTPUT + 'search_result.html', 'w', encoding='utf-8');

def init_html():
    outputfile.write("""
<html>
<head><title>Search Result</title>
<META content="text/html; charset=UTF-8" http-equiv="Content-Type" /></head>
<body><h1>Keyword: 
""" + keyword + "</h1>")

def fini_html():
    outputfile.write("</body></html>")

def output(url, str_item):
    outputfile.write("<p><a href='"+ url + "'>" + str_item + "</a></p>")

print('Search In Progress for ', keyword, ' please wait.')

init_html();

for file in files:
    #if counter % 100 ==0:
        #print(counter)
    counter = counter+1;
    for guess in guess_list:
        try:
            fileobj = open(BASE_PATH + file,'r', encoding=guess)
            file_content = fileobj.read()
        except:
            pass
    find_result = file_content.find(keyword)
    if find_result >= 0:
        print(file2url[file[:-4]])
        output(file2url[file[:-4]], file_content[find_result-20:find_result+20])
    fileobj.close()
fini_html();
outputfile.close();
