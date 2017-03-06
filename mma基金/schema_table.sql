USE External 
--- �ꤺ--

drop table MMA�ꤺ����򥻸��
CREATE TABLE MMA�ꤺ����򥻸�� (
	fundID CHAR(15) not null primary key,
	�D�n���ϰ� nVARCHAR(500),
	�O�޻Ȧ� VARCHAR(100),
	������q VARCHAR(100),
	����W�� nVARCHAR(500) not null,
	����g�z�H VARCHAR(100),
	[����W��(��)] VARCHAR(100),
	������� decimal(3,1),
	������� VARCHAR(100),
	���ߤ�� VARCHAR(100),
	[���߮ɳW��(��)] VARCHAR(100),
	���ϰ� nVARCHAR(500),
	���Ъ� nVARCHAR(1000)
)




CREATE TABLE MMA�ꤺ��������g�z�H(
	
	fundID CHAR(15) NOT NULL,
	[�x���Z��(%)] VARCHAR(10),
	[�ާ@�Z��(%)] VARCHAR(10),
	[�ɶ�] VARCHAR(100),
	[����(��)] VARCHAR(100),
	[�{�����] nVARCHAR(3000),
	[�g�z�H] VARCHAR(100)
)



CREATE TABLE MMA�ꤺ������Ѫ��p_�Ӫ� (
	
	fundID CHAR(15) NOT NULL,
	[�W��] VARCHAR(10),
	[����(�d��)] VARCHAR(10),
	[���] CHAR(5),
	[�Ѳ��W��] nVARCHAR(100),
	[��Ƥ��] CHAR(8)
	CONSTRAINT [UK_mmafund_stock] UNIQUE CLUSTERED
 	(
        	fundID,��Ƥ��,�Ѳ��W��
	)
	
)

drop table MMA�ꤺ������Ѫ��p_�Ӫ�


CREATE TABLE MMA�ꤺ������Ѫ��p_����(

	fundID CHAR(15) NOT NULL,
	[����] VARCHAR(8) NOT NULL,
	[�����B(�U��)] VARCHAR(10),
	[��Ƥ��] VARCHAR(10),
	[����] VARCHAR(50)
	CONSTRAINT [UK_mmafund_share] UNIQUE CLUSTERED
 	(
        	fundid,��Ƥ��,����,����
	)
	
)
drop table MMA�ꤺ������Ѫ��p_����
--- �ҥ~ ----

CREATE TABLE [MMA�ҥ~����򥻸��] (

	fundID CHAR(15) not null primary key ,
	�O�޾��c VARCHAR(200),
	�ʪ���� CHAR(2),
	�x�W�`�N�z VARCHAR(50),
	����W�� nVARCHAR(500),
	����^��W�� VARCHAR(200),
	����W�� VARCHAR(50),
	������� DECIMAL(2,1),
	������� VARCHAR(50),
	���ߤ�� CHAR(10),
	���ϰ� VARCHAR(50),
	���Ъ� VARCHAR(50),
	��굦�� nVARCHAR(2000),
	���Ы��� VARCHAR(500),
	���~�o�椽�q VARCHAR(100),
	�g�z�H VARCHAR(500),
	�p�����O VARCHAR(10),
	���U�a VARCHAR(20)

)
drop table MMA�ҥ~����򥻸��


CREATE TABLE [MMA�ҥ~������Ѫ��p_�Ӫ�] (

	fundID CHAR(15),
	���ѦW�� VARCHAR(100),
	��� CHAR(8),
	��Ƥ�� CHAR(10),
	CONSTRAINT [UK_mma_wstock] UNIQUE CLUSTERED
 	(
        	[fundID], [���ѦW��], [��Ƥ��]
	)
)
drop table MMA�ҥ~������Ѫ��p_�Ӫ�

CREATE TABLE [MMA�ҥ~������Ѫ��p_����] (

	fundID CHAR(15),
	���� VARCHAR(10),
	[�����B(����:�U)] VARCHAR(10),
	��Ƥ�� CHAR(10),
	���� VARCHAR(50),
	CONSTRAINT [UK_mma_wshare] UNIQUE CLUSTERED
 	(
        	[fundID], [����], [��Ƥ��],[����]
	)
)

drop table MMA�ҥ~������Ѫ��p_����


--------------------------------------------------------------------------------------------
---- TEST --
--------------------------------------------------------------------------------------------


SELECT * FROM MMA�ꤺ��������g�z�H
SELECT * FROM MMA�ꤺ����򥻸��
SELECT * FROM MMA�ꤺ������Ѫ��p_�Ӫ� 
SELECT * FROM MMA�ꤺ������Ѫ��p_����

SELECT * FROM MMA�ҥ~����򥻸��
SELECT * FROM MMA�ҥ~������Ѫ��p_�Ӫ�
SELECT * FROM MMA�ҥ~������Ѫ��p_����





alter table MMA�ꤺ��������g�z�H
-- alter column [�ާ@�Z��(%)] VARCHAR(10)
alter column [�x���Z��(%)] VARCHAR(10)