import sys
try:
    from pysnmp.entity.rfc3413.oneliner import cmdgen
    from pysnmp.proto import rfc1902
except ImportError:
    print "pySNMP module missing, please install it else this program will not work"
    print " you could try running 'easy_install pysnmp'"
    sys.exit(0)

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
