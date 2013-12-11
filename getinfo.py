import urllib.request
import io
import os
import re
import hashlib
import psycopg2
import datetime
from http import cookiejar
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

procQue = []
visited = set()
conn = psycopg2.connect(database='crawlData', user='python',password='123')
cur = conn.cursor()

cj = cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

procQue.insert(0,"http://www.nwpu.edu.cn/")
visited.add("http://www.nwpu.edu.cn/")

guess_list = ["utf-8","gbk"]

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
                            visited.add(urlAbs)
                            procQue.append(urlAbs)
        elif tag=="script" or tag=="style":
            self.needstep+=1
    def handle_endtag(self, tag):
        if tag=="script" or tag=="style":
            self.needstep-=1
    def handle_data(self, data):
        if self.needstep<=0:
            self.output.write(data)

try:
    while len(procQue)>=1:
        currentUrl = procQue.pop()
        print(currentUrl)
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
        if count&0xF==0:  conn.commit(); print('Database Commited');
        count+=1
        cur.execute("select sha1 from content where sha1=%s",(m.digest(),))
        if cur.rowcount==0:
            cur.execute("insert into content values(%s,%s)",(m.digest(),content))
        cur.execute("insert into url values(%s,%s,%s)",(currentUrl, m.digest(),datetime.datetime.now()))
except KeyboardInterrupt:
    print("Terminated.")
    cur.close()
    conn.close()
