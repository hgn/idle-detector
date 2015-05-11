#!/usr/bin/env python3
#
# Email: Hagen Paul Pfeifer <hagen@jauu.net>

# Idle detector is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# MachineCodeAnalyzer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MachineCodeAnalyzer. If not, see <http://www.gnu.org/licenses/>.


import sys
import os
import optparse
import subprocess
import time

# Required Python Dependencies
#
# Debian:
#   sudo aptitude install python3-pyinotify
# Arch Linux:
#   sudo pacman -S community/python-pyinotify



# if for a given time no data is tx'ed or rx'ed 
OBSERVED_PORTS_BIDIRECTIONAL = [ 22, 80 ]

# Timeout in seconds (30 min)
TIMEOUT = 1800

# executed command ofter timeout
EXEC_CMD = "echo 1 > /tmp/foo"


__programm__ = "idle-detector"
__author__   = "Hagen Paul Pfeifer"
__version__  = "1"
__license__  = "GPLv3"

# custom exceptions
class ArgumentException(Exception): pass
class InternalSequenceException(Exception): pass
class InternalException(Exception): pass
class NotImplementedException(InternalException): pass
class UnitException(Exception): pass



class IdleDetector:


    def __init__(self):
        self.parse_local_options()
        self.verbose("idle-detector - 2015\n")


    def exec_iptables(self, cmd):
        self.process("%s %s" % ("iptables", cmd))


    def parse_local_options(self):
        parser = optparse.OptionParser()
        parser.usage = "idle-detector"
        parser.add_option( "-v", "--verbose", dest="verbose", default=False,
                          action="store_true", help="show verbose")
        self.opts, args = parser.parse_args(sys.argv[0:])



    def process(self, cmd):
        self.verbose('execute: \"%s\"\n' % (cmd))
        p = subprocess.Popen(cmd.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            self.print("%s\n" % (line))
        return


    def verbose(self, string):
        if not self.opts.verbose:
            return
        sys.stdout.write(string)


    def print(self, string):
        sys.stdout.write(string)


    def which(self, program):
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            full_path = os.path.join(path, program)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                return full_path
        return None


    def print_version(self):
        sys.stdout.write("%s\n" % (__version__))


    def register_idletimer_targets(self):
        for port in OBSERVED_PORTS_BIDIRECTIONAL:
            print(port)
        #self.exec_iptables()


    def run(self):
        self.register_idletimer_targets()



    def print_usage(self):
        sys.stderr.write("Usage: mca [-h | --help]" +
                         " [--version]" +
                         " <modulename> [<module-options>] <binary>\n")





if __name__ == "__main__":
    try:
        idi = IdleDetector()
        sys.exit(idi.run())
    except KeyboardInterrupt:
        sys.stderr.write("SIGINT received, exiting\n")
