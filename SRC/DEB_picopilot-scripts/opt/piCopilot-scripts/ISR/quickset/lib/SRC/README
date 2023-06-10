# quickset
quickset was a Bash script and now has a twin Python Script.  Changes will be made only on a bug basis for [quickset.sh](https://github.com/stryngs/quickset/blob/main/quickset.sh).  All development efforts are now towards [qs.py](https://github.com/stryngs/quickset/blob/main/qs.py).

Converting quickset to qs will take time and some of the functionality that quickset had, qs will not replace; there is not a reason to do so.

The bash version of quickset will always be maintained where it does not make sense to port to the Python twin.  If you find a bug, please raise an issue.

## Recommendations
Usage of the quickset library may produce unintended results if you are not aware of the potential secondary effects it may have in a given network scenario.  It is highly recommended to read the documentation and test the associated code prior to deploying outside of a lab environment.

## Curious human do
```
python3 -m venv env
source env/bin/activate
python3 -m pip install ipython3
python3 -m pip install lib/*.tar.gz
ipython3
%run qs.py
qs.<tab> <tab> tab it out...
||
python3 -m venv env
source env/bin/activate
python3 -m pip install ipython3
python3 -m pip install lib/*.tar.gz
python3 ./qs.py
||
bash ./quickset.sh
```

### Unit tests
Find and replace within this document based on the following schema:
```
192.168.100.1     = <Gateway IP>
192.168.100.219   = <Source IP>
192.168.100.226   = <Destination IP>
192.168.100.254   = <3rd party sniff IP>
11:22:33:44:55:55 = <BSSID>
11:22:33:44:55:66 = <Source MAC>
11:22:33:44:55:44 = <Destination MAC>
```

#### Gratuitous ARP using the To-DS flag
```
%run qs.py
qs.sh.bus = 'RadioTap'
qs.sh.fcField = 1
qs.sh.spare = 'not'
qs.sh.macGw = '11:22:33:44:55:55'
qs.sh.macTx = '11:22:33:44:55:66'
qs.sh.macRx = '11:22:33:44:55:44'
qs.sh.ipSrc = '192.168.100.254'
qs.sh.ipDst = '192.168.100.254'
z = qs.arps.gratCast()
qs.sh.qsView()
qs.sendp(z, iface = 'wlan1mon')
```

#### Gratuitous ARP using the From-DS flag
```
%run qs.py
qs.sh.bus = 'RadioTap'
qs.sh.fcField = 2
qs.sh.spare = 'not'
qs.sh.macGw = '11:22:33:44:55:55'
qs.sh.macTx = '11:22:33:44:55:66'
qs.sh.macRx = '11:22:33:44:55:44'
qs.sh.ipSrc = '192.168.100.254'
qs.sh.ipGtw = '192.168.100.1'
qs.sh.ipDst = '192.168.100.254'
z = qs.arps.gratCast()
qs.sh.qsView()
qs.sendp(z, iface = 'wlan1mon')
```

#### Gratuitous ARP using Ether
```
%run qs.py
qs.sh.bus = 'Ether'
qs.sh.macGw = '11:22:33:44:55:55'
qs.sh.macTx = '11:22:33:44:55:66'
qs.sh.macRx = '11:22:33:44:55:44'
qs.sh.ipSrc = '192.168.100.254'
qs.sh.ipGtw = '192.168.100.1'
qs.sh.ipDst = '192.168.100.254'
z = qs.arps.gratCast()
qs.sh.qsView()
qs.sendp(z, iface = 'wlan0')
```

#### ARP using To-DS
```
%run qs.py
qs.sh.bus = 'RadioTap'
qs.sh.fcField = 1
qs.sh.macGw = '11:22:33:44:55:55'
qs.sh.macTx = '11:22:33:44:55:66'
qs.sh.macRx = '11:22:33:44:55:44'
qs.sh.ipSrc = '192.168.100.219'
qs.sh.ipGtw = '192.168.100.1'
qs.sh.ipDst = '192.168.100.226'
z = qs.arps.oneWay()
qs.sh.qsView()
qs.sendp(z, iface = 'wlan1mon')
```

#### ARP using From-DS
```
%run qs.py
qs.sh.bus = 'RadioTap'
qs.sh.fcField = 2
qs.sh.macGw = '11:22:33:44:55:55'
qs.sh.macTx = '11:22:33:44:55:66'
qs.sh.macRx = '11:22:33:44:55:44'
qs.sh.ipSrc = '192.168.100.219'
qs.sh.ipGtw = '192.168.100.1'
qs.sh.ipDst = '192.168.100.226'
z = qs.arps.oneWay()
qs.sh.qsView()
qs.sendp(z, iface = 'wlan1mon')
```

#### ARP using Ether
```
%run qs.py
qs.sh.bus = 'Ether'
qs.sh.macGw = '11:22:33:44:55:55'
qs.sh.macTx = '11:22:33:44:55:66'
qs.sh.macRx = '11:22:33:44:55:44'
qs.sh.ipSrc = '192.168.100.219'
qs.sh.ipGtw = '192.168.100.1'
qs.sh.ipDst = '192.168.100.226'
z = qs.arps.oneWay()
qs.sh.qsView()
qs.sendp(z, iface = 'wlan0')
```

#### ARP ping using To-DS
```
%run qs.py
qs.sh.bus = 'RadioTap'
qs.sh.fcField = 1
qs.sh.macGw = '11:22:33:44:55:55'
qs.sh.macTx = '11:22:33:44:55:66'
qs.sh.macRx = '11:22:33:44:55:44'
qs.sh.ipSrc = '192.168.100.219'
qs.sh.ipGtw = '192.168.100.1'
qs.sh.ipDst = '192.168.100.226'
z = qs.arps.ping()
qs.sh.qsView()
qs.sendp(z, iface = 'wlan1mon')
```

#### ARP ping using From-DS
```
%run qs.py
qs.sh.bus = 'RadioTap'
qs.sh.fcField = 2
qs.sh.macGw = '11:22:33:44:55:55'
qs.sh.macTx = '11:22:33:44:55:66'
qs.sh.macRx = '11:22:33:44:55:44'
qs.sh.ipSrc = '192.168.100.219'
qs.sh.ipGtw = '192.168.100.1'
qs.sh.ipDst = '192.168.100.226'
z = qs.arps.ping()
qs.sh.qsView()
qs.sendp(z, iface = 'wlan1mon')
```

#### ARP ping using Ether
```
%run qs.py
qs.sh.bus = 'Ether'
qs.sh.macGw = '11:22:33:44:55:55'
qs.sh.macTx = '11:22:33:44:55:66'
qs.sh.macRx = '11:22:33:44:55:44'
qs.sh.ipSrc = '192.168.100.219'
qs.sh.ipGtw = '192.168.100.1'
qs.sh.ipDst = '192.168.100.226'
z = qs.arps.ping()
qs.sh.qsView()
qs.sendp(z, iface = 'wlan0')
```

#### Two-way ARP using To-DS
```
%run qs.py
qs.sh.bus = 'RadioTap'
qs.sh.macGw = '11:22:33:44:55:55'
qs.sh.macTx = '11:22:33:44:55:66'
qs.sh.macRx = '11:22:33:44:55:44'
qs.sh.ipSrc = '192.168.100.219'
qs.sh.ipGtw = '192.168.100.1'
qs.sh.ipDst = '192.168.100.226'
z = qs.arps.twoWay()
qs.sh.qsView()
qs.sendp(z, iface = 'wlan1mon', inter = .5, loop = 1)
```

#### Two-way ARP using Ether
```
%run qs.py
qs.sh.bus = 'Ether'
qs.sh.macGw = '11:22:33:44:55:55'
qs.sh.macTx = '11:22:33:44:55:66'
qs.sh.macRx = '11:22:33:44:55:44'
qs.sh.ipSrc = '192.168.100.219'
qs.sh.ipGtw = '192.168.100.1'
qs.sh.ipDst = '192.168.100.226'
z = qs.arps.twoWay()
qs.sh.qsView()
qs.sendp(z, iface = 'wlan0', inter = .5, loop = 1)
```
