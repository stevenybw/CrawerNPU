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

procQue = queue.Queue()
task_num = 4
visited = set()
BASE_PATH = "I:\\WebCrawer\\"

cj = cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

procQue.put("http://www.nwpu.edu.cn/")
visited.add("http://www.nwpu.edu.cn/")

lock = threading.Lock()

guess_list = ["utf-8","gbk"]

def printMessage(a,b,c):
    lock.acquire()
    print(a,b,c)
    lock.release()

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
                            procQue.put(urlAbs)
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
    threadid = -1
    def __init__(self, ID):
        threading.Thread.__init__(self)
        self.threadid=ID
    def run(self):
        while 1:
            self.currentUrl = procQue.get()
            for i in range(2):
                try:
                    y=opener.open(self.currentUrl,timeout=10)
                    break
                except:
                    pass
            else:
                printMessage(self.threadid, "\t" + self.currentUrl, " Dead, Passed")
                procQue.task_done()
                continue
            if y.getheader('Content-Type').lower() != 'text/html':
                procQue.task_done()
                continue
            
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
                procQue.task_done()
                continue;
            file = open(BASE_PATH + m.hexdigest() + ".txt", 'w', encoding='utf-8')
            file.write(content)
            file_relation.write(m.hexdigest() + "\t" + self.currentUrl+'\n')
            printMessage(self.threadid, "\t", self.currentUrl)
            file.close()
            procQue.task_done()
            

file_relation = open(BASE_PATH + "relation.conf", 'w')

tasks = list();
for i in range(task_num):
    tasks.append(GetContentAsync(i))
for task in tasks:
    print("Task ",task.threadid, " Scheduled. ")
    task.start()
procQue.join()

    
file_relation.close()
