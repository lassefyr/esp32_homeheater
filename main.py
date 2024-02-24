from machine import Pin
from machine import Timer
from machine import RTC
from ds18x20 import DS18X20

import onewire 
import uasyncio
import ntptime
import gethtml
import readPrice
import secrets

#url1 = "https://api.spot-hinta.fi/JustNow"
#url1="http://worldtimeapi.org/api/timezone/Europe/Helsinki"
    
class LEDModule:
    """This will represent our LED"""
    
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.led_pin = Pin(self.pinNumber, Pin.OUT)
        
    def get_value(self):
        return self.led_pin.value()
    
    def set_on(self):
        self.led_pin.value(1)

    def set_off(self):
        self.led_pin.value(0)

    def toggle(self):
        self.led_pin.value(not self.get_value())

class HState:
    def __init__(self):        
        self.p15kW = Pin(12, Pin.OUT, value=0)
        self.p9kW = Pin(14, Pin.OUT, value=0)
        self.pIn = Pin(27, Pin.IN, Pin.PULL_UP)
        self.pTemp = onewire.OneWire(Pin(26, Pin.IN, Pin.PULL_UP))
        self.ds = DS18X20(self.pTemp)
        self.roms = self.ds.scan()
        self.noT = True
        if len(self.roms) == 1:
            self.noT = False
            self.ds.convert_temp()
        self.tavg = [22.2,22.3,22.2]
        self.abeg = 0        
        self.tim15kW = 0        
        
    def tempRead(self):
        if self.noT == True:
            return
        
        try:
            self.tavg[self.abeg] = self.ds.read_temp(self.roms[0])
        except onewire.OneWireError:
            readPrice.currPrice.temp = 0
            print("Temp Error")
            return
                
        self.abeg+=1
        if(self.abeg>2):
            self.abeg = 0
        ave = sum(self.tavg)/len(self.tavg)
        readPrice.currPrice.temp = ave
        print( str(ave) )
        self.ds.convert_temp()
                
    def en_15kW(self):
        self.p15kW.value(1)
    
    def dis_15kW(self):
        self.p15kW.value(0)

    def en_9kW(self):
        self.p9kW.value(1)
        
    def dis_9kW(self):
        self.p9kW.value(0)
    
    def chk15kW(self):
        if(self.pIn.value()):
            self.tim15kW+=1
            if(self.tim15kW > 10):
                self.tim15kW = 10
                self.en_9kW()
        else:
            self.dis_9kW()
            self.tim15kW=0
                

def myTimer(t):
    print("Timer")
    pass

async def myBG():
    '''
    from machine import WDT
    wdt = WDT(timeout=2000)  # enable it with a timeout of 2s
    wdt.feed()'''
    import readPrice
    # Our LED Module
    led_m = LEDModule(2)
    relMod = HState()
    
    ntptime.settime()
    myP = readPrice.currPrice()
    myP.forceUpd()
    await uasyncio.sleep(1) # wait for temp conversion
    
    while True:        
        now = RTC().datetime()        
        myP.checkIfUpd(myP.getCH())        
        print("CurPrice = "+str(myP.getCurrPrice(myP.getCH())))
        print("Limit = "+str(myP.getLim()))
        print(gc.mem_free())
        if( myP.getPriceNow() > myP.getLim()):
            print("drives OFF")
            readPrice.currPrice.oOff=False
            relMod.dis_15kW()
        else:
            print("Halpaa -- ON")
            readPrice.currPrice.oOff=True
            relMod.en_15kW()
        relMod.chk15kW()
        led_m.toggle()
        relMod.tempRead()
        
        await uasyncio.sleep(10)        
        #print("Local time after synchronization：%s" %str(time.localtime()))

def doConnect():
    import network
    import machine
    import time
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.connect(secrets.SSID, secrets.PASSWORD)
        for retry in range(200):
            connected = sta_if.isconnected()
            if connected:
                break
            time.sleep(0.1)
            print('.', end='')
        if connected:
            print('\nConnected. Network config: ', sta_if.ifconfig())
        else:
            print("Failed connection")
            machine.soft_reset()
        '''
        try:
            sta_if.connect(ssid, password)
        except OSError as e:
            print("Failed connection")
        uasyncio.sleep(10)                
        if( not sta_if.isconnected() ):
            print("Failed connection")
            machine.soft_reset()
        '''
    #print("Connected! Network config:", sta_if.ifconfig())    
        #while not sta_if.isconnected():
        #    pass
    #print('Connected! Network config:', sta_if.ifconfig())

gc.collect()
from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template

print("Connecting to your wifi...")
doConnect()

#tim1 = Timer(1)
#tim1.init(period=10000, mode=Timer.PERIODIC, callback=myTimer)

uasyncio.create_task(myBG())
myGet = gethtml.getHTML()

app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/')
async def index(request):
    return myGet.getPage() #, led_value=led_module.get_value(5))

@app.route('/toggle')
async def toggle_led(request):
    print("Receive Toggle Request!")
    led_module.toggle()
    return "OK"

@app.route('/pup')
async def priceUp(request):
    myGet.limUp()
    print("PriceUp!")
    return "OK"

@app.route('/pdown')
async def priceDown(request):
    myGet.limDown()
    print("PriceDown!")
    return "OK"

@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'

@app.route('/static/<path:path>')
def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)

app.run()



