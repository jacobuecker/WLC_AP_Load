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
        query = "CREATE TABLE if not exists wlc_ap_groups (id INTEGER PRIMARY KEY, group_name TEXT, ap_lat REAL, ap_lng REAL)"
        sql.write_data_raw(query)
        query = "CREATE TABLE if not exists wlc_ap_group_binding (id INTEGER PRIMARY KEY, group_id, ap_key TEXT)"
        sql.write_data_raw(query)
        query = "CREATE TABLE if not exists wlc_ap_clients (id INTEGER PRIMARY KEY, ap_key text,timestamp INTEGER, clients INTEGER)"
        sql.write_data_raw(query)
        query = "CREATE INDEX if not exists timestampSort on wlc_ap_clients (timestamp DESC)"
        sql.write_data_raw(query)
        sql.commit()

    def save_data(self, ap_data):
        sql = Database(self.filePath)
        paramList = []
        timestamp = time.time()
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
            params = (str(ap['key']),str(timestamp),str(ap['clients']),)
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
            node['key'] = ap[0]
            node['name'] = ap[1]
            node['location'] = ap[2]
            node['cnt'] = int(db.get_data_single("SELECT clients from wlc_ap_clients WHERE ap_key=? ORDER BY timestamp DESC",(str(ap[0]),)))
            data.append(node)
        data = sorted(data, key=lambda k: k['cnt'], reverse = True)
        return data

    def get_groups(self):
        db = Database(self.filePath)
        data = []
        groups = db.get_data_raw("SELECT * FROM wlc_ap_groups")
        for group in groups:
            node = {}
            node['id'] = group[0]
            node['name'] = group[1]
            node['lat'] = group[2]
            node['lng'] = group[3]
            node['aps'] = []
            node['cnt'] = 0
            bindings = db.get_data("SELECT * FROM wlc_ap_group_binding WHERE group_id=?",(node['id'],))
            for binding in bindings:
                apNode = {}
                apNode['key'] = binding[2]
                adDetails = db.get_data("SELECT * FROM wlc_aps WHERE ap_key=?",(apNode['key'],))
                apNode["name"] = adDetails[0][1]
                node['aps'].append(apNode)
                node['cnt'] += int(db.get_data_single("SELECT clients from wlc_ap_clients WHERE ap_key=? ORDER BY timestamp DESC",(str(apNode['key']),)))
            data.append(node)
        data = sorted(data, key=lambda k: k['cnt'], reverse = True)
        return data

    def save_groups(self,groups):
        db = Database(self.filePath)
        for group in groups:
            groupID = group['id']
            if group['id'] is not None:
                #update
                db.write_data("UPDATE wlc_ap_groups SET group_name=?,ap_lat=?,ap_lng=? WHERE id=?",(group['name'],group['lat'],group['lng'],group['id'],))
            else:
                #insert
                db.write_data("INSERT INTO wlc_ap_groups (group_name, ap_lat, ap_lng) VALUES (?,?,?)",(group['name'],group['lat'],group['lng'],))
                groupID = db.get_data_single_raw("SELECT max(id) from wlc_ap_groups")

            db.write_data("DELETE FROM wlc_ap_group_binding WHERE group_id=?",(groupID,))
            APs = group['aps'].split(":")
            for ap in APs:
                if ap != "":
                    db.write_data("INSERT INTO wlc_ap_group_binding (group_id,ap_key) VALUES (?,?)",(groupID,ap,))
        db.commit()

    def delete_group(self,groupID):
        db = Database(self.filePath)
        db.write_data("DELETE FROM wlc_ap_group_binding WHERE group_id=?",(groupID,))
        db.write_data("DELETE FROM wlc_ap_groups WHERE id=?",(groupID,))
        db.commit()

    def get_group_history(self, groupID):
        db = Database(self.filePath)
        history = db.get_data("select SUM(clients), timestamp from wlc_ap_clients where ap_key in (select ap_key from wlc_ap_group_binding where group_id=?) group by timestamp order by timestamp asc",(groupID,))
        data = []
        for x in xrange(0,len(history)):
            node = {}
            node['val'] = history[x][0]
            node['timestamp'] = history[x][1]
            data.append(node)
        return data




