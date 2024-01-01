#!/usr/bin/python3

import argparse
import sys
from scapy.all import *

class Fox(object):
    """ Traces the source of a given 802.11 transmission based on the specs from
    IEEE in reference to ADDRs 1-4 for the source of a given frame that has been
    transmitted.
    """
    __slots__ = ['i', 't', 'spC', 'spA', 'freqDict']
    def __init__(self, i, t):
        self.i = i
        self.t = t
        self.spC = 4
        self.spA = ['|',
                    '/',
                    '~',
                    '\\',
                    '*']
        self.freqDict = {2412: 1,
                         2417: 2,
                         2422: 3,
                         2427: 4,
                         2432: 5,
                         2437: 6,
                         2442: 7,
                         2447: 8,
                         2452: 9,
                         2457: 10,
                         2462: 11,
                         2467: 12,
                         2472: 13,
                         2484: 14,
                         5180: 36,
                         5200: 40,
                         5210: 42,
                         5220: 44,
                         5240: 48,
                         5250: 50,
                         5260: 52,
                         5290: 58,
                         5300: 60,
                         5320: 64,
                         5745: 149,
                         5760: 152,
                         5765: 153,
                         5785: 157,
                         5800: 160,
                         5805: 161,
                         5825: 165}


    def lFilter(self, tgtMac):
        def tailChaser(packet):

            ## Null the flags
            fromDS = False
            toDS = False
            fcField = None

            ## With FCS
            if packet.haslayer(Dot11FCS):
                ## Notate bits
                if self.nthBitSet(packet[Dot11FCS].FCfield, 0) is True:
                    toDS = True
                if self.nthBitSet(packet[Dot11FCS].FCfield, 1) is True:
                    fromDS = True

                ## Who sent it
                if fromDS & toDS:
                    theMac = packet[Dot11FCS].addr4
                elif toDS:
                    theMac = packet[Dot11FCS].addr2
                elif fromDS:
                    theMac = packet[Dot11FCS].addr3
                else:
                    if packet[Dot11FCS].addr2 is None:
                        theMac = ''
                    else:
                        theMac = packet[Dot11FCS].addr2

            ## No FCS
            elif packet.haslayer(Dot11):

                ## Notate bits

                if self.nthBitSet(packet[Dot11].FCfield, 0) is True:
                    toDS = True
                if self.nthBitSet(packet[Dot11].FCfield, 1) is True:
                    fromDS = True

                ## Who sent it
                if fromDS & toDS:
                    theMac = packet[Dot11].addr4
                elif toDS:
                    theMac = packet[Dot11].addr2
                elif fromDS:
                    theMac = packet[Dot11].addr3
                else:
                    if packet[Dot11].addr2 is None:
                        theMac = ''
                    else:
                        theMac = packet[Dot11].addr2

            ## Was it ours
            try:
                if theMac == tgtMac.lower():
                    return True
            except Exception as E:
                pass
                # print(E)
                # wrpcap('debug.pcap', packet)
                # sys.exit()

        return tailChaser


    def nthBitSet(self, integer, bit):
        """Determine if the nth bit is set on a given integer.
        The first bit is considered the zeroth bit.  stdout is the decimal value
        of the bit you turn on with this method, it also returns a True.
        Using the Python bitwise operator for AND, &.

        Give it a number, it will let you know if the binary on the specified
        bit from right to left is a 1 (True) or a 0 (False).
        """
        if integer & (1 << bit):
            return True
        return False


    def pHandler(self, tgtMac):
        """ prn """
        def snarf(packet):
            print(f'{self.spinner()} {tgtMac.lower()} --> {self.freqDict.get(packet[RadioTap].ChannelFrequency)} @ {packet[RadioTap].dBm_AntSignal}' )
        return snarf


    def spinner(self):
        """ Track and return the spins """
        ## Grab orig value
        sp = self.spA[self.spC]
        self.spC += 1

        ## Increase or set to 0 new value
        if self.spC >= len(self.spA):
            self.spC = 0
        return sp


def main(args):
    """Grab a fox by the tail"""
    fx = Fox(args.i, args.t)
    lFilter = fx.lFilter(args.t)
    pHandler = fx.pHandler(args.t)
    mNic = args.i
    sniff(iface = mNic, prn = pHandler, lfilter = lFilter, store = 0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Fox hunting for 802.11')
    parser.add_argument('-t',
                        metavar = 'MAC to listen for',
                        help = 'MAC to listen for', required = True)
    parser.add_argument('-i',
                        metavar = 'NIC to sniff with',
                        help = 'NIC to sniff with', required = True)
    args = parser.parse_args()
    main(args)
