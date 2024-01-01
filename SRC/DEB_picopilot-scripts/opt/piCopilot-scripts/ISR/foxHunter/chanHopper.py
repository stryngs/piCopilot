#!/usr/bin/python3

import argparse
import os
import random
import sys
import time

class Chanhopper():
    """
    Hop to channel based on chanList

    Jumbles the list for a scattershot approach while staying within the
    boundaries of the requested channels per cycle.
    """
    def __init__(self, nic = 'wlan0mon'):
        self.nic = nic
    def chanHop(self, chanList, interval):
        while True:
            random.shuffle(chanList)
            for chan in chanList:
                os.system('iwconfig {0} channel {1}'.format(self.nic, chan))    ## stderr alerts to any issues
                time.sleep(interval)

b2 = '1 2 3 4 5 6 7 8 9 10 11'
b5 = '36 40 44 48 52 56 60 64 100 104 108 112 116 120 124 128 132 136 140 144 149 153 157 161 165'
b25 = b2 + ' ' + b5
if __name__ == '__main__':
    ## user options
    parser = argparse.ArgumentParser(description = 'chanHopper - Hop a channel')
    parser.add_argument('-b',
                        help = 'Bands to hop',
                        metavar = '2 for 2.4, 5 for 5, 25 for both')
    parser.add_argument('-i',
                        help = 'Your interface to be hopped',
                        metavar = '<interface>',
                        required = True)
    parser.add_argument('-t',
                        help = 'Time between hops',
                        metavar = '<2sec default time delay>')
    args = parser.parse_args()

    ## determine the band to sniff on
    if not args.b:
        chanStr = b2
    else:
        if args.b == '2':
            chanStr = b2
        elif args.b == '5':
            chanStr = b5
        elif args.b == '25':
            chanStr = b25
        else:
            print('Enter valid band\n 2  - 2.4GHz\n 5  - 5GHz \n 25 - 2.4GHz and 5GHz')
            sys.exit()

    ## hop
    chanList = [int(i) for i in chanStr.split(' ')]
    c = Chanhopper(args.i)
    if not args.t:
        args.t = 2
    c.chanHop(chanList, int(args.t))
