#
#  Copyright (C) 2016 David Brookshire <dave@brookshire.org>
#
import time

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


def do_blink(lamp, count=1, delay=0.5):
    while count:
        lamp.on()
        time.sleep(delay)
        lamp.off()
        time.sleep(0.2)
        count -= 1


def do_shutdown(*leds):
    if len(leds) >= 2:
        do_blink(leds[0], 4)
        do_blink(leds[1], 1)
    else:
        do_blink(leds[0], 4)
        do_blink(leds[0], 1, 5)

    for l in leds:
        l.off()

if __name__ == '__main__':

    # GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    lamp1 = Lamp(LED1_GPIO)
    lamp2 = Lamp(LED2_GPIO)
    trigger = Button(BUTTON_GPIO)

    try:
        while True:
            input_state = trigger.get_state()

            if not input_state:
                print("Button pressed")
                i = 0
                while not input_state:
                    if i % 2:
                        lamp1.on()
                        lamp2.off()
                    else:
                        lamp1.off()
                        lamp2.on()

                    i += 1
                    time.sleep(0.2)
                    input_state = trigger.get_state()

                print("Button released")
                lamp1.off()
                lamp2.off()

    except KeyboardInterrupt:
        print("Shutting down")
        do_shutdown(lamp1, lamp2)
        GPIO.cleanup()
        print("Exiting")
