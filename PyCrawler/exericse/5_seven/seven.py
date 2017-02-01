import requests
from lxml import etree
from cStringIO import StringIO
# from xml.etree import ElementTree

url = 'http://emap.pcsc.com.tw/EMapSDK.aspx'
payload = {'commandid':'SearchStore',
'city':'台北市',
'town':'文山區'}

headers= {
    'Cookie':'ASP.NET_SessionId=cfcavh55o53snuynicarlw45'
}
# print res.text
res = requests.post(url,data=payload,headers = headers)
# tree = ElementTree.fromstring(res.content)
xml = StringIO(res.content)
tree = etree.parse(xml)
for e in tree.xpath('/iMapSDKOutput/GeoPosition'):
    print e[0].text,e[1].text,e[6].text