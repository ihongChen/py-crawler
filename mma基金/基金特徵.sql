USE external 

---- �ꤺ����򥻸��(�t�g�z�H�g���Z��) ---
SELECT top 100 
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


---- ��ꪬ�p ---
SELECT DISTINCT ���� FROM dbo.MMA�ꤺ������Ѫ��p_����
-- ORDER BY convert(float,[�����B(�U��)]) DESC
WHERE ����= '���~'
�����B(�U��)


SELECT top 10 * FROM dbo.MMA�ҥ~����򥻸��
SELECT distinct ���� FROM
dbo.MMA�ҥ~������Ѫ��p_����

SELECT distinct ���� FROM dbo.MMA�ҥ~������Ѫ��p_����