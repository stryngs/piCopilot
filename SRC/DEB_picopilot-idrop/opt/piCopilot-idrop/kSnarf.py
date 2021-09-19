#!/usr/bin/python3

import argparse
import logging
import psycopg2
import signal
import sys
from configparser import ConfigParser
from easyThread import Backgrounder
from lib.dbControl import Builder
from lib.unifier import Unify
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

def crtlC(cap, unity):
    """Handle CTRL+C."""
    def tmp(signal, frame):
        print('\nTrying to stop gracefully')
        #cap.con.commit()
        cap.con.close()
        try:
            unity.conBeat.close()
        except:
            print('Could not close heartbeat connection')
        sys.exit(0)
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
        unity = Unify(args)

    ## Setup quiet time for packets
    unity.seenMaxTimer = conf.seenMax

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

    ## Create the snarf instance that holds the database
    snarf = Snarf(cap, unity, pArgs)

    ## Active sniffing
    if args.r is None:
        ### Perhaps switch logic to lfilter
        ### For now the logic is in sniffer method

        ## Listen with no target
        if conf.mode == 'listen':
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

        ## ids
        if conf.mode == 'ids':

            ## Add our function to Backgrounder and kick off a heartbeat
            Backgrounder.theThread = snarf.hb.heartRhythm

            ## Instantiate using #s other than defaults
            bg = Backgrounder()

            ## Start the heartbeat
            bg.easyLaunch()

            ## Continue with a sniff
            pHandler = snarf.liveSniff()
            sniff(iface = conf.nic, prn = pHandler, filter = 'udp port 514 and host {0}'.format(args.fwip), store = 0)

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
    parser = argparse.ArgumentParser(description = 'kSnarf - FOSS Intelligence Gathering of the 802.11 spectrum',
                                     prog = 'kSnarf')
    parser.add_argument('-e',
                        help = 'exclusions',
                        choices = ['beacon'])
    parser.add_argument('-r',
                        help = 'receive data from a pcap')
    parser.add_argument('-w',
                        help = 'whitelist')
    parser.add_argument('--beat',
                        help = 'Heartbeat timing')
    parser.add_argument('--fwip',
                        help = 'Firewall ip to listen for syslog')
    parser.add_argument('--pcap',
                        action = 'store_true',
                        help = 'Write a pcap for any non-excluded frames')
    parser.add_argument('--recover',
                        action = 'store_true',
                        help = 'PSQL recovery mode to not start new for tuple')
    parser.add_argument('--wipe',
                        action = 'store_true',
                        help = 'drop all PSQL tables')
    args = parser.parse_args()

    main(args)
