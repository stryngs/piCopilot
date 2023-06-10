# frameTracer
frameTracer follows a single MAC Address or a pair of MAC Addresses and records the traffic to a pcap.

## Setup
```
git clone https://github.com/stryngs/packetEssentials
python3 -m pip install packetEssentials/RESOURCEs/packetEssentials*
python3 -m pip install scapy
```

## Usage
```
./frameTracer.py -i wlan0mon -x aa:bb:cc:dd:ee:ff -v -t
```
