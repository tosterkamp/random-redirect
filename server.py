import random


def application(env, start_response):
    print(env['HTTP_HOST'])
    if(env['HTTP_HOST'].startswith('jitsi')):
        list = jitsi
    elif(env['HTTP_HOST'].startswith('pad')):
        list = pad
    else:
        start_response('404', [()])
        return [b"test"]
    list.renew()
    start_response('302', [('Location',random.choice(list.servers))])
    #start_response('302', [('Location',random.choice(urls))])
    return [b"redirected"] 



class ServerList:
    def __init__(self, filename):
        self.file = 'res/' + filename
        self.servers = []


    def renew(self):
        self.servers.clear()
        with open(self.file, 'r') as f:
            self.servers = f.readlines()


jitsi = ServerList('jitsi_servers.lst')
pad = ServerList('pad_servers.lst')
