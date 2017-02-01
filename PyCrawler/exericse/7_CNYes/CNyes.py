#! encoding = "utf-8" 
import requests
from lxml import etree
import lxml.html
from HTMLParser import HTMLParser
import pandas as pd

parser = HTMLParser()

def getNewsData(url):
    res = requests.get(url)
    res.encoding = "utf8"
    doc = etree.HTML(res.text)
    
    data = {"title":doc.xpath(
            "//div[@class='newsContent bg_newsPage_Lblue']/h1")[0].text,
            "info":doc.xpath(
            "//div[@class='newsContent bg_newsPage_Lblue']/div[@class='info']")[0].text,
            "url":url            
           }
    e = doc.xpath("//div[@class='newsContent bg_newsPage_Lblue']/div[@id='newsText']")[0]
    data["body"] = parser.unescape(lxml.html.tostring(e))
    return data

def listNewsUrls(url):
	## given:url ->output:links of each headline's url
    res = requests.get(url)
    doc = etree.HTML(res.text)
    e = doc.xpath("//ul[@class='list_1 bd_dbottom']//li/a")
    urls = [n.attrib["href"] for n in e]
    return urls

url = "http://news.cnyes.com/headline_channel/list.shtml" # headlines website
urls = listNewsUrls(url)
data = map(getNewsData,urls)

df = pd.DataFrame(data)
df