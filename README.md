#Overview
This is a small script that polls a Cisco Wireless Lan controller via SNMP. It collects the number of clients connected by access point and records it. After 10mins the script will poll again. The data is stored in a SQLite database. At the same time the script fires off a cherrypy thread that presents the data in unique ways using graphs and google maps.

For more information visit <http://lanceingle.com/blog/2012/10/wlc-load/>

##Depends
- CherryPy
- PySNMP

##Usage
     wlc_ap_load.py wlcIP communityString
e.g. wlc_ap_load.py 10.0.0.15 public

##ToDo

- 10/5/12 ~~Add web interface for a small dashboard~~
- 9/17/12 ~~Come back and use a diffrent SQL library so that other databases can be used.~~
- 9/17/12 ~~Maybe add somesort of config file instead of 6 params~~