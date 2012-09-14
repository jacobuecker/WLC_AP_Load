import time, datetime

try:
    import _mssql
except ImportError:
    print "_mssql module missing, please install it else this program will not work"
    sys.exit(0)
    
try:
    from pysnmp.entity.rfc3413.oneliner import cmdgen
    from pysnmp.proto import rfc1902
except ImportError:
    print "pySNMP module missing, please install it else this program will not work"
    print " you could try running 'easy_install pysnmp'"
    sys.exit(0)
    
class SQL:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.database = ""
        self.ip_address = ""
        self.conn = ""
        self.connected = False
    
    def convert_epoch(self,ts):
        return time.strftime("%Y%m%d %H:%M:%S",time.localtime(ts))
    
    def connect(self):
        self.conn = _mssql.connect(server=self.ip_address, user=self.username, password=self.password, database=self.database)
        print '[*] Sucessfully Connected to the SQL Server'
        self.connected = True
    
    def disconnect(self):
        if self.connected:
            self.conn.close()
            print '[*] Sucessfully Closed the Connection to the SQL Server'
        
    def get_data(self,sql):
        self.conn.execute_query(sql)
        list = []
        for row in self.conn:
            list.append(row)
        return list
    
    def write_data(self, sql):
        #print sql
        self.conn.execute_non_query(sql)
        
class SNMP:
    #This is the class used to connect to the SNMP server and pull info based on the OID
    def __init__(self):
        self.port = 161
        self.ip_address = ""
        self.community = "public"
        self.version = "2c"

    def get_config(self):
        """
        This function returns the configuration required for the router according to the version
        of SNMP being used.We have assumed an SNMP version 2c for our program but this can be changed easily.
        A sample code is :
        >>> snmp.version = "2c"
        >>> snmp_config = self.get_config()
        This function is used internally only.
        """
        if self.version == "1":
            return  cmdgen.CommunityData('test-agent', self.community, 0),
        elif self.version == "2c":
            return cmdgen.CommunityData('test-agent', self.community)
        elif self.version == "3":
            return cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),

    def oidstr_to_tuple(self, s):
        """ This function removes the '.' (dots) from the OID specified in the program
        and returns it in the form of a tuple, which is used by pySNMP to get info from the router.
        
        Error in Function - remove trailing dot if there is one
        Sample Implementation -
        >>> oid = self.oidstr_to_tuple(oid)
        """
        return tuple([int(n) for n in s.split(".")])

    def get_value(self, oid):
        """
        This function gets a single data from the router, such as the router name or
        the system description.For lists of data such as a list of interfaces or a
        list of neighbors of the router, a different function called snmp_getnext is used.
        Example
        >>> sys_descr = snmp.get_value(OID_SYSDESCR)[1]
        This function returns a tuple of data back and the useful datum from that is the 2nd part,
        hence the use of the [1] in the function.
        """
        r = ()
        oid = self.oidstr_to_tuple(oid)
        snmp_config = self.get_config()
        errorIndication, errorStatus, \
            errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
            snmp_config, cmdgen.UdpTransportTarget((self.ip_address, self.port)), oid)

        if errorIndication:
            print errorIndication
            print errorStatus
            print errorIndex
        else:
            if errorStatus:
                print '%s at %s\n' % (
                    errorStatus.prettyPrint(), varBinds[int(errorIndex)-1])
            else:
                for name, val in varBinds:
                    return (name.prettyPrint(), val.prettyPrint())

    def get_values(self, oid):
        """ This function is used to get a list of data from the router, such as
        a list of interfaces or neighbors the router has. This information must then
        be parsed through with a for loop to go through all the returned data.
        Sample -
        >>> r = snmp.snmp_getnext(OID_CDP_CACHE_ENTRY)
        >>> for e in r:
        >>>     snmpoid, value = e[0], e[1]
        
        """
        r = []
        oid = self.oidstr_to_tuple(oid)
        snmp_config = self.get_config()
        errorIndication, errorStatus, errorIndex, \
            varBindTable = cmdgen.CommandGenerator().nextCmd(
            snmp_config, cmdgen.UdpTransportTarget((self.ip_address, self.port)), oid)
            
        if errorIndication:
            print errorIndication
            print errorStatus
            print errorIndex
        else:
            if errorStatus:
                print '%s at %s\n' % (
                    errorStatus.prettyPrint(), varBindTable[-1][int(errorIndex)-1])
            else:
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        r.append((name.prettyPrint(), val))
        return r

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
        query = "SELECT * FROM wlc_aps WHERE ap_key='" + str(ap['key']) + "'"
        apCnt = sql.get_data(query)
        if len(apCnt) > 0:
            query = "UPDATE wlc_aps SET ap_name='" + str(ap['name']) + "', ap_location='" + str(ap['location']) + "' WHERE ap_key='" + str(ap['key']) + "'"
            #print query
            sql.write_data(query)
        else:
            query = "Insert INTO wlc_aps (ap_key,ap_name,ap_location) VALUES ('"+str(ap['key'])+"','"+ str(ap['name']) + "','" + str(ap['location'])+"')"
            sql.write_data(query)
        query = "INSERT INTO wlc_ap_clients (ap_key,num_of_clients) VALUES ('"+str(ap['key'])+"','"+str(ap['clients'])+"')"
        sql.write_data(query)

def main():
    try:
        while(True):
            #open the sql connection
            sql = SQL()
            sql.username = 'username'
            sql.ip_address = '0.0.0.0'
            sql.password = 'password'
            sql.database = 'dataBases'
            sql.connect()
        
            print '[*] '+str(datetime.datetime.now())+' Polling the WLC for the APs '
            
            snmp = SNMP()
            snmp.ip_address = "0.0.0.0" 	# IP address for the wireless lan controller
            snmp.community = "community"
            
            
            #get a list of switches
            ap_names = get_ap_names(snmp)
            ap_clients = get_ap_client_count(snmp)
            ap_locations = get_ap_locations(snmp)
            
            ap_data = merge_ap_data(ap_names, ap_clients, ap_locations)

            #for ap in ap_data:
            #    print ap
                
            print "[*] "+str(datetime.datetime.now())+" Saving Data"

            save_data(ap_data, sql)
                
            #save the data to the disk
            
            
            #close the SQL connection
            sql.disconnect()
            
            print '[*] Sleeping 15 mins'
            time.sleep(60 * 15);
            
    except KeyboardInterrupt:
        exit(0)

if __name__ == "__main__":
    main()