#
#  Copyright (C) 2016 David Brookshire <dave@brookshire.org>
#
import time
import sys

import RPi.GPIO as GPIO

class Relay():
    state = False  # True==On, False==Off
    gpio = None

    def __init__(self, gpio):
        self.gpio = gpio
        GPIO.setup(self.gpio, GPIO.OUT)
        self.off()

    def __repr__(self):
        return "Relay-%d" % self.gpio

    def on(self):
        GPIO.output(self.gpio, True)
        self.state = True

    def off(self):
        GPIO.output(self.gpio, False)
        self.state = False


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    relays = []

    for i in 17,18,27,22,23:
        r = Relay(i)
        r.off()
        relays.append(r)

    count = 0
    dir = True
    print(len(relays))
    try:
        while True:
            print(count)
            if relays[count].state:
                relays[count].off()
            else:
                relays[count].on()

            count += 1
            if count >= len(relays):
                count = 0
            time.sleep(.25)

    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)