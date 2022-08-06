#!/usr/bin/python3

import argparse
import hashlib
import json
import logging
import os
import psutil
import signal
import sys
import time
from configparser import ConfigParser
from easyThread import Backgrounder
from lib.dbControl import Builder
from lib.unifier import Unify
from scapy.all import *
from threading import Thread

## pypy3
try:
    from psycopg2cffi import compat
    compat.register()
except:
    pass
import psycopg2

## Custom imports start here
## blah
## Custom imports end here

## Custom functions start here
## blah
## Custom functions end here

def crtlC(cap, unity):
    """Handle CTRL+C."""
    def tmp(signal, frame):
        print('\nTrying to stop gracefully')
        cap.con.close()
        unity.conBeat.close()
        for i in psutil.process_iter():
            if 'kSnarf.py' in ' '.join(i.cmdline()):
                i.kill()
    return tmp


def main(args):

    ## Configuration setup
    class Foo(object):
        pass

    ## Setup
    conf = Foo()
    parser = ConfigParser()
    parser.read('system.conf')
    conf.user = parser.get('creds', 'dbUser')
    conf.password = parser.get('creds', 'dbPass')
    conf.host = parser.get('creds', 'dbHost')
    conf.db = parser.get('creds', 'dbName')
    conf.devid = int(parser.get('creds', 'devid'))
    conf.nic = parser.get('hw', 'nic')
    conf.drv = parser.get('hw', 'drv')
    conf.seenMax = int(parser.get('prop', 'seenMax'))
    conf.protocols = parser.get('prop', 'protocols')
    conf.channels = parser.get('prop', 'channels')
    conf.hop = int(parser.get('prop', 'hop'))
    conf.mode = parser.get('prop', 'mode')

    ## Usage scenarios
    if conf.mode != 'ids':
        from lib.os_control import Control
        from lib.snarf import Snarf

        ## No channel hopping
        if conf.channels is None:
            control = Control(conf.nic)

        ## Channel hopping
        else:

            ## Hop of 10 sec default
            if conf.hop is None:
                control = Control(conf.nic, chanList = conf.channels.split())

            ## Hop time defined
            else:
                control = Control(conf.nic, chanList = conf.channels.split(), interval = conf.hop)
        unity = Unify(args, control = control, driver = conf.drv, conf = conf)
    else:
        unity = Unify(args, conf = conf)

    ## Setup quiet time for packets
    unity.seenMaxTimer = conf.seenMax

    ## ids integrations start here
    ## blah
    ## ids integrations end here

    ## Instantiate the DB
    cap = Builder(unity)

    ## Handle interrupts
    signal_handler = crtlC(cap, unity)
    signal.signal(signal.SIGINT, signal_handler)

    ## Take split arguments
    if len(conf.protocols) > 0:
        pArgs = conf.protocols.split()
    else:
        pArgs = None

    ## snarf integrations start here
    ## Create the snarf instance that holds the database
    snarf = Snarf(cap, unity, pArgs)
    ## snarf integrations end here

    ## Active sniffing starts here
    if args.r is None:
        ### Perhaps switch logic to lfilter
        ### For now the logic is in sniffer method

        print('RUNNING')
        if args.w is not None:
            with open(args.w, 'r') as iFile:
                wList = iFile.read().splitlines()
            unity.wSet = set()
            for i in wList:
                unity.wSet.add(i.lower().strip())
                unity.wSet = iFile.read().splitlines()
            unity.wSet.discard('')

        ## go
        pHandler = snarf.sniffer()
        sniff(iface = conf.nic, prn = pHandler, store = 0)
    ## Active sniffing stops here

    ## PCAP reading
    else:
        if args.w is not None:
            with open(args.w, 'r') as iFile:
                wList = iFile.read().splitlines()
            unity.wSet = set()
            for i in wList:
                unity.wSet.add(i.lower().strip())
            unity.wSet.discard('')
        pHandler = snarf.reader()
        sniff(offline = args.r, prn = pHandler, store = 0)


if __name__== '__main__':
    ## Custom logging starts here
    ## blah
    ## Custom logging ends here

    parser = argparse.ArgumentParser(description = 'kSnarf - FOSS Intelligence Gathering of the RF spectrum',
                                     prog = 'kSnarf')
    parser.add_argument('-e',
                        help = 'exclusions',
                        choices = ['beacon'])
    parser.add_argument('-r',
                        help = 'receive data from a pcap')
    parser.add_argument('-w',
                        help = 'whitelist')
    parser.add_argument('--beat',
                        action = 'store_true',
                        help = 'heartbeats')

    ## Custom args start here
    ## blah
    ## Custom args end here

    ## Launch
    args = parser.parse_args()
    main(args)
