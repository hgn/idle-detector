#!/usr/bin/env python3
#
# Email: Hagen Paul Pfeifer <hagen@jauu.net>
# Licence: Public Domain


import sys
import os
import optparse
import subprocess
import time
import pyinotify

# Required Python Dependencies
#
# Debian:
#   sudo aptitude install python3-pyinotify
# Arch Linux:
#   sudo pacman -S community/python-pyinotify


# if for a given time (TIMEOUT) no data is tx'ed or rx'ed 
# EXEC_CMD is executed.
OBSERVED_PORTS_BIDIRECTIONAL = [ ['tcp', 22], ['tcp', 70] ]

# Timeout in seconds (1800 -> 30 min)
TIMEOUT = 1800

# executed command ofter timeout
EXEC_CMD = "poweroff"


TIMER_ID = "trafficidle"


class IdleDetector(pyinotify.ProcessEvent):

    def __init__(self):
        self.parse_local_options()
        self.verbose("idle-detector - 2015\n")

    def process_IN_MODIFY(self, event):
        print("IN_MODIFY triggered %s\n" % (event.pathname))
        print("execute: %s\n" % (EXEC_CMD))
        subprocess.Popen(EXEC_CMD.split(), shell=False,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)


    def exec_iptables(self, cmd):
        self.print("setting iptables rule: %s\n" % (cmd))
        self.process("%s %s" % ("iptables", cmd))


    def parse_local_options(self):
        parser = optparse.OptionParser()
        parser.usage = "idle-detector"
        parser.add_option( "-v", "--verbose", dest="verbose", default=False,
                          action="store_true", help="show verbose")
        self.opts, args = parser.parse_args(sys.argv[0:])


    def process(self, cmd):
        self.verbose('execute: \"%s\"\n' % (cmd))
        p = subprocess.Popen(cmd.split(), shell=False,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            self.print("%s\n" % (line))
        return


    def verbose(self, string):
        if not self.opts.verbose:
            return
        sys.stdout.write(string)


    def print(self, string):
        sys.stdout.write(string)

    def clean_iptables(self):
        self.exec_iptables(" -F")
        self.exec_iptables(" -X")

    def exec_idletimer_targets(self):
        for port in OBSERVED_PORTS_BIDIRECTIONAL:
            rule = " -I INPUT -p %s --sport %s -j IDLETIMER --timeout %s --label %s" % \
                   (port[0], port[1], TIMEOUT, TIMER_ID)
            self.exec_iptables(rule)
            rule = " -I INPUT -p %s --dport %s -j IDLETIMER --timeout %s --label %s" % \
                   (port[0], port[1], TIMEOUT, TIMER_ID)
            self.exec_iptables(rule)


    def run(self):
        self.clean_iptables()
        self.exec_idletimer_targets()
        handler = self
        wm = pyinotify.WatchManager()
        notifier = pyinotify.Notifier(wm, handler)
        self.print("now waiting for idle timer event\n")
        wm.add_watch('/sys/devices/virtual/xt_idletimer/timers/%s' % \
                     (TIMER_ID), pyinotify.IN_MODIFY)
        notifier.loop()


if __name__ == "__main__":
    try:
        idi = IdleDetector()
        sys.exit(idi.run())
    except KeyboardInterrupt:
        sys.stderr.write("SIGINT received, exiting\n")
