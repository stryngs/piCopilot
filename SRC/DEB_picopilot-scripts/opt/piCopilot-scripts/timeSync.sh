#!/bin/bash

## Start the GPS
gpsLoad--()
{
systemctl start gpsd
sleep 10
}

## Stop the GPS
gpsUnload--()
{
systemctl stop gpsd
systemctl stop gpsd.socket
}

## Start the NTP
ntpLoad--()
{
systemctl start ntp
}

## Stop the NTP
ntpUnload--()
{
systemctl stop ntp
}

## Sync time to GPS
timeSync--()
{
ntpUnload--
x=$(gpspipe -w -n 4 2>/dev/null | grep -Po '(?<=time":").*Z(?=")')
sCheck=$(echo "$x" | awk '{print length}')
if [[ $sCheck -eq 24 ]]; then
    date -s $x
    sleep 3
    ntpLoad--
    echo "timestamp - $x" > /tmp/timeStamp
else
    sleep 10
    x=$(gpspipe -w -n 4 2>/dev/null | grep -Po '(?<=time":").*Z(?=")')
    sCheck=$(echo "$x" | awk '{print length}')
    if [[ $sCheck -eq 24 ]]; then
        date -s $x
        sleep 3
        ntpLoad--
        echo "timestamp - $x" > /tmp/timeStamp
    fi
fi
}

### main
date -s "Mon, 1 Aug 2022 00:00:00 -0000" ## Hardcoded as a workaround to the gpsd problem where the time is incorrect
gpsUnload--
gpsLoad--
timeSync--
