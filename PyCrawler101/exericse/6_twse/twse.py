import requests
import pandas as pd

url = 'http://mops.twse.com.tw/mops/web/ajax_t51sb01'
payload = {'encodeURIComponent':'1',
'step':'1',
'firstin':'1',
'TYPEK':'sii',
'code':'01'}
res = requests.post(url,data=payload)
tables = pd.read_html(res.content,encoding='utf-8')
df = tables[0]

dg = df.ix[0:2][[1,4,12]];
dg.columns=['company','founder','value of stock']