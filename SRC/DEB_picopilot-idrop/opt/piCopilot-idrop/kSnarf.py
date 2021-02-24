#!/usr/bin/python3

import argparse
import logging
import psycopg2
import signal
import sys
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

    ## Non usage scenarios
    if args.m != 'ids':                                                         ## Might be a good pivot for menu sanity
        from lib.os_control import Control
        from lib.snarf import Snarf

    if args.m is not None:
        if args.m == 'k9' and args.t is None:
            if args.m == 'k9' and args.k is None:
                print('Mode k9 requires -t or -k\n')
                sys.exit(1)
        if args.m == 'listen' and args.t:
            print('Targeted functionality not currently implemented for listen mode\n')
            sys.exit(1)
    if args.i is None and args.d is None:
        print('-i OR -d must be selected\n')
        sys.exit(1)
    if args.i is not None and args.m is None:
        print('-i must be used with -m')
        sys.exit(1)

    ## Proceed with snarfing
    else:

        ## Notate the driver in use
        if args.i is not None:
            nic = args.i[0]

            ## No channel hopping
            if args.c is None:

                if args.m != 'ids':
                    control = Control(nic)

            ## Channel hopping
            else:

                ## Hop of 10 sec default
                if args.hop is None:
                    control = Control(nic, chanList = args.c[0].split())

                ## Hop time defined
                else:
                    control = Control(nic, chanList = args.c[0].split(), interval = int(args.hop))

        ## Instantiate unity with driver selection

        if args.m != 'ids':
            unity = Unify(args, control)
        else:
            unity = Unify(args)

        ## Setup quiet time for packets
        if not args.s:
            unity.seenMaxTimer = 30
        else:
            unity.seenMaxTimer = int(args.s)

        ## Instantiate the DB
        cap = Builder(unity)

        ## Handle interrupts
        signal_handler = crtlC(cap, unity)
        signal.signal(signal.SIGINT, signal_handler)

        ## Take split arguments
        if args.p:
            pArgs = args.p[0].split()
        else:
            pArgs = None

        ## Create the snarf instance that holds the database
        if args.m == 'k9' or args.m == 'listen':
            snarf = Snarf(cap, unity, pArgs)

        ## Active sniffing
        if args.r is None:
            ### Perhaps switch logic to lfilter
            ### For now the logic is in sniffer method

            ## Listen with no target
            if args.m == 'listen':
                if args.w is not None:
                    with open(args.w, 'r') as iFile:
                        wList = iFile.read().splitlines()
                    unity.wSet = set()
                    for i in wList:
                        print(type(unity))
                        unity.wSet.add(i.lower().strip())
                        unity.wSet = iFile.read().splitlines()
                    unity.wSet.discard('')

                ## go
                pHandler = snarf.sniffer()
                sniff(iface = nic, prn = pHandler, store = 0)

            ## k9
            if args.m == 'k9':

                ## Single target, no list
                if args.t is not None and args.k is None:
                    kDict = {args.t.lower(): 'k9 Target -- {0}'.format(args.t.lower())}


                ## Single target, list
                if args.t is not None and args.k is not None:
                    print('-t and -k cannot be used together')
                    sys.exit(0)

                ## List
                if args.k is not None and args.t is None:
                    kDict = {}
                    with open(args.k, 'r') as iFile:
                        kList = iFile.read().splitlines()
                        for i in kList:
                            mac = i.split(',')[0].lower().strip()
                            alias = i.split(',')[1].strip()
                            kDict.update({mac: alias})

                pHandler = snarf.k9(kDict)
                sniff(iface = nic, prn = pHandler, store = 0)

            ## ids
            if args.m == 'ids':

                ## Add our function to Backgrounder and kick off a heartbeat
                Backgrounder.theThread = snarf.hb.heartRhythm

                ## Instantiate using #s other than defaults
                bg = Backgrounder()

                ## Start the heartbeat
                bg.easyLaunch()

                ## Continue with a sniff
                if args.debug is not None:
                    pHandler = snarf.DEBUG(args.debug)
                else:
                    pHandler = snarf.liveSniff()
                sniff(iface = nic, prn = pHandler, filter = 'udp port 514 and host {0}'.format(args.fwip), store = 0)

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
    parser.add_argument('-c',
                        help = 'channels',
                        nargs = '*')

    ## Required for wifi, hmm...
    parser.add_argument('-d',
                        choices = ['ath9k',
                                   'ath9k_htc',
                                   'iwlwifi',
                                   'rt2800usb',
                                   'rt2800usb-NEH',
                                   'wl12xx'],

                        # choices =    #unity.peDrivers.typeDict.keys(),
                        help = 'driver choice')


    parser.add_argument('--debug',
                        help = 'debug mode')


    parser.add_argument('--export',
                        help = 'Export some fun')

    parser.add_argument('-e',
                        help = 'exclusions',
                        choices = ['beacon'])
    parser.add_argument('-i',
                        help = 'interface',
                        nargs = 1)
    parser.add_argument('-k',
                        help = 'k-9 hunt list')
    parser.add_argument('-m',
                        help = 'mode',
                        choices = ['k9', 'listen', 'ids'])
    parser.add_argument('-p',
                        help = 'protocol',
                        nargs = '*')
    parser.add_argument('-q',
                        help = 'db query')
    parser.add_argument('-r',
                        help = 'receive data from a pcap')
    parser.add_argument('-s',
                        help = 'Silent time')
    parser.add_argument('-t',
                        help = 'target MAC')
    parser.add_argument('-w',
                        help = 'whitelist')
    parser.add_argument('--beat',
                        help = 'Heartbeat timing')
    parser.add_argument('--db',
                        help = 'database name')
    parser.add_argument('--fwip',
                        help = 'Firewall ip to listen for syslog')
    parser.add_argument('--hop',
                        help = 'Channel hop timing\n  [10 second default]')
    parser.add_argument('--host',
                        help = 'PGSQL host')
    parser.add_argument('--id',
                        help = 'Identifier' )
    parser.add_argument('--password',
                        help = 'PGSQL Password')
    parser.add_argument('--pcap',
                        action = 'store_true',
                        help = 'Write a pcap for any non-excluded frames')
    parser.add_argument('--psql',
                        action = 'store_true',
                        help = 'Operate kSnarf using psql as the backend storage')
    parser.add_argument('--recover',
                        action = 'store_true',
                        help = 'PSQL recovery mode to not start new for tuple')
    parser.add_argument('--user',
                        help = 'PGSQL username')
    parser.add_argument('--wipe',
                        action = 'store_true',
                        help = 'drop all PSQL tables')
    args = parser.parse_args()

    ## Deal with groups later
    if not (args.i or args.r or (args.t and not args.m)):
        print('Try:\nkSnarf --help\n')
        sys.exit(1)

    main(args)


"""
-- Future planning
The next evolution is to remove packet processing if it is not needed.
Why verify water.feel == 'wet' if processing in the desert?

This is going to require a rewrite of the framework. The code will get longer.
Through length we will obtain speed, and this is a huge handoff.

We can modularize the approach with some logic pre sniff()
"""
