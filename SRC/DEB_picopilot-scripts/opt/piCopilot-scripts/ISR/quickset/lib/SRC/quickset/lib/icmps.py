import binascii
from scapy.all import *

class Icmps(object):
    """Handles ICMP scenarios

    Expects a class passed as shared with a minimum of:
        essid   == 802.11 network name
        macGw   == Gateway MAC address (also serves the purpose of bssid)
        macRx   == Receiving MAC address
        macTx   == Transmitting MAC address
    """
    __slots__ = ['sh']

    def __init__(self, shared):
        self.sh = shared

    def request(self):
        ADDR1, ADDR2, ADDR3 = self.sh.whichWay()
        return RadioTap()\
               /Dot11(addr1 = ADDR1,
                      addr2 = ADDR2,
                      addr3 = ADDR3,
                      FCfield = self.sh.fcField,
                      type = 2,
                      subtype = 8,)\
               /Dot11QoS()\
               /LLC()\
               /SNAP()\
               /IP(flags = 'DF',
                   proto = 1,
                   src = self.sh.ipSrc,
                   dst = self.sh.ipDst)\
               /ICMP()\
               /Raw(binascii.unhexlify('CD 54 70 63 00 00 00 00 28 E7 05 00 00 00 00 00 10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F 30 31 32 33 34 35 36 37'.replace(' ', '')))
