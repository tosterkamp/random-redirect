import random


def application(env, start_response):
    print(env['HTTP_HOST'])
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
    else:
        redirect_server = 'https://github.com/tosterkamp/random-redirect/'
    
    print('redirect from ' + env['HTTP_HOST'] + ' to ' + redirect_server)
    start_response('302', [('Location', redirect_server)])
    return [b"redirected"] 



class ServerList:
    def __init__(self, filename):
        self.file = 'res/' + filename
        self.servers = []

    def get_random(self):
        self.renew()
        return random.choice(self.servers)

    def renew(self):
        self.servers.clear()
        with open(self.file, 'r') as f:
            self.servers = f.readlines()


jitsi = ServerList('jitsi_servers.lst')
poll = ServerList('poll_servers.lst')
pad = ServerList('pad_servers.lst')
codimd = ServerList('codimd_servers.lst')
cryptpad = ServerList('cryptpad_servers.lst')
etherpad = ServerList('etherpad_servers.lst')
ethercalc = ServerList('ethercalc_servers.lst')
