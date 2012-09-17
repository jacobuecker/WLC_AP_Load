import sqlite3

class Database:
    def __init__(self,filePath):
        self.conn = sqlite3.connect(filePath)

    def write_data_raw(self, sql):
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()
        self.cur.close()

    def write_data(self, sql, params):
        self.cur = self.conn.cursor()
        self.cur.execute(sql,params)
        self.conn.commit()
        self.cur.close()
    
    def get_data(self,sql,params):
        self.cur = self.conn.cursor()
        self.cur.execute(sql,params)
        results = self.cur.fetchall()
        self.cur.close
        return results

    def get_count(self,sql,params):
        self.cur = self.conn.cursor()
        self.cur.execute(sql,params)
        results = self.cur.rowcount
        self.cur.close
        return results