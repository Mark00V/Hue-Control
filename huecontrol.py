import urllib.request
import ssl, json, pprint
import time
import keyboard
import os

# Use keyboard to access lamps piano-style
# Delay required for standard lamps, no delay for entertainment lamps

class Huecontrol:
    
    global context
    context = ssl._create_unverified_context()
    
    def __init__(self, user, ip):
        self.user = user
        self.ip = ip
    
    def get_json(self, url):
        req = urllib.request.Request(url=url, method='GET')
        f = urllib.request.urlopen(req, context=context)
        return json.loads(f.read())

    def put(self, url, content):
        req = urllib.request.Request(url=url,
            data=content.encode('UTF-8'), method='PUT')
        f = urllib.request.urlopen(req, context=context)
        
    def turnon(self, light, duration):
        light = light
        self.put(f'https://{ip}/api/{user}/lights/{light}/state', '{"on":true}')
        time.sleep(duration)
        self.put(f'https://{ip}/api/{user}/lights/{light}/state', '{"on":false}')
    
    def initswitchoff(self, *lights):
        time.sleep(0.4)
        for il in lights:
            print("Switch off light",il)
            light = il
            self.put(f'https://{ip}/api/{user}/lights/{light}/state', '{"on":false}')
            time.sleep(0.4)

    def callback(self, event):
        name = event.name
        if name == "t":
            self.turnon(3,0.2)
        elif name == "z":
            self.turnon(8,0.2)
        elif name == "u":
            self.turnon(9,0.2)
        elif name == "q":
            print("Key pressed:", name)  
            print("Q for quit pressed...quitting!")
            os._exit(0) 
        
        else:
            pass
        print("Key pressed:", name)            
    
    def start(self):
        print("---Start---")
        print("User:",self.user)
        print("IP:  ",self.ip)
        print("Switch off lights")
        self.initswitchoff(3,8,9)
        keyboard.on_release(callback=self.callback)
        keyboard.wait()
        

# ------------------------------------------------------------------
# Setup User and IP of HUE Bridge
user = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # User Bridge
ip = 'XXX.XXX.XXX.XXX'                            # IP der Bridge
# ------------------------------------------------------------------

huecontrol = Huecontrol(user=user,ip=ip)
huecontrol.start()   
