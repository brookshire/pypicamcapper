#
#  Copyright (C) 2016 David Brookshire <dave@brookshire.org>
#
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
print("MODESET")

GPIO.setup(17, GPIO.OUT)
print("PING 17 SET FOR GPIO.OUT")

GPIO.setup(18, GPIO.OUT)
print("PING 18 SET FOR GPIO.OUT")

i = 0

try:
    while True:
        if i % 2:
            GPIO.output(17, True)
            GPIO.output(18, False)
        else:
            GPIO.output(17, False)
            GPIO.output(18, True)

        i += 1
        time.sleep(0.2)
except KeyboardInterrupt:
    print("Deactivating LEDs")
    GPIO.output(17, False)
    GPIO.output(18, False)
    print("Exiting")
