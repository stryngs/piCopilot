import binascii
import threading
import time
from .lib.arps import Arps
from .lib.beacons import Beacons
from .lib.deauths import Deauths
from .lib.icmps import Icmps
from .lib.probes import Probes
from .lib.supplicants import Supplicants
from scapy.all import *
from scapy.sendrecv import __gen_send as gs

class Shared(object):
    """Create a shared class for all modules

    algo      == Algorithm to use for 802.11
    bus       == Ether or RadioTap interface type
    esrates   == ...
    essid     == Extended Service Set Identifier (i.e. 802.11 network name)
    fcField   == The field for marking whether this is From-DS or To-DS
    injSocket == Static socket for speed purposes, use this to inject
    ipDst     == Destination IP Address
    ipGtw     == Gateway IP Address
    ipSrc     == Source IP Address
    macGw     == Gateway MAC address (also serves the purpose of bssid)
    macRx     == Receiving MAC address
    macTx     == Transmitting MAC address
    nic       == Network Interface Card
    channel   == 802.11 channel to transmit on
    pHandler  == Shared packet handler
    qsList    == Overview of the shared slots
    rates     == ...
    reason    == ...
    seqNum    == Sequence number
    spare     == spare object slot
    """
    __slots__ = ['algo',
                 'bus',
                 'channel',
                 'esrates',
                 'essid',
                 'fcField',
                 'injSocket',
                 'ipDst',
                 'ipGtw',
                 'ipSrc',
                 'macGw',
                 'macRx',
                 'macTx',
                 'nic',
                 'qsList',
                 'rates',
                 'reason',
                 'seqNum',
                 'spare']


    def __init__(self,
                 algo = 0,
                 bus = 'RadioTap',
                 channel = 1,
                 esrates = [48, 72, 96, 108],
                 essid = None,
                 fcField = 1,
                 injSocket = None,
                 ipDst = None,
                 ipGtw = None,
                 ipSrc = None,
                 macGw = None,
                 macRx = 'ff:ff:ff:ff:ff:ff',
                 macTx = 'ff:ff:ff:ff:ff:ff',
                 nic = None,
                 # qsList = None,
                 rates = [2, 4, 11, 22, 12, 18, 24, 36],
                 reason = 7,
                 seqNum = 1,
                 spare = None):
        self.algo = algo
        self.bus = bus
        self.channel = channel
        self.esrates = esrates
        self.essid = essid
        self.fcField = fcField
        self.injSocket = injSocket
        self.ipDst = ipDst
        self.ipGtw = ipGtw
        self.ipSrc = ipSrc
        self.macGw = macGw
        self.macRx = macRx
        self.macTx = macTx
        self.nic = nic
        # self.qsList = qsList
        self.rates = rates
        self.reason = reason
        self.seqNum = seqNum
        self.spare = spare


    def qsView(self):
        """Update qsList for easy remembering of the set values"""
        self.qsList = []
        self.qsList.append('algo       - {0}'.format(self.algo))
        self.qsList.append('bus        - {0}'.format(self.bus))
        self.qsList.append('channel    - {0}'.format(self.channel))
        self.qsList.append('esrates    - {0}'.format(self.esrates))
        self.qsList.append('essid      - {0}'.format(self.essid))
        self.qsList.append('fcField    - {0}'.format(self.fcField))
        self.qsList.append('injSocket  - {0}'.format(self.injSocket))
        self.qsList.append('ipDst      - {0}'.format(self.ipDst))
        self.qsList.append('ipGtw      - {0}'.format(self.ipGtw))
        self.qsList.append('ipSrc      - {0}'.format(self.ipSrc))
        self.qsList.append('macGw      - {0}'.format(self.macGw))
        self.qsList.append('macRx      - {0}'.format(self.macRx))
        self.qsList.append('macTx      - {0}'.format(self.macTx))
        self.qsList.append('nic        - {0}'.format(self.nic))
        self.qsList.append('rates      - {0}'.format(self.rates))
        self.qsList.append('reason     - {0}'.format(self.reason))
        self.qsList.append('seqNum     - {0}'.format(self.seqNum))
        self.qsList.append('spare      - {0}'.format(self.spare))
        for i in self.qsList:
            print(i)


    def whichWay(self, bcast = 0):
        """Orders addrs 1-3 based on FCfield requirements

        Does not account for all From-DS/To-DS scenarios

        Add an option to have the source be the bssid
        """
        if bcast == 0:
            if self.fcField == 1 or self.fcField == 65:
                ADDR1 = self.macGw
                ADDR2 = self.macTx
                ADDR3 = self.macRx
            elif self.fcField == 2 or self.fcField == 66:
                ADDR1 = self.macRx
                ADDR2 = self.macGw
                ADDR3 = self.macTx
            else:
                return None
        else:
            if self.fcField == 1 or self.fcField == 65:
                ADDR1 = self.macGw
                ADDR2 = self.macTx
                ADDR3 = 'ff:ff:ff:ff:ff:ff'
            elif self.fcField == 2 or self.fcField == 66:
                ADDR1 = 'ff:ff:ff:ff:ff:ff'
                ADDR2 = self.macGw
                ADDR3 = self.macTx
            else:
                return None
        return ADDR1, ADDR2, ADDR3

## Instatiations
sh = Shared()
arps = Arps(sh)
beacons = Beacons(sh)
deauths = Deauths(sh)
icmps = Icmps(sh)
probes = Probes(sh)
supplicants = Supplicants(sh)
