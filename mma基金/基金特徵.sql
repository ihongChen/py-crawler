USE external 
---------------------------------------------------------------------------------------------------------------------------------
--- ����򥻸�� ---
--- �إߥ��T��datatype ---
---------------------------------------------------------------------------------------------------------------------------------
select 	
	fundid,
	�Ҥ��~,
	����W��,
	������q,
	-- ������ߤ��yyyymmdd ---
	case when ���ߤ�� like '%�~%' then left(���ߤ��,4) 
		when ���ߤ�� = 'N/A' then NULL
		else left(���ߤ��,4) end as yyyy,
	case 	when ���ߤ�� = 'N/A' then NULL
		when ���ߤ�� not like '%��%' and left(���ߤ��,7) not like '%��%' then substring(���ߤ��,6,2) 
		when left(���ߤ��,7) not like '%��%' then substring(���ߤ��,6,2)
		else '0' + substring(���ߤ��,6,1) end as mm,
	case when ���ߤ�� = 'N/A' then NULL
		when ���ߤ�� not like '%��%' and left(���ߤ��,7) not like '%��%' then substring(���ߤ��,9,2)
		when right(���ߤ��,3) not like '%��%' then substring(right(���ߤ��,3),1,2)
		else '0'+ substring(right(���ߤ��,3),2,1) end as dd,	
	-- ����W�� ---
	case when ����W�� = 'N/A' then NULL
		when ����W��  like '%�x��%' then convert(decimal(10,2),replace(replace(����W��,'�x��',''),right(replace(����W��,'�x��',''),12),''))
		when ����W��  like '%(%' then replace(����W��,right(����W��,17),'')
		else replace(����W��,right(����W��,5),'') end as [����W��(���)],
	case when �p�����O <> '�x��' then '�ʸU' + �p�����O else '�x��(��)' end as ����W�ҭp�����O,	
	case when left(���߮ɳW��,3)='N/A' then NULL
		when right(���߮ɳW��,4) like '%(%)%' then convert(decimal(10,2),replace(���߮ɳW��,right(���߮ɳW��,4),''))
		else replace(���߮ɳW��,right(���߮ɳW��,5),'') end as [���߮ɳW��(���)],
	case when ���߮ɳW�� like '%�x��%' then  '�x��' 
		when ���߮ɳW�� like '%�H����%'  then '�H����'
		when ���߮ɳW�� like '%�n�D��%'  then '�n�D��'
		when ���߮ɳW�� like '%�D��%'  then '�D��'
		when ���߮ɳW�� like '%�ڤ�%'  then '�ڤ�'
		when ���߮ɳW�� like '%����%'  then '����'
		else NULL end as [���߮ɳW�ҭp�����O(��)],
	-- ������� --
	convert(decimal(3,1),�������) as �Ź��T�������,
	����g�z�H,
	�������,
	�O�޾��c,
	�D�n���ϰ�,
	���ϰ�,
	���Ъ�,
	�ʪ����,
	�x�W�`�N�z,
	���Ы���,
	�p�����O,
	���U�a,
	���~�o�椽�q,
	��굦��,
	��s�ɶ�
into #����򥻸��
from dbo.MMA����򥻸��

select 
	fundid as FundID,
	[�Ź��T�������],
	�Ҥ��~,
	����W��,
	������q,
	convert(datetime,yyyy+mm+dd) as  '������߮ɶ�',
	[����W��(���)],
	[����W�ҭp�����O],
	[���߮ɳW��(���)],
	[���߮ɳW�ҭp�����O(��)],
	[����g�z�H],
	[�������],
	[�O�޾��c],
	[�D�n���ϰ�],
	[���ϰ�],
	[���Ъ�],
	[�ʪ����],
	[�x�W�`�N�z],
	[���Ы���],
	[�p�����O],
	[���U�a],
	[���~�o�椽�q],
	[��굦��],
	[��s�ɶ�]
into MMA����򥻸��2
from #����򥻸��

select top 10 * from MMA����򥻸��2
select distinct ������� from MMA����򥻸��2

select ����W��, ��굦��  from MMA����򥻸��2
where ��굦��  like '%%'


---------------------------------------------------------------------------------------------------------------------------------
-- �����ز��~ ???-- 
-- ���X������A���~�O���e�T�W ---
---------------------------------------------------------------------------------------------------------------------------------

select t1.fundID, 
	t1.����,
	convert(int,t1.[�����B(�U)]) ���B,
	count(*) �ƦW
into �����겣�~����
from MMA������Ѫ��p_���� t1
	join MMA������Ѫ��p_���� t2
		on t1.fundID = t2.fundID 
			and (convert(int,t2.[�����B(�U)]) >= convert(int,t1.[�����B(�U)]))
			and t2.fundID < = t1.fundID
where t1.����= '���~'  and t2.����= '���~'
group by t1.fundid,t1.����, t1.[�����B(�U)]
having count(*) <= 3
order by t1.fundid,�ƦW

-- ��z��--- > �����겣�~�Ƨ�1,

select fundid,
	max(case when �ƦW=1 then ���� else null end) as �����겣�~����1,
	max(case when �ƦW=2 then ���� else null end) as �����겣�~����2,
	max(case when �ƦW=3 then ���� else null end) as �����겣�~����3
into #�����겣�~����2
from #�����겣�~���� 
group by FUNDID

--- 
select * 
-- into MMA����򥻸��_�t��겣�~�O	
from MMA����򥻸��2 a
	left join #�����겣�~����2 b 
		on a.FundID = b.fundid

---------------------------------------------------------------------------------------------------------------------------------
---- �����Ӱϰ� -- 
---------------------------------------------------------------------------------------------------------------------------------
select t1.fundID, 
	t1.����,
	convert(int,t1.[�����B(�U)]) ���B,
	count(*) �ƦW
into #������ϰ����
from MMA������Ѫ��p_���� t1
	join MMA������Ѫ��p_���� t2
		on t1.fundID = t2.fundID 
			and (convert(int,t2.[�����B(�U)]) >= convert(int,t1.[�����B(�U)]))
			and t2.fundID < = t1.fundID
where t1.����= '�ϰ�'  and t2.����= '�ϰ�'
group by t1.fundid,t1.����, t1.[�����B(�U)]
having count(*) <= 3
order by t1.fundid,�ƦW

-- �ԥ�
select fundid,
	max(case when �ƦW=1 then ���� else null end) as ������ϰ����1,
	max(case when �ƦW=2 then ���� else null end) as ������ϰ����2,
	max(case when �ƦW=3 then ���� else null end) as ������ϰ����3
into #������ϰ����2
from #������ϰ���� 
group by FUNDID



---------------------------------------------------------------------------------------------------------------------------------
---- ���������� -- 
---------------------------------------------------------------------------------------------------------------------------------
select t1.fundID, 
	t1.����,
	convert(int,t1.[�����B(�U)]) ���B,
	count(*) �ƦW
into #���������Ѥ���
from MMA������Ѫ��p_���� t1
	join MMA������Ѫ��p_���� t2
		on t1.fundID = t2.fundID 
			and (convert(int,t2.[�����B(�U)]) >= convert(int,t1.[�����B(�U)]))
			and t2.fundID < = t1.fundID
where t1.����= '��������'  and t2.����= '��������'
group by t1.fundid,t1.����, t1.[�����B(�U)]
having count(*) <= 3
order by t1.fundid,�ƦW

-- �ԥ�
select fundid,
	max(case when �ƦW=1 then ���� else null end) as ���������Ѥ���1,
	max(case when �ƦW=2 then ���� else null end) as ���������Ѥ���2,
	max(case when �ƦW=3 then ���� else null end) as ���������Ѥ���3
into #���������Ѥ���2
from #���������Ѥ��� 
group by FUNDID



--test ---
-- select * from MMA������Ѫ��p_���� a
-- 	left join #�����겣�~����2 b on a.fundid=b.fundid
-- where ���� = '��������'
select * from #���������Ѥ���2


---------------------------------------------------------------------------------------------------------------------------------
--- �N��겣�~����/�ϰ����/���Ѥ��� ----- ��z�� < MMA����򥻸��_�t���Ъ��Ӷ�>
---------------------------------------------------------------------------------------------------------------------------------
select a.*,
	b.�����겣�~����1,
	b.�����겣�~����2,
	b.�����겣�~����3,
	c.������ϰ����1,
	c.������ϰ����2,
	c.������ϰ����3,
	d.���������Ѥ���1,
	d.���������Ѥ���2,
	d.���������Ѥ���3
into external.dbo.MMA����򥻸��_�t���Ъ��Ӷ�
from 
dbo.MMA����򥻸��2 a
left join #�����겣�~����2 b
	on a.fundid = b.fundid
	left join #������ϰ����2 c
		on c.fundid = a.fundid
		left join  #���������Ѥ���2 d
			on d.fundid = a.fundid


select * from dbo.MMA����򥻸��_�t���Ъ��Ӷ�
select * from dbo.MMA����Z�Ĩ���

---------------------------------------------------------------------------------------------------------------------------------
--- �إ� view 
---------------------------------------------------------------------------------------------------------------------------------

ALTER  VIEW v_MMA�����T as
SELECT 
	RIGHT(a.fundID,3) [����N�X],	
	a.*,
	b.[������(�Ϋ���)],
	b.[�~�ƼзǮt(%)],
	case when left(b.Sharpe,3) = 'N/A' then NULL else convert(decimal(5,2),b.[Sharpe]) end as [Sharpe],
	case when left(b.[Beta],3) = 'N/A' then NULL 	else convert(decimal(5,2),b.[Beta]) end as [Beta],	
	case when left(b.�b��,3) = 'N/A' then NULL 
		when b.�b�� like '%,%' then convert(decimal(15,2),replace(b.[�b��],',','')) 
		else convert(decimal(15,2),b.[�b��]) end as [�b��],
	replace(b.[�b�Ȥ��],'/','') as �b�Ȥ��,
	case when left(b.[�@�Ӥ�ֿn���S�v(%)],3)='N/A' then NULL 
		else convert(decimal(5,2),b.[�@�Ӥ�ֿn���S�v(%)]) end as [�@�Ӥ�ֿn���S�v(%)],
	case when left(b.[�T�Ӥ�ֿn���S�v(%)],3)='N/A' then NULL 
		else convert(decimal(5,2),b.[�T�Ӥ�ֿn���S�v(%)]) end as [�T�Ӥ�ֿn���S�v(%)],
	case when left(b.[���Ӥ�ֿn���S�v(%)],3)='N/A' then NULL 
		else convert(decimal(5,2),b.[���Ӥ�ֿn���S�v(%)]) end as [���Ӥ�ֿn���S�v(%)],
	case when left(b.[�@�~�ֿn���S�v(%)],3)='N/A' then NULL 
		else convert(decimal(5,2),b.[�@�~�ֿn���S�v(%)]) end as [�@�~�ֿn���S�v(%)],
	case when left(b.[�G�~�ֿn���S�v(%)],3)='N/A' then NULL 
		else convert(decimal(5,2),b.[�G�~�ֿn���S�v(%)]) end as [�G�~�ֿn���S�v(%)],
	case when left(b.[�T�~�ֿn���S�v(%)],3)='N/A' then NULL 
		else convert(decimal(5,2),b.[�T�~�ֿn���S�v(%)]) end as [�T�~�ֿn���S�v(%)],
	case when left(b.[���~�ֿn���S�v(%)],3)='N/A' then NULL 
		else convert(decimal(5,2),b.[���~�ֿn���S�v(%)]) end as [���~�ֿn���S�v(%)],
	case when left(b.[�ۤ��~�H�ӳ��S�v(%)],3)='N/A' then NULL 
		else convert(decimal(10,2),b.[�ۤ��~�H�ӳ��S�v(%)]) end as [�ۤ��~�H�ӳ��S�v(%)],
	case when left(b.[�ۦ��ߤ�_���S�v(%)],3)='N/A' then NULL 
		when [�ۦ��ߤ�_���S�v(%)] like '%,%' then convert(decimal(10,2), replace(b.[�ۦ��ߤ�_���S�v(%)],',',''))
		else convert(decimal(10,2),b.[�ۦ��ߤ�_���S�v(%)]) end as [�ۦ��ߤ�_���S�v(%)]
-- 	b.[�T�Ӥ�ֿn���S�v(%)],
-- 	b.[���Ӥ�ֿn���S�v(%)],
-- 	b.[�@�~�ֿn���S�v(%)],
-- 	b.[�G�~�ֿn���S�v(%)],
-- 	b.[�T�~�ֿn���S�v(%)],
-- 	b.[���~�ֿn���S�v(%)],
-- 	b.[�ۤ��~�H�ӳ��S�v(%)],
-- 	b.[�ۦ��ߤ�_���S�v(%)]
FROM dbo.MMA����򥻸��_�t���Ъ��Ӷ� a
LEFT JOIN MMA����Z�Ĩ��� b  
	on a.fundID = b.fundID





---------------------------------------------------------------------------------------------------------------------------------
------ ��ꪬ�p���� ---
-- ��~: �ݧ��Ъ� (�Ѳ���/�෽/���q��/...) �������(��@��a��/���y��/�ϰ쫬)
-- �ꤺ: �ݰ������(���ʲ��Ҩ�ƫ�/���y�զX�����ū�/���y�զX����L/...)
---------------------------------------------------------------------------------------------------------------------------------



select ���Ъ�,������� from MMA����򥻸��
where 
	�Ҥ��~ = '�ꤺ'
-- ��굦�� like '%�෽%'
-- ���Ъ� like '%���q�Ũ�%'
-- ������� like '%�෽%'

select ���Ъ�,
	��굦��,
	�������,
	* 
from MMA����򥻸��
where ���Ъ� like '%���q�Ũ�%'
----

select * from MMA������Ѫ��p_����
where fundid = 'ACAI27-268'




order by convert(int,[�����B(�U)]) DESC

select top 10 * from MMA������Ѫ��p_����
where fundID = 'JFZB5-J0V'
order by convert(int,[�����B(�U)]) DESC

select top 10 * from MMA����򥻸��2
where fundID = 'JFZB5-J0V'
------ ����W��----

select 	
	case when ����W�� = 'N/A' then NULL
		when ����W��  like '%�x��%' then convert(decimal(10,2),replace(replace(����W��,'�x��',''),right(replace(����W��,'�x��',''),12),''))
		when ����W��  like '%(%' then replace(����W��,right(����W��,17),'')
		else replace(����W��,right(����W��,5),'') end as [����W��(���)],
	case when �p�����O <> '�x��' then '�ʸU' + �p�����O else '�x��(��)' end as ����W�ҭp�����O,	
	����W��	
from external.dbo.MMA����򥻸��

--���߮ɳW��

select 
	case when left(���߮ɳW��,3)='N/A' then NULL
		when right(���߮ɳW��,4) like '%(%)%' then convert(decimal(10,2),replace(���߮ɳW��,right(���߮ɳW��,4),''))
		else replace(���߮ɳW��,right(���߮ɳW��,5),'') end as [���߮ɳW��(���)],
	case when ���߮ɳW�� like '%�x��%' then  '�x��' 
		when ���߮ɳW�� like '%�H����%'  then '�H����'
		when ���߮ɳW�� like '%�n�D��%'  then '�n�D��'
		when ���߮ɳW�� like '%�D��%'  then '�D��'
		when ���߮ɳW�� like '%�ڤ�%'  then '�ڤ�'
		when ���߮ɳW�� like '%����%'  then '����'
		else NULL end as [���߮ɳW�ҭp�����O(��)],
	���߮ɳW��		
from external.dbo.MMA����򥻸��

select distinct right(���߮ɳW��,4) from external.dbo.MMA����򥻸��


---- MMA�Z�Ĩ���-�b�Ȥ�� -----

select 
	case when replace(�b�Ȥ��,'/','') ='' then NULL
	else replace(�b�Ȥ��,'/','') end as  [�b�Ȥ��yyyymmdd],
	[�~�ƼзǮt(%)],
	case when left([�~�ƼзǮt(%)],3) = 'N/A' then NULL else convert(decimal(10,2),[�~�ƼзǮt(%)]) end as [�~�ƼзǮt2(%)],
	*
from MMA����Z�Ĩ���


select top 100 * from dbo.MMA������Ѫ��p_�Ӫ�


select top 100 * from external.dbo.MMA����Z�Ĩ���


ALTER VIEW v_MMA�����T as
SELECT 
	RIGHT(a.fundID,3) [����N�X],	
	a.*,
-- 	c.[�x���Z��(%)],
-- 	c.[�ާ@�Z��(%)],
-- 	c.�ɶ�,
-- 	c.[����(��)],
	b.[������(�Ϋ���)],
	b.[�~�ƼзǮt(%)],
	b.[Sharpe],
	b.[Beta],
	b.[�b��],
	b.[�b�Ȥ��],
	b.[�@�Ӥ�ֿn���S�v(%)],
	b.[�T�Ӥ�ֿn���S�v(%)],
	b.[���Ӥ�ֿn���S�v(%)],
	b.[�@�~�ֿn���S�v(%)],
	b.[�G�~�ֿn���S�v(%)],
	b.[�T�~�ֿn���S�v(%)],
	b.[���~�ֿn���S�v(%)],
	b.[�ۤ��~�H�ӳ��S�v(%)],
	b.[�ۦ��ߤ�_���S�v(%)]
FROM dbo.MMA����򥻸�� a
LEFT JOIN MMA����Z�Ĩ��� b  
	on a.fundID = b.fundID
-- 	LEFT JOIN MMA�ꤺ��������g�z�H c
-- 		on b.fundID = c.fundID










select distinct ���Ъ� from MMA����򥻸��
select top 10 * from dbo.MMA����Z�Ĩ���

select * from dbo.MMA����򥻸�� a
	left join dbo.MMA����Z�Ĩ��� b 
		on a.fundid = b.fundid
where right(a.fundid,3) in ('MU7','L17','72C','F24','J07','H03')

select top 10 * from MMA����򥻸��
where fundid = 'ACFH03-H03'

---- �g�z�H�Z��----
select b.[����W��],[�ާ@�Z��(%)],[���Ӥ�ֿn���S�v(%)],[�T�~�ֿn���S�v(%)],[���~�ֿn���S�v(%)],* from 
external.dbo.MMA�ꤺ��������g�z�H a
	left join MMA����򥻸�� b 
		on a.fundID = b.fundID
	left join MMA����Z�Ĩ��� c
		on c.fundID = b.fundID			
where right(�ɶ�,2) = '�ܤ�'
order by convert(decimal(5,2),[�ާ@�Z��(%)]) desc



select convert(VARCHAR(6),getdate(),112)
select top 10 * from 

--VIEW-- ����򥻸��(�t�g�z�H�g���Z��) ---

select * from v_MMA�����T 
select * from dbo.MMA����Z�Ĩ���


select top 100 ���Ъ�,* from v_MMA�����T 
where �Ҥ��~= '�ҥ~' and ���Ъ� in ('�ѵM�귽','���p����','���Ī�')


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

declare @ch_date varchar(12) 
-- set @ch_date = '2016�~9��5��'
select @ch_date = '2016�~9��5��'

select convert(varchar(20),left(@ch_date,4) + substring(@ch_date,6,7))

select *,
	case when ���ߤ�� like ('%�~%') then '0' else ���ߤ�� end as [���ߤ��-1]
from external.dbo.MMA����򥻸��

select top 10 * from external.dbo.MMA����򥻸��

--- db�����T --
select top 10 * from db_wm.dbo.v_fund where �R����O = 0
select top 100
	����N�X,
	�ӫ~����ݩ�,
	�������W��,
	�ϰ�O,
	�ꤺ�~������O,
	b.*
from db_wm.dbo.v_fund a
	left join MMA����򥻸�� b
		on a.����N�X= right(b.fundid,3)

--- db�̼������ -- 

select  
	�������W��,
	count(*),
	sum(�w�s�����l�����B) 
from DB_WM.dbo.v_�w�s����s�q���R 
where DB����='a.�@�먭��' and YYYYMM > '201603' 
group by �������W�� order by 2 desc



select a.�������W�� ,
	b.* 
from DB_WM.dbo.v_�w�s����s�q���R a
	left join external.dbo.v_MMA�����T b on a.����N�X= b.����N�X


--- ������(MMA + WM) ----
select * from external.dbo.v_MMA�����T a
	left join DB_WM.dbo.v_Fund b
		on a.����N�X = b.����N�X
where (�ɶ� like '%�ܤ�%' or �ɶ� is NULL )



--- 	