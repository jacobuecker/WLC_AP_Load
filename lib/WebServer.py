import os, time, json
import cherrypy

from sqliteDB import Database

class WebServer(object):
    def __init__(self,dbPath):
        self.clientData = []
        self.db = dbPath

    def _header(self,inject):
        html = open(os.path.join(os.curdir,'html','frags') + '/header','r').read()
        if inject is None:
            html = html.replace("##HEADINJECT##","")
        else:
            html = html.replace("##HEADINJECT##",inject)
        return html
    
    def _footer(self):
        return open(os.path.join(os.curdir,'html','frags') + '/footer','r').read()

    def index(self):
        html = self._header("<script type='text/javascript' src='/html/js/index.js'></script>")
        html += "<div id='currentLoad' style='height:1500px;width300px;'></div>"
        html += self._footer()
        return html

    def page(self,id):
        html = self._header(None)
        html += str(id)
        html += self._footer()
        return html
    
    def api_get_currentLoad(self):
        db = Database(self.db);
        APs = db.get_data_raw("SELECT * FROM wlc_aps")
        data = []
        for ap in APs:
            node = {}
            node['name'] = ap[1]
            node['location'] = ap[2]
            node['cnt'] = int(db.get_data_single("SELECT clients from wlc_ap_clients WHERE ap_key='" + str(ap[0]) + "'"))
            data.append(node)
        data = sorted(data, key=lambda k: k['cnt'], reverse = True)
        return json.dumps(data)
    
    index.exposed = True
    page.exposed = True
    api_get_currentLoad.exposed = True