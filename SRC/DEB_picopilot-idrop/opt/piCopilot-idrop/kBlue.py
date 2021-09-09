#!/usr/bin/python3

"""
kBlue -- Sniff teh bluetooths
"""

import argparse
import netaddr
import os
import re
import time
import signal
import sys
import psycopg2
from configparser import ConfigParser
from easyThread import Backgrounder
from lib.unifier import Unify
from scapy.all import *
from subprocess import Popen

class Blinder(object):
    """Figure out whether or not to pay attention to a given bluetooth object"""

    def choiceMaker(self, packet):
        proceed = False
        for choice in self.choices[:-4]:
            if packet.haslayer(choice):
                self.chosen = str(choice).split('.')[-1].split("'")[0]                ## Change logic before threading
                return True
        return False

    ### Move to a common library with snarf.py
    def seenTest_ignore(self, packet):
        """Gather essential identifiers for "have I seen this packet" test.

        Return False to continue with this test.  If not seen, then continue.

        Will return False if the delta of now and previous timestamp
        for a given frame are > self.unity.seenMaxTimer {Default 30 seconds},
        otherwise we ignore, and thus by ignoring, we do not clog up the logs.

        Create a table, and store this data so we can query on the fly.
            - only with psql
        """
        self.bTuple = self.tupleGen(packet)
        if self.bTuple is not None:

            ## ignore if needed
            ### Add logic later to keep for parents with > 1 MAC per object
            if set(i for i in self.bTuple[1:]) & self.ignoreSet:
                # print('[+] ignoring: {0}'.format(set(i for i in self.bTuple[1:])))
                return True
            # else:
                # print ('[-] not ignoring: {0}'.format(set(i for i in self.bTuple[1:])))

            ## Figure out if this combo has been seen before
            if self.bTuple is not None:
                if self.bTuple not in self.unity.seenDict:
                    self.unity.seenDict.update({self.bTuple: (1, time.time())})

                    # print("I AM NOT FOUND")
                    return False

                ## Has been seen, now check time
                else:
                    lastTime = self.unity.seenDict.get(self.bTuple)[1]
                    lastCount = self.unity.seenDict.get(self.bTuple)[0]
                    if (time.time() - lastTime) > self.unity.seenMaxTimer:

                        ## Update delta timestamp
                        self.unity.seenDict.update({self.bTuple: (lastCount + 1, time.time())})
                        # print ('PASS TIMER')
                        return False
                    else:
                        # print ('FAIL TIMER')
                        return True


    ### Move to a common library with snarf.py
    def seenTest_noignore(self, packet):
        """Gather essential identifiers for "have I seen this packet" test.

        Return False to continue with this test.  If not seen, then continue.

        Will return False if the delta of now and previous timestamp
        for a given frame are > self.unity.seenMaxTimer {Default 30 seconds},
        otherwise we ignore, and thus by ignoring, we do not clog up the logs.

        Create a table, and store this data so we can query on the fly.
            - only with psql
        """
        self.bTuple = self.tupleGen(packet)
        if self.bTuple is not None:

            ## Figure out if this combo has been seen before
            if self.bTuple is not None:
                if self.bTuple not in self.unity.seenDict:
                    self.unity.seenDict.update({self.bTuple: (1, time.time())})

                    # print("I AM NOT FOUND")
                    return False

                ## Has been seen, now check time
                else:
                    lastTime = self.unity.seenDict.get(self.bTuple)[1]
                    lastCount = self.unity.seenDict.get(self.bTuple)[0]
                    if (time.time() - lastTime) > self.unity.seenMaxTimer:

                        ## Update delta timestamp
                        self.unity.seenDict.update({self.bTuple: (lastCount + 1, time.time())})
                        # print ('PASS TIMER')
                        return False
                    else:
                        # print ('FAIL TIMER')
                        return True


    def tupleGen(self, packet):
        """Generate the unique tuple of a given bluetooth object"""
        bTuple = None
        try:
            if self.chosen == 'BTLE_ADV_IND':
                bTuple = (self.chosen,
                          packet[BTLE_ADV_IND].AdvA,
                          None,
                          None)
            if self.chosen == 'BTLE_ADV_NONCONN_IND':
                bTuple = (self.chosen,
                          packet[BTLE_ADV_NONCONN_IND].AdvA,
                          None,
                          None)
            if self.chosen == 'BTLE_ADV_SCAN_IND':
                bTuple = (self.chosen,
                          packet[BTLE_ADV_SCAN_IND].AdvA,
                          None,
                          None,)
            if self.chosen == 'BTLE_SCAN_REQ':
                bTuple = (self.chosen,
                          packet[BTLE_SCAN_REQ].AdvA,
                          None,
                          packet[BTLE_SCAN_REQ].ScanA)
            if self.chosen == 'BTLE_SCAN_RSP':
                bTuple = (self.chosen,
                          packet[BTLE_SCAN_RSP].AdvA,
                          None,
                          None)
            if self.chosen == 'BTLE_ADV_DIRECT_IND':
                bTuple = (self.chosen,
                          packet[BTLE_ADV_DIRECT_IND].AdvA,
                          None,
                          packet[BTLE_ADV_DIRECT_IND].InitA)
            return bTuple
        except Exception as E:
            print(E)
            return None



class Blue(object):
    """Handle all things for bluetooth"""

    def __init__(self, args, blinder):
        ## Prep our mac filter
        self.blinder = blinder

        ##Do some filtering to ignore parsing we don't need
        self.onlyCare()
        self.pipeSleep = 20
        self.availPipes = ['/mnt/usb_storage/bluesPipe-1',
                           '/mnt/usb_storage/bluesPipe-2']

        ## Check for known macs to ignore -- need to use regex...
        if os.path.isfile('ignore.lst'):
            with open('ignore.lst', 'r') as iFile:
                iList = iFile.read().splitlines()
            self.blinder.ignoreSet = set()
            for i in iList:
                if len(i) == 17:
                    self.blinder.ignoreSet.add(i.lower())
                    self.IGNORE = True
        else:
            self.IGNORE = False

        ## Remove a cycle by ignoring at this level of the Class
        if self.IGNORE is True:
            self.eyeball = self.blinder.seenTest_ignore
            print('\n[~] Ignoring MACs from ignore.lst:\n{0}\n'.format(self.blinder.ignoreSet))
        else:
            self.eyeball = self.blinder.seenTest_noignore
            print('\n[~] Not ignoring any MACs\n')

        ## db creds
        class Foo(object):
            pass
        self.conf = Foo()
        parser = ConfigParser()
        parser.read('system.conf')
        self.conf.dbUser = parser.get('creds', 'dbUser')
        self.conf.dbPass = parser.get('creds', 'dbPass')
        self.conf.dbHost = parser.get('creds', 'dbHost')
        self.conf.dbName = parser.get('creds', 'dbName')
        self.conf.devid = int(parser.get('creds', 'devid'))
        self.conf.seenMax = int(parser.get('prop', 'seenMax'))

        ## Connect to the db
        self.con, self.db, self.dbName = self.pgsqlPrep()
        self.PRN = self.pgsqlFilter()

        ## Store the args
        self.args = args


    def onlyCare(self):
        """Only load parsers for what we care about
        self.choices[:-4] is the list of objects we rip from currently
        """
        self.choices = [scapy.layers.bluetooth4LE.BTLE_ADV_IND,
                        scapy.layers.bluetooth4LE.BTLE_ADV_NONCONN_IND,
                        scapy.layers.bluetooth4LE.BTLE_ADV_SCAN_IND,
                        scapy.layers.bluetooth4LE.BTLE_SCAN_REQ,
                        scapy.layers.bluetooth4LE.BTLE_SCAN_RSP,
                        scapy.layers.bluetooth4LE.BTLE_ADV_DIRECT_IND,
                        scapy.layers.bluetooth4LE.BTLE,
                        scapy.layers.bluetooth4LE.BTLE_RF,
                        scapy.layers.bluetooth4LE.BTLE_ADV,
                        scapy.layers.bluetooth4LE.EIR_Hdr]
        self.blinder.choices = self.choices
        conf.layers.filter(self.choices)


    def pipePush(self, pipe, sVal):
        # bPipe = os.system('/usr/bin/timeout {0} /usr/bin/ubertooth-btle -f -q {1} 1>/dev/null'.format(sVal, pipe))
        bPipe = os.system('/usr/bin/timeout 0 /usr/bin/ubertooth-btle -f -q "/mnt/usb_storage/bluesPipe-1"')


    def pgsqlFilter(self):
        def snarf(packet):
            self.blinder.unity.times()

            ## Only test if known MAC field(s) exists
            if self.blinder.choiceMaker(packet) is True:

                ### THIS IS ENTRY POINT
                if self.eyeball(packet) is False:

                    ### CLEARED HOT TO LOG
                    try:
                        pSignal = packet[BTLE_RF].signal
                        pNoise = packet[BTLE_RF].noise

                        ## Update the db
                        self.db.execute("""
                                        INSERT INTO blue (pi_timestamp,
                                                          coord,
                                                          parent,
                                                          adva,
                                                          inita,
                                                          scana,
                                                          signal,
                                                          noise)
                                                     VALUES (%s,
                                                             %s,
                                                             %s,
                                                             %s,
                                                             %s,
                                                             %s,
                                                             %s,
                                                             %s);
                                                 """, (self.blinder.unity.pi_timestamp,
                                                       self.blinder.unity.coord,
                                                       self.blinder.bTuple[0],
                                                       self.blinder.bTuple[1],
                                                       self.blinder.bTuple[2],
                                                       self.blinder.bTuple[3],
                                                       pSignal,
                                                       pNoise))
                    except Exception as E:
                        print(E)
        return snarf


    def pgsqlPrep(self):
        """ Connect and prep the pgsql db"""
        try:
            cStr = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(self.conf.dbName, self.conf.dbUser, self.conf.dbHost, self.conf.dbPass)
            con = psycopg2.connect(cStr)
            con.autocommit = True
            db = con.cursor()

            ## db prep
            db.execute("""
                       CREATE TABLE IF NOT EXISTS blue(pi_timestamp TIMESTAMPTZ,
                                                       coord TEXT,
                                                       parent TEXT,
                                                       adva TEXT,
                                                       inita TEXT,
                                                       scana TEXT,
                                                       signal INT,
                                                       noise INT);
                       """)
        except Exception as E:
            print ("I am unable to connect to the database idrop")
            print(E)
            sys.exit(1)
        dbName = 'idrop'

        return (con, db, dbName)


    def main(self):
        ## Unify it up
        self.blinder.unity = Unify(self.args, control = None, kBlue = True, conf = self.conf)
        self.blinder.unity.seenMaxTimer = self.conf.seenMax
        self.blinder.unity.seenDict = {}

        ### Semi real-time
        # while True:
        #     for pipe in self.availPipes:
        #         print('sniffing pipe {0}'.format(pipe))
        #         self.pipePush(pipe, self.pipeSleep)
        #         p = sniff(offline = '{0}'.format(pipe), prn = self.PRN)
        #         time.sleep(.1)

        ### Real-time
        Backgrounder.theThread = uberThread
        bg = Backgrounder()
        bg.easyLaunch()
        time.sleep(3)                                                           ### Clean this up later
        sniff(opened_socket = Reader('/mnt/usb_storage/bluesPipe-1'), prn = self.PRN)
        con.close()                                                             ## This connection never really.... gets closed.



class Reader(PcapReader):
    def read_packet(self, size = 65535):                                        ## MTU obj not loaded
        try:
            return super(Reader, self).read_packet(size)
        except EOFError:
            return None


def crtlC(args):
    """Handle CTRL+C."""
    def tmp(signal, frame):
        sys.exit(0)
    return tmp


def uberThread(self):
    os.system('/usr/bin/ubertooth-btle -f -q "/mnt/usb_storage/bluesPipe-1" 1>/dev/null')


if __name__ == '__main__':

    ## ARGUMENT PARSING
    parser = argparse.ArgumentParser(description = 'kBlue')
    args = parser.parse_args()

    ## ADD SIGNAL HANDLER
    signal_handler = crtlC(args)
    signal.signal(signal.SIGINT, signal_handler)

    ## Launch
    blinder = Blinder()
    bl = Blue(args, blinder)
    bl.main()
