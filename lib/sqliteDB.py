import sqlite3

class Database:
    def __init__(self,filePath):
        self.conn = sqlite3.connect(filePath)

    def write_data_raw(self, sql):
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.cur.close()

    def write_data(self, sql, params):
        self.cur = self.conn.cursor()
        self.cur.execute(sql,params)
        self.cur.close()

    def write_data_dump(self, sql, params):
        self.cur = self.conn.cursor()
        self.cur.executemany(sql,params)
        self.cur.close()
    
    def get_data_raw(self,sql):
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        results = self.cur.fetchall()
        self.cur.close
        return results
    
    def get_data(self,sql,params):
        self.cur = self.conn.cursor()
        self.cur.execute(sql,params)
        results = self.cur.fetchall()
        self.cur.close
        return results

    def get_data_single(self,sql,params):
        self.cur = self.conn.cursor()
        self.cur.execute(sql,params)
        results = self.cur.fetchone()[0]
        self.cur.close
        return results

    def get_data_single_raw(self,sql):
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        results = self.cur.fetchone()[0]
        self.cur.close
        return results

    def is_present(self,sql,params):
        self.cur = self.conn.cursor()
        self.cur.execute(sql,params)
        results = self.cur.fetchone()
        self.cur.close
        if results is None:
            return False
        else :
            return True

    def commit(self):
        self.conn.commit()