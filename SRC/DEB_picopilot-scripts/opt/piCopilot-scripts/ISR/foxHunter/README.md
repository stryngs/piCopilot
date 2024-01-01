# foxHunter
foxHunter tracks a given MAC Address based on the Source Address as prescribed by the IEEE.  It will show the user a real-time stream of the RSSI for the MAC Address in question.

## Setup
```
python3 -m pip install scapy
```

## Usage
```
./foxHunter.py -i wlan0mon -t aa:bb:cc:dd:ee:ff
```
