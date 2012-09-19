import time, datetime, sys, os
import SocketServer
from multiprocessing import Process
import cherrypy

import lib

dbFilePath = os.getcwd() + '/' +"wlc_load.db"

def get_and_store_data():
    while(True):
            #open the sql connection
            repo = lib.DataRepo(dbFilePath)
            settings = lib.Settings(dbFilePath)
            repo.check_db()
            
            print '[*] ' + str(datetime.datetime.now()) + ' Polling the WLC for the APs '
            
            snmpInterface = lib.WlcInterface(sys.argv[1],sys.argv[2])
            
            
            #get a list of switches
            ap_names = snmpInterface.get_ap_names()
            ap_clients = snmpInterface.get_ap_client_count()
            ap_locations = snmpInterface.get_ap_locations()
            
            ap_data = snmpInterface.merge_ap_data(ap_names, ap_clients, ap_locations)
                
            #print "[*] "+str(datetime.datetime.now())+" Saving Data"

            
            repo.save_data(ap_data)
            settings.set("lastUpdate",time.time())

            print '[*] Sleeping 15 mins'
            time.sleep(60 * 5)
            #time.sleep(60 * 15)

def start_mainWebServer():
    global_conf = {
           'global':    { 'server.environment': 'production',
                          'tools.staticdir.on': True,
                          'tools.staticdir.dir' : os.getcwd() + '/',
                          'engine.autoreload_on': True,
                          'engine.autoreload_frequency': 5,
                          'server.socket_host': '0.0.0.0',
                          'log.access_file' : "/tmp/access.log",
                          'log.screen': False,
                          'server.socket_port':8080,
                        }
                  }
    cherrypy.quickstart(lib.WebServer(dbFilePath),config=global_conf)

def main():
    try:
        p0 = Process(target=get_and_store_data,args=())
        p1 = Process(target=start_mainWebServer,args=())
        
        p0.daemon = True
        p1.daemon = True

        p0.start()
        p1.start()

        while True:
            time.sleep(.5)

    except KeyboardInterrupt:
        print "Killing all the children processes"
        p0.terminate()
        p1.terminate()
        exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'Usage: ', sys.argv[0] , ' <wlcIP> <communityString>'
        sys.exit(1)
    else:
        main()