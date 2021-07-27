# WiGLE
A set of Python scripts to do useful things with WiGLE API results.  To run the code in this folder you need to have officeTasks installed:
```
git clone https://github.com/stryngs/officeTasks.git
python3 -m pip install officeTasks/officeTasks-*
```

### wigleGrabber.py
wigleGrabber reaches out to the WiGLE API and scrapes a given place on Earth, left or right by the value of iCre based on the amount of turns listed in token.  iCre is an increment against the Latitudes for this code.  token is a counter.

An example configuration file called wigle.ini has been created for you.  This is the name of the expected file.

Modify accordingly if you want to involve changing the Latitudes.

An example config for shifting by iCre of -.0067 would be:
```
[loc]
bLat = <bottom Latitude with 4 decimal points>
tLat = <top Latitude with 4 decimal points>
lLong = <left Longitude with 4 decimal points>
rLong = <right Longitude with 4 decimal points>
iCre = -.0067
token = 10
```
The more zoomed in you are with respect to the bounding box above, the more likely you are to grab all known points for a given boundary.
</br>
An example config for the WiGLE API credentials would be:
```
[creds]
api_name = <USERNAME TOKEN>
api_token = <PASSWORD TOKEN>
```

To see an example, change api_name and api_token accordingly, then run.

### wiglePlotter.py
wiglePlotter leverages the power of Plotly to generate a map showing the geographical area covered by the execution of wigleGrabber.py.  This map aims to assist the user in tailoring their search patterns.

### wigleUpdater.py
wigleUpdater queries the wigle.sqlite3 database and updates the idrop database accordingly.  If you don't know what idrop is, check out piCopilot:
```
https://github.com/stryngs/piCopilot
```
After wigleUpdater has finished, run the following queries against the idrop database:
```
DROP TABLE IF EXISTS unique_probes;
DROP TABLE IF EXISTS wigle_addr1;
DROP TABLE IF EXISTS wigle_addr2;
DROP TABLE IF EXISTS wigle_addr3;
DROP TABLE IF EXISTS wigle_addr4;
DROP TABLE IF EXISTS wigle_essids;
CREATE TABLE unique_probes AS SELECT DISTINCT(essid) FROM probes WHERE essid IS NOT NULL and essid != '';
CREATE TABLE wigle_addr1 AS SELECT W.*, M.pid, M.epoch, M.pi_timestamp, M.date, M.time, M.addr1, M.addr1_oui, M.addr2, M.addr2_oui, M.addr3, M.addr3_oui, M.addr4, M.addr4_oui, M.channel AS frame_channel, M.type AS frame_type, M.subtype, M.rssi, M.direc, M.txrx FROM wigle W INNER JOIN main M ON LOWER(W.netid) = LOWER(M.addr1);
CREATE TABLE wigle_addr2 AS SELECT W.*, M.pid, M.epoch, M.pi_timestamp, M.date, M.time, M.addr1, M.addr1_oui, M.addr2, M.addr2_oui, M.addr3, M.addr3_oui, M.addr4, M.addr4_oui, M.channel AS frame_channel, M.type AS frame_type, M.subtype, M.rssi, M.direc, M.txrx FROM wigle W INNER JOIN main M ON LOWER(W.netid) = LOWER(M.addr2);
CREATE TABLE wigle_addr3 AS SELECT W.*, M.pid, M.epoch, M.pi_timestamp, M.date, M.time, M.addr1, M.addr1_oui, M.addr2, M.addr2_oui, M.addr3, M.addr3_oui, M.addr4, M.addr4_oui, M.channel AS frame_channel, M.type AS frame_type, M.subtype, M.rssi, M.direc, M.txrx FROM wigle W INNER JOIN main M ON LOWER(W.netid) = LOWER(M.addr3);
CREATE TABLE wigle_addr4 AS SELECT W.*, M.pid, M.epoch, M.pi_timestamp, M.date, M.time, M.addr1, M.addr1_oui, M.addr2, M.addr2_oui, M.addr3, M.addr3_oui, M.addr4, M.addr4_oui, M.channel AS frame_channel, M.type AS frame_type, M.subtype, M.rssi, M.direc, M.txrx FROM wigle W INNER JOIN main M ON LOWER(W.netid) = LOWER(M.addr4);
CREATE TABLE wigle_essids AS SELECT * FROM wigle W INNER JOIN unique_probes P ON LOWER(W.ssid) = LOWER(P.essid);
SELECT 'addr1', COUNT(*) FROM wigle_addr1
UNION ALL SELECT 'addr2', COUNT(*) FROM wigle_addr2
UNION ALL SELECT 'addr3', COUNT(*) FROM wigle_addr3
UNION ALL SELECT 'addr4', COUNT(*) FROM wigle_addr4
UNION ALL SELECT 'essids', COUNT(*) FROM wigle_essids
ORDER BY 1 ASC;
```
When finished you will have generated tables showing some of the relational aspects between various BSSIDs, MACs and ESSIDs.  The output is a summary of the rows in each generated table.
