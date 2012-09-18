import time, datetime, sys, thread, os

import cherrypy

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

def check_db(sql):
    #init DB
    query = "CREATE TABLE if not exists wlc_aps (ap_key TEXT,ap_name TEXT,ap_location TEXT)"
    sql.write_data_raw(query)
    query = "CREATE TABLE if not exists wlc_ap_clients (id INTEGER PRIMARY KEY, ap_key text,timestamp INTEGER, clients INTEGER)"
    sql.write_data_raw(query)
    #query = "CREATE INDEX if not exists timestampSort on wlc_ap_clients (timestamp DESC)"
    #sql.write_data_raw(query)
    sql.commit()

def get_and_store_data():
    while(True):
            #open the sql connection
            db = lib.Database(os.getcwd() + '/' +"wlc_load.db")
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
            time.sleep(60)
            #time.sleep(60 * 15)

def main():
    try:
        thread.start_new_thread(get_and_store_data,())
        global_conf = {
           'global':    { 'server.environment': 'production',
                          'tools.staticdir.on': True,
                          'tools.staticdir.dir' : os.getcwd() + '/',
                          'engine.autoreload_on': True,
                          'engine.autoreload_frequency': 5,
                          'server.socket_host': '0.0.0.0',
                          'log.access_file' : "/tmp/access.log",
                          'log.screen': False,
                          'tools.sessions.on': True,
                          'server.socket_port':8080,
                        }
                  }
        cherrypy.quickstart(lib.WebServer(os.getcwd() + '/' +"wlc_load.db"),config=global_conf)
    except KeyboardInterrupt:
        exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'Usage: ', sys.argv[0] , ' <wlcIP> <communityString>'
        sys.exit(1)
    else:
        main()