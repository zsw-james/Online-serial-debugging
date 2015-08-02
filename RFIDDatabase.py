# encoding=utf-8
import sqlite3

class RFIDDatabase(object):
    def __init__(self):
        # 连接数据库
        self.conn = sqlite3.connect('RFIDDatabase.db')
        self.tableName = "rfidtable"
        self.sql = None

        print "Opend database successfully"

        #self.createRfidtable()

    def createRfidtable(self):
        # 建立rfidtable表,仅仅在第一调用的时候使用
        #self.tableName = tableName
        self.sql = '''CREATE TABLE rfidtable
          (numbers INTEGER PRIMARY KEY AUTOINCREMENT,
          cardID INT NOT NULL ,
          triggerID INT NOT NULL);'''

        self.conn.execute(self.sql)
        print "rfid table created successfully"

    def saveID(self,cardID,triggerID,):
        self.sql = '''INSERT INTO rfidtable VALUES (?, ?, ?) '''

        self.conn.execute(self.sql, (None, cardID, triggerID))
        self.conn.commit()

    def findID(self,number):
        #获得触发器ID和卡号
        self.sql = '''SELECT cardID,triggerID from rfidtable WHERE numbers = ?'''
        self.cursor = self.conn.execute(self.sql, (number,))
        for row in self.cursor:
            cardID = row[0]
            triggerID = row[1]
        return cardID,triggerID

    def findcardID(self, number):
        #获得卡号
        self.sql = '''SELECT cardID from rfidtable WHERE number = ?'''
        self.cursor = self.conn.execute(self.sql, (number,))
        for row in self.cursor:
            cardID = row[0]
        return cardID

    def findTriggerID(self, number):
        #获得卡号
        self.sql = '''SELECT triggerID from ? WHERE number = ?'''
        self.cursor = self.conn.execute(self.sql, (self.tableName, number))
        for row in self.cursor:
            triggerID = row[0]
        return triggerID

    def _dropRfidtable(self):
        #删除rfidtable表
        self.sql = '''DROP TABLE rfidtable'''

        self.conn.execute(self.sql)
        print "删除table成功"

    # 时间戳默认是当前时间,所以不用存
    # def savaTimestamp(self):
    #     # 记录数据发来的Timestamp构建数据行
    #     self.sql = "INSERT INTO ? (TIMESTAMP ) VALUES (?) ;"
    #
    #     self.conn.execute(self.sql, (self.tableName, ))

rfidDb = RFIDDatabase()

if __name__ == '__main__':
    rfidDb = RFIDDatabase()
    rfidDb.createRfidtable()
    rfidDb.saveID(6, 1)
    rfidDb.saveID(5, 6)