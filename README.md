#Overview#
This is a small script that was requested by a friend. It connects to a Cisco Wireless Lan Controller that has SNMP enabled and pulls information. Once the information has been pulled then the data is inserted into a SQL Database. Sadly, it dumps the data into a Microsoft SQL database.

#Usage#
     wlc_ap_load.py dbUsername dbIP dbPassword dbName wlcIP communityString
e.g. wlc_ap_load.py username 10.0.0.10 password clients 10.0.0.15 public

#ToDo#
Come back and use a diffrent SQL library so that other databases can be used.
Maybe add somesort of config file instead of 6 params