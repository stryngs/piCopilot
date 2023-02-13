#!/bin/bash

## ./gStreamWrapper.sh 640 480 192.168.10.10

## Detect current stream states
motionStatus=$(netstat -tulpn | grep 8081 | grep motion | cut -d\/ -f2)
vmStatus=$(lsmod | grep bcm2835_v4l[2] | head -n 1 | awk '{print $1}')
gStatus=$(ps aux | grep -o raspivi[d] | head -n 1)

## Stop motion
if [[ "$motionStatus" == 'motion' ]]; then
  systemctl stop motioneye
  sleep 1
  systemctl stop motion
fi

## Kill any prior resolutions
killall -9 raspivid

## Load driver if not already loaded
[[ "$vmStatus" != "bcm2835_v4l2" ]] && modprobe bcm2835-v4l2

## GStreamer
raspivid -n -fl -w $1 -h $2 -b 10000000 -fps 30 -t 0 -rot 0 --exposure auto -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host=$3 port=5600
echo "GStreamer" > /tmp/videoStream
# fi
