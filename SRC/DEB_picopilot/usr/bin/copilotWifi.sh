#!/bin/bash

sleep 15 && rfkill unblock all && grep '#' /etc/network/interfaces.d/wlan0 1>/dev/null && systemctl start hostapd && /usr/bin/copilotDhcp.sh
