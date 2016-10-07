#
#  Copyright (C) 2016 David Brookshire <dave@brookshire.org>
#
import RPi.GPIO as GPIO
import time

BUTTON_GPIO = 4

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
print("MODESET")

GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
print("PING %d SET FOR GPIO.IN" % BUTTON_GPIO)

try:
    while True:
        input_state = GPIO.input(BUTTON_GPIO)
        if not input_state:
            print('Button Pressed')
            while not input_state:
                input_state = GPIO.input(BUTTON_GPIO)
except KeyboardInterrupt:
    GPIO.cleanup()