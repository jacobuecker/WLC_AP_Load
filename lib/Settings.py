
from sqliteDB import Database

class Settings:
    def __init__(self, filePath):
        self.filePath = filePath

    def get(self, key):
        sql = Database(self.filePath)
        return sql.get_data_single("SELECT value FROM wlc_settings WHERE key=?",(key,))

    def set(self, key, value):
        sql = Database(self.filePath)
        if sql.is_present("SELECT * FROM wlc_settings WHERE key=?",(key,)):
            sql.write_data("UPDATE wlc_settings SET value=? WHERE key=?",(value,key,))
        else:
            sql.write_data("INSERT INTO wlc_settings (key,value) VALUES (?,?)",(key,value,))
        sql.commit()