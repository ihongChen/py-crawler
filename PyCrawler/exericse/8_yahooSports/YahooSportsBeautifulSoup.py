# this code crawl start from the yahoo_sport's homepage
from bs4 import BeautifulSoup
import requests
import pandas as pd
def getYahooData(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text)
    headline = soup.select('.headline')[0].text
    provider = soup.select('.provider.org')[0].text
    publishDate = soup.select('abbr')[0].get('title')
    list1 = soup.select('.bd > p')
    body = ''.join(str(e) for e in list1) # string
    body = unicode(body,'utf8') # convert to utf8
    data = {"headline":headline,"provider":provider,"publishDate":publishDate,"body":body}
    return data

url = 'https://tw.sports.yahoo.com/'
# link for crawling each page, under tag '.list-story .txt > a'
res = requests.get(url)
soup = BeautifulSoup(res.text)
linksToCrawl = [url + 
				e.get('href') for e in soup.select('.list-story .txt > a')]
# type:List of dictionary
dataList = map(getYahooData,linksToCrawl)

# convert to dataframe
df = pd.DataFrame(dataList)

# save to csv file
df.to_csv("yahoo_news.csv", encoding="utf8", index=False)

# save to db-sqlite
import sqlite3
conn = sqlite3.connect('yahoo_news.db')
df.to_sql(name = "news", con=conn, if_exists="append")
read_sql_df = pd.read_sql(sql="select * from news",con=conn)
read_sql_df