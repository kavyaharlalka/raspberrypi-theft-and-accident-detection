import serial
import time

i=1
def send_text(number, text, path='/dev/ttyUSB0'):	
	ser = serial.Serial(path, timeout=5)
     ser.write('AT+CMGF=%d\r' % 1)
	ser.write('AT+CMGS="%s"\r' % number)
	ser.write('%s\x1a' % text)
	ser.close()

while i<=2:
        send_text('+91XXXXXXXX28', 'ENTER PIN')
        i=i+1
time.sleep(5)
i=1
while i<=5:
        ind=""
        temp = 0
        tem = 0
        ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=5)
        ser.write('AT+CMGF=%d\r' % 1)
        ser.write('AT+CMGR=0\r')
        list = ser.readlines()
        for msg in list:
                if "91XXXXXXXX28" in msg:
                        tem=1		
                if tem==1:
                        temp = temp+1		
                if temp==2:
                        ind = msg[0:4]
                        break
        if ind:
                if ">" in ind:
                        i = i+1
                else:
                        break
        else:
                i=i+1
if tem==1:
	if "1234" in ind:
		print "USER RECOGNIZED"
	else:
		print "WRONG PASSWORD"
		tem=0
if tem==0:
	print "VEHICLE STOLEN"
ser.write('AT+CMGD=1,4\r')
ser.close()