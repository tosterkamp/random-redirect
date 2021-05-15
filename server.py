import random
import requests
from datetime import datetime, timedelta
import threading
import time
import logging
import uwsgi



def application(env, start_response):
    if(env['HTTP_HOST'].startswith('jitsi')):
        redirect_server = jitsi.get_random()
    elif(env['HTTP_HOST'].startswith('poll')):
        redirect_server = poll.get_random()
    elif(env['HTTP_HOST'].startswith('pad')):
        redirect_server = pad.get_random()
    elif(env['HTTP_HOST'].startswith('hedgedoc')):
        redirect_server = hedgedoc.get_random()
    elif(env['HTTP_HOST'].startswith('cryptpad')):
        redirect_server = cryptpad.get_random()
    elif(env['HTTP_HOST'].startswith('etherpad')):
        redirect_server = etherpad.get_random()
    elif(env['HTTP_HOST'].startswith('ethercalc')):
        redirect_server = ethercalc.get_random()
    elif(env['HTTP_HOST'].startswith('bbb')):
        redirect_server = bbb.get_random()
    elif(env['HTTP_HOST'].startswith('lstu')):
        redirect_server = lstu.get_random()
    else:
        redirect_server = 'https://timo-osterkamp.eu/random-redirect.html'

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
        self.test_request = t_request;
        self.servers = []
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
            self.servers = online
            self.offline_servers = offline
            self.lock.release()
            #print("online: ")
            #print(self.servers)






jitsi = ServerList('jitsi_servers.lst', 'sounds/outgoingRinging.wav')
poll = ServerList('poll_servers.lst', 'images/date.png')
pad = ServerList('pad_servers.lst', None)
hedgedoc = ServerList('hedgedoc_servers.lst', 'screenshot.png')
cryptpad = ServerList('cryptpad_servers.lst', 'customize/images/AGPL.png')
etherpad = ServerList('etherpad_servers.lst', 'locales.json')
ethercalc = ServerList('ethercalc_servers.lst', 'static/img/davy/bg/home2.png')
bbb = ServerList('bbb_servers.lst', None)
lstu = ServerList('lstu_servers.lst', None)

def reload(signum):
    print("start reload")
    global jitsi
    global poll
    global pad
    global hedgedoc
    global cryptpad
    global etherpad
    global ethercalc
    global bbb
    global lstu
    jitsi.renew()
    poll.renew()
    pad.renew()
    hedgedoc.renew()
    cryptpad.renew()
    etherpad.renew()
    ethercalc.renew()
    bbb.renew()
    lstu.renew()
    print("finish reload")

uwsgi.register_signal(99, "", reload)
uwsgi.add_timer(99, 600)
