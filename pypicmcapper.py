#
# Copyright (C) 2016, David Brookshire <dave@brookshire.org>
#
# Process which will manage periodically capturing an image from a raspberry pi camera, and
# uploading it to a remote(ish) website.
#
import argparse
import datetime
import logging
import os
import re
import subprocess
import sys
import time

import picamera

# Regex to provide a unique'ish identifier for naming image capture files.
hwaddr_pat = re.compile('HWaddr [0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:([0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2})')

# Enable debug logging to screen if true
debug = False

# Default sleep time between image captures
default_wait = 10
default_path = "/tmp"
default_prefix = "image"


def fname():
    """
    Determine what the image files from this pi should be named--for now we're using the last three values of
    the MAC address of eth0, as reported by the ifconfig command.  Not truly unique, but good enough for our
    purposes here.

    :return: Return a string to be used in naming the image capture files base on this specific computer.
    """

    cmd = "/sbin/ifconfig eth0"
    p = subprocess.Popen(cmd.split(),
                         stdout=subprocess.PIPE,
                         shell=False)
    rc = p.wait()

    line = p.stdout.readline()
    mo = hwaddr_pat.search(line, re.IGNORECASE)
    if not mo:
        # provide a default value should the ifconfig command above fail to return something useful.
        ret = "image"
    else:
        # use the matching values, but concatenate the hex values, removing the ':' characters.
        ret = mo.group(1).replace(':', '')

    return ret

class PyPiCamCapper():
    def __init__(self, path=default_path, wait=default_wait, prefix=default_prefix):
        """
        Initialize the picamera object at the time we create a PyPiCamCapper instance.

        :param args:
        :param kwargs:
        """
        self.cap_path = path
        self.cap_wait = wait
        self.cap_prefix = prefix
        self.cam = picamera.PiCamera()
        self.logger = logging.getLogger(__name__)  # .addHandler(NullHandler)

        if debug:
            logger_handler = logging.StreamHandler(sys.stdout)
            logger_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
            logger_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(logger_handler)
            self.logger.setLevel(logging.DEBUG)



    def run(self):
        self.logger.info("Starting capture, every %d seconds, to %s, named %s." % (self.cap_wait,
                                                                                   self.cap_path,
                                                                                   self.cap_prefix))

        while True:
            cap_name = self.cap_prefix + '-' + datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + '.jpg'
            cap_out = os.path.join(self.cap_path, cap_name)
            self.logger.info("Capturing " + cap_out)
            self.cam.capture(cap_out)
            time.sleep(self.cap_wait)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Capture images from camera module")
    parser.add_argument("--debug", "-d",
                        action='store_true',
                        help="Enable debugging messages")
    parser.add_argument("--time", "-t", default=default_wait,
                        help="Time between image captures")
    parser.add_argument("--output", "-o", default=default_path,
                        help="Default output path")
    parser.add_argument("--prefix", "-p", default=fname(),
                        help="Prefix for image capture files")

    args = parser.parse_args()
    if args.debug:
        debug = True

    x = PyPiCamCapper(path=args.output, wait=int(args.time), prefix=args.prefix)
    try:
        x.run()
    except KeyboardInterrupt:
        x.logger.info("Capture complete.")