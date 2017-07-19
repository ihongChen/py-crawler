#! encoding = utf8
# %%
# %%

def dataToDb(data_dict,table,con):
    """利用dict資料格式(配合pypyodbc)寫入tsql-2000 
               
    ### params
    
    inputs : 
        * `data_dict` : dict or defaultdict 
        * `table` : 寫入的table name
        * `con`   : 透過pypyodbc.connect 建立成功的連線

    output : 
        * None
    """
    if data_dict:        
        cursor = con.cursor()
        sql_insert = """INSERT INTO {0}({1}) VALUES ({2})"""
        # sql_delete = """DELETE FROM {} WHERE fundID = '{}' """      

        try:
            df = pd.DataFrame(data_dict)
        except ValueError as e:
            df = pd.DataFrame([data_dict])
        # keyList = list(df.columns)
        
        ## 轉成 list of dict 格式 : [{'col1':'val11','col2':'val12',...},
        ##                              {'col1','val21','col2':'val22',...},...]
        ## 以此格式塞進db

        dataSets = list(df.T.to_dict().values())
        for index, row in enumerate(dataSets):
            # row data
            # :{'postid':'xxx','content':'xx','nametitle':'xx','type':'xx','created_time':'xx'}

            fields = '['+'],['.join(row.keys()) + ']'
            values = list(row.values())
            num_quest = '?' + ',?' * (len(row.keys())-1)
            try:
                cursor.execute(sql_insert.format(table,fields,num_quest), values)

            except pypyodbc.IntegrityError:
                pass
                # fundid = row['fundid'][0] if type(row['fundid'])==list else row['fundid']
                # cursor.execute(sql_delete.format(table,fundid)) 
                # cursor.execute(sql_insert.format(table,fields,num_quest),list(row.values()))

        # print("oops~資料更新嚕!!")
        cursor.close()
        con.commit()


def getFundStar(starTag):
    '''取得基金評等數字(影像<星星>標記 --> 數字)

    params
    ======
    input:
        starTag: 含有星號圖案的bs4 tag
    output: 
        基金評等(int)
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


def getDomesticFundBasicInfo(fundid):
    """取得(國內)基金基本資料
    
    params
    ======
    input:
        fundid
    output : 
        OrderedDict => {'fundid': 'ACUS03-UN2','投資區域': '台灣',
                            '保管機構': '中國信託銀行','基金公司': '永豐投信',...}
    """
    #### fundid ####
    # fundid = re.findall(r'(?:a=)(.+)',soup.select('#itemTab')[0].find('a').get('href'))[0]
    ################
    url_dom_base = 'http://mmafund.sinopac.com/w/wr/wr01.djhtm?a='
    r = requests.get(url_dom_base + fundid)
    soup = BS(r.text,"lxml")
    
    info_colName = [
        'fundid',
        '基金名稱',
        '基金公司',
        '成立日期',
        '基金經理人',
        '基金規模',
        '成立時規模',
        '基金類型',
        '保管機構',
        '投資產業',
        # '主要投資區域', 
        '投資區域',
        '基金評等',
        '投資標的',
        '基金統編', # 新增
        '配息頻率' # 新增
    ]

    fieldList = [fundid]

    if soup.select('.just-tb-v-4'):
        fieldsname = [e.text for e in soup.select('.just-tb-v-4')[0].find_all('td')]
        
        fields = fieldsname[0:8]
        fields.extend([
            fieldsname[-7],
            fieldsname[-8],
            getFundStar(soup.select('small a')[0]),
            fieldsname[-2],
            fieldsname[-6],
            fieldsname[-5]
            ])
        fields.insert(0,fundid)

        dataList = list(zip(info_colName,fields)) 
        dataList.insert(1,('境內外','國內'))
        
        
        dataDict = defaultdict(list)
        ## 將資料格式轉換為 defaultdict ##
        for k,v in dataList:
            dataDict[k] = v
        dataDict['計價幣別'] = '台幣'
        dataDict['更新時間'] = pd.datetime.today()
        return dataDict



def getDomesticStockHolding(fundid,soup):
    """取得國內持股資料中股票張數(表格)
    params 
    ======
    input: 
    * fundid - 國內基金編號 (嘉實id- 永豐id)
    * soup - html經BS包裝後變數, 
            
    output: 
    * defaultdict {增減:[],
                            持股名稱:[],
                            持股(千股):[],
                            比例:[],
                            資料月份,[]}
    """
    ### 資料月份 ###
    
    

    ###############
    
    def parseElement(e):
        """利用此函數剖析持股狀態中(境內)表格元素
        """
        row1 = []; row2=[];
        for index,field in enumerate(e.select('td')):        
            if index > 3:
                row2.append(field.text.strip())
            else:
                row1.append(field.text.strip())
        return row1,row2
    
    
    ######## 資料月份 ##########
    try:
        update_dateStr = soup.select('h4')[-1].text
        update_temp = re.findall(r'\d+',update_dateStr)
        tableSoup = soup.select('.just-tb-h') 

        if update_temp and tableSoup:
            update_date = '/'.join(update_temp)
            date_colname = '資料月份'
            
            
            ###########################
            
            
            fundShareTableList = []
            rowData = {}
            
            
            for index,e in enumerate(tableSoup[0].select('tr')[1:-1]):
                colnames = []
                # if index == 0:
                col1 = [                    
                        '股票名稱',
                        '持股(千股)',
                        '比例',
                        '增減',
                        'fundID',
                        '資料月份'
                        ]
                col2 = col1
                
                row1,row2 = parseElement(e)
                row1+=[fundid,update_date]
                row2+=[fundid,update_date]
                
                fundShareTableList.append(list(zip(col1,row1))) 
                fundShareTableList.append(list(zip(col2,row2)))
            # print(fundShareTableList)
            ### 輸出成dict格式 ##
            stocks_dict = defaultdict(list)
            for row in fundShareTableList:
                for name,value in row:    
                    stocks_dict[name].append(value)
            try :
                stock_name = stocks_dict.pop('股票名稱') ## 更名 : 股票名稱 -> 持股名稱
                stocks_dict['持股名稱'] = stock_name
            except KeyError: ## 沒有此資料
                pass
            finally:
                stocks_dict['更新時間'] = pd.datetime.today()
                return stocks_dict
    except IndexError:
        pass # 沒資料傳回None

def getForeignFundInfo(fundid):
    """取得境外基金基本資訊
    ======
    ### params
    
    input : 
        * fundid ('嘉實id-永豐id')
    output: 
        * defaultDict --> {'fundid':xxxx, '保管機構'}
    """

    url_fund_foreign = 'http://mmafund.sinopac.com/w/wb/wb01.djhtm?a=' + fundid
    soup = BS(requests.get(url_fund_foreign).text,"lxml")

    colNames = [
        'fundid',
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
        # '投資標的', # 無
        'ISIN_CODE', # 新增
        '配息頻率', # 新增
        '保管機構',
        '傘狀基金',
        '基金經理人',
        '基金評等',    
        '投資策略'    
    ]
    if soup.select('.just-tb-v-4'):
        fieldsname = [e.text.strip() for e in soup.select('.just-tb-v-4')[0].find_all('td')] 

        fields = fieldsname[0:7]
        
        fields.extend(fieldsname[9:13])
        fields.extend(fieldsname[-11:-7]) #
        fields.append(fieldsname[-6]) # 經理人
        fields.append(getFundStar(soup.select('small a')[0])) #基金評等
        fields.append(fieldsname[-3]) #投資策略
        
        fields.insert(0,fundid)
        
        dataList = list(zip(colNames,fields))

        # foreign_fund = dataList.pop(2) ## 剔除英文基金名稱

        fundInfo_dict = defaultdict(list)
        fundInfo_dict['fundid'] = fundid
        for name,v in dataList:
            fundInfo_dict[name] = v
        fundInfo_dict['境內外'] = '境外'
        fundInfo_dict['更新時間'] = pd.datetime.today()
        return fundInfo_dict


def getForeignStockHolding(fundid,soup):
    
    """取得[境外]持股資料中股票張數(表格)
    params 
    ======
    input: soup --- html經BS包裝後變數
            fundid --- 基金id (嘉實id-永豐id)

    output: defaultdict {持股名稱:[],
                            fundid:[],                            
                            比例:[],
                            資料月份,[]}
    
    """
    
    
    
    ### 資料月份 ###
    
    try:
        update_dateStr = soup.select('h4')[-1].text
        update_temp = re.findall(r'\d+',update_dateStr)

        if update_temp:
            update_date = '/'.join(update_temp)
            # print('資料月份:{}'.format(update_date))
            
            
            keys = [e.text for e in soup.select('tbody')[0].select('.text-left')]
            values_str = [e.text.strip() for e in soup.select('tbody')[0].select('.text-right')]
            values = [float(re.findall(r'(.+)(?:%)',e)[0]) for e in values_str] 
    
            colNames = ['持股名稱','比例']
            foreignStockDict = defaultdict(list)
            foreignStockDict['資料月份'] = update_date
            foreignStockDict['fundID'] = fundid
    
            dataList = [keys,values]
            for index,data in enumerate(dataList):
                foreignStockDict[colNames[index]] = list(data)
            # print(foreignStockDict)
            foreignStockDict['更新時間'] = pd.datetime.today()
            return foreignStockDict
    except IndexError:
        pass


    
    

def getShareHolding(fundid,html_text, domestic_tag = True):
    """取得國內(外)持股資料(圓餅圖)
    =====
    剖析mma中html含有js程式碼，資料隱藏在js其中
    
    params
    =====
    `input` :     
         * `html_text` : raw text(str)

    `output` : 
        * list of defaultdict
    """
    def getShareHoldingTable(stockGroupList):
        """轉換國內持股圓餅圖資料(getDomesticShareHolding)為dict格式(pd.dataframe可直接使用)    
        """
        stockGroup = defaultdict(list)
        for index,(k,v) in enumerate(stockGroupList):

            if index >1:
                stockGroup['項目'].append(k) 
                stockGroup['投資金額(萬)'].append(v)
            else:
                stockGroup[k] = v                
        return stockGroup

    
    soup = BS(html_text,"lxml")    
    # print('fundid:{}'.format(fundid))

    ##### 取得 欄位名稱, 資料日期 ####
    update_dateSoup = soup.select('h4')        
        
    update_dateList = [] # 存資料更新日期(list)
    colname_list = []
    try:
        last_check = re.findall(r'資料月份',update_dateSoup[-1].text) ## 
        if last_check:
            dataSoup = update_dateSoup[:-1] # 排除最後一張table標題(表格欄)
        else :
            dataSoup = update_dateSoup ## 無表格全取
            
        for date_soup in dataSoup: 
            ### 取得更新日期
            update_date = re.findall(r'\d+',date_soup.text)
            update_dateStr = '-'.join(update_date)
            update_dateList.append(update_dateStr) 
    
            ### 取得欄位名稱
            try:
                colname = re.findall(r"區域|產業|持股", date_soup.text)[-1]
                colname_list.append(colname)
            except IndexError :
                break
    
    
        if update_dateList and colname_list:                
            #######################
            string1 = 'DJGraphObj1' # 切出目標字串    
            target_text = html_text[html_text.index(string1):]
            
            pat1 = r"(?:[^//]\'Title\':)(.+)" # 忽略//,只抓Title:之後的資料
            investTitle = re.findall(pat1,target_text) # 取得並切分表單table
                   
            pat2 = r"(?:\')(.*?)(?:\')" # 取出包含在 ' '內的字串
            pat3 = r"(?:\'PieV\':)(.+)" # 取出包含在 PieV 後的字串
            
            table = defaultdict(list)
            tableAns = [] ; idx = 0
            for index,titleText in enumerate(investTitle):
                titleList = re.findall(pat2,titleText)
                
                if len(titleList)==1 :
                    continue
    
                titleList.pop(0)
                titleList.insert(0,'fundid')
                titleList.insert(1,'資料日期')
    
                valueList = re.findall(pat2,re.findall(pat3,target_text)[index])
                valueList.insert(0,fundid)
                valueList.insert(1,update_dateList[idx]) #
                # print(titleList,valueList)
    
                table[colname_list[idx]]= list(zip(titleList,valueList))
                
                share_Holding_dict = getShareHoldingTable(table[colname_list[idx]])
    
                if domestic_tag :                      
                    share_Holding_dict['幣別'] = '台幣'
                else:
                    share_Holding_dict['幣別'] = '美金'
                
                share_Holding_dict['分類'] = colname_list[idx]
                share_Holding_dict['更新時間'] = pd.datetime.today()
    
                tableAns.append(share_Holding_dict)
    
                idx += 1
    
            return tableAns
        
    except IndexError:
        pass

def getPerformance(fundid):
    '''取得基金績效指數            
    ======
    input: fundid

    output:  dict-> {FundID:xxx, 比較基金:xxxx, ....}
    '''
    url = 'http://mmafund.sinopac.com/w/wr/wr03.djhtm?a=' + fundid
    html = requests.get(url).text
    soup = BS(html,'lxml')

    ## 第一個table ##
    values = [e.text for e in soup.select('table')[0].select('td')]    
    keys = [e.text for e in soup.select('table')[0].select('th')]
    
    fund_pref = { k:v for k,v in zip(keys,values)}
    fund_pref.pop('基金')
    fund_pref['FundID'] = fundid

    # beta = fund_pref.pop('b')
    # fund_pref['Beta'] = beta
    pat_compare_fund = r'(?:＊)(.+)(?:＊)'

    compare_index = re.findall(pat_compare_fund,html)[0]
    fund_pref['比較基金(或指數)'] = compare_index

    ## 第二個table ##
    fund_hist_perf = [e.text for e in soup.select('table')[1].select('td')]
    fund_hist_perf.pop(0)
    fund_hist_perf.insert(0,fundid)

    colnames = [e.text for e in soup.select('table')[1].select('th')]
    colnames.pop(0)
    colnames.insert(0,'FundID')

    for k,v in zip(colnames,fund_hist_perf):
        fund_pref[k] = v
    
    # fund_pref['一個月累積報酬率(%)'] = fund_pref.pop('一個月') 
    # fund_pref['三個月累積報酬率(%)'] = fund_pref.pop('三個月') 
    # fund_pref['六個月累積報酬率(%)'] = fund_pref.pop('六個月') 
    # fund_pref['一年累積報酬率(%)'] = fund_pref.pop('一年') 
    # fund_pref['二年累積報酬率(%)'] = fund_pref.pop('二年') 
    # fund_pref['三年累積報酬率(%)'] = fund_pref.pop('三年') 

    fund_pref['更新時間'] = pd.datetime.today()

    return fund_pref

def parseFunds(funds_ListOfJson):
        """解析json基金格式
        ====

        `input`:
            * list of json format

        `output`:
             * list of fundids ('嘉實id'-'永豐id')        
        """
        fundids = []
        for agent in funds_ListOfJson:        
            for fund in agent['child']:
                sinopac_id = fund['bid'] # 永豐銀基金id
                sysJust_id = fund['sid'] # 嘉實資訊基金id
                fundid = sysJust_id + '-' + sinopac_id 
                fundids.append(fundid)
        return fundids



if __name__ == '__main__':

    ##### library ########
    from bs4 import BeautifulSoup as BS
    from collections import defaultdict,OrderedDict
    import pandas as pd
    import requests
    import re
    import pypyodbc

    ##### 基金id清單 ######
    url_fundids = 'http://mmafund.sinopac.com/wData/djjson/fundlistJson.djjson?P1=sinopac&P2=False&P3=False&P4=False&P5=1'
    json_ids = requests.get(url_fundids).json()
    domestic_idsets = json_ids.get('ResultSet')['Result'][0]
    foreign_idsets = json_ids.get('ResultSet')['Result'][1]
    fundids =[]
    
    
    domestic_ids = parseFunds(domestic_idsets)
    foreign_ids = parseFunds(foreign_idsets)
    print('國內基金數:',len(domestic_ids))
    print('國外基金數:',len(foreign_ids))
    
    con = pypyodbc.connect("DRIVER={SQL Server};SERVER=dbm_public;UID=sa;PWD=01060728;DATABASE=External")


    ### 國內基金 ##
    # fundidsList = parseFunds(domestic_idsets)
    # ## 取得國內基金基本資料/持股狀況(個股/各分類)/績效走勢 ##
    # url_dom_stock_base = 'http://mmafund.sinopac.com/w/wr/wr04.djhtm?a=' # 持股url

    # for no,fundid in enumerate(fundidsList[162:]):
            
    #     html_domestic_stock = requests.get(url_dom_stock_base + fundid).text
    #     soup_domestic_stock = BS(html_domestic_stock,"lxml") 

    #     fundInfo_domestic = getDomesticFundBasicInfo(fundid) ## 國內基金資訊 
        
    #     fundStock_domestic = getDomesticStockHolding(fundid,soup_domestic_stock) ## 國內基金持股(表格)
    #     fundShare_domestic = getShareHolding(fundid, html_domestic_stock, domestic_tag = True)  ## 國內基金圓餅圖(數量)

    #     fundPerformance = getPerformance(fundid)

    #     dataToDb(fundInfo_domestic,'[MMA基金基本資料_v2]',con)    
    #     dataToDb(fundStock_domestic, '[MMA基金持股狀況_個股_v2]', con)
    #     dataToDb(fundPerformance, '[MMA基金績效走勢_v2]', con)

    #     if fundShare_domestic: 

    #         for index,fundShare in enumerate(fundShare_domestic):
                
    #             dataToDb(fundShare, '[MMA基金持股狀況_分類_v2]', con) 

    #         print('No.{} 國內基金: {} updated....'.format(no+1,fundid)) 

    print('====================='*2)


    ###### 境外基金 #######
    wfundidsList = parseFunds(foreign_idsets)

    ## 取得境外基金 ##
    url_foreign_base = 'http://mmafund.sinopac.com/w/wb/'
    
    for no,wfundid in enumerate(wfundidsList[807:]):
        html_foreign_info = requests.get(url_foreign_base + 'wb01.djhtm?a=' + wfundid).text
        soup_foreign_info = BS(html_foreign_info,"lxml") 

        html_foreign_stock = requests.get(url_foreign_base + 'wb04.djhtm?a=' + wfundid).text
        soup_foreign_stock = BS(html_foreign_stock,"lxml") 

        fundInfo_foreign = getForeignFundInfo(wfundid) ## 國外基金資訊
        fundStock_foreign = getForeignStockHolding(wfundid,soup_foreign_stock) ## 國外基金持股(表格)
        fundShare_foreign = getShareHolding(wfundid,html_foreign_stock,domestic_tag=False) ## 國外基金持股圓餅圖
        wfundPerformance = getPerformance(wfundid) ## 基金績效

        dataToDb(fundInfo_foreign, '[MMA基金基本資料_v2]', con)
        dataToDb(fundStock_foreign, '[MMA基金持股狀況_個股_v2]', con)
        dataToDb(wfundPerformance, '[MMA基金績效走勢_v2]', con)


        if fundShare_foreign:
            for index, wfundShare in enumerate(fundShare_foreign):                
                dataToDb(wfundShare, '[MMA基金持股狀況_分類_v2]', con) 
                

        print('NO.{} 境外基金: {} updated....'.format(no+1,wfundid))

