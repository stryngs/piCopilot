#!/bin/bash

source shell/accessPoints.sh
source shell/dhcps.sh
source shell/hellos.sh
source shell/mains.sh
source shell/nicControl.sh
source shell/routes.sh
source shell/attacks/arpSpoofs.sh
source shell/attacks/dnsSpoofs.sh
source shell/attacks/ferrets.sh
source shell/attacks/menus.sh
source shell/attacks/strips.sh
source shell/attacks/wifis.sh

## launcher
current_ver=3.8.4
rel_date="12 November 2022"
envir--
if [[ "$UID" -ne 0 ]];then
	echo -e "$wrn\nMust be ROOT to run this script"
	exit 87
fi

if [[ -z $1  ]]; then
	phys_dev= ## Physical NIC variable
	kill_mon= ## Variable to determine if the "killing a monitor mode option" has been selected
	dev_check= ## Nulled

	ie=$(route -en | grep UG | awk '{print $8}' | head -n1)
	if [[ -n $ie ]];then

    ### Added a cut because of loose :
		ie=$(ifconfig $ie | awk '{print $1}' | head -n1 | cut -d: -f1)
	fi

	pii=$(iwconfig | grep -i monitor | awk '{print $1}' | head -n1)
	greet--
else
	usage--
fi
