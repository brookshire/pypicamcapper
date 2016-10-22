#
#  Copyright (C) 2016 David Brookshire <dave@brookshire.org>
#
import time

import RPi.GPIO as GPIO

RELAY1_GPIO = 18


class Relay():
    state = False  # True==On, False==Off
    gpio = None

    def __init__(self, gpio):
        self.gpio = gpio
        GPIO.setup(self.gpio, GPIO.OUT)

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
    relay1 = Relay(RELAY1_GPIO)
    count = 0
    try:
        while True:
            if count % 2:
                relay1.on()
            else:
                relay1.off()

            count += 1
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Shutting down")
        GPIO.cleanup()
        print("Exiting")
