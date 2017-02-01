# -*- coding: utf8 -*-
## sinyi-house web crawling

from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3 
import datetime

buy_api = 'http://buy.sinyi.com.tw/cgi/search/listSearch.json'


def getZipCode(address):
    # given chinese address return zipCode
    zipCodeApi = 'http://zipcode.mosky.tw/api/find?address=' + address
    req = requests.get(zipCodeApi)
    return int(req.json()['result'])

def scrap_sinyi_buy(url):
    # web crawler 

    # get cookie
    resTest = requests.get(url)
    cookie=resTest.headers['set-cookie']
    headers={'Cookie':cookie}
    page = 1
    
    params = {"returnParams":"NO,name,description,address,areaLand,areaBuilding,areaBuildingMain,areaBalcony,price,priceFirst,discount,type,use,room,hall,bathroom,openroom,roomplus,hallplus,bathroomplus,openroomplus,age,floor,inc,imgCount,imgDefault,staffpick,decoar,pingratesup,community,lift,parking,customize,keyword",\
             "page":page,"limit":"30"}
    req = requests.post(url,params,headers=headers)

    totalPages = req.json()['OPT']['totalPage'] # totalPages
    nowpage = req.json()['OPT']['page']

    houseData=pd.DataFrame(req.json()['OPT']['List'])
    today = datetime.date.today()

    totalPages = 3
    ## scrapy all pages and store it 
    for page,_ in enumerate(range(totalPages),1):
        params = {"returnParams":"NO,name,description,address,areaLand,areaBuilding,areaBuildingMain,areaBalcony,price,priceFirst,discount,type,use,room,hall,bathroom,openroom,roomplus,hallplus,bathroomplus,openroomplus,age,floor,inc,imgCount,imgDefault,staffpick,decoar,pingratesup,community,lift,parking,customize,keyword",
             "page":page,"limit":"30"} # formdata
        res = requests.post(url,params,headers=headers)      
        print "scrapy page: %s/%s, response:%s"%(page,totalPages,res)

        dataPage = pd.DataFrame(res.json()['OPT']['List'])
        zipCode = pd.Series([getZipCode(e) for e in dataPage['address']])
        dataPage['zipCode'] = zipCode
        dataPage['crawlDate'] = today
        dataPage['source'] = u'信義房屋'

        dataStore=dataPage[["address","zipCode","name","areaBuilding","areaBuildingMain","areaLand","age","use","type","room",\
               "hall","bathroom","openroom","floor","parking","lift","price","source","crawlDate"]]
        
        ## store to db 
        con = sqlite3.dbapi2.connect('house_price.db')
        dataStore.to_sql("house",con,if_exists='append',index=False)

    con.close()
        
        

    
    

