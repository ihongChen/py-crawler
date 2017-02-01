# -*- coding: utf-8
## sinyi crawler, with thread

from bs4 import BeautifulSoup
from threading import Thread,Lock
import Queue
import sqlite3 
import pandas as pd
import datetime,requests,ipdb
import time


def getZipCode(address):
    # given chinese address return zipCode
    zipCodeApi = 'http://zipcode.mosky.tw/api/find?address=' + address
    req = requests.get(zipCodeApi)
    return int(req.json()['result'])

def doCrawl(*args):
    # task to crawl by thread agent 
    Que = args[0]
    while Que.qsize()>0:
        job=Que.get()
        job.toCrawl()
    # Q.join()

url='http://buy.sinyi.com.tw/cgi/search/listSearch.json'
resTest = requests.get(url)
cookie=resTest.headers['set-cookie']
headers={'Cookie':cookie}

class CrawlerJob:

    def __init__(self,page,headers):
        
        self.page = page
        # self.params = {"returnParams":"NO,name,address,areaLand,areaBuilding,areaBuildingMain,areaBalcony,price,type,use,room,hall,bathroom,age,floor,lift,parking",\
        self.params = {"returnParams":"NO,name,address,areaLand,areaBuilding,areaBuildingMain,areaBalcony,price,priceFirst,discount,type,use,room,hall,bathroom,openroom,roomplus,hallplus,bathroomplus,openroomplus,age,floor,staffpick,decoar,pingratesup,lift,parking,customize,keyword",\
             "page":page,"limit":"30"}
        self.headers = headers
        self.lock = Lock()
        
        
        # req = requests.post(self.url,self.params,headers=self.headers)
        # self.totalpages = req.json()['OPT']['totalPage'] # totalPages
    

    def toCrawl(self):
        # scrape the page and store it into db
        
        # print "crawling...page:%d"%self.page
        global TOTALPAGE
 
        req = requests.post(url,self.params,headers=self.headers)
        try:
            TOTALPAGE = req.json()['OPT']['totalPage']        
            print "page:%d/%d,resopnse:%s"%(self.page,TOTALPAGE,req)
        except keyError:
            print "key Error..."

        
        # ipdb.set_trace()
        with self.lock:

            dataPage = pd.DataFrame(req.json()['OPT']['List'])

            today = datetime.date.today()
            dataPage["crawlDate"]=today
            dataPage["source"] = u'信義房屋'

            print "getting zipcode on page:%d"%self.page
            zipCodeList = [getZipCode(e) for e in dataPage['address']]
            zipCode = pd.Series(zipCodeList)
            dataPage['zipCode']=zipCode
            

            print "storing page %d to database..."%self.page
            con = sqlite3.dbapi2.connect('house_price.db')
            dataPage.to_sql("house",con,if_exists='append',index=False)
            con.close()



start = datetime.datetime.now()
# queue: put the CrawleJob into que (qsize=no. of pages)
que =Queue.Queue()

# job = CrawlerJob(page=1)
totalpages = 2731
for page,_ in enumerate(range(totalpages),1):
    # print page
    que.put(CrawlerJob(page,headers))

print("[Info] Queue size={0}...\n".format(que.qsize()))  

# open multi-thread
tds = []
noOfthreads = 10
for i in range(noOfthreads):
    td = Thread(target=doCrawl,args=(que,))
    # thread.daemon=True
    td.start()
    tds.append(td)

for td in tds:
    while td.is_alive():
        time.sleep(30)
        break
    td.join(timeout=1)
    

end = datetime.datetime.now()
print "[Info] Spending time={0}!".format(end-start)

