import os, time, json
import cherrypy

from DataRepo import DataRepo

class WebServer(object):
    def __init__(self,dbpath):
        self.clientData = []
        self.dbpath = dbpath
        

    def _header(self,inject):
        html = open(os.path.join(os.curdir,'html','frags','header'),'r').read()
        if inject is None:
            html = html.replace("##HEADINJECT##","")
        else:
            html = html.replace("##HEADINJECT##",inject)
        return html
    
    def _footer(self):
        return open(os.path.join(os.curdir,'html','frags','footer'),'r').read()

    def index(self):
        html = self._header("<script type='text/javascript' src='/html/js/index.js'></script>")
        html += open(os.path.join(os.curdir,'html','pages','index.html'),'r').read()
        html += self._footer()
        return html

    def showmap(self):
        html = self._header("<script type='text/javascript' src='/html/js/showMap.js'></script><script src='http://maps.google.com/maps/api/js?sensor=false'></script>")
        html += open(os.path.join(os.curdir,'html','pages','showMap.html'),'r').read()
        html += self._footer()
        return html

    def showGroupDetails(self, groupID):
        scripts = "<script type='text/javascript' src='/html/js/showGroupDetails.js'></script>"
        scripts += "<script type='text/javascript' src='/html/js/jquery.slidePicker.min.js'></script>"
        scripts += "<script src='http://maps.google.com/maps/api/js?sensor=false'></script>"
        html = self._header(scripts)
        html += open(os.path.join(os.curdir,'html','pages','showGroupDetails.html'),'r').read()
        html += self._footer()
        return html

    def map_settings(self):
        scripts = "<script type='text/javascript' src='/html/js/map_settings.js'></script>"
        scripts += "<script src='/html/js/jquery.simplemodal.1.4.3.min.js'></script>"
        scritps += "<script src='http://maps.google.com/maps/api/js?sensor=false'></script>"
        html = self._header(scripts)
        html += open(os.path.join(os.curdir,'html','pages','map_settings.html'),'r').read()
        html += self._footer()
        return html

    def api_get_groupData(self, id):
        repo = DataRepo(self.dbpath)
        history = repo.get_group_history(id)
        return json.dumps(history)

    def api_save_groups(self,data):
        repo = DataRepo(self.dbpath)
        data = json.loads(data)
        repo.save_groups(data)
        jsonData = {}
        jsonData['success'] = True
        jsonData['msg'] = 'Groups were saved'
        return json.dumps(jsonData)

    def api_get_currentLoad(self):
        repo = DataRepo(self.dbpath)
        data = repo.get_current_load()
        return json.dumps(data)

    def api_get_groups(self):
        repo = DataRepo(self.dbpath)
        data = repo.get_groups()
        return json.dumps(data)
    
    def api_delete_group(self,id):
        repo = DataRepo(self.dbpath)
        repo.delete_group(id)
        return json.dumps({"success":True})

    index.exposed = True
    showmap.exposed = True
    map_settings.exposed = True
    showGroupDetails.exposed = True
    api_save_groups.exposed = True
    api_get_currentLoad.exposed = True
    api_get_groups.exposed = True
    api_delete_group.exposed = True
    api_get_groupData.exposed = True