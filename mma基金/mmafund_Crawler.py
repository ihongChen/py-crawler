# coding: utf-8

# # MMA基金資料
import pandas as pd
import re
import requests
import pandas as pd
import pymysql
from bs4 import BeautifulSoup as BS
from collections import defaultdict


def getForeignFundInfo(soup):
    """
    """
    ## fundid ##
    fundid = re.findall(r"(?:a=)(.+)",soup.select('#itemTab')[0].find('a').get('href'))[0]

    fieldSoup = soup.select('.wfb5l')
    fieldList = []
    for e in fieldSoup[:15]:
    #     print(e.text)
        fieldList.append(e.text)
    starNum = getFundStar(fieldSoup[-4])
    fieldList.append(starNum)
    fieldList.append(fieldSoup[-2].text)
    colNames = [
        '基金名稱',
        '基金英文名稱',
        '台灣總代理',
        '海外發行公司',
        '指標指數',
        '成立日期',
        '註冊地',
        '基金規模',
        '計價幣別',
        '基金類型',
        '投資區域',
        '投資標的',
        '保管機構',
        '傘狀基金',
        '經理人',
        '基金評等',
        '投資策略'
    ]
    dataList = list(zip(colNames,fieldList))
    fundInfo_dict = defaultdict(list)
    fundInfo_dict['fundid'] = fundid
    for name,v in dataList:
        fundInfo_dict[name] = v
    return fundInfo_dict

def getForeignStockHolding(soup):

    """取得[境外]持股資料中股票張數(表格)
    params
    ======
    input: soup --- html經BS包裝後變數
    return : defaultdict {持股名稱:[],
                            fundid:[],
                            比例:[],
                            資料月份,[]}

    """
    ### fundid ####
    fundid = re.findall(r"(?:a=)(.+)",soup.select('#itemTab')[0].find('a').get('href'))[0]

    ### 資料月份 ###
    update_date = '/'.join(re.findall(r"\d+",soup.select('.wfb1ar')[-1].text)) ## 資料月份
    print('資料月份:{}'.format(update_date))

    a = list(zip(soup.select('.wfb2l'),soup.select('.wfb2r')))
    b = list(zip(soup.select('.wfb5l'),soup.select('.wfb5r')))
    dataList = zip(*[(e1.text,e2.text.strip()) for (e1,e2) in a+b]) # [(k1,k2,k3),(v1,v2,v3...)]

    colNames = ['持股名稱','比例']
    foreignStockDict = defaultdict(list)
    foreignStockDict['資料月份'] = update_date
    foreignStockDict['fundid'] = fundid
    for index,data in enumerate(dataList):
        foreignStockDict[colNames[index]] = list(data)
    return foreignStockDict

def getForeignShareHolding(html_text):
    """取得國外持股資料(圓餅圖)
    剖析mma中html含有js程式碼，資料隱藏在js其中
    params
    html_text : raw text(str)
    return : list of defaultdict
    """
    def getShareHoldingTable(stockGroupList):
        """轉換國外持股圓餅圖資料(getForeignShareHolding)為dict格式(pd.dataframe可直接使用)
        """
        stockGroup = defaultdict(list)
        for index,(k,v) in enumerate(stockGroupList):

            if index >1:
                stockGroup['項目'].append(k)
                stockGroup['投資金額(美元:萬)'].append(v)
            else:
                stockGroup[k] = v
        return stockGroup

    soup = BS(html_text,"lxml")
    update_date = '/'.join(re.findall(r"\d+",soup.select('.wfb1ar')[0].text)) ## 資料更新日期

    ### fundid ####
    fundid = re.findall(r"(?:a=)(.+)",soup.select('#itemTab')[0].find('a').get('href'))[0]
    ###############

    string1 = 'DJGraphObj1' # 切出目標字串
    target_text = html_text_wb[html_text_wb.index(string1):]

    pat1 = r"(?:\'Title\':)(.+)"
    investTitle = re.findall(pat1,target_text) # 取得並切分表單table

    pat2 = r"(?:\')(.*?)(?:\')" # 取出包含在 ' '內的字串
    pat3 = r"(?:\'PieV\':)(.+)" # 取出包含在 PieV 後的字串
    #     investTitleByStock = re.findall(pat2,investTitle[0]) ## 依產業標題(List)
    #     investTitleByStock
    table = defaultdict(list)
    tableAns = []

    for index,titleText in enumerate(investTitle):
        titleList = re.findall(pat2,titleText)
        if len(titleList) == 1:
            continue
        colname = titleList[0]
        titleList = titleList[1:]
        titleList.insert(0,'fundid')
        titleList.insert(1,'資料日期')
        valueList = re.findall(pat2,re.findall(pat3,target_text)[index])
        valueList.insert(0,fundid)
        valueList.insert(1,update_date)
    #         print(titleList,valueList)
        table[colname]= (list(zip(titleList,valueList)))
        tableAns.append(getShareHoldingTable(table[colname]))

    return tableAns

def getFundBasicInfo(soup):
    """
    取得國內基金基本資料

    params
    ======
    input  : soup
    output : defaultDict ==>{'fundid': 'ACUS03-UN2','主要投資區域': '台灣',
                            '保管銀行': '中國信託銀行','基金公司': '永豐投信',...}
    """
    #### fundid ####
    fundid = re.findall(r'(?:a=)(.+)',soup.select('#itemTab')[0].find('a').get('href'))[0]
    ################
    fieldSoup = soup.select('.wfb5l')
    fieldList = [fundid]
    for e in fieldSoup[:10]:
    #     print(e.text)
        fieldList.append(e.text)
    starNum = getFundStar(fieldSoup[-3])
    fieldList.append(starNum)
    fieldList.append(fieldSoup[-1].text)
    info_colName = [
        'fundid',
        '基金名稱',
        '基金公司',
        '成立日期',
        '基金經理人',
        '基金規模(億)',
        '成立時規模(億)',
        '基金類型',
        '保管銀行',
        '主要投資區域',
        '投資區域',
        '基金評等',
        '投資標的'
    ]
    dataList = list(zip(info_colName,fieldList)) ## list of tuples ==> [(fundid,xxxx),(基金名稱,xxxxx),(基金公司,xxxx),...]

    dataDict = defaultdict(list)
    ## 將資料格式轉換為 defaultdict ##
    for k,v in dataList:
        dataDict[k] = v
    return dataDict

def getFundManager(soup):
    """
    取得歷任經理人資料
    """
    #### fundid ####
    fundid = re.findall(r'(?:a=)(.+)',soup.select('#itemTab')[0].find('a').get('href'))[0]
    ################
    managerList = []
    managerDict = defaultdict(list)
    managerBSTable = soup.select('#oMainTable')[1]
    colNames = [
        '經理人',
        '時間',
        '期間(月)',
        '操作績效(%)',
        '台股績效(%)',
        '現任基金'
    ]

    managerDict['fundid'] = fundid
    for index,manager in enumerate(managerBSTable.select('tr')[2:]):
        row = []
        for index,field in enumerate(manager.select('td')):
            try:
                field = float(field.text)
                row.append(field) # 轉換數字部分
            except ValueError as e:
                field = field.text
                row.append(field)
            managerDict[colNames[index]].append(field)

    return managerDict

def getFundStar(starTag):
    '''取得基金評等數字(影像<星星>標記 --> 數字)
    params ------
    starTag: 含有星號圖案的bs4 tag
    return: 基金評等(int)
    '''
    starList = starTag.select('img') # bs4 tag
    starList = [star['src'] for star in starList ] # 取出src裡面的url
    starStr = '**'.join(starList) # 接成string
    if re.findall('/BT_Coin_b.gif',starStr):
        starNum = 0.5
    else:
        starNum = 0
    starNum += len(re.findall('/BT_Coin_a.gif',starStr))
    print('星星幾顆:{}'.format(starNum))
    return starNum

def getDomesticShareHolding(html_text):
    """取得國內持股資料(圓餅圖)
    剖析mma中html含有js程式碼，資料隱藏在js其中
    params
    html_text : raw text(str)
    return : list of defaultdict
    """
    def getShareHoldingTable(stockGroupList):
        """轉換國內持股圓餅圖資料(getDomesticShareHolding)為dict格式(pd.dataframe可直接使用)
        """
        stockGroup = defaultdict(list)
        for index,(k,v) in enumerate(stockGroupList):

            if index >1:
                stockGroup['項目'].append(k)
                stockGroup['投資金額(萬元)'].append(v)
            else:
                stockGroup[k] = v
        return stockGroup

    ### 取得 fundid ###
    soup = BS(html_text,"lxml")
    fundid = re.findall(r"(?:a=)(.+)",soup.select('#itemTab')[0].find('a').get('href'))[0]
    print('fundid:{}'.format(fundid))
    ##### 取得 資料日期 ####
    update_dateStr = re.findall(r"\d+\/\d+\/\d+",soup.select('.wfb1ar')[-1].text)[0] # xx分布--資料日期
    #######################
    string1 = 'DJGraphObj1' # 切出目標字串
    target_text = html_text[html_text.index(string1):]

    pat1 = r"(?:\'Title\':)(.+)"
    investTitle = re.findall(pat1,target_text) # 取得並切分表單table

    pat2 = r"(?:\')(.*?)(?:\')" # 取出包含在 ' '內的字串
    pat3 = r"(?:\'PieV\':)(.+)" # 取出包含在 PieV 後的字串
    table = defaultdict(list)
    tableAns = []
    for index,titleText in enumerate(investTitle):
        titleList = re.findall(pat2,titleText)
        if len(titleList) == 1:
            continue
        colname = titleList[1]
        titleList = titleList[2:]
        titleList.insert(0,'fundid')
        titleList.insert(1,'資料日期')
        valueList = re.findall(pat2,re.findall(pat3,target_text)[index])
        valueList.insert(0,fundid)
        valueList.insert(1,update_dateStr)
        # print(titleList,valueList)
        table[colname]= (list(zip(titleList,valueList)))
        tableAns.append(getShareHoldingTable(table[colname]))
    return tableAns

def getShareHoldingTable(stockGroupList):
    """轉換國內持股圓餅圖資料(getDomesticShareHolding)為dict格式(pd.dataframe可直接使用)
    """
    stockGroup = defaultdict(list)
    for index,(k,v) in enumerate(stockGroupList):

        if index >1:
            stockGroup['項目'].append(k)
            stockGroup['投資金額(萬元)'].append(v)
        else:
            stockGroup[k] = v
    return stockGroup

def getDomesticStockHolding(soup):
    """取得國內持股資料中股票張數(表格)
    params
    ======
    input: soup --- html經BS包裝後變數
    return : defaultdict {增減:[],
                            股票名稱:[],
                            持股(千股):[],
                            比例:[],
                            資料月份,[]}
    """
    ### 取得 fundid ###
    fundid = re.findall(r"(?:a=)(.+)",soup.select('#itemTab')[0].find('a').get('href'))[0]
    ###############

    def parseElement(e):
        """利用此函數剖析表格內元素
        """
        row1 = []; row2=[];
        for index,field in enumerate(e.select('td')):
            if index > 3:
                row2.append(field.text)
            else:
                row1.append(field.text)
        return row1,row2


    ######## 資料月份 ##########
    update_dateStr = soup.select('#oMainTable')[1].select('tr')[0].text # 資料月份
    update_date = re.findall(r'\d+/\d+',update_dateStr)[0]
    date_colname = '資料月份'
    print(date_colname,update_date)

    ###########################


    fundShareTableList = []
    rowData = {}
    for index,e in enumerate(soup.select('#oMainTable')[1].select('tr')[1:]):
        colnames = []
        if index == 0:
            col1,col2 = parseElement(e)
            col1+=['fundid',date_colname]
            col2+=['fundid',date_colname]
        else:
            row1,row2 = parseElement(e)
            row1+=[fundid,update_date]
            row2+=[fundid,update_date]

            fundShareTableList.append(list(zip(col1,row1)))
            fundShareTableList.append(list(zip(col2,row2)))
    ### 輸出成dict格式 ##
    stocks_dict = defaultdict(list)
    for row in fundShareTableList:
        for name,value in row:
            stocks_dict[name].append(value)
    return stocks_dict


# ## 資料庫

#
# import pypyodbc
#
# con = pypyodbc.connect("DRIVER={SQL Server};SERVER=xxxxx;UID=xxxxxx;PWD=xxxxxxxx;DATABASE=xxxxxxx")
# cursor = con.cursor()
#
#
# sql_insert = """
# INSERT INTO [基金持股狀況_依持有類股分]
# VALUES (?,?,?,?)
# """
#
# df = pd.DataFrame(dataToDB_dict)
#
#
# dataToDB_dict = ACJS24_Z21[0]
# dataToDB_pd_dict = pd.DataFrame(dataToDB_dict).to_dict()
#
#
# dataToDB_pd_dict.keys()
#
# for e in list(df.T.to_dict().values()):
# #     cursor.execute(sql_insert,list(e.values()))
#     print(list(e.values()))
#
# con.commit()
#
#
# for e in df.T.to_dict().values():
#     print(list(e.values()))


if __name__ == '__main__':

    requests.packages.urllib3.disable_warnings()  # disable warning insecure

    url_basic = 'http://mmafund.sinopac.com/w/wr/wr01.djhtm?a=ACUS03-UN2'
    res = requests.get(url_basic)
    soup = BS(res.text,"lxml")

    url_stock = 'http://mmafund.sinopac.com/w/wr/wr04.djhtm?a=ACUS03-UN2'
    res_stock = requests.get(url_stock)
    html_stock = res_stock.text
    soup_stock = BS(html_stock,'lxml')

    ## 國內 ###
    df_domestic_managers = pd.DataFrame(getFundManager(soup))
    df_domestic_info = pd.DataFrame([getFundBasicInfo(soup)])
    df_domestic_info
    pd.DataFrame(getDomesticShareHolding(html_stock)[0]) # 基金各類股
    pd.DataFrame(getDomesticStockHolding(soup_stock)) # 基金持股

    ### 境外 #####
    url_wb_info =  'http://mmafund.sinopac.com/w/wb/wb01.djhtm?a=ANZ45-A28'
    url_wbTest_stock = 'http://mmafund.sinopac.com/w/wb/wb04.djhtm?a=ANZ45-A28'
    soup_wb_info = BS(requests.get(url_wb_info).text,"lxml")
    html_wb_stock = requests.get(url_wbTest_stock).text
    soup_wb_stock = BS(html_text_wb,"lxml")

    pd.DataFrame([getForeignFundInfo(soup_wb_info)])
    pd.DataFrame(getForeignShareHolding(html_wb_stock)[0])

    # [網頁](http://mmafund.sinopac.com/w/wb/wb04.djhtm?a=ANZ45-A28)
