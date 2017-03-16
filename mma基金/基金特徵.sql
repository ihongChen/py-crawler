USE external 
---------------------------------------------------------------------------------------------------------------------------------
--- 基金基本資料 ---
--- 建立正確的datatype ---
---------------------------------------------------------------------------------------------------------------------------------
select 	
	fundid,
	境內外,
	基金名稱,
	基金公司,
	-- 基金成立日期yyyymmdd ---
	case when 成立日期 like '%年%' then left(成立日期,4) 
		when 成立日期 = 'N/A' then NULL
		else left(成立日期,4) end as yyyy,
	case 	when 成立日期 = 'N/A' then NULL
		when 成立日期 not like '%月%' and left(成立日期,7) not like '%月%' then substring(成立日期,6,2) 
		when left(成立日期,7) not like '%月%' then substring(成立日期,6,2)
		else '0' + substring(成立日期,6,1) end as mm,
	case when 成立日期 = 'N/A' then NULL
		when 成立日期 not like '%月%' and left(成立日期,7) not like '%日%' then substring(成立日期,9,2)
		when right(成立日期,3) not like '%月%' then substring(right(成立日期,3),1,2)
		else '0'+ substring(right(成立日期,3),2,1) end as dd,	
	-- 基金規模 ---
	case when 基金規模 = 'N/A' then NULL
		when 基金規模  like '%台幣%' then convert(decimal(10,2),replace(replace(基金規模,'台幣',''),right(replace(基金規模,'台幣',''),12),''))
		when 基金規模  like '%(%' then replace(基金規模,right(基金規模,17),'')
		else replace(基金規模,right(基金規模,5),'') end as [基金規模(原幣)],
	case when 計價幣別 <> '台幣' then '百萬' + 計價幣別 else '台幣(億)' end as 基金規模計價幣別,	
	case when left(成立時規模,3)='N/A' then NULL
		when right(成立時規模,4) like '%(%)%' then convert(decimal(10,2),replace(成立時規模,right(成立時規模,4),''))
		else replace(成立時規模,right(成立時規模,5),'') end as [成立時規模(原幣)],
	case when 成立時規模 like '%台幣%' then  '台幣' 
		when 成立時規模 like '%人民幣%'  then '人民幣'
		when 成立時規模 like '%南非幣%'  then '南非幣'
		when 成立時規模 like '%澳幣%'  then '澳幣'
		when 成立時規模 like '%歐元%'  then '歐元'
		when 成立時規模 like '%美元%'  then '美元'
		else NULL end as [成立時規模計價幣別(億)],
	-- 基金評等 --
	convert(decimal(3,1),基金評等) as 嘉實資訊基金評等,
	基金經理人,
	基金類型,
	保管機構,
	主要投資區域,
	投資區域,
	投資標的,
	傘狀基金,
	台灣總代理,
	指標指數,
	計價幣別,
	註冊地,
	海外發行公司,
	投資策略,
	更新時間
into #基金基本資料
from dbo.MMA基金基本資料

select 
	fundid as FundID,
	[嘉實資訊基金評等],
	境內外,
	基金名稱,
	基金公司,
	convert(datetime,yyyy+mm+dd) as  '基金成立時間',
	[基金規模(原幣)],
	[基金規模計價幣別],
	[成立時規模(原幣)],
	[成立時規模計價幣別(億)],
	[基金經理人],
	[基金類型],
	[保管機構],
	[主要投資區域],
	[投資區域],
	[投資標的],
	[傘狀基金],
	[台灣總代理],
	[指標指數],
	[計價幣別],
	[註冊地],
	[海外發行公司],
	[投資策略],
	[更新時間]
into MMA基金基本資料2
from #基金基本資料

select top 10 * from MMA基金基本資料2
select distinct 基金類型 from MMA基金基本資料2

select 基金名稱, 投資策略  from MMA基金基本資料2
where 投資策略  like '%%'


---------------------------------------------------------------------------------------------------------------------------------
-- 投資哪種產業 ???-- 
-- 取出基金投資，產業別中前三名 ---
---------------------------------------------------------------------------------------------------------------------------------

select t1.fundID, 
	t1.項目,
	convert(int,t1.[投資金額(萬)]) 金額,
	count(*) 排名
into 基金投資產業分類
from MMA基金持股狀況_分類 t1
	join MMA基金持股狀況_分類 t2
		on t1.fundID = t2.fundID 
			and (convert(int,t2.[投資金額(萬)]) >= convert(int,t1.[投資金額(萬)]))
			and t2.fundID < = t1.fundID
where t1.分類= '產業'  and t2.分類= '產業'
group by t1.fundid,t1.項目, t1.[投資金額(萬)]
having count(*) <= 3
order by t1.fundid,排名

-- 整理成--- > 基金投資產業排序1,

select fundid,
	max(case when 排名=1 then 項目 else null end) as 基金投資產業分類1,
	max(case when 排名=2 then 項目 else null end) as 基金投資產業分類2,
	max(case when 排名=3 then 項目 else null end) as 基金投資產業分類3
into #基金投資產業分類2
from #基金投資產業分類 
group by FUNDID

--- 
select * 
-- into MMA基金基本資料_含投資產業別	
from MMA基金基本資料2 a
	left join #基金投資產業分類2 b 
		on a.FundID = b.fundid

---------------------------------------------------------------------------------------------------------------------------------
---- 投資哪個區域 -- 
---------------------------------------------------------------------------------------------------------------------------------
select t1.fundID, 
	t1.項目,
	convert(int,t1.[投資金額(萬)]) 金額,
	count(*) 排名
into #基金投資區域分類
from MMA基金持股狀況_分類 t1
	join MMA基金持股狀況_分類 t2
		on t1.fundID = t2.fundID 
			and (convert(int,t2.[投資金額(萬)]) >= convert(int,t1.[投資金額(萬)]))
			and t2.fundID < = t1.fundID
where t1.分類= '區域'  and t2.分類= '區域'
group by t1.fundid,t1.項目, t1.[投資金額(萬)]
having count(*) <= 3
order by t1.fundid,排名

-- 拉皮
select fundid,
	max(case when 排名=1 then 項目 else null end) as 基金投資區域分類1,
	max(case when 排名=2 then 項目 else null end) as 基金投資區域分類2,
	max(case when 排名=3 then 項目 else null end) as 基金投資區域分類3
into #基金投資區域分類2
from #基金投資區域分類 
group by FUNDID



---------------------------------------------------------------------------------------------------------------------------------
---- 投資哪個類股 -- 
---------------------------------------------------------------------------------------------------------------------------------
select t1.fundID, 
	t1.項目,
	convert(int,t1.[投資金額(萬)]) 金額,
	count(*) 排名
into #基金投資類股分類
from MMA基金持股狀況_分類 t1
	join MMA基金持股狀況_分類 t2
		on t1.fundID = t2.fundID 
			and (convert(int,t2.[投資金額(萬)]) >= convert(int,t1.[投資金額(萬)]))
			and t2.fundID < = t1.fundID
where t1.分類= '持有類股'  and t2.分類= '持有類股'
group by t1.fundid,t1.項目, t1.[投資金額(萬)]
having count(*) <= 3
order by t1.fundid,排名

-- 拉皮
select fundid,
	max(case when 排名=1 then 項目 else null end) as 基金投資類股分類1,
	max(case when 排名=2 then 項目 else null end) as 基金投資類股分類2,
	max(case when 排名=3 then 項目 else null end) as 基金投資類股分類3
into #基金投資類股分類2
from #基金投資類股分類 
group by FUNDID



--test ---
-- select * from MMA基金持股狀況_分類 a
-- 	left join #基金投資產業分類2 b on a.fundid=b.fundid
-- where 分類 = '持有類股'
select * from #基金投資類股分類2


---------------------------------------------------------------------------------------------------------------------------------
--- 將投資產業分類/區域分類/類股分類 ----- 整理成 < MMA基金基本資料_含投資標的細項>
---------------------------------------------------------------------------------------------------------------------------------
select a.*,
	b.基金投資產業分類1,
	b.基金投資產業分類2,
	b.基金投資產業分類3,
	c.基金投資區域分類1,
	c.基金投資區域分類2,
	c.基金投資區域分類3,
	d.基金投資類股分類1,
	d.基金投資類股分類2,
	d.基金投資類股分類3
into external.dbo.MMA基金基本資料_含投資標的細項
from 
dbo.MMA基金基本資料2 a
left join #基金投資產業分類2 b
	on a.fundid = b.fundid
	left join #基金投資區域分類2 c
		on c.fundid = a.fundid
		left join  #基金投資類股分類2 d
			on d.fundid = a.fundid


select * from dbo.MMA基金基本資料_含投資標的細項
select * from dbo.MMA基金績效走勢

---------------------------------------------------------------------------------------------------------------------------------
--- 建立 view 
---------------------------------------------------------------------------------------------------------------------------------

ALTER  VIEW v_MMA基金資訊 as
SELECT 
	RIGHT(a.fundID,3) [基金代碼],	
	a.*,
	b.[比較基金(或指數)],
	b.[年化標準差(%)],
	case when left(b.Sharpe,3) = 'N/A' then NULL else convert(decimal(5,2),b.[Sharpe]) end as [Sharpe],
	case when left(b.[Beta],3) = 'N/A' then NULL 	else convert(decimal(5,2),b.[Beta]) end as [Beta],	
	case when left(b.淨值,3) = 'N/A' then NULL 
		when b.淨值 like '%,%' then convert(decimal(15,2),replace(b.[淨值],',','')) 
		else convert(decimal(15,2),b.[淨值]) end as [淨值],
	replace(b.[淨值日期],'/','') as 淨值日期,
	case when left(b.[一個月累積報酬率(%)],3)='N/A' then NULL 
		else convert(decimal(5,2),b.[一個月累積報酬率(%)]) end as [一個月累積報酬率(%)],
	case when left(b.[三個月累積報酬率(%)],3)='N/A' then NULL 
		else convert(decimal(5,2),b.[三個月累積報酬率(%)]) end as [三個月累積報酬率(%)],
	case when left(b.[六個月累積報酬率(%)],3)='N/A' then NULL 
		else convert(decimal(5,2),b.[六個月累積報酬率(%)]) end as [六個月累積報酬率(%)],
	case when left(b.[一年累積報酬率(%)],3)='N/A' then NULL 
		else convert(decimal(5,2),b.[一年累積報酬率(%)]) end as [一年累積報酬率(%)],
	case when left(b.[二年累積報酬率(%)],3)='N/A' then NULL 
		else convert(decimal(5,2),b.[二年累積報酬率(%)]) end as [二年累積報酬率(%)],
	case when left(b.[三年累積報酬率(%)],3)='N/A' then NULL 
		else convert(decimal(5,2),b.[三年累積報酬率(%)]) end as [三年累積報酬率(%)],
	case when left(b.[五年累積報酬率(%)],3)='N/A' then NULL 
		else convert(decimal(5,2),b.[五年累積報酬率(%)]) end as [五年累積報酬率(%)],
	case when left(b.[自今年以來報酬率(%)],3)='N/A' then NULL 
		else convert(decimal(10,2),b.[自今年以來報酬率(%)]) end as [自今年以來報酬率(%)],
	case when left(b.[自成立日起報酬率(%)],3)='N/A' then NULL 
		when [自成立日起報酬率(%)] like '%,%' then convert(decimal(10,2), replace(b.[自成立日起報酬率(%)],',',''))
		else convert(decimal(10,2),b.[自成立日起報酬率(%)]) end as [自成立日起報酬率(%)]
-- 	b.[三個月累積報酬率(%)],
-- 	b.[六個月累積報酬率(%)],
-- 	b.[一年累積報酬率(%)],
-- 	b.[二年累積報酬率(%)],
-- 	b.[三年累積報酬率(%)],
-- 	b.[五年累積報酬率(%)],
-- 	b.[自今年以來報酬率(%)],
-- 	b.[自成立日起報酬率(%)]
FROM dbo.MMA基金基本資料_含投資標的細項 a
LEFT JOIN MMA基金績效走勢 b  
	on a.fundID = b.fundID





---------------------------------------------------------------------------------------------------------------------------------
------ 投資狀況分類 ---
-- 國外: 看投資標的 (股票型/能源/公司債/...) 基金類型(單一國家型/全球型/區域型)
-- 國內: 看基金類型(不動產證券化型/全球組合型平衡型/全球組合型其他/...)
---------------------------------------------------------------------------------------------------------------------------------



select 投資標的,基金類型 from MMA基金基本資料
where 
	境內外 = '國內'
-- 投資策略 like '%能源%'
-- 投資標的 like '%公司債券%'
-- 基金類型 like '%能源%'

select 投資標的,
	投資策略,
	基金類型,
	* 
from MMA基金基本資料
where 投資標的 like '%公司債券%'
----

select * from MMA基金持股狀況_分類
where fundid = 'ACAI27-268'




order by convert(int,[投資金額(萬)]) DESC

select top 10 * from MMA基金持股狀況_分類
where fundID = 'JFZB5-J0V'
order by convert(int,[投資金額(萬)]) DESC

select top 10 * from MMA基金基本資料2
where fundID = 'JFZB5-J0V'
------ 基金規模----

select 	
	case when 基金規模 = 'N/A' then NULL
		when 基金規模  like '%台幣%' then convert(decimal(10,2),replace(replace(基金規模,'台幣',''),right(replace(基金規模,'台幣',''),12),''))
		when 基金規模  like '%(%' then replace(基金規模,right(基金規模,17),'')
		else replace(基金規模,right(基金規模,5),'') end as [基金規模(原幣)],
	case when 計價幣別 <> '台幣' then '百萬' + 計價幣別 else '台幣(億)' end as 基金規模計價幣別,	
	基金規模	
from external.dbo.MMA基金基本資料

--成立時規模

select 
	case when left(成立時規模,3)='N/A' then NULL
		when right(成立時規模,4) like '%(%)%' then convert(decimal(10,2),replace(成立時規模,right(成立時規模,4),''))
		else replace(成立時規模,right(成立時規模,5),'') end as [成立時規模(原幣)],
	case when 成立時規模 like '%台幣%' then  '台幣' 
		when 成立時規模 like '%人民幣%'  then '人民幣'
		when 成立時規模 like '%南非幣%'  then '南非幣'
		when 成立時規模 like '%澳幣%'  then '澳幣'
		when 成立時規模 like '%歐元%'  then '歐元'
		when 成立時規模 like '%美元%'  then '美元'
		else NULL end as [成立時規模計價幣別(億)],
	成立時規模		
from external.dbo.MMA基金基本資料

select distinct right(成立時規模,4) from external.dbo.MMA基金基本資料


---- MMA績效走勢-淨值日期 -----

select 
	case when replace(淨值日期,'/','') ='' then NULL
	else replace(淨值日期,'/','') end as  [淨值日期yyyymmdd],
	[年化標準差(%)],
	case when left([年化標準差(%)],3) = 'N/A' then NULL else convert(decimal(10,2),[年化標準差(%)]) end as [年化標準差2(%)],
	*
from MMA基金績效走勢


select top 100 * from dbo.MMA基金持股狀況_個股


select top 100 * from external.dbo.MMA基金績效走勢


ALTER VIEW v_MMA基金資訊 as
SELECT 
	RIGHT(a.fundID,3) [基金代碼],	
	a.*,
-- 	c.[台股績效(%)],
-- 	c.[操作績效(%)],
-- 	c.時間,
-- 	c.[期間(月)],
	b.[比較基金(或指數)],
	b.[年化標準差(%)],
	b.[Sharpe],
	b.[Beta],
	b.[淨值],
	b.[淨值日期],
	b.[一個月累積報酬率(%)],
	b.[三個月累積報酬率(%)],
	b.[六個月累積報酬率(%)],
	b.[一年累積報酬率(%)],
	b.[二年累積報酬率(%)],
	b.[三年累積報酬率(%)],
	b.[五年累積報酬率(%)],
	b.[自今年以來報酬率(%)],
	b.[自成立日起報酬率(%)]
FROM dbo.MMA基金基本資料 a
LEFT JOIN MMA基金績效走勢 b  
	on a.fundID = b.fundID
-- 	LEFT JOIN MMA國內基金歷任經理人 c
-- 		on b.fundID = c.fundID










select distinct 投資標的 from MMA基金基本資料
select top 10 * from dbo.MMA基金績效走勢

select * from dbo.MMA基金基本資料 a
	left join dbo.MMA基金績效走勢 b 
		on a.fundid = b.fundid
where right(a.fundid,3) in ('MU7','L17','72C','F24','J07','H03')

select top 10 * from MMA基金基本資料
where fundid = 'ACFH03-H03'

---- 經理人績效----
select b.[基金名稱],[操作績效(%)],[六個月累積報酬率(%)],[三年累積報酬率(%)],[五年累積報酬率(%)],* from 
external.dbo.MMA國內基金歷任經理人 a
	left join MMA基金基本資料 b 
		on a.fundID = b.fundID
	left join MMA基金績效走勢 c
		on c.fundID = b.fundID			
where right(時間,2) = '至今'
order by convert(decimal(5,2),[操作績效(%)]) desc



select convert(VARCHAR(6),getdate(),112)
select top 10 * from 

--VIEW-- 基金基本資料(含經理人經營績效) ---

select * from v_MMA基金資訊 
select * from dbo.MMA基金績效走勢


select top 100 投資標的,* from v_MMA基金資訊 
where 境內外= '境外' and 投資標的 in ('天然資源','中小型股','金融股')


select 基金代碼,* from v_MMA基金資訊 order by 基金代碼
-----
select * from v_MMA基金資訊 a
	left join db_wm.dbo.v_fund b
		on a.基金代碼= b.基金代碼


--- AC0001-K23
select * from 
dbo.MMA國內基金持股狀況_分類
where fundID = 'AC0001-K23' 
order by convert(int,[投資金額(萬元)]) desc

declare @ch_date varchar(12) 
-- set @ch_date = '2016年9月5日'
select @ch_date = '2016年9月5日'

select convert(varchar(20),left(@ch_date,4) + substring(@ch_date,6,7))

select *,
	case when 成立日期 like ('%年%') then '0' else 成立日期 end as [成立日期-1]
from external.dbo.MMA基金基本資料

select top 10 * from external.dbo.MMA基金基本資料

--- db基金資訊 --
select top 10 * from db_wm.dbo.v_fund where 刪單註記 = 0
select top 100
	基金代碼,
	商品投資屬性,
	基金中文名稱,
	區域別,
	國內外基金註記,
	b.*
from db_wm.dbo.v_fund a
	left join MMA基金基本資料 b
		on a.基金代碼= right(b.fundid,3)

--- db最熱門基金 -- 

select  
	基金中文名稱,
	count(*),
	sum(庫存基金原始投資金額) 
from DB_WM.dbo.v_庫存基金存量分析 
where DB分類='a.一般身分' and YYYYMM > '201603' 
group by 基金中文名稱 order by 2 desc



select a.基金中文名稱 ,
	b.* 
from DB_WM.dbo.v_庫存基金存量分析 a
	left join external.dbo.v_MMA基金資訊 b on a.基金代碼= b.基金代碼


--- 基金資料(MMA + WM) ----
select * from external.dbo.v_MMA基金資訊 a
	left join DB_WM.dbo.v_Fund b
		on a.基金代碼 = b.基金代碼
where (時間 like '%至今%' or 時間 is NULL )



--- 	