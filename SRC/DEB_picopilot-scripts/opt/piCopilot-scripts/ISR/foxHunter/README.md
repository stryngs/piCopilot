# foxHunter
foxHunter tracks a given MAC Address based on the Source Address as prescribed by the IEEE.  It will show the user a real-time stream of the RSSI for the MAC Address in question.

## Setup
```
git clone https://github.com/stryngs/packetEssentials
python3 -m pip install packetEssentials/RESOURCEs/packetEssentials*
python3 -m pip install scapy
```

## Usage
```
./foxHunter.py -t aa:bb:cc:dd:ee:ff -i wlan0mon
```
