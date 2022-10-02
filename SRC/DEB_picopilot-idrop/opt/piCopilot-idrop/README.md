# kSnarf
kSnarf operates in Linux for extracting various intelligence correlation data points.  Those gathered points can be monitored in real time or for a period of time in the past.

The default usage for kSnarf is aimed at wireless traffic and works with any network card so long as it can drop to monitor mode at a minimum.  [piCopilot](https://github.com/stryngs/piCopilot#lessons-learned-from-tools-like-picopilot) is one such tool leveraging kSnarf in this manner.

kSnarf has an experimental Bluetooth module called kBlue which leverages the [Ubertooth One](https://greatscottgadgets.com/ubertoothone/).  

Private modules are available upon [request](https://gitter.im/ICSec/kSnarf)  for supporting Ethernet style traffic and other such IDS or IPS type needs.

# Getting started
Install PostgreSQL locally
Modify ./system.conf if nothing else to ensure prop.nic makes sense, by default prop.nic is set to wlan1mon.
```sql
CREATE ROLE root WITH SUPERUSER LOGIN;
ALTER USER root WITH PASSWORD 'idrop';
CREATE DATABASE idrop;
```
```bash
sudo python3 ./kSnarf.py
```
```bash
sudo psql idrop
```
```sql
SELECT * FROM main;
```
