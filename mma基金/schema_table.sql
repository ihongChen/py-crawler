USE External 

---  基金資料(整併國內外) -----
-- 基本資料 --
CREATE TABLE MMA基金基本資料 (
	fundID VARCHAR(15) not null primary key,
	境內外	VARCHAR(4) not null,
	基金名稱 NVARCHAR(500),
	基金公司 VARCHAR(100),
	成立日期 VARCHAR(100),
	基金經理人 VARCHAR(100),
	基金規模 VARCHAR(100),
	成立時規模 VARCHAR(100),
	基金類型 VARCHAR(100),
	保管機構 VARCHAR(100),
	主要投資區域 NVARCHAR(500),
	投資區域 NVARCHAR(500),
	基金評等 VARCHAR(4),
	投資標的 NVARCHAR(1000),
	傘狀基金 VARCHAR(4),
	台灣總代理 VARCHAR(50),
	指標指數 VARCHAR(500),
	計價幣別 VARCHAR(10),
	註冊地 VARCHAR(20),
	海外發行公司 VARCHAR(100),
	投資策略 NVARCHAR(2000)
)

alter table MMA基金基本資料 
add 投資策略 NVARCHAR(2000)

-- 基金持股狀況
CREATE TABLE MMA基金持股狀況_個股 (
	
	fundID VARCHAR(15) NOT NULL,
	[增減] VARCHAR(10),
	[持股(千股)] VARCHAR(10),
	[比例] VARCHAR(5),
	[持股名稱] nVARCHAR(100),
	[資料月份] VARCHAR(8)
	CONSTRAINT [UK_mma_stock] UNIQUE CLUSTERED
 	(
        	fundID,持股名稱,資料月份
	)	
)


CREATE TABLE MMA基金持股狀況_分類(

	fundID VARCHAR(15) NOT NULL,
	[分類] VARCHAR(8) NOT NULL,
	[投資金額(萬)] VARCHAR(10),
	[幣別] VARCHAR(4),
	[資料日期] VARCHAR(10),
	[項目] VARCHAR(50)
	CONSTRAINT [UK_mma_share] UNIQUE CLUSTERED
 	(
        	fundid,分類,項目,資料日期
	)
)




--- 國內--

CREATE TABLE MMA國內基金基本資料 (
	fundID VARCHAR(15) not null primary key,
	主要投資區域 nVARCHAR(500),
	保管銀行 VARCHAR(100),
	基金公司 VARCHAR(100),
	基金名稱 nVARCHAR(500) not null,
	基金經理人 VARCHAR(100),
	[基金規模(億)] VARCHAR(100),
	基金評等 VARCHAR(4),
	基金類型 VARCHAR(100),
	成立日期 VARCHAR(100),
	[成立時規模(億)] VARCHAR(100),
	投資區域 nVARCHAR(500),
	投資標的 nVARCHAR(1000)
)


CREATE TABLE MMA國內基金歷任經理人(
	
	fundID VARCHAR(15) NOT NULL,
	[台股績效(%)] VARCHAR(10),
	[操作績效(%)] VARCHAR(10),
	[時間] VARCHAR(100),
	[期間(月)] VARCHAR(100),
	[現任基金] nVARCHAR(3000),
	[經理人] VARCHAR(100)
	CONSTRAINT [UK_mmafund_manager] UNIQUE CLUSTERED
 	(
        	fundID,時間,經理人
	)
)


CREATE TABLE MMA國內基金持股狀況_個股 (
	
	fundID VARCHAR(15) NOT NULL,
	[增減] VARCHAR(10),
	[持股(千股)] VARCHAR(10),
	[比例] VARCHAR(5),
	[股票名稱] nVARCHAR(100),
	[資料月份] VARCHAR(8)
	CONSTRAINT [UK_mmafund_stock] UNIQUE CLUSTERED
 	(
        	fundID,股票名稱
	)
	
)


CREATE TABLE MMA國內基金持股狀況_分類(

	fundID VARCHAR(15) NOT NULL,
	[分類] VARCHAR(8) NOT NULL,
	[投資金額(萬元)] VARCHAR(10),
	[資料日期] VARCHAR(10),
	[項目] VARCHAR(50)
	CONSTRAINT [UK_mmafund_share] UNIQUE CLUSTERED
 	(
        	fundid,分類,項目
	)
)

--- 境外 ----

CREATE TABLE [MMA境外基金基本資料] (

	fundID VARCHAR(15) not null primary key ,
	保管機構 VARCHAR(200),
	傘狀基金 VARCHAR(4),
	台灣總代理 VARCHAR(50),
	基金名稱 nVARCHAR(500),
	基金英文名稱 VARCHAR(200),
	基金規模 VARCHAR(50),
	基金評等 VARCHAR(4),
	基金類型 VARCHAR(50),
	成立日期 CHAR(10),
	投資區域 VARCHAR(50),
	投資標的 VARCHAR(50),
	投資策略 nVARCHAR(2000),
	指標指數 VARCHAR(500),
	海外發行公司 VARCHAR(100),
	經理人 VARCHAR(500),
	計價幣別 VARCHAR(10),
	註冊地 VARCHAR(20)

)



CREATE TABLE [MMA境外基金持股狀況_個股] (

	fundID VARCHAR(15),
	持股名稱 VARCHAR(200),
	比例 VARCHAR(8),
	資料月份 VARCHAR(10),
	CONSTRAINT [UK_mma_wstock] UNIQUE CLUSTERED
 	(
        	[fundID], [持股名稱]
	)
)


CREATE TABLE [MMA境外基金持股狀況_分類] (

	fundID VARCHAR(15),
	分類 VARCHAR(10),
	[投資金額(美元:萬)] VARCHAR(10),
	資料日期 VARCHAR(10),
	項目 VARCHAR(50),
	CONSTRAINT [UK_mma_wshare] UNIQUE CLUSTERED
 	(
        	[fundID], [分類],[項目]
	)
)



------ 更改schema--- 合併國內外基金

CREATE TABLE MMA基金基本資料 (
	fundID VARCHAR(15) not null primary key,
	主要投資區域 nVARCHAR(500),
	保管銀行 VARCHAR(100),
	基金公司 VARCHAR(100),
	基金名稱 nVARCHAR(500) not null,
	基金經理人 VARCHAR(100),
	[基金規模(億)] VARCHAR(100),
	基金評等 VARCHAR(4),
	基金類型 VARCHAR(100),
	成立日期 VARCHAR(100),
	[成立時規模(億)] VARCHAR(100),
	投資區域 nVARCHAR(500),
	投資標的 nVARCHAR(1000)
)




--------------------------------------------------------------------------------------------
---- TEST --
--------------------------------------------------------------------------------------------
Drop table MMA境外基金持股狀況_分類

SELECT * FROM MMA國內基金歷任經理人
SELECT * FROM MMA國內基金基本資料
SELECT top 10 * FROM MMA國內基金持股狀況_個股 
SELECT top 10 * FROM MMA國內基金持股狀況_分類

SELECT * FROM MMA境外基金基本資料
SELECT * FROM MMA境外基金持股狀況_個股
SELECT * FROM MMA境外基金持股狀況_分類




SELECT * FROM MMA基金基本資料
SELECT * FROM MMA基金持股狀況_個股
SELECT * FROM MMA基金持股狀況_分類