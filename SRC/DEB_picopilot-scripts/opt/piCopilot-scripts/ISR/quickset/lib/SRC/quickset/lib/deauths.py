from scapy.all import *

"""
0 - Reserved.
1  - Unspecified reason.
2  - Previous authentication no longer valid.
3  - Deauthenticated because sending station (STA) is leaving or has left Independent Basic Service Set (IBSS) or ESS.
4  - Disassociated due to inactivity.
5  - Disassociated because WAP device is unable to handle all currently associated STAs.
6  - Class 2 frame received from nonauthenticated STA.
7  - Class 3 frame received from nonassociated STA.
8  - Disassociated because sending STA is leaving or has left Basic Service Set (BSS).
9  - STA requesting (re)association is not authenticated with responding STA.
10 - Disassociated because the information in the Power Capability element is unacceptable.
11 - Disassociated because the information in the Supported Channels element is unacceptable.
12 - Disassociated due to BSS Transition Management.
13 - Invalid element, that is, an element defined in this standard for which the content does not meet the specifications in Clause 8.
14 - Message integrity code (MIC) failure.
15 - 4-Way Handshake timeout.
16 - Group Key Handshake timeout.
17 - Element in 4-Way Handshake different from (Re)Association Request/ Probe Response/Beacon frame.
18 - Invalid group cipher.
19 - Invalid pairwise cipher.
20 - Invalid AKMP.
21 - Unsupported RSNE version.
22 - Invalid RSNE capabilities.
23 - IEEE 802.1X authentication failed.
24 - Cipher suite rejected because of the security policy.
"""

class Deauths(object):
    """Handles Deauthentication scenarios

    Expects a class passed as shared with a minimum of:
        macRx  == Receiving MAC address
        macTx  == Transmitting MAC address
        reason == ...
    """
    __slots__ = ['sh']

    def __init__(self, shared):
        self.sh = shared


    def deauth(self):
        return RadioTap()\
               /Dot11(type = 0,
                      subtype = 12,
                      addr1 = self.sh.macRx,
                      addr2 = self.sh.macTx,
                      addr3 = self.sh.macTx)\
               /Dot11Deauth(reason = self.sh.reason)
