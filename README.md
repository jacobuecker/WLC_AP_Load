#Overview#
This is a small script that was requested by a friend. It connects to a Cisco Wireless Lan Controller that has SNMP enabled and pulls information. Once the information has been pulled then the data is inserted into a SQLite database.

#Usage#
     wlc_ap_load.py wlcIP communityString
e.g. wlc_ap_load.py 10.0.0.15 public

#ToDo#
Add web interface for a small dashboard
9/17/12~~Come back and use a diffrent SQL library so that other databases can be used.~~
9/17/12~~Maybe add somesort of config file instead of 6 params~~