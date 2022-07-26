import urllib.request
import ssl, json, pprint
import time
import keyboard
import os, sys

class Huecontrol:
    
    global context
    context = ssl._create_unverified_context()
    
    def __init__(self, user, ip, all_lights):
        self.user = user
        self.ip = ip
        self.all_lights = all_lights
    
    def get_json(self, url):
        req = urllib.request.Request(url=url, method='GET')
        f = urllib.request.urlopen(req, context=context)
        return json.loads(f.read())

    def put(self, url, content):
        req = urllib.request.Request(url=url,
            data=content.encode('UTF-8'), method='PUT')
        f = urllib.request.urlopen(req, context=context)
    
    def getinformation(self):
        # Get informations about all hue lights
        data = self.get_json(f'https://{ip}/api/{self.user}/lights')
        pp = pprint.PrettyPrinter(indent=4)   
        pp.pprint(data)       
              
    def keyboarddefs(self,name):
        # Return values for the number, duration, brightness and temperature of the lights:
        # [Nr of light, duration in s, Brightness "bri" 1...254, colortemperature "ct" 153...500]
        # Use template to define keys
        keydict = {
        "w": [3,0.2], 
        "e": [8,0.2],
        "r": [9,0.2],
        "t": [3,0.2,10],
        "z": [3,0.2,200],
        "u": [3,0.2,10,153],
        "i": [3,0.2,200,500]
        }
        if name in keydict:
            val = keydict.get(name)
            return val
        elif name not in keydict:
            return [None,None]

    def turnon(self,*vals):
        """turn on lights to specified values in keyboarddefs"""
        if vals[0] != None:
            light = vals[0]
            duration = vals[1]
            self.put(f'https://{ip}/api/{self.user}/lights/{light}/state', '{"on":true}')
            if len(vals) >= 3:
                brightness = vals[2]
                put_string = "{\"bri\":" + str(brightness) + "}"
                self.put(f'https://{ip}/api/{self.user}/lights/{light}/state', put_string)
            if len(vals) >=4:
                colortemp = vals[3]
                put_string = "{\"ct\":" + str(colortemp) + "}"
                self.put(f'https://{ip}/api/{self.user}/lights/{light}/state', put_string)
            time.sleep(duration)
            self.put(f'https://{ip}/api/{self.user}/lights/{light}/state', '{"on":false}')   
        else:
            pass
        
    def resetlights(self, *lights):
        # Reset all lights to specified values of brightness and colortemp and turn them off
        for il in lights:
            print("Reset light",il)
            light = il
            self.put(f'https://{ip}/api/{self.user}/lights/{light}/state', '{"on":true}')
            brightness = 1
            put_string = "{\"bri\":" + str(brightness) + "}"
            self.put(f'https://{ip}/api/{self.user}/lights/{light}/state', put_string)
            colortemp = 153
            put_string = "{\"ct\":" + str(colortemp) + "}"
            self.put(f'https://{ip}/api/{self.user}/lights/{light}/state', put_string)
            self.put(f'https://{ip}/api/{self.user}/lights/{light}/state', '{"on":false}') 
            
    def initswitchoff(self, *lights):
        # Initially switch off all lights 
        time.sleep(0.4)
        for il in lights:
            print("Switch off light",il)
            light = il
            try:
                self.put(f'https://{ip}/api/{self.user}/lights/{light}/state', '{"on":false}')
                time.sleep(0.4)
            except Exception as e:
                print(e)
                print("---------------------")
                print("""No connection...quitting program! 
                I) Check wifi and connection to bridge. 
                II) Check user and IP.
                III) Try again""")
                time.sleep(5)
                sys.exit()

    def callback(self, event):
        name = event.name
        if name == "a":
            print("Reset lights")
            self.resetlights(*self.all_lights)
        
        if name == "q":
            print("Key pressed:", name)  
            print("Q for quit pressed...quitting!")
            os._exit(0) # Because sys.exit doesnt exit keyboard hook...WIP       
        else:
            vals = self.keyboarddefs(name)
            self.turnon(*vals)         
    
    def start(self):
        print("---Start---")
        print("User:",self.user)
        print("IP:  ",self.ip)
        print("Switch off lights")
        self.initswitchoff(*self.all_lights)
        keyboard.on_release(callback=self.callback)
        keyboard.wait()
        

# ------------------------------------------------------------------
# Setup User and IP of HUE Bridge
user = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # User Bridge
ip = 'XXX.XXX.XXX.X'                              # IP der Bridge
all_lights = [3,8,9]                              # lights to control
# ------------------------------------------------------------------

huecontrol = Huecontrol(user=user,ip=ip,all_lights=all_lights)
huecontrol.getinformation()
huecontrol.start()
