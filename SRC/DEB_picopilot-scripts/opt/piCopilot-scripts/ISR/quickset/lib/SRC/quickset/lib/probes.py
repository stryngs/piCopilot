from scapy.all import *
import binascii

class Probes(object):
    """Handles Probe scenarios

    Expects a class passed as shared with a minimum of:
        esrates == ...
        essid   == 802.11 network name
        macRx   == Receiving MAC address
        macTx   == Transmitting MAC address
        channel == 802.11 channel to transmit on
        rates   == ...
    """
    __slots__ = ['sh']

    def __init__(self, shared):
        self.sh = shared


    def request(self):
        return RadioTap()\
               /Dot11(type = 0,
                      subtype = 4,
                      addr1 = self.sh.macRx,
                      addr2 = self.sh.macTx,
                      addr3 = self.sh.macRx)\
               /Dot11ProbeReq()\
               /Dot11Elt(ID = 'SSID', info = self.sh.essid)\
               /Dot11Elt(ID = 'Rates', info = b'\x82\x84\x8b\x96\x0c\x12\x18')\
               /Dot11Elt(ID = 'ESRates', info = b'\x30\x48\x60\x6c')\
               /Dot11Elt(ID = 'DSset', info = chr(self.sh.channel))


    def response(self):
        """[1.0(B) Mbps, 2.0(B) Mbps, 5.5(B) Mbps, 11.0(B) Mbps]"""
        return RadioTap()\
               /Dot11FCS(addr1 = self.sh.macRx,
                         addr2 = self.sh.macTx,
                         addr3 = self.sh.macTx,
                         FCfield = 8,
                         ID = 14849,
                         proto = 0,
                         SC = 51920,
                         subtype = 5,
                         type = 0)\
               /Dot11ProbeResp(cap = 'ESS')\
               /Dot11Elt(info = self.sh.essid)\
               /Dot11EltRates(rates = [130, 132, 139, 150])\
               /Dot11EltDSSSet(channel = self.sh.channel)\
               /Dot11EltVendorSpecific(binascii.unhexlify('DD 09 00 10 18 02 01 F0 2C 00 00'.replace(' ', '')))


    def wiPeep(self):
        """
        This module provides the fundamentals to experiment with the concepts
        described in Wi-Peep.  As time goes forward and perhaps patches
        released, updates to this code will occur.  Updates may also occur if
        further public POCs are created.

        How to figure out the magic frame:
            https://deepakv.web.illinois.edu/assets/papers/WiPeep_Mobicom2022.pdf
            https://dl.acm.org/doi/pdf/10.1145/3495243.3560530
            https://community.arubanetworks.com/blogs/gstefanick1/2016/01/25/80211-tim-and-dtim-information-elements
            https://www.oreilly.com/library/view/80211-wireless-networks/0596100523/ch04.html
            https://mrncciew.com/2014/10/02/cwap-802-11-control-frame-types/
            https://dot11zen.blogspot.com/2018/02/80211-power-management-with-packet.html
            https://web.cse.ohio-state.edu/~xuan.3/papers/08_icdcs_gyqxj.pdf
            https://scapy.readthedocs.io/en/latest/
        """
        bList = [b'\x00\x01\x00']
        bStr = bytes()
        for i in range(1):
            bList.append(b'\xff')
        for b in bList:
            bStr += b
        return RadioTap()\
               /Dot11FCS(type = 0,
                         subtype = 8,
                         addr1 = 'ff:ff:ff:ff:ff:ff',
                         addr2 = self.sh.macGw,
                         addr3 = self.sh.macGw)\
               /Dot11Beacon()\
               /Dot11Elt(ID = 0,
                         info = self.sh.essid,
                         len = len(self.sh.essid))\
               /Dot11EltRates(rates = self.sh.rates)\
               /Dot11EltDSSSet(channel = self.sh.channel)\
               /Dot11Elt(ID = 5,
                         info = bStr)
