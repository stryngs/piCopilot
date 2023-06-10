#!/usr/bin/python3
import quickset as qs

def ghostArpping(ipDst = '192.168.100.252',
                 ipSrc = '192.168.100.219',
                 macGw = 'aa:bb:cc:dd:ee:ff',
                 macTx = '11:22:33:44:55:66',
                 nic = 'wlan1mon',
                 fcField = 2):
    """An example of an Arp ping technique as performed by Nmap that will bypass
    firewall rules.

    This is traffic which masquerades as the Access Point iself relaying the
    traffic that would have originally been sent using a To-DS frame instead.

    The ARP traffic will reach the wireless destination.
    """
    qs.sh.fcField = fcField
    qs.sh.ipDst = ipDst
    qs.sh.ipSrc = ipSrc
    qs.sh.macGw = macGw
    qs.sh.macTx = macTx
    qs.sh.nic = nic
    f = qs.arps.ping()
    print(f.summary())
    uChoice = input('Should the traffic be sent? [Y/n]\n')
    if uChoice.lower() == 'y' or uChoice.lower == '':
        qs.sendp(f, iface = qs.sh.nic)
    return f


def ghostPing(ipDst = '192.168.100.252',
              ipSrc = '192.168.100.219',
              macGw = 'aa:bb:cc:dd:ee:bb',
              macRx = 'aa:bb:cc:dd:ee:ff',
              macTx = 'aa:bb:cc:dd:ee:aa',
              nic = 'wlan1mon',
              fcField = 2):
    """An example of an ICMP request that will bypass firewall rules.

    This is traffic which masquerades as the Access Point itself relaying
    traffic that would have originally been sent using a To-DS frame instead.

    The ICMP traffic will reach the wireless destination.
    """
    qs.sh.fcField = fcField
    qs.sh.ipDst = ipDst
    qs.sh.ipSrc = ipSrc
    qs.sh.macGw = macGw
    qs.sh.macRx = macRx
    qs.sh.macTx = macTx
    qs.sh.nic = nic
    f = qs.icmps.request()
    print(f.summary())
    uChoice = input('Should the traffic be sent? [Y/n]\n')
    if uChoice.lower() == 'y' or uChoice.lower == '':
        qs.sendp(f, iface = qs.sh.nic)
    return f


def normalPing(ipDst = '192.168.100.252',
               ipSrc = '192.168.100.219',
               macGw = 'aa:bb:cc:dd:ee:bb',
               macRx = 'aa:bb:cc:dd:ee:ff',
               macTx = 'aa:bb:cc:dd:ee:aa',
               nic = 'wlan1mon',
               fcField = 1):
    """An example of a ICMP request in a wireless network.

    This is the traffic that a device would send to the Access Point if it was
    was trying to ping another device on the network.

    If there are firewall rules in place to prevent ICMP, this traffic would not
    reach the wireless destination.
    """
    qs.sh.fcField = fcField
    qs.sh.ipDst = ipDst
    qs.sh.ipSrc = ipSrc
    qs.sh.macGw = macGw
    qs.sh.macRx = macRx
    qs.sh.macTx = macTx
    qs.sh.nic = nic
    f = qs.icmps.request()
    print(f.summary())
    uChoice = input('Should the traffic be sent? [Y/n]\n')
    if uChoice.lower() == 'y' or uChoice.lower == '':
        qs.sendp(f, iface = qs.sh.nic)
    return f

if __name__ == '__main__':
    qs.sh.qsView()
    print('\n  Run normalPing(), ghostArpping() or ghostPing() to get started with this library.\n')
