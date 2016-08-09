#
# Copyright (C) 2016, David Brookshire <dave@brookshire.org>
#

import picamera
import os
import time
import subprocess
import re
import datetime
from threading import Thread

hwaddr_pat = re.compile('HWaddr [0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:([0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2})')

class PyPiCamCapper(Thread):
    cap_path = "/tmp"
    cap_wait = 30 # seconds
    stitch_cleanup = False

    def __init__(self, *args, **kwargs):
        self.cam = picamera.PiCamera()
        self.fname = self.get_fname()
        super(PyPiCamCapper, self).__init__(args, kwargs)

    def get_fname(self):

        cmd = "/sbin/ifconfig eth0"
        p = subprocess.Popen(cmd.split(),
                             stdout=subprocess.PIPE,
                             shell=False)
        rc = p.wait()
        line = p.stdout.readline()
        mo = hwaddr_pat.search(line, re.IGNORECASE)
        if not mo:
            ret = "image"
        else:
            ret = mo.group(1).replace(':', '')

        return ret

    def run(self):
        while True:
            fname = self.fname + '-' + datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + '.jpg'
            out = os.path.join(self.cap_path, fname)
            print("Capturing camera to " + out)
            self.cam.capture(out)
            time.sleep(self.cap_wait)

    # def stitch(self):
    #     all_files = os.listdir(self.cap_path)
    #     img_files = []
    #     mp = re.compile("^%s-.+\.jpg$" % self.fname)
    #
    #     for fname in all_files:
    #         mo = mp.match(fname);
    #         if mo:
    #             img_files.append(os.path.join(self.cap_path, fname))
    #
    #     cmd = "convert -delay 10 -loop 1 %s %s" % (' '.join(img_files),
    #                                                os.path.join(self.cap_path, self.fname + ".animation.gif"))
    #     print(cmd)
    #     p = subprocess.Popen(cmd.split(), shell=False)
    #     rc = p.wait()
    #     print("rc = %d" % rc )
    #
    #     # Clean up
    #     if self.stitch_cleanup:
    #         for fname in img_files:
    #             os.unlink(os.path.join(self.cap_path, fname))

if __name__ == '__main__':
    x = PyPiCamCapper()
    x.cap_path = "/var/www/html"
    try:
        x.run()
    except KeyboardInterrupt:
        pass
        # x.stitch()