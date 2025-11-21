#!/bin/bash

## ./gStreamWrapper.sh 640 480 192.168.10.10
## viewer -> gst-launch-1.0 -v udpsrc port=5600 caps="application/x-rtp,media=video,encoding-name=H264,payload=96" ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false

## Detect current stream states
vmStatus=$(lsmod | grep bcm2835_v4l[2] | head -n 1 | awk '{print $1}')

## Kill any prior resolutions
killall -9 raspivid

## Load driver if not already loaded
[[ "$vmStatus" != "bcm2835_v4l2" ]] && modprobe bcm2835-v4l2

## GStreamer
# raspivid -n -fl -w $1 -h $2 -b 10000000 -fps 30 -t 0 -rot 0 --exposure auto -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host=$3 port=5600
rpicam-vid -n --inline -t 0 --width $1 --height $2 --framerate 30 --bitrate 4000000 --rotation 0 --exposure normal -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host=$3 port=5600
echo "GStreamer" > /tmp/videoStream
