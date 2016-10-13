#
#  Copyright (C) 2016 David Brookshire <dave@brookshire.org>
#
from sense_hat import SenseHat
from time import sleep

from random import randint

min_color_value = 40
max_color_value = 120
delay = 1

def gen_color():
    r = randint(min_color_value, max_color_value)
    g = randint(min_color_value, max_color_value)
    b = randint(min_color_value, max_color_value)
    return [r, g, b]

def build_display():
    i = 0
    ret = []
    while i < 64:
        ret.append(gen_color())
        i += 1
    return ret

sense = SenseHat()

try:
    while True:
        sense.set_pixels(build_display())
        sleep(delay)
except KeyboardInterrupt:
    sense.clear()