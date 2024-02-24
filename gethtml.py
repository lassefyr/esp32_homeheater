import readPrice

htdata_1="""<!DOCTYPE html>
<html>
<head>
<title>Pajutie 25B Boiler</title>
<style>
.parent {
text-align: left;
}
.myGage {
display: inline-block;
vertical-align: middle;
width:auto; 
height:100px
}
.chart {
width: auto;
height: auto;
border: 1px solid black;
}
.pushable {
background: rgb(0, 102, 0);
border-radius: 12px;
border: none;
padding: 0;
cursor: pointer;
outline-offset: 4px;
}
.front {
    display: block;
    padding: 12px 42px;
    border-radius: 12px;
    font-size: 1.25rem;
    background: rgb(0, 153, 51);
    color: white;
    transform: translateY(-6px);
  }

.pushable:active .front {
    transform: translateY(-2px);
  }
</style>
</head>
<body>
<h1>Temperature Graph</h1>
<button class="pushable" id="button1">
<span class="front">
Price Up
</span>
</button>

<button class="pushable" id="button2">
<span class="front">
Price Down
</span>
</button>
<script>
    // JavaScript code to handle button clicks
    var button1 = document.getElementById("button1");
    var button2 = document.getElementById("button2");

    button1.addEventListener("click", function() {
        fetch(`/pup`)
        .then(response => {
        console.log(response);
        location.reload(true);
        })
        .catch(error => {
        console.log(error)
        });
    });

    button2.addEventListener("click", function() {
        fetch(`/pdown`)
        .then(response => {
        console.log(response);
        location.reload(true);
        })
        .catch(error => {
        console.log(error)        
        });
    });
</script>



<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/raphael/2.1.4/raphael-min.js"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/justgage/1.2.9/justgage.min.js"></script>

<div class='parent'>
<div class="myGage" id="gage1"></div>
<div class="myGage"> <p></p><b>Current Time: </b>"""

htdata_2="""<br><b>Boiler State: </b><input type="checkbox" disabled="disabled\""""


htdata_3="""</div>
</div>

<script type="text/javascript">
mySectors = {
  percents: true, // lo and hi values are in %
  ranges: [{
    color : "#FA8072",
    lo : 0,
    hi : 49
  },
  {
    color : "#FFFF99",
    lo : 50,
    hi : 59
  },
  {
    color : "#ADFF2F",
    lo : 60,
    hi : 100
  }]
}
    function drawGage() {
        var g1 = new JustGage({
            id: "gage1",
            value: """

htdata_4 = """,
            min: 0,
            max: 100,
            symbol: '°C',
            pointer: true,
            pointerOptions: {
                toplength: 10,
                bottomlength: 10,
                bottomwidth: 2
            },
            customSectors: mySectors,
            gaugeWidthScale: 0.9,
            startAnimationTime: 500,
            startAnimationType: ">",
            label: "Boiler Temp.",
        });
    }
    drawGage();
</script>

<script>
        // JavaScript code to handle button clicks
        var button1 = document.getElementById("button1");
        var button2 = document.getElementById("button2");

        button1.addEventListener("click", function() {
                fetch(`/pup`)
                .then(response => {
                console.log(response)
                })
                .catch(error => {
                console.log(error)
                });
        });

        button2.addEventListener("click", function() {
                fetch(`/pdown`)
                .then(response => {
                console.log(response)
                })
                .catch(error => {
                console.log(error)
                });
        });
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js"></script>
<div class="chart">
        <canvas id="myChart"></canvas>
</div>
<script>
const ctx = document.getElementById('myChart').getContext('2d');
const data = {
        labels: ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'],
        datasets: [
        {
        type: 'bar',
        label: 'Bar Dataset',
        data: ["""

htdata_5="""],
    backgroundColor:  ["""
    
htdata_6="""],
    borderColor: 'rgba(75, 192, 192, 1)',
    borderWidth: 1
    },
    {
    type: 'line',
    label: 'Cost Limit',
    data: ["""  
    #0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05
    
htdata_7="""],
    fill: false,
    borderColor: 'rgba(192, 75, 192, 1)',
    borderWidth: 2
    }]};

const chart = new Chart(ctx, {
    type: 'bar',
    data: data,
    options: {
        animation: false,
        responsive: true,
        scales: {
            y: {
            beginAtZero: true
            }
        }
    }
});
</script>
</body>
</html>"""

#import onewire, ds18x20

class getHTML:
    def __init__(self):
        self.myP=readPrice.currPrice()

    def gTemp(self):        
        return("{:.1f}".format(self.myP.getT()))

    def limUp(self):        
        myF = self.myP.getLim()
        myF+=0.005
        if myF > 0.20:
            myF = 0.20
        self.myP.setLim(myF)
        del myF
        
    def limDown(self):
        myF = self.myP.getLim()
        myF-= 0.005
        if myF<0.005:
            myF = 0
        self.myP.setLim(myF)
        del myF
    
    def getTime(self):
        myT = self.myP.getTime()
        print(str(self.myP.getTime()))
        Dy, Dm, Dd, Dx, Dh, Dmi, Ds1, Ds2 = (myT)
        df = "{:02d}/{:02d}/{} {:02d}:{:02d}"
        return(df.format(Dd, Dm, Dy, self.myP.getCH(), Dmi))        
    
    def getPrices(self):
        myprices = ""
        for i in range(24):     
            myprices = myprices+str(self.myP.getCurrPrice(i))
            if i >= 23:
                print(myprices)
                return myprices
            myprices = myprices + ","
    
    def getBkCol(self):
        mycolor = ""
        
        for i in  range(24):
            if( self.myP.limP>self.myP.getCurrPrice(i) ):
                if(i==self.myP.getCH()):
                    mycolor = mycolor + "\"#20a020\""
                else:
                    mycolor = mycolor + "\"#00f000\""
            else:
                if(i==self.myP.getCH()):
                    mycolor = mycolor + "\"#a02020\""
                else:
                    mycolor = mycolor + "\"#f00000\""
            if i >= 23:
                return mycolor
            mycolor = mycolor + ","
                
    def getLimit(self):
        limitval = ""
        for i in range(24):
            limitval = limitval + str(self.myP.limP)
            if i >= 23:
                return limitval
            limitval = limitval + ","
            
    def getPage(self):
        yield(htdata_1)
        #yield("1.2.2022 18:30")#self.getTime()) #timefun
        yield(self.getTime()) #timefun
        yield(htdata_2)
        yield(self.myP.gOnOffSt())
        yield(htdata_3)
        yield(self.gTemp())
        yield(htdata_4)
        yield(self.getPrices())
        yield(htdata_5)
        yield(self.getBkCol())
        yield(htdata_6)
        yield(self.getLimit())        
        yield(htdata_7)

'''
myGet = getHTML()
result=myGet.getPage()
print(next(result), end="")
print(next(result), end="")
print(next(result), end="")
print(next(result), end="")
print(next(result), end="")
print(next(result), end="")
print(next(result))
'''