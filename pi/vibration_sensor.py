import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN)
count = 0

while 1==1:
    value = GPIO.input(16)
    if value == 1:
        count = count+1
    else:
        if count>100000:
            print count
        count = 0