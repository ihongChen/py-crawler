USE external 
drop view MMA基金資訊

---
select top 100 * from MMA國內基金基本資料 a
	left join MMA國內基金歷任經理人 b on a.fundID = b.fundID
---- 國內基金基本資料(含經理人經營績效) ---
ALTER VIEW v_MMA基金資訊 as
SELECT top 10 
	RIGHT(a.fundID,3) [基金代碼],	
	a.*,
	b.[台股績效(%)],
	b.[操作績效(%)],
	b.時間,
	b.[期間(月)]
FROM dbo.MMA國內基金基本資料 a
LEFT JOIN MMA國內基金歷任經理人 b
	on a.fundID = b.fundID
WHERE a.基金經理人 = b.經理人






select distinct 基金代碼 from v_MMA基金資訊
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




---- 投資狀況 ---
SELECT DISTINCT 項目 FROM dbo.MMA國內基金持股狀況_分類
-- ORDER BY convert(float,[投資金額(萬元)]) DESC
WHERE 分類= '產業'
投資金額(萬元)


SELECT top 10 * FROM dbo.MMA境外基金基本資料
SELECT distinct 分類 FROM
dbo.MMA境外基金持股狀況_分類

SELECT distinct 分類 FROM dbo.MMA境外基金持股狀況_分類


select top 10 * from db_wm.dbo.v_fund where 刪單註記 = 0


--- 系統最熱門基金 -- 

select top 100 
	基金中文名稱,
	count(*),
	sum(庫存基金原始投資金額) 
from DB_WM.dbo.v_庫存基金存量分析 
where DB分類='a.一般身分' and YYYYMM > '201603' 
group by 基金中文名稱 order by 2 desc
