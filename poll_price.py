import machine
import time
import network
import urequests as requests
import ujson as json

ssid = "pokonet"    # Replace with Your SSID
password = 'pokodeRgeniuS2' # Replace with Your Password
#url1 = "https://api.spot-hinta.fi/JustNow"
url1="http://worldtimeapi.org/api/timezone/Europe/Helsinki"
sta_if = network.WLAN(network.STA_IF)

sta_if.active(True) #Activate interface
#sta_if.disconnect()
myctr = 0
try:
    sta_if.connect(ssid, password) 		# Connect to an AP
    
except OSError as e:
    print("could not connect to AP, retrying: ", e)    

if( sta_if.isconnected() ):
    print("Connected")
    print(sta_if.ifconfig())
else:
    print("Failed connection")
    machine.soft_reset()

gc.enable()
led = machine.Pin(2, machine.Pin.OUT)
#myhdr = {Rank DateTime PriceNoTax PriceWithTax}
while True:
    led.value(1)
    time.sleep(4)
    print(gc.mem_free())
    myctr+=1
    if(myctr>10):
        myctr=0
        gc.collect()#runs out without this 103808, 103808
    
    if( sta_if.isconnected()):
        try:
            curPrice=requests.get(url=url1)
#        curPrice.close()
#            print( curPrice.text )
        except:
            print("Error in request get")
            continue
 #           print(str(curPrice.status_code))
 
        #curPrice.close()
           
    print(type(curPrice))
    if(curPrice.status_code==200):
        try:
            mytext = curPrice.json()
        except ValueError:
            print("can not parse curPrice")
            continue        
            
    #print(curPrice.text)
    #parsed = json.dumps(curPrice)
    try:
        myPrice = mytext.get("utc_datetime")        
    except ValueError:
        print("can not get value")
        continue
    
    curPrice.close()
    #print("kakki")
    print(str(myPrice))
    #print(curPrice.json())
    #print(curPrice.json("PriceWithTax"))
    print("tossa")
    #try:
     #   json.loads(curPrice)        
    #except ValueError as e:
     #   print("no valid json")

    
    
    led.value(0)
    time.sleep_ms(200)