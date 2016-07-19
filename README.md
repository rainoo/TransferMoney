# TransferMoney
一个Python操作MYSQL数据库的例子

1）要想用Python操作mysql，就需要安装MySQL-python驱动，它是Python操作Mysql必不可少的模块。目前windows版的只提供32位的安装文件，所以你的Python也需要时32位的，64位无法工作。
使用如下命令可以测试一下MySQLdb模块是否已经正常导入。
>>> import MySQLdb


2）在本地MYSQL数据库上使用test数据库

3）在test库上建立如下表，因为有事务处理，注意不能设置为MyISAM
CREATE TABLE `account` (
	`acctid` INT(11) DEFAULT NULL COMMENT '账户ID',
	`money` INT(11) DEFAULT NULL COMMENT '余额'
) ENGINE = INNODB DEFAULT CHARSET = utf8 

4）需要在执行控制台上进行三项参数设置：转出账号ID，转出账号ID，转出金额。
