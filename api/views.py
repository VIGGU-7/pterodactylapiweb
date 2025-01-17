from django.shortcuts import render
import requests
baseurl=""
class User:
    def __init__(self,serverid,key):
        self.serverid=serverid
        self.key=key
    def get_apikey(self):
        return self.key
    def get_serverid(self):
        return self.serverid
def home(request):
    return render(request,'base.html')
def server(request):
        serverid = request.GET['serverid']
        apikey=request.GET['api']
        power=request.GET['power']
        session=User(serverid=serverid,key=apikey)
        auth={"Accept":"application/json",}
        auth['Authorization']=f"Bearer {session.get_apikey()}"
        try:
            response=requests.get(baseurl+f"/api/application/servers/{session.get_serverid()}",headers=auth)
            serveride=response.json()['attributes']['identifier']
            context={'name':response.json()['attributes']['name'],'memory':response.json()['attributes']['limits']['memory'],'cpu':response.json()['attributes']['limits']['cpu'],'disk':response.json()['attributes']['limits']['disk'],'apikeyforpower':session.get_apikey(),'serveridforpower':session.get_serverid(),'logs':"details fetched successfully choose an option here"}
        except:
            return "Failed"
        ##poweraction
        if 'none' in power:
            pass
        if 'none' not in power:
            try:
                params={}
                params['ID']=serveride
                params['signal'] = power
                requests.post(baseurl+f"/api/client/servers/{serveride}/power?type=admin",headers=auth,params=params)
                context['logs']=f"server {power}ed succefully"
                return render(request,'server.html',context=context)
            except:
                context['logs']=f"server {power} failed"
                return render(request,'server.html',context=context)
        ##response for servers
        return render(request,'server.html',context=context)
