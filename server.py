import random
import requests
from datetime import datetime, timedelta
import threading
import time
import logging
import uwsgi
import server_utils



def application(env, start_response):
    #if(env['HTTP_HOST'].startswith('jitsi')):
    #    redirect_server = jitsi.get_random(env['QUERY_STRING'])
    #elif(env['HTTP_HOST'].startswith('poll')):
    #    redirect_server = poll.get_random(env['QUERY_STRING'])
    #elif(env['HTTP_HOST'].startswith('pad')):
    #    redirect_server = pad.get_random()
    #elif(env['HTTP_HOST'].startswith('codimd')):
    #    redirect_server = codimd.get_random(env['QUERY_STRING'])
    #elif(env['HTTP_HOST'].startswith('cryptpad')):
    #    redirect_server = cryptpad.get_random(env['QUERY_STRING'])
    #elif(env['HTTP_HOST'].startswith('etherpad')):
    #    redirect_server = etherpad.get_random(env['QUERY_STRING'])
    #elif(env['HTTP_HOST'].startswith('ethercalc')):
    #    redirect_server = ethercalc.get_random(env['QUERY_STRING'])
    #elif(env['HTTP_HOST'].startswith('bbb')):
    #    redirect_server = bbb.get_random()
    #else:
    #    redirect_server = 'https://github.com/tosterkamp/random-redirect/'
    # 
    #print('redirect from ' + env['HTTP_HOST'] + ' to ' + redirect_server)
    #start_response('302', [('Location', redirect_server)])
    #return [b"redirected"]
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    return [jitsi.get_list(env['QUERY_STRING'])]



class ServerList:
    def __init__(self, filename, t_request):
        """
        @param filename: name of the file with the serverlist in the folder res
        @param t_request: file, which is located on the searched servers, which can be used to measure the speed of the server
        """
        self.lock = threading.Lock()
        self.file = 'res/' + filename
        self.test_request = t_request
        self.servers = []
        self.properties = []
        self.offline_servers = []
        self.renew()

    def get_random(self, params=""):
        """
        return a random server from self.servers
        """
        allowBadHoster = False
        allowBadStun = False
        allowOnlyCountry = []
        if (params.casefold().find("allowBadHoster".casefold()) != -1):
            allowBadHoster = True
        if (params.casefold().find("allowBadStun".casefold()) != -1):
            allowBadStun = True
        if (params.casefold().find("country-code".casefold()) != -1):
            splits = params.casefold().split("&")
            for item in splits:
                if (item.find("country-code".casefold()) != -1):
                    allowOnlyCountry.append(item.split("=",1)[1])

        tmp_list = []
        self.lock.acquire()
        for i in range(len(self.servers)):
            if ((not allowBadHoster) and self.properties[i]["badHoster"]):
                print("badHoster: " + self.servers[i])
            elif ((not allowBadStun) and self.properties[i]["badStun"]):
                print("badStun: " + self.servers[i])
            elif (allowOnlyCountry):
                for country in allowOnlyCountry:
                    if (country.casefold() == self.properties[i]["country_code"].casefold()):
                        tmp_list.append(self.servers[i])
                        break
            else:
                tmp_list.append(self.servers[i])
        tmp = random.choice(tmp_list)
        self.lock.release()
        return tmp

    def get_list(self, params=""):
        allowBadHoster = False
        allowBadStun = False
        allowOnlyCountry = []
        if (params.casefold().find("allowBadHoster".casefold()) != -1):
            allowBadHoster = True
        if (params.casefold().find("allowBadStun".casefold()) != -1):
            allowBadStun = True
        if (params.casefold().find("country-code".casefold()) != -1):
            splits = params.casefold().split("&")
            for item in splits:
                if (item.find("country-code".casefold()) != -1):
                    allowOnlyCountry.append((item.split("=",1)[1]).casefold())

        tmp_list = dict(filter(lambda (url, badHoster, badStun, country_code)): (not (not allowBadHoster) and self.properties[i]["badHoster"]) and (not ((not allowBadStun) and self.properties[i]["badStun"])) and (self.properties[i]["country_code"].casefold() in allowOnlyCountry), self.properties.items()))
        
        return tmp_dict


    def renew(self):
        """
        get current list from filesystem and check if the servers are online
        """
        if self.test_request is None:
            with open(self.file, 'r') as f:
                self.servers = f.readlines()
        else:
            online = []
            offline = []
            with open(self.file, 'r') as f:
                all_servers = f.readlines()
            for x in all_servers:
                try:
                    r = requests.get(str.rstrip(x) + self.test_request, timeout=0.5)
                    if (r.status_code == requests.codes.ok):
                        #print(str.rstrip(x) + " is online")
                        online.append(x)
                    else:
                        #print(str.rstrip(x) + " returns status code: " + str(r.status_code))
                        offline.append(x)
                except Exception as inst:
                    #print(str.rstrip(x) + " Error: " + str(inst))
                    offline.append(x)
            #print("offline: ")
            #print(offline)
            props = []
            for i in range(len(online)):
                props.append(1)
                tmp_dict = {
                    "url": online[i],
                    "badHoster": server_utils.hasBadHoster(online[i]),
                    "badStun": server_utils.hasBadStun(online[i]),
                    "country_code": server_utils.getCountry(online[i])
                }
                props[i] = tmp_dict

            self.servers = online
            self.properties = props
            self.offline_servers = offline
            self.lock.release()
            #print("online: ")
            #print(self.servers)






jitsi = ServerList('jitsi_servers.lst', 'sounds/outgoingRinging.wav')
#poll = ServerList('poll_servers.lst', 'images/date.png')
#pad = ServerList('pad_servers.lst', None)
#codimd = ServerList('codimd_servers.lst', 'screenshot.png')
#cryptpad = ServerList('cryptpad_servers.lst', 'customize/images/AGPL.png')
#etherpad = ServerList('etherpad_servers.lst', 'locales.json')
#ethercalc = ServerList('ethercalc_servers.lst', 'static/img/davy/bg/home2.png')
#bbb = ServerList('bbb_servers.lst', None)

def reload(signum):
    print("start reload")
    global jitsi
    #global poll
    #global pad
    #global codimd
    #global cryptpad
    #global etherpad
    #global ethercalc
    #global bbb
    #jitsi.renew()
    #poll.renew()
    #pad.renew()
    #codimd.renew()
    #cryptpad.renew()
    #etherpad.renew()
    #ethercalc.renew()
    #bbb.renew()
    print("finish reload")

uwsgi.register_signal(99, "", reload)
uwsgi.add_timer(99, 600)
