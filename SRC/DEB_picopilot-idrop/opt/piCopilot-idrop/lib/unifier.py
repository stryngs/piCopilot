import os
import netaddr
import packetEssentials as PE
import psutil
import re
import time
from lib.location import Location

class Unify(object):
    """This class acts a singular point of contact for tracking purposes"""

    def __init__(self, args, control = None, kBlue = None, conf = None):
        self.epoch = None
        self.coord = None
        self.loc = Location()

        ## Custom init starts here
        ## blah
        ## Custom init ends here

        ## Set the orig timestamp
        self.origTime = int(time.time())
        #self.timeMarker = self.origTime

        ## make args avail
        self.args = args

        ## Tgts
        self.kTargets = set()

        if conf is not None:
            self.conf = conf
            self.devid = conf.devid

        ## idrop only
        if kBlue is None:

            ## Grab the OS control object
            self.control = control
            self.PE = PE

        ## Setup base
        self.baseDir = os.getcwd()

        # Grab OUIs
        print ('Loading OUIs')
        self.ouiDict = {}

        try:
            with open(self.baseDir + '/lib/support/oui.txt', 'r', encoding = 'UTF-8') as iFile:
                ouiRows = iFile.read().splitlines()
        except:
            ouiRows = []
            print('OUIs empty')

        for i in ouiRows:
            oui = re.findall('(.*)\s+\(hex\)\s+(.*)', i)
            if len(oui) == 1:
                self.ouiDict.update({oui[0][0].replace('-', ':').lower().strip(): oui[0][1]})
        print ('OUIs loaded\n')

        ## Set whitelist
        self.wSet = set()


    def macGrab(self, addr):
        """Last ditch effort if outDict{} does not have the OUI"""
        try:
            parsed_oui = netaddr.EUI(addr)
            return parsed_oui.oui.registration().org
        except netaddr.core.NotRegisteredError:
            return None


    def parachute(self):
        """Problem detected, pull out!"""
        for i in psutil.process_iter():
            if 'kSnarf.py' in ' '.join(i.cmdline()):
                i.kill()


    def times(self):
        """Timestamp function

        Sets a unified timestamp marker
        """
        ### This converts to Wireshark style
        #int(wepCrypto.endSwap('0x' + p.byteRip(f.notdecoded[8:], qty = 8, compress = True)), 16)
        epoch = time.localtime()
        self.coord = self.loc.getCoord()
        self.pi_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', epoch)
        #self.timeMarker = self.epoch

        ## kBlue fun
        try:
            self.marker += 1
        except:
            pass
