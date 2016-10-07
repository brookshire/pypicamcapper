#
#  Copyright (C) 2016 David Brookshire <dave@brookshire.org>
#
import time
import picamera
import datetime
import os

import RPi.GPIO as GPIO

BUTTON_GPIO = 4
LED1_GPIO = 17
LED2_GPIO = 18


class Lamp():
    state = False  # True==On, False==Off
    gpio = None

    def __init__(self, gpio):
        self.gpio = gpio
        GPIO.setup(self.gpio, GPIO.OUT)

    def __repr__(self):
        return "LAMP-%d" % self.gpio

    def on(self):
        GPIO.output(self.gpio, True)

    def off(self):
        GPIO.output(self.gpio, False)


class Button():
    gpio = None

    def __init__(self, gpio):
        self.gpio = gpio
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __repr__(self):
        return "BUTTON-%d" % self.gpio

    def get_state(self):
        return GPIO.input(self.gpio)

class CamCapper():
    def __init__(self,
                 prefix="wc",
                 delay=2,
                 target_dir="/tmp",
                 rotate=False):
        self.prefix = prefix
        self.delay = delay
        self.target_dir = target_dir
        self.cam = picamera.PiCamera()
        self.cam.led = True
        if rotate:
            self.cam.rotation = 180

    def take_snapshot(self):
        ds = datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S")
        fname = os.path.join(self.target_dir,
                             self.prefix + "." + ds + ".jpg")
        self.cam.capture(fname)
        time.sleep(self.delay)

def do_blink(lamp, count=1, delay=0.5):
    while count:
        lamp.on()
        time.sleep(delay)
        lamp.off()
        time.sleep(0.2)
        count -= 1


def warn_message(*leds):
    if len(leds) >= 2:
        do_blink(leds[0], 4, 0.5)
        do_blink(leds[1], 1)
    else:
        do_blink(leds[0], 4, 0.5)
        do_blink(leds[0], 1, 1)

    for l in leds:
        l.off()

if __name__ == '__main__':

    # GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    lamp1 = Lamp(LED1_GPIO)
    lamp2 = Lamp(LED2_GPIO)
    trigger = Button(BUTTON_GPIO)
    cam = CamCapper(target_dir='/var/www/html',
                    rotate=True)

    try:
        while True:
            input_state = trigger.get_state()

            if not input_state:
                print("Button pressed")
                warn_message(lamp1, lamp2)
                cam.take_snapshot()

    except KeyboardInterrupt:
        print("Shutting down")
        do_blink(lamp2, 4)
        GPIO.cleanup()
        print("Exiting")
