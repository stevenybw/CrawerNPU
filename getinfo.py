import urllib.request;
import io;
import os;
import hashlib;
from http import cookiejar;
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

procQue = [];
visited = set();
BASE_PATH = "I:\\WebCrawer\\";

cj = cookiejar.CookieJar();
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj));

procQue.insert(0,"http://www.nwpu.edu.cn/");
visited.add("http://www.nwpu.edu.cn/");

def isInBound(x):
    return x.find("nwpu.edu.cn")>=0;

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag=="a":
            for ituple in attrs:
                if ituple[0]=='href':
                    url = ituple[1];
                    urlAbs = urljoin(currentUrl, url);
                    if isInBound(urlparse(urlAbs).netloc):
                        if(not urlAbs in visited):
                            visited.add(urlAbs);
                            procQue.insert(0,urlAbs);

file_relation = open(BASE_PATH + "relation.conf", 'w');
while len(procQue)>=1:
    currentUrl = procQue.pop();
    try:
        y=opener.open(currentUrl,timeout=1);
    except:
        continue;
    if y.getheader('Content-Type').lower() != 'text/html':
        continue;
    httpContent = y.read();
    m = hashlib.sha1();
    m.update(httpContent);
    if(os.path.exists(BASE_PATH + m.hexdigest() + ".html")):
        continue;
    file = open(BASE_PATH + m.hexdigest() + ".html", 'wb');
    file.write(httpContent);
    file_relation.write(m.hexdigest() + "\t" + currentUrl+'\n');
    print(currentUrl);
    file.close();
    parser = MyHTMLParser();
    parser.feed(str(httpContent));
file_relation.close();
