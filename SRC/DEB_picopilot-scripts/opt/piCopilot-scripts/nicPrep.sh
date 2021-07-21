#!/bin/bash

## Get list of MACs
nicList=$(airmon-ng | grep -o wlan.* | cut -f1)
nic1=$(echo $nicList | cut -d' ' -f1)
nic2=$(echo $nicList | cut -d' ' -f2)

## Get our perm mac
nic1Perm=$(macchanger $nic1 | grep Permanent | cut -d: -f2- | awk '{print $1}')
nic2Perm=$(macchanger $nic2 | grep Permanent | cut -d: -f2- | awk '{print $1}')

## Determine Pi mac
piNIC=$(airmon-ng | grep brcmfmac | awk '{print $2}')
if [[ $piNIC == $nic1 ]]; then piNIC="$nic1"; nonpiNIC="$nic2"; else piNIC="$nic2"; nonpiNIC="$nic1"; fi

## Grab piNIC mac
piNICmac=$(macchanger $piNIC | grep Permanent | cut -d: -f2- | awk '{print $1}')
nonpiNICmac=$(macchanger $nonpiNIC | grep Permanent | cut -d: -f2- | awk '{print $1}')

## Stop the wifi madness
cat <<EOF > /etc/udev/rules.d/70-persistent-net.rules
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="$piNICmac", ATTR{dev_id}=="0x0", ATTR{type}=="1", KERNEL=="wlan*", NAME="wlan0"
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="$nonpiNICmac", ATTR{dev_id}=="0x0", ATTR{type}=="1", KERNEL=="wlan*", NAME="wlan1"
EOF

## Shutdown the box
shutdown -h now
