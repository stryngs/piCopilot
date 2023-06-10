from scapy.all import *

class Beacons(object):
    """Handles Beacon scenarios

    Expects a class passed as shared with a minimum of:
        essid == 802.11 network name
        macTx == Transmitting MAC address
    """

    __slots__ = ['sh']

    def __init__(self, shared):
        self.sh = shared


    def chanSwitch(self, beacon = None): ### < Broken!
        """Creates a channel switch announcement - CSA

        Returns count 1 and 2 in a list for the CSA

        From https://github.com/Hackndo/krack-poc/blob/master/Krack.py
        An interesting approach from a layered perspective
        Channel Switch Announcement
        + Dot11
            \x0d Action

        + Raw
            \x00 Management
            \x04 CSA
            \x25 Element ID [37]
            \x03 Length
            \x00 Channel Switch Mode
            \x04 New Channel Num
            \x00 Channel Switch Count
        """

        if beacon is not None:

            ## Check for strings
            if beacon == 'open':
                ourBeacon = self.open()
            elif beacon == 'halfway':
                ourBeacon = self.halfway()
            elif beacon == 'protected':
                ourBeacon = self.protected()

            ## Assume beacon is a scapy beacon object
            else:
                ourBeacon = beacon

            ## Lazy deferrals
            try:

                ## https://github.com/lucascouto/mitm-channel-based-package/blob/master/mitm_channel_based/mitm_code.py#L334
                csa_pkt_I = RadioTap()/\
                            Dot11(addr1 = self.sh.macRx,
                                  addr2 = self.sh.macTx,
                                  addr3 = self.sh.macTx,
                                  type = 0,
                                  subtype = 0x0d)/\
                            Raw("\x00\x04\x25\x03\x00" + chr(self.sh.channel) + "\x02")

                csa_pkt_II = RadioTap()/\
                             Dot11(addr1 = self.sh.macRx,
                                   addr2 = self.sh.macTx,
                                   addr3 = self.sh.macTx,
                                   type = 0,
                                   subtype = 0x0d)/\
                             Raw("\x00\x04\x25\x03\x00" + chr(self.sh.channel) + "\x01")
                pkts = []
                pkts.append(csa_pkt_I)
                pkts.append(csa_pkt_II)
                return pkts

            except Exception as E:
                print(E)

        return RadioTap()/\
               Dot11(type = 0,
                      subtype = 10,
                      addr1 = self.sh.macRx,
                      addr2 = self.sh.macTx,
                      addr3 = self.sh.macTx)/\
                Raw("\x00\x04\x25\x03\x00" + chr(client_channel) + "\x00")


    def open(self):
        """Send open beacon"""
        return RadioTap()\
               /Dot11(type = 0,
                      subtype = 8,
                      addr1 = 'ff:ff:ff:ff:ff:ff',
                      addr2 = self.sh.macTx,
                      addr3 = self.sh.macTx)\
               /Dot11Beacon()\
               /Dot11Elt(ID = 'SSID',
                         info = self.sh.essid,
                         len = len(self.sh.essid))


    def halfway(self):
        """Send protected beacon, kind of..."""
        return RadioTap()\
               /Dot11(type = 0,
                      subtype = 8,
                      addr1 = 'ff:ff:ff:ff:ff:ff',
                      addr2 = self.sh.macTx,
                      addr3 = self.sh.macTx)\
               /Dot11Beacon(cap = 'ESS+privacy')\
               /Dot11Elt(ID = 'SSID', info = self.sh.essid, len = len(self.sh.essid))


    def protected(self):
        """Send protected beacon"""
        return RadioTap()\
               /Dot11(type = 0,
                      subtype = 8,
                      addr1 = 'ff:ff:ff:ff:ff:ff',
                      addr2 = self.sh.macTx,
                      addr3 = self.sh.macTx)\
               /Dot11Beacon(cap = 'ESS+privacy')\
               /Dot11Elt(ID = 'SSID', info = self.sh.essid, len = len(self.sh.essid))\
               /Dot11Elt(ID = 'RSNinfo', info = (b'\x01\x00'                     #RSN Version 1
                                                 b'\x00\x0f\xac\x02'             #Group Cipher Suite : 00-0f-ac TKIP
                                                 b'\x02\x00'                     #2 Pairwise Cipher Suites (next two lines)
                                                 b'\x00\x0f\xac\x04'             #AES Cipher
                                                 b'\x00\x0f\xac\x02'             #TKIP Cipher
                                                 b'\x01\x00'                     #1 Authentication Key Managment Suite (line below)
                                                 b'\x00\x0f\xac\x02'             #Pre-Shared Key
                                                 b'\x00\x00'))                   #RSN Capabilities (no extra capabilities)
