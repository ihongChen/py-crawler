
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import re

stock_id = 2451
url = 'https://tw.stock.yahoo.com/d/s/major_{stock_id}.html'.format(
    stock_id=stock_id)
res = requests.get(url)

tables = pd.read_html(url)
filtered_talbes = [xx for xx in tables if xx.shape[1] == 8]

df = filtered_talbes[0]
df = pd.DataFrame(np.r_[df.values[1:, 0:3], df.values[1:, 4:7]], columns=[
                  "broker", "long", "short"])
pat = re.compile(u"([0-9]+ /[0-9]+ /[0-9]+)")
date = map(int, pat.findall(res.text)[0].split("/"))
date[0] = 1911 + date[0]
date = datetime(*date)

df["stock_id"] = stock_id
df["date"] = date

df = df[["date", "stock_id", "broker", "long", "short"]]
