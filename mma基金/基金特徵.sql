USE external 
drop view MMA�����T

---
select top 100 * from MMA�ꤺ����򥻸�� a
	left join MMA�ꤺ��������g�z�H b on a.fundID = b.fundID
---- �ꤺ����򥻸��(�t�g�z�H�g���Z��) ---
ALTER VIEW v_MMA�����T as
SELECT top 10 
	RIGHT(a.fundID,3) [����N�X],	
	a.*,
	b.[�x���Z��(%)],
	b.[�ާ@�Z��(%)],
	b.�ɶ�,
	b.[����(��)]
FROM dbo.MMA�ꤺ����򥻸�� a
LEFT JOIN MMA�ꤺ��������g�z�H b
	on a.fundID = b.fundID
WHERE a.����g�z�H = b.�g�z�H






select distinct ����N�X from v_MMA�����T
select ����N�X,* from v_MMA�����T order by ����N�X
-----
select * from v_MMA�����T a
	left join db_wm.dbo.v_fund b
		on a.����N�X= b.����N�X


--- AC0001-K23
select * from 
dbo.MMA�ꤺ������Ѫ��p_����
where fundID = 'AC0001-K23' 
order by convert(int,[�����B(�U��)]) desc




---- ��ꪬ�p ---
SELECT DISTINCT ���� FROM dbo.MMA�ꤺ������Ѫ��p_����
-- ORDER BY convert(float,[�����B(�U��)]) DESC
WHERE ����= '���~'
�����B(�U��)


SELECT top 10 * FROM dbo.MMA�ҥ~����򥻸��
SELECT distinct ���� FROM
dbo.MMA�ҥ~������Ѫ��p_����

SELECT distinct ���� FROM dbo.MMA�ҥ~������Ѫ��p_����


select top 10 * from db_wm.dbo.v_fund where �R����O = 0


--- �t�γ̼������ -- 

select top 100 
	�������W��,
	count(*),
	sum(�w�s�����l�����B) 
from DB_WM.dbo.v_�w�s����s�q���R 
where DB����='a.�@�먭��' and YYYYMM > '201603' 
group by �������W�� order by 2 desc
