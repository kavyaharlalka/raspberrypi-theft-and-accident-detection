import serial
import RPi.GPIO as GPIO      
import os, time
from pygeocoder import Geocoder
import sqlite3
from decimal import *

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
i=1
results = Geocoder.reverse_geocode(19.17496166666666666666666667, 72.86765)
print results.postal_code
sqlite_file = '/home/pi/Zipcodes.db'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
text = ('SELECT phone from zip WHERE postalcode = "%s"' %results.postal_code)
c.execute(text)
temp = c.fetchone()[0]
print temp
conn.close()
def send_text(number, text, path='/dev/ttyUSB0'):   
    ser = serial.Serial(path, timeout=5)
    ser.write('ATZ\r')
    ser.write('ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0\r')
    ser.write('AT+CGDCONT=1,"IP","airtelgprs.com"\r')
    ser.write('AT+CMGF=%d\r' % 1)
    ser.write('AT+CSCS="GSM"\r')
    ser.write('AT+CMGS="%s"\r' % temp)
    ser.write('%s\x1a' % text)
    ser.close()

while i<=2:
    send_text('+91XXXXXXXX28', 'ACCIDENT AT http://maps.google.com/maps?q=%s,%s' %(s1,s2))
    i=i+1