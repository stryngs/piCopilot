import os
import subprocess
import threading
import time
import packetEssentials as PE
from shlex import split

class Hopper(object):
    """Threading class for channel hopping

    Will hop chan based on chanList every 10 seconds as default
    mod via system.conf
    """

    def __init__(self, controlObj):
        self.controlObj = controlObj
        thread = threading.Thread(target = self.controlObj.chanHop,
                                  args = (self.controlObj.chanList, self.controlObj.interval))
        thread.daemon = True
        thread.start()


class Control(object):
    """Control the underlying OS"""
    def __init__(self, nic, chanList = False, interval = 10):
        self.nic = nic
        self.chanList = chanList
        self.interval = interval
        self.curChan = None
        self.curFreq = None

        ## Deal with channel hopping
        if chanList is not False:
            Hopper(self)

        ## Deal with no channel hopping
        else:
            self.curChan = int(self.iwGet().split('(Channel')[1].strip().split(')')[0])
            self.curFreq = PE.chanFreq.twoFourRev(int(self.curChan))


    def chanHop(self, chanList, interval):
        """Hop to channel based on chanList"""
        while True:
            for chan in chanList:
                self.iwSet(chan)
                self.curChan = chan
                self.curFreq = PE.chanFreq.twoFourRev(int(self.curChan))
                time.sleep(interval)


    def iwSet(self, channel):
        """Set the wifi channel"""
        os.system('iwconfig {0} channel {1}'.format(self.nic, channel))


    def iwGet(self):
        """Show the current wifi channel in str() format"""
        p1 = subprocess.Popen(split('iwlist %s channel' % self.nic),
                              stdout = subprocess.PIPE)
        p2 = subprocess.Popen(split('tail -n 2'),
                              stdin = p1.stdout,
                              stdout = subprocess.PIPE)
        p3 = subprocess.Popen(split('head -n 1'),
                              stdin = p2.stdout,
                              stdout = subprocess.PIPE)
        return p3.communicate()[0].strip()


    def iwDriver(self):
        """Determine driver in use"""
        p1 = subprocess.Popen(split("grep 'DRIVER=' '/sys/class/net/%s/device/uevent'" % self.nic),
                              stdout = subprocess.PIPE)
        p2 = subprocess.Popen(split('cut -d= -f2'),
                              stdin = p1.stdout,
                              stdout = subprocess.PIPE)
        return p2.communicate()[0].strip()
