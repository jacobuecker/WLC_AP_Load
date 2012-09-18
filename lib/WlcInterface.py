from SNMP import SNMP

class WlcInterface:
    def __init__(self, ip, comm):
        self.snmp = SNMP()
        self.snmp.ip_address = ip
        self.snmp.community = comm

    def strip_oid(self,list, oid):
        oid = oid + "."
        newList = []
        for x in range(len(list)):
            item = {}
            item['key'] = str(list[x][0].replace(oid,""))
            item['value'] = str(list[x][1])
            newList.append(item)
        return newList

    def get_ap_locations(self):
        oid = "1.3.6.1.4.1.14179.2.2.1.1.4"
        list = self.snmp.get_values(oid)
        if len(list) == 0:
            return False
        else:
            return self.strip_oid(list,oid)

    def get_ap_client_count(self):
        oid = "1.3.6.1.4.1.14179.2.2.13.1.4"
        list = self.snmp.get_values(oid)
        if len(list) == 0:
            return False
        else:
            return self.strip_oid(list,oid)
        
    def get_ap_names(self):
        oid = '1.3.6.1.4.1.14179.2.2.1.1.3'
        list = self.snmp.get_values(oid)
        if len(list) == 0:
            return False
        else:
            return self.strip_oid(list,oid)

    def search_for_ap_by_key_location(self, list,key):
        for x in range(len(list)):
            if list[x]['key'].find(key) != -1:
                return x
        return -1

    def search_for_ap_by_key_client(self,list,key):
        for x in range(len(list)):
            if list[x]['key'].startswith(key):
                return x
        return -1

    def merge_ap_data(self,names, clients, locations):
        newList = []
        for x in range(len(names)):
            item = {}
            item['key'] = names[x]['key']
            item['name'] = names[x]['value']
            
            locationIndex = self.search_for_ap_by_key_location(locations,item['key'])
            if locationIndex != -1:
                item['location'] = locations[locationIndex]['value']
                
            clientIndex = self.search_for_ap_by_key_client(clients,item['key'])
            if locationIndex != -1:
                item['clients'] = clients[clientIndex]['value']
                
            newList.append(item)
        return newList