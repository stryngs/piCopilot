#!/bin/bash

## Detect current stream states
motionStatus=$(netstat -tulpn | grep 8081 | grep motion | cut -d\/ -f2)
vmStatus=$(lsmod | grep bcm2835_v4l[2] | head -n 1 | awk '{print $1}')
gStatus=$(ps aux | grep -o raspivi[d] | head -n 1)

if [[ "$motionStatus" != 'motion' ]]; then

    ## Stop raspivid if running
    if [[ "$gStatus" == 'raspivid' ]]; then
        pkill -9 raspivid
    fi
    
    systemctl start motion
    sleep 1
    systemctl start motioneye
    
    echo "motion" > /tmp/videoStream
fi
