import os, time, json
import cherrypy

from DataRepo import DataRepo

class WebServer(object):
    def __init__(self,dbPath):
        self.clientData = []
        self.dbpath = dbPath
        

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
        db = DataRepo(self.dbpath)
        data = db.get_current_load()
        return json.dumps(data)
    
    index.exposed = True
    page.exposed = True
    api_get_currentLoad.exposed = True