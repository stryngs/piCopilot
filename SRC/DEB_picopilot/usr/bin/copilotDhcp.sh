#!/bin/bash

## Set DHCP per the expected schema
cat << "EOF" > /etc/dnsmasq.conf
dhcp-range=192.168.10.2,192.168.10.253,255.255.255.0,12h
#dhcp-option=option:router,192.168.10.254
#dhcp-option=option:dns-server,192.168.10.254
dhcp-authoritative
EOF

## Stop and start the DNS
systemctl stop dnsmasq
systemctl start dnsmasq
