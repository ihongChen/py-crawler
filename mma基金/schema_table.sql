USE External 

---  ������(��ְꤺ�~) -----
-- �򥻸�� --
CREATE TABLE MMA����򥻸�� (
	fundID VARCHAR(15) not null primary key,
	�Ҥ��~	VARCHAR(4) not null,
	����W�� NVARCHAR(500),
	������q VARCHAR(100),
	���ߤ�� VARCHAR(100),
	����g�z�H VARCHAR(100),
	����W�� VARCHAR(100),
	���߮ɳW�� VARCHAR(100),
	������� VARCHAR(100),
	�O�޾��c VARCHAR(100),
	�D�n���ϰ� NVARCHAR(500),
	���ϰ� NVARCHAR(500),
	������� VARCHAR(4),
	���Ъ� NVARCHAR(1000),
	�ʪ���� VARCHAR(4),
	�x�W�`�N�z VARCHAR(50),
	���Ы��� VARCHAR(500),
	�p�����O VARCHAR(10),
	���U�a VARCHAR(20),
	���~�o�椽�q VARCHAR(100),
	��굦�� NVARCHAR(2000)
)

alter table MMA����򥻸�� 
add ��굦�� NVARCHAR(2000)

-- ������Ѫ��p
CREATE TABLE MMA������Ѫ��p_�Ӫ� (
	
	fundID VARCHAR(15) NOT NULL,
	[�W��] VARCHAR(10),
	[����(�d��)] VARCHAR(10),
	[���] VARCHAR(5),
	[���ѦW��] nVARCHAR(100),
	[��Ƥ��] VARCHAR(8)
	CONSTRAINT [UK_mma_stock] UNIQUE CLUSTERED
 	(
        	fundID,���ѦW��,��Ƥ��
	)	
)


CREATE TABLE MMA������Ѫ��p_����(

	fundID VARCHAR(15) NOT NULL,
	[����] VARCHAR(8) NOT NULL,
	[�����B(�U)] VARCHAR(10),
	[���O] VARCHAR(4),
	[��Ƥ��] VARCHAR(10),
	[����] VARCHAR(50)
	CONSTRAINT [UK_mma_share] UNIQUE CLUSTERED
 	(
        	fundid,����,����,��Ƥ��
	)
)




--- �ꤺ--

CREATE TABLE MMA�ꤺ����򥻸�� (
	fundID VARCHAR(15) not null primary key,
	�D�n���ϰ� nVARCHAR(500),
	�O�޻Ȧ� VARCHAR(100),
	������q VARCHAR(100),
	����W�� nVARCHAR(500) not null,
	����g�z�H VARCHAR(100),
	[����W��(��)] VARCHAR(100),
	������� VARCHAR(4),
	������� VARCHAR(100),
	���ߤ�� VARCHAR(100),
	[���߮ɳW��(��)] VARCHAR(100),
	���ϰ� nVARCHAR(500),
	���Ъ� nVARCHAR(1000)
)


CREATE TABLE MMA�ꤺ��������g�z�H(
	
	fundID VARCHAR(15) NOT NULL,
	[�x���Z��(%)] VARCHAR(10),
	[�ާ@�Z��(%)] VARCHAR(10),
	[�ɶ�] VARCHAR(100),
	[����(��)] VARCHAR(100),
	[�{�����] nVARCHAR(3000),
	[�g�z�H] VARCHAR(100)
	CONSTRAINT [UK_mmafund_manager] UNIQUE CLUSTERED
 	(
        	fundID,�ɶ�,�g�z�H
	)
)


CREATE TABLE MMA�ꤺ������Ѫ��p_�Ӫ� (
	
	fundID VARCHAR(15) NOT NULL,
	[�W��] VARCHAR(10),
	[����(�d��)] VARCHAR(10),
	[���] VARCHAR(5),
	[�Ѳ��W��] nVARCHAR(100),
	[��Ƥ��] VARCHAR(8)
	CONSTRAINT [UK_mmafund_stock] UNIQUE CLUSTERED
 	(
        	fundID,�Ѳ��W��
	)
	
)


CREATE TABLE MMA�ꤺ������Ѫ��p_����(

	fundID VARCHAR(15) NOT NULL,
	[����] VARCHAR(8) NOT NULL,
	[�����B(�U��)] VARCHAR(10),
	[��Ƥ��] VARCHAR(10),
	[����] VARCHAR(50)
	CONSTRAINT [UK_mmafund_share] UNIQUE CLUSTERED
 	(
        	fundid,����,����
	)
)

--- �ҥ~ ----

CREATE TABLE [MMA�ҥ~����򥻸��] (

	fundID VARCHAR(15) not null primary key ,
	�O�޾��c VARCHAR(200),
	�ʪ���� VARCHAR(4),
	�x�W�`�N�z VARCHAR(50),
	����W�� nVARCHAR(500),
	����^��W�� VARCHAR(200),
	����W�� VARCHAR(50),
	������� VARCHAR(4),
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



CREATE TABLE [MMA�ҥ~������Ѫ��p_�Ӫ�] (

	fundID VARCHAR(15),
	���ѦW�� VARCHAR(200),
	��� VARCHAR(8),
	��Ƥ�� VARCHAR(10),
	CONSTRAINT [UK_mma_wstock] UNIQUE CLUSTERED
 	(
        	[fundID], [���ѦW��]
	)
)


CREATE TABLE [MMA�ҥ~������Ѫ��p_����] (

	fundID VARCHAR(15),
	���� VARCHAR(10),
	[�����B(����:�U)] VARCHAR(10),
	��Ƥ�� VARCHAR(10),
	���� VARCHAR(50),
	CONSTRAINT [UK_mma_wshare] UNIQUE CLUSTERED
 	(
        	[fundID], [����],[����]
	)
)



------ ���schema--- �X�ְꤺ�~���

CREATE TABLE MMA����򥻸�� (
	fundID VARCHAR(15) not null primary key,
	�D�n���ϰ� nVARCHAR(500),
	�O�޻Ȧ� VARCHAR(100),
	������q VARCHAR(100),
	����W�� nVARCHAR(500) not null,
	����g�z�H VARCHAR(100),
	[����W��(��)] VARCHAR(100),
	������� VARCHAR(4),
	������� VARCHAR(100),
	���ߤ�� VARCHAR(100),
	[���߮ɳW��(��)] VARCHAR(100),
	���ϰ� nVARCHAR(500),
	���Ъ� nVARCHAR(1000)
)




--------------------------------------------------------------------------------------------
---- TEST --
--------------------------------------------------------------------------------------------
Drop table MMA�ҥ~������Ѫ��p_����

SELECT * FROM MMA�ꤺ��������g�z�H
SELECT * FROM MMA�ꤺ����򥻸��
SELECT top 10 * FROM MMA�ꤺ������Ѫ��p_�Ӫ� 
SELECT top 10 * FROM MMA�ꤺ������Ѫ��p_����

SELECT * FROM MMA�ҥ~����򥻸��
SELECT * FROM MMA�ҥ~������Ѫ��p_�Ӫ�
SELECT * FROM MMA�ҥ~������Ѫ��p_����




SELECT * FROM MMA����򥻸��
SELECT * FROM MMA������Ѫ��p_�Ӫ�
SELECT * FROM MMA������Ѫ��p_����