import time, datetime, sys
    
import lib

def strip_oid(list, oid):
    oid = oid + "."
    newList = []
    for x in range(len(list)):
        item = {}
        item['key'] = str(list[x][0].replace(oid,""))
        item['value'] = str(list[x][1])
        newList.append(item)
    return newList

def get_ap_locations(snmp):
    oid = "1.3.6.1.4.1.14179.2.2.1.1.4"
    list = snmp.get_values(oid)
    if len(list) == 0:
        return False
    else:
        return strip_oid(list,oid)

def get_ap_client_count(snmp):
    oid = "1.3.6.1.4.1.14179.2.2.13.1.4"
    list = snmp.get_values(oid)
    if len(list) == 0:
        return False
    else:
        return strip_oid(list,oid)
    
def get_ap_names(snmp):
    oid = '1.3.6.1.4.1.14179.2.2.1.1.3'
    list = snmp.get_values(oid)
    if len(list) == 0:
        return False
    else:
        return strip_oid(list,oid)

def search_for_ap_by_key_location(list,key):
    for x in range(len(list)):
        if list[x]['key'].find(key) != -1:
            return x
    return -1

def search_for_ap_by_key_client(list,key):
    for x in range(len(list)):
        if list[x]['key'].startswith(key):
            return x
    return -1

def merge_ap_data(names, clients, locations):
    newList = []
    for x in range(len(names)):
        item = {}
        item['key'] = names[x]['key']
        item['name'] = names[x]['value']
        
        locationIndex = search_for_ap_by_key_location(locations,item['key'])
        if locationIndex != -1:
            item['location'] = locations[locationIndex]['value']
            
        clientIndex = search_for_ap_by_key_client(clients,item['key'])
        if locationIndex != -1:
            item['clients'] = clients[clientIndex]['value']
            
        newList.append(item)
    return newList

def save_data(ap_data, sql):
    for ap in ap_data:
        params = (str(ap['key']),)
        query = "SELECT * FROM wlc_aps WHERE ap_key=?"
        apCnt = sql.get_count(query,params)
        if apCnt > 0:
            params = (str(ap['name']),str(ap['location']),str(ap['key']))
            query = "UPDATE wlc_aps SET ap_name=?, ap_location=? WHERE ap_key=?"
            sql.write_data(query, params)
        else:
            params = (str(ap['key']),str(ap['name']),str(ap['location']))
            query = "Insert INTO wlc_aps (ap_key,ap_name,ap_location) VALUES (?,?,?)"
            sql.write_data(query,params)
        params = (str(ap['key']),str(time.time()),str(ap['clients']))
        query = "INSERT INTO wlc_ap_clients (ap_key, timestamp , num_of_clients) VALUES (?,?,?)"
        sql.write_data(query,params)

def check_db(sql):
    #init DB
    query = "create table if not exists wlc_aps (ap_key TEXT,ap_name TEXT,ap_location TEXT)"
    sql.write_data_raw(query)
    query = "create table if not exists wlc_ap_clients (id INTEGER PRIMARY KEY, ap_key text,timestamp TEXT, num_of_clients INTEGER)"
    sql.write_data_raw(query)

def main():
    try:
        while(True):
            #open the sql connection
            db = lib.Database("wlc_load.db")
            check_db(db)
            
            print '[*] ' + str(datetime.datetime.now()) + ' Polling the WLC for the APs '
            
            snmp = lib.SNMP()
            snmp.ip_address = sys.argv[1] 	# IP address for the wireless lan controller
            snmp.community = sys.argv[2]
            
            
            #get a list of switches
            ap_names = get_ap_names(snmp)
            ap_clients = get_ap_client_count(snmp)
            ap_locations = get_ap_locations(snmp)
            
            ap_data = merge_ap_data(ap_names, ap_clients, ap_locations)

            #for ap in ap_data:
            #    print ap
                
            print "[*] "+str(datetime.datetime.now())+" Saving Data"

            save_data(ap_data, db)
            
            print '[*] Sleeping 15 mins'
            time.sleep(60 * 15);
            
    except KeyboardInterrupt:
        exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'Usage: ', sys.argv[0] , ' <wlcIP> <communityString>'
        sys.exit(1)
    else:
        main()