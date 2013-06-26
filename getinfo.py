import urllib.request
import io
import os
import re
import hashlib
import threading
import queue
from http import cookiejar
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

procQue = []
task_num = 4
visited = set()
m_lock = threading.Lock()
que_lock = threading.Lock()
BASE_PATH = "I:\\WebCrawer\\"

cj = cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

procQue.insert(0,"http://www.nwpu.edu.cn/")
visited.add("http://www.nwpu.edu.cn/")

guess_list = ["utf-8","gbk"]

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
                            visited.add(urlAbs)
                            procQue.insert(0,urlAbs)
        elif tag=="script" or tag=="style":
            self.needstep+=1
    def handle_endtag(self, tag):
        if tag=="script" or tag=="style":
            self.needstep-=1
    def handle_data(self, data):
        if self.needstep<=0:
            self.output.write(data)

class GetContentAsync(threading.Thread):
    currentUrl = ""
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while 1:
            m_lock.acquire()
            if len(procQue)>=1:
                self.currentUrl = procQue.pop()
            else:
                m_lock.release()
                break
            m_lock.release()
            for i in range(2):
                try:
                    y=opener.open(self.currentUrl,timeout=10)
                    break
                except:
                    print(self.currentUrl, " Time Out")
                    pass
            else:
                print(self.currentUrl, " Dead, Passed")
                continue
            if y.getheader('Content-Type').lower() != 'text/html':
                continue
            
            m_lock.acquire()
            
            httpContent = y.read()
            for guess in guess_list:
                try:
                    httpContentStr = str(httpContent, encoding=guess)
                except:
                    pass
            i=0
            
            #There is a subtle encoding problem. The first char of
            #httpContentStr is /uFFFE which is unrecognizable. I try
            #to delete it while I don't know whether it is right.
            while not httpContentStr[i].isprintable():
                i+=1
            httpContentStr = httpContentStr[i:]

            #Parse html for extending nodes and retrieving data
            parser = MyHTMLParser(self.currentUrl)
            parser.feed(httpContentStr)
            content = parser.output.getvalue()

            #Remove respectively Comments, Spaces
            content = re.sub(r"<!--[\w\W]*?-->",r"",content)
            content = re.sub(r"//.*?\n",r"",content)
            content = re.sub(r"/[*][\w\W]*?[*]/",r"",content)
            content = re.sub(r"[\s]",r"",content)

            m = hashlib.sha1()
            m.update(content.encode('utf-8'))
            if(os.path.exists(BASE_PATH + m.hexdigest() + ".html")):
                continue;
            file = open(BASE_PATH + m.hexdigest() + ".txt", 'w', encoding='utf-8')
            file.write(content)
            file_relation.write(m.hexdigest() + "\t" + self.currentUrl+'\n')
            print(self.currentUrl)
            file.close()
            m_lock.release();

file_relation = open(BASE_PATH + "relation.conf", 'w')

tasks = list();
for i in range(task_num):
    tasks.append(GetContentAsync())
for task in tasks:
    task.start()
print("Tasks Scheduled. ")
for task in tasks:
    task.join()
    
file_relation.close()
