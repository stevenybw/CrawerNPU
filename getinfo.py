import urllib.request
import io
import os
import sys
import re
import hashlib
import threading
import psycopg2
from http import cookiejar
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin
from persistent import *
from on_exit_console import *

procQue = []
visited = set()
db = PersistentData(database='crawlData', user='python',password='123')

cj = cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

procQue.insert(0,"http://www.nwpu.edu.cn/")

guess_list = ["utf-8","gbk"]

onExit = threading.Event()
onExitAck = threading.Event()

count = 1 #定期更新数据库

def isInBound(x):
    return x.find("nwpu.edu.cn")>=0;

class MyHTMLParser(HTMLParser):
    output = io.StringIO()
    needstep = 0
    currentUrl = ""
    def __init__(self, cURL):
        HTMLParser.__init__(self)
        self.currentUrl = cURL
        self.output.close()
        self.output = io.StringIO()
    def handle_starttag(self, tag, attrs):
        if tag=="a":
            for ituple in attrs:
                if ituple[0]=='href':
                    url = ituple[1]
                    urlAbs = urljoin(self.currentUrl, url)
                    if isInBound(urlparse(urlAbs).netloc):
                        if(not urlAbs in visited):
                            procQue.append(urlAbs)
        elif tag=="script" or tag=="style":
            self.needstep+=1
    def handle_endtag(self, tag):
        if tag=="script" or tag=="style":
            self.needstep-=1
    def handle_data(self, data):
        if self.needstep<=0:
            self.output.write(data)

def on_exit(signal):
    print("On Exit.")
    onExit.set()
    onExitAck.wait()
    print("On Exit Wait OK.")
    db.saveLastStatus(procQue)
    db.commit()
    db.close()
    onExit.set()
    return True
    
#Register Callback
RegisterOnExit(on_exit)
#load_initial_state
db.getLastStatus(procQue)
db.getVisitedNodes(visited)

while len(procQue)>=1:
    if(onExit.is_set()):
        print("OnExitAck Setted.")
        onExitAck.set()
        onExit.clear()
        onExit.wait()
        exit()
    currentUrl = procQue.pop()
    print(currentUrl)
    if(currentUrl in visited):
        print("Existed, step.. ")
        continue
    visited.add(currentUrl)
    for i in range(2):
        try:
            y=opener.open(currentUrl,timeout=1)
            break
        except:
            print(currentUrl, " Time Out")
            pass
    else:
        print(currentUrl, " Dead, Passed")
        continue
    if y.getheader('Content-Type').lower() != 'text/html':
        continue
    for i in range(2):
        try:
            httpContent = y.read()
            break
        except:
            print("Error reading, try again.")
            pass
    else:
        print(currentUrl, " Dead, Passed")
        continue
    
    for guess in guess_list:
        try:
            httpContentStr = str(httpContent, encoding=guess)
            break
        except:
            pass
    else:
        print('Unknown Charset, Passed')
        continue
    i=0
    
    #There is a subtle encoding problem. The first char of
    #httpContentStr is /uFFFE which is unrecognizable. I try
    #to delete it while I don't know whether it is right.
    while not httpContentStr[i].isprintable():
        i+=1
    httpContentStr = httpContentStr[i:]

    #Parse html for extending nodes and retrieving data
    parser = MyHTMLParser(currentUrl)
    parser.feed(httpContentStr)
    content = parser.output.getvalue()

    #Remove respectively Comments, Spaces
    content = re.sub(r"<!--[\w\W]*?-->",r"",content)
    content = re.sub(r"//.*?\n",r"",content)
    content = re.sub(r"/[*][\w\W]*?[*]/",r"",content)
    content = re.sub(r"[\s]",r"",content)

    m = hashlib.sha1(content.encode('utf-8'))
    if count&0xF==0:  db.commit(); print('Database Commited');
    if count&0x1FF==0: db.saveLastStatus(procQue)
    count+=1
    digest=m.digest()
    if not db.bExistSuchDigest(digest):
        db.addContent(digest,content)
    db.addUrl(currentUrl,digest)
