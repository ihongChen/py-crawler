USE external 

---- 國內基金基本資料(含經理人經營績效) ---
SELECT top 100 
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


---- 投資狀況 ---
SELECT DISTINCT 項目 FROM dbo.MMA國內基金持股狀況_分類
-- ORDER BY convert(float,[投資金額(萬元)]) DESC
WHERE 分類= '產業'
投資金額(萬元)


SELECT top 10 * FROM dbo.MMA境外基金基本資料
SELECT distinct 分類 FROM
dbo.MMA境外基金持股狀況_分類

SELECT distinct 分類 FROM dbo.MMA境外基金持股狀況_分類