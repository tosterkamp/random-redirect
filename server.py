import random
import requests
from datetime import datetime, timedelta
import threading
import time
import logging
import uwsgi
import server_utils



def application(env, start_response):
    if(env['HTTP_HOST'].startswith('jitsi')):
        redirect_server = jitsi.get_random()
    elif(env['HTTP_HOST'].startswith('poll')):
        redirect_server = poll.get_random()
    elif(env['HTTP_HOST'].startswith('pad')):
        redirect_server = pad.get_random()
    elif(env['HTTP_HOST'].startswith('codimd')):
        redirect_server = codimd.get_random()
    elif(env['HTTP_HOST'].startswith('cryptpad')):
        redirect_server = cryptpad.get_random()
    elif(env['HTTP_HOST'].startswith('etherpad')):
        redirect_server = etherpad.get_random()
    elif(env['HTTP_HOST'].startswith('ethercalc')):
        redirect_server = ethercalc.get_random()
    elif(env['HTTP_HOST'].startswith('bbb')):
        redirect_server = bbb.get_random()
    else:
        redirect_server = 'https://github.com/tosterkamp/random-redirect/'
    
    print('redirect from ' + env['HTTP_HOST'] + ' to ' + redirect_server)
    start_response('302', [('Location', redirect_server)])
    return [b"redirected"] 



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

    def get_random(self):
        """
        return a random server from self.list
        """
        self.lock.acquire()
        tmp = random.choice(self.servers)
        self.lock.release()
        return tmp

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
            self.lock.acquire()
            props = []
            for i in range(len(online)):
                props.append(1)
                tmp_dict = {
                    "badHoster": server_utils.trustworthyHoster(online[i])
                }
                #self.properties[i]["badHoster"] = server_utils.trustworthyHoster(online[i])
                props[i] = tmp_dict
            print(self.props)

            self.servers = online
            self.offline_servers = offline
            self.lock.release()
            #print("online: ")
            #print(self.servers)





jitsi = ServerList('jitsi_servers.lst', 'sounds/outgoingRinging.wav')
poll = ServerList('poll_servers.lst', 'images/date.png')
pad = ServerList('pad_servers.lst', None)
codimd = ServerList('codimd_servers.lst', 'screenshot.png')
cryptpad = ServerList('cryptpad_servers.lst', 'customize/images/AGPL.png')
etherpad = ServerList('etherpad_servers.lst', 'locales.json')
ethercalc = ServerList('ethercalc_servers.lst', 'static/img/davy/bg/home2.png')
bbb = ServerList('bbb_servers.lst', 'html5client/resources/sounds/LeftCall.mp3')

def reload(signum):
    print("start reload")
    global jitsi
    global poll
    global pad
    global codimd
    global cryptpad
    global etherpad
    global ethercalc
    global bbb
    jitsi.renew()
    poll.renew()
    pad.renew()
    codimd.renew()
    cryptpad.renew()
    etherpad.renew()
    ethercalc.renew()
    bbb.renew()
    print("finish reload")

uwsgi.register_signal(99, "", reload)
uwsgi.add_timer(99, 600)
