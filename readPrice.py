from machine import RTC
import urequests as requests
#import requests
import json

#url = "https://api.porssisahko.net/v1/latest-prices.json"  # Replace with the actual URL
url = "https://api.spot-hinta.fi/Today"

class currPrice:
    needRd = True
    curPr=[]
    clkDev = 0
    limP = 0.07
    oOff = False
    temp = 0

    def gOnOffSt(self) -> str:
        if currPrice.oOff:
            return("checked=\"checked\"> <label>Boiler ON</label>")
        else:
            return("> <label>Boiler OFF</label>")
    
    def setT(self, cT):
        currPrice.temp = cT
    
    def getT(self) -> float:
        return(currPrice.temp)
        
    def setLim(self, value):
        #print("setlimit to " + str(value))
        currPrice.limP = value
    
    def getLim(self):
        return currPrice.limP
        
    def read_json_from_url(self):
        try:
            #f=open("Today.json")
            #json_data = json.load(f)
            response = requests.get(url=url)            
            json_data = response.json()            
            return json_data
        except:
            print("Error in read_json")
            return None

    def getCurrPrice(self, myH) -> float:
        if len(currPrice.curPr)>myH:
            return(currPrice.curPr[myH])
        return(0)

    def get7H(self) -> float:
        tlist = sorted(currPrice.curPr, key=lambda x:float(x))
        if len(tlist) == 24:
            currPrice.limP = tlist[6]+0.005
            del tlist
        return(currPrice.limP)

    def getCH(self) -> int:
        now = RTC().datetime()
        myH=int(now[4])+currPrice.clkDev
        del now
        if(myH>=24):
            myH=myH-24
        return(myH)

    def getTime(self):
        return(RTC().datetime())

    def getPriceNow(self):
        return(currPrice.curPr[self.getCH()])

    def getCurClkDev(self):
        return currPrice.clkDev

    def setCurClkDev(self, cDev):
        currPrice.clkDev = cDev

    def forceUpd(self):
        currPrice.needRd=True
        self.checkIfUpd(0)

    def checkIfUpd(self, hour):
        if currPrice.needRd and hour == 0:
            myData = self.read_json_from_url( )
            if myData is not None:
                currPrice.curPr = []
                currPrice.needRd = False
                myStr=myData[0]["DateTime"]   # Format "2023-06-19T00:00:00+03:00"
                #print(myStr[21:22])
                try:
                    self.setCurClkDev(int(myStr[21:22]))
                except ValueError:
                    self.setCurClkDev(2)
                for i in myData:
                    currPrice.curPr.append(i["PriceWithTax"])
                self.get7H()
            del myData

        if hour == 23:
            currPrice.needRd = True
