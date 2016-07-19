#coding=utf-8
import sys
import MySQLdb

class TransferMoney(object):
    def __init__(self, conn):
        self.conn = conn
    
    # 检查账户是否可用 
    def check_acct_available(self, acctid):
        try:
            cursor = self.conn.cursor()
            sql = "select * from account where acctid=%s"%acctid
            cursor.execute(sql)
            print "check_acct_available:" + sql
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("账号%s不存在"% acctid)
        finally:
            cursor.close()
    
    # 检查账户金额是否足够
    def has_enough_money(self, acctid, money):
        try:
            cursor = self.conn.cursor()
            sql = "select * from account where acctid=%s and money>%s" % (acctid, money)
            cursor.execute(sql)
            print "has_enough_money:" + sql
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("账号%s金额不足"% acctid)
        finally:
            cursor.close()
    
    # 从账户中扣除指定金额
    def reduce_money(self, acctid, money):
        try:
            cursor = self.conn.cursor()
            sql = "update account set money=money-%s where acctid=%s" % (money, acctid)
            print sql
            cursor.execute(sql)
            print "reduce_money:" + sql
            if cursor.rowcount != 1:
                raise Exception("账号%s减款失败"% acctid)
        finally:
            cursor.close()
    
    # 从账户中增加指定金额
    def add_money(self, acctid, money):
        try:
            cursor = self.conn.cursor()
            sql = "update account set money=money+%s where acctid=%s" % (money, acctid)
            cursor.execute(sql)
            print "add_money:" + sql
            if cursor.rowcount != 1:
                raise Exception("账号%s加款失败"% acctid)
        finally:
            cursor.close()
    
    
    # 转账方法
    def transfer(self, from_acctid, to_acctid, money):
        try:
            # 检查转出账户是否可用 
            self.check_acct_available(from_acctid)
            # 检查转入账户是否可用
            self.check_acct_available(to_acctid)
            # 检查转出账户是否有足够的钱
            self.has_enough_money(from_acctid, money)
            # 将转出账户的钱减少
            self.reduce_money(from_acctid, money)
            # 将转入账户的钱增加
            self.add_money(to_acctid, money)
            # 事务提交
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e


if __name__=="__main__":
    # 传入三个参数，依次为转入ID，转到ID，转账数额
    from_acctid = sys.argv[1]
    to_acctid = sys.argv[2]
    money = sys.argv[3]

    # 建立数据库连接器
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', port=3306, db='test',charset = 'utf8')
    tr_money = TransferMoney(conn)
    
    try:
        tr_money.transfer(from_acctid, to_acctid, money)
    except Exception as e:
        print "出现问题：" + str(e)
    finally:
        conn.close()
    
    