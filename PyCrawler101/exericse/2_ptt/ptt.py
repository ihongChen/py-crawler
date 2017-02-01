import requests
from bs4 import BeautifulSoup

url_ptt = 'https://www.ptt.cc/bbs/Gossiping/index.html'
payload = {'from':'/bbs/Gossiping/index.html','yes':'yes'}

rs = requests.session()
res = rs.post('https://www.ptt.cc/ask/over18',payload,verify=False)
res = rs.get(url_ptt,verify=False)
soup = BeautifulSoup(res.text)

# print out title in the newest page
titleList = soup.select('.r-ent')
for title in titleList:
    print title.a.text