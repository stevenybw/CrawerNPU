import psycopg2
import datetime
class PersistentData:
    def __init__(self, database, user, password):
        self.conn = psycopg2.connect(database='crawlData', user='python',password='123')
        self.cur = self.conn.cursor()
    '''
    # queue:
    # The queue that is to be loaded into
    '''
    def getLastStatus(self, que):
        self.cur.execute("select url from tocrawl order by id desc")
        for i in range(self.cur.rowcount):
            que.append(self.cur.fetchone()[0])
    def getVisitedNodes(self, the_set):
        self.cur.execute("select url from url")
        for i in range(self.cur.rowcount):
            the_set.add(self.cur.fetchone()[0])
    def saveLastStatus(self, que):
        self.cur.execute("delete from tocrawl")
        id=0
        for url in que:
            self.cur.execute("insert into tocrawl(id,url) values(%s,%s)",(id,url))
            id+=1
        self.conn.commit()
    #is the digest existed on the content
    def bExistSuchDigest(self,digest):
        self.cur.execute("select sha1 from content where sha1=%s",(digest,))
        flag = (self.cur.rowcount!=0)
        self.cur.fetchall()
        return flag
    def addContent(self, digest, content):
        self.cur.execute("insert into content(sha1,content) values(%s,%s)",(digest, content))
    def addUrl(self, url, content_digest):
        self.cur.execute("insert into url(url,content,stamp_fetched) values(%s,%s,%s)",(url, content_digest, datetime.datetime.now()))
    def commit(self):
        self.conn.commit()
    def close(self):
        self.cur.close()
        self.conn.close()
if __name__=="__main__":
    procQue = []
    db = PersistentData(database='crawlData', user='python',password='123')
    db.getLastStatus(procQue)
    db.close()
