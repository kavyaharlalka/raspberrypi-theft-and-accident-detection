import urllib2, time
import serial
import RPi.GPIO as GPIO

delay = 1

GPIO.setmode(GPIO.BOARD)    

def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=5)
cd=1
ck=0
fd=''
s1=0.0
s2=0.0
while 1==1:
    while ck <= 50:
        rcv = port.read(10)

        fd=fd+rcv
        ck=ck+1
    #print fd
    if '$GPRMC' in fd:
        ps=fd.find('$GPRMC')
        dif=len(fd)-ps
        #print dif
        if dif > 50:
            data=fd[ps:(ps+50)]
            p=list(find(data, ","))
            lat=data[(p[2]+1):p[3]]
            lon=data[(p[4]+1):p[5]]

            s1=lat[2:len(lat)]
            s1=Decimal(s1)
            s1=s1/60
            s11=int(lat[0:2])
            s1=s11+s1

            s2=lon[3:len(lon)]
            s2=Decimal(s2)
            s2=s2/60
            s22=int(lon[0:3])
            s2=s22+s2
            if s1>0.0:
                if s2>0.0:
                    break
port.close()
print s1
print s2
data = s1 + "," + s2
print data
def publishtoInternet(temp):
    print url
    result = urllib2.urlopen(url).read()
    print result+ str(temp)
publishtoInternet(data)
