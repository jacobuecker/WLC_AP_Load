from sqliteDB import Database
import time


class DataRepo:
    def __init__(self, filePath):
        self.filePath = filePath

    def get_updateStamp(self):
        sql = Database(self.filePath)
        query = "SELECT value from wlc_settings WHERE key='lastUpdate'"
        return sql.get_data_single(query)

    def set_updateStamp(self,timestamp):
        sql = Database(self.filePath)
        params = (timestamp,)
        query = "UPDATE wlc_settings SET value=? WHERE key='lastUpdate'"
        return sql.write_data(query,params)

    def check_db(self):
        #init DB
        sql = Database(self.filePath)
        query = "CREATE TABLE if not exists wlc_aps (ap_key TEXT, ap_name TEXT, ap_location TEXT)"
        sql.write_data_raw(query)
        query = "CREATE TABLE if not exists wlc_settings (key TEXT PRIMARY KEY, value TEXT)"
        sql.write_data_raw(query)
        query = "CREATE TABLE if not exists wlc_ap_clients (id INTEGER PRIMARY KEY, ap_key text,timestamp INTEGER, clients INTEGER)"
        sql.write_data_raw(query)
        query = "CREATE INDEX if not exists timestampSort on wlc_ap_clients (timestamp DESC)"
        sql.write_data_raw(query)
        sql.commit()

    def save_data(self, ap_data):
        sql = Database(self.filePath)
        paramList = []
        for ap in ap_data:
            params = (str(ap['key']),)
            query = "SELECT * FROM wlc_aps WHERE ap_key=?"
            apPresent = sql.is_present(query,params)
            if apPresent:
                params = (str(ap['name']),str(ap['location']),str(ap['key']))
                query = "UPDATE wlc_aps SET ap_name=?, ap_location=? WHERE ap_key=?"
                sql.write_data(query, params)
            else:
                params = (str(ap['key']),str(ap['name']),str(ap['location']))
                query = "Insert INTO wlc_aps (ap_key,ap_name,ap_location) VALUES (?,?,?)"
                sql.write_data(query,params)
            params = (str(ap['key']),str(time.time()),str(ap['clients']),)
            paramList.append(params)
        query = "INSERT INTO wlc_ap_clients (ap_key, timestamp , clients) VALUES (?,?,?)"
        sql.write_data_dump(query,paramList)
        sql.commit()

    def get_current_load(self):
        db = Database(self.filePath)
        APs = db.get_data_raw("SELECT * FROM wlc_aps")
        data = []
        for ap in APs:
            node = {}
            node['name'] = ap[1]
            node['location'] = ap[2]
            node['cnt'] = int(db.get_data_single("SELECT clients from wlc_ap_clients WHERE ap_key='" + str(ap[0]) + "' ORDER BY timestamp DESC"))
            data.append(node)
        data = sorted(data, key=lambda k: k['cnt'], reverse = True)
        return data