import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from numpy import NaN

def Crawler104(url,kw):
	# given datapage url and return well-structured(dict) data
	 
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text)

        jobSummary= soup.select('.content > p ')[0]
        company = soup.select('.company .cn')[0].text
        candidates = soup.select('.sub > a')[0].text.strip()
        salary = soup.select('.content > dl > dd')[1].text
        e1 = soup.select('dd.addr ')[0].text
        e1 = e1.strip().split()
        address = e1[0]
        e2 = soup.select('h1')[1]
        jobName = e2.text.strip().split('\n')[0]
        jobName = jobName.strip()
        requirement = soup.select('.content')[1].text.strip()
        crawlTime = datetime.utcnow()

        data = {"company":company,"jobName":jobName,"address":address,"jobSummary":jobSummary,"salary":salary,"requirement":requirement,"candidates":candidates,"searched_keyword":kw,'url':url,"crawlTime":crawlTime}
        return data
    except Exception:
        print "ERROR!"
        return {"company":NaN,"jobName":NaN,"address":NaN,"jobSummary":NaN,"salary":NaN,"requirement":NaN,"candidates":NaN,"searched_keyword":kw,'url':NaN,"crawlTime":NaN}

def getURLs(url):
	# this function get a list of urls linked to crawling page
    res = requests.get(url)
    soup = BeautifulSoup(res.text)        
    urls = ['http://www.104.com.tw' + e.get('href') for e in soup.select('.jobname_summary.job_name > a')]
    return urls

def getAllCrawlerUrls(url,kw,page=1):
	# handling next page issue
	urls = []
	while True:
		url = 'http://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&keyword={kw}&order=1&asc=0&page={page}'.format(kw=kw,page=page)
		if len(getURLs(url))!=0:
			urls+=getURLs(url)
			print 'This is the job of "{kw}",and {page} page crawled.'.format(kw=kw,page=page)
			page +=1
			time.sleep(1) # time delay for data loading purpose
		else:
			print '---------done--------'
			break

	return urls

def getData(kw,page=1):
    kw.replace(' ','+')
    url = 'http://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&keyword={kw}&order=1&asc=0&page={page}'.format(kw=kw,page=page)
    urls = getAllCrawlerUrls(url,kw,page=page)
    dataList = map(Crawler104,urls,[kw]*len(urls))
    df = pd.DataFrame(dataList)
    return df

gdf = getData('python',page=1).groupby('company').size()
gdf.sort(ascending=False)
print gdf