# coding: utf-8
## MMA基金資料 ##

import requests
import pandas as pd
import re
import pypyodbc
from bs4 import BeautifulSoup as BS
from collections import defaultdict
requests.packages.urllib3.disable_warnings()  # disable warning insecure
import pdb

def dictToDb(data_dict,table,con):
    """ 利用dict資料格式(配合pypyodbc)寫入tsql-2000
    
    資料若有重複(判斷fundID),先刪除資料再插入
    
    params
    ======
    inputs : 
        data_dict : dict or defaultdict 
        table : 寫入的table name
        con   : 透過pypyodbc.connect 建立成功的連線
    output : None
    """
    if data_dict:        
        cursor = con.cursor()
        sql_insert = """INSERT INTO {} VALUES ({})"""
        sql_delete = """DELETE FROM {} WHERE fundID = '{}' """
        try:
            df = pd.DataFrame(data_dict)
        except ValueError as e:
            df = pd.DataFrame([data_dict])
        keyList = list(df.columns)
        
        quest = '?' + ',?'*(df.shape[1]-1)
        for e in list(df.T.to_dict().values()):
            try:
                cursor.execute(sql_insert.format(table,quest),list(e.values()))

            except pypyodbc.IntegrityError:
                fundid = e['fundid'][0] if type(e['fundid'])==list else e['fundid']
                cursor.execute(sql_delete.format(table,e['fundid']))
                cursor.execute(sql_insert.format(table,quest),list(e.values()))
        # print("oops~資料更新嚕!!")
        cursor.close()
        con.commit()

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
    # print('星星幾顆:{}'.format(starNum))
    return starNum

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
    update_temp = re.findall(r'\d+/\d+',update_dateStr)

    if update_temp:
        update_date = update_temp[0]
        date_colname = '資料月份'
        # print(date_colname,update_date)
        
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
    # print('fundid:{}'.format(fundid))
    ##### 取得 資料日期 ####
    date_temp = soup.select('.wfb1ar')
    if date_temp:
        try:
            update_dateStr = re.findall(r"\d+\/\d+\/\d+",soup.select('.wfb1ar')[-1].text)[0] # xx分布--資料日期
        except IndexError:
            update_date = re.findall(r'\d+/\d+',date_temp[-1].text)[0] ## 年/月
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
            table[colname]= list(zip(titleList,valueList))
            
            share_Holding_dict = getShareHoldingTable(table[colname])
            
            
            typeName = ['持有類股','區域','產業']
            share_Holding_dict['分類'] = typeName[index]
            
            tableAns.append(share_Holding_dict)
        return tableAns

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
        # print(row)
    if managerDict['經理人'] == ['查無資料']:
        return None
    return managerDict

def getFundBasicInfo(soup):
    """
    取得()基金基本資料
    
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

def getForeignShareHolding(html_text_wb):
    """取得境外持股資料(圓餅圖)
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
    
    soup = BS(html_text_wb,"lxml")
    date_temp = soup.select('.wfb1ar')
    if date_temp:
        update_date = '/'.join(re.findall(r"\d+",soup.select('.wfb1ar')[0].text)) ## 資料更新日期
        
        ### fundid ####
        fundid = re.findall(r"(?:a=)(.+)",soup.select('#itemTab')[0].find('a').get('href'))[0]
        fundid = fundid.strip()
        ###############
        
        string1 = 'DJGraphObj1' # 切出目標字串    
        target_text = html_text_wb[html_text_wb.index(string1):]

        pat1 = r"(?:\'Title\':)(.+\')(?:])"
        investTitle = re.findall(pat1,target_text) # 取得並切分表單table

        pat2 = r"(?:\')(.*?)(?:\')" # 取出包含在 ' '內的字串
        pat3 = r"(?:\'PieV\':)(.+)" # 取出包含在 PieV 後的字串
        #     investTitleByStock = re.findall(pat2,investTitle[0]) ## 依產業標題(List)
        #     investTitleByStock
        table = defaultdict(list)
        tableAns = []
        # pdb.set_trace()
        for index,titleText in enumerate(investTitle):

            titleList = re.findall(pat2,titleText)
            if len(titleList) == 1 :
                continue
            colname = titleList[0]
            titleList = titleList[1:]
            titleList.insert(0,'fundid')
            titleList.insert(1,'資料日期')
            valueList = re.findall(pat2,re.findall(pat3,target_text)[index])
            valueList.insert(0,fundid)
            valueList.insert(1,update_date)
            
            table[colname]= list(zip(titleList,valueList))
            
            typeName = ['持有類股','區域','產業']
            share_Holding_Dict = getShareHoldingTable(table[colname])
            share_Holding_Dict['分類'] = typeName[index]
            
            tableAns.append(share_Holding_Dict)
            
        return tableAns

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
    fundid = fundid.strip()
    ### 資料月份 ###
    
    date_temp = soup.select('.wfb1ar')
    data_temp = soup.select('.wfb2l')
    if date_temp and data_temp:
        update_date = '/'.join(re.findall(r"\d+",date_temp[-1].text)) ## 資料月份
        # print('資料月份:{}'.format(update_date))
        
        a = list(zip(soup.select('.wfb2l'),soup.select('.wfb2r')))
        b = list(zip(soup.select('.wfb5l'),soup.select('.wfb5r')))
        dataList = zip(*[(e1.text,e2.text.strip()) for (e1,e2) in a+b]) # [(k1,k2,k3),(v1,v2,v3...)]
        
        colNames = ['持股名稱','比例']
        foreignStockDict = defaultdict(list)
        foreignStockDict['資料月份'] = update_date
        foreignStockDict['fundid'] = fundid
        for index,data in enumerate(dataList):
            foreignStockDict[colNames[index]] = list(data)
        # print(foreignStockDict)

        return foreignStockDict

def getForeignFundInfo(soup):
    """取得境外基金基本資訊
    params
    ======
    input : soup (BeautifulSoup)
    output : defaultdict --> {'fundid':xxxx, '保管機構'}
    """
    ## fundid ##
    fundid = re.findall(r"(?:a=)(.+)",soup.select('#itemTab')[0].find('a').get('href'))[0]
    
    fieldSoup = soup.select('.wfb5l')
    if fieldSoup:
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



if __name__ == '__main__':

    ## 連結database ## 
    con = pypyodbc.connect("DRIVER={SQL Server};SERVER=dbm_public;UID=sa;PWD=01060728;DATABASE=External")
    
    ##### 基金id清單 ######
    # 國內
    url_fundid= 'http://mmafund.sinopac.com/w/js/WtFundlistJS.djjs'
    html_fundids = requests.get(url_fundid).text

    fundids_Str = re.findall(r"(?:g_TFundList = ')(.+)(?:\')",html_fundids)[0]
    fundDict = defaultdict(list) ## 國內基金清單變數 => key: 基金id(fundid), value: 基金名(name)
    for index,nameStr in enumerate(re.split(r";|!",fundids_Str)):
        if index != 0:
            fundid,name = nameStr.split(',')
            if '-' in fundid:

                fundDict[fundid] = name 
    
    print('MMA基金數:{}'.format(len(fundDict)))


    # 境外
    url_f_fund = 'http://mmafund.sinopac.com/w/js/WFundlistJS.djjs'
    html_ffundids = requests.get(url_f_fund).text


    wfundids_Str = re.findall(r"(?:g_WFundList = ')(.+)(?:\')",html_ffundids)[0]
    wfundDict = defaultdict(list) ## 境外基金清單變數 => key: 基金id(wfundid), value: 基金名(name)
    for index,nameStr in enumerate(re.split(r";|!",wfundids_Str)):
        if index != 0:
            wfundid,name = nameStr.split(',')
            if '-' in wfundid:
                wfundDict[wfundid] = name

    print('MMA境外基金數:{}'.format(len(wfundDict)))
    print('=================='*2)
    
    ## 國內基金 ##
    # fundidsList = list(fundDict.keys())
    # ## 取得國內基金基本資料/經理人資料/持股狀況(個股/各分類) ##
    # url_domestic_base = 'http://mmafund.sinopac.com/w/wr/'
    # for no,fundid in enumerate(fundidsList):
    #     html_domestic_info = requests.get(url_domestic_base + 'wr01.djhtm?a=' + fundid).text
    #     soup_domestic_info = BS(html_domestic_info,"lxml")

    #     html_domestic_stock = requests.get(url_domestic_base + 'wr04.djhtm?a=' + fundid).text
    #     soup_domestic_stock = BS(html_domestic_stock,"lxml")

    #     fundInfo_domestic = getFundBasicInfo(soup_domestic_info) 
    #     fundManager_domestic = getFundManager(soup_domestic_info)

    #     fundStock_domestic = getDomesticStockHolding(soup_domestic_stock) 
    #     fundShare_domestic = getDomesticShareHolding(html_domestic_stock)

    #     dictToDb(fundInfo_domestic,'[MMA國內基金基本資料]',con)
    #     dictToDb(fundManager_domestic,'[MMA國內基金歷任經理人]',con)

    #     dictToDb(fundStock_domestic, '[MMA國內基金持股狀況_個股]', con)

    #     if fundShare_domestic:

    #         for index,fundShare in enumerate(fundShare_domestic):
    #             dictToDb(fundShare, '[MMA國內基金持股狀況_分類]', con)

    #         print('No.{} 國內基金: {} updated....'.format(no+1,fundid))

    ## 境外基金 ## 
    wfundidsList = list(wfundDict.keys())
    ## 取得境外基金 ##
    url_foreign_base = 'http://mmafund.sinopac.com/w/wb/'
    for no,wfundid in enumerate(wfundidsList):
        html_foreign_info = requests.get(url_foreign_base + 'wb01.djhtm?a=' + wfundid).text
        soup_foreign_info = BS(html_foreign_info,"lxml")

        html_foreign_stock = requests.get(url_foreign_base + 'wb04.djhtm?a=' + wfundid).text
        soup_foreign_stock = BS(html_foreign_stock,"lxml")

        fundInfo_foreign = getForeignFundInfo(soup_foreign_info)        
        fundStock_foreign = getForeignStockHolding(soup_foreign_stock)
        fundShare_foreign = getForeignShareHolding(html_foreign_stock)

        dictToDb(fundInfo_foreign, '[MMA境外基金基本資料]', con)
        dictToDb(fundStock_foreign, '[MMA境外基金持股狀況_個股]', con)

        if fundShare_foreign:
            for index, wfundShare in enumerate(fundShare_foreign):                
                dictToDb(wfundShare, '[MMA境外基金持股狀況_分類]', con)

        print('NO.{} 境外基金: {} updated....'.format(no+1,wfundid))

    

