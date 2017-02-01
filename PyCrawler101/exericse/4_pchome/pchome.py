#! -*- coding: utf8 -*-
import requests
url = 'http://ecshweb.pchome.com.tw/search/v3.3/all/results?q=thinkpad&page=2&sort=rnk/dc'
res = requests.get(url)

data = res.json()
for e in data['prods']:
    name = e['name']
    price = e['price']

    print name,price
