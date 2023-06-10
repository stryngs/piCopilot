chan_check--()
{
chan_res=$(iwlist $1 channel | grep Current | awk '{print $5}' | sed 's/)//')
if [[ -z $chan_res ]];then
	clear
	echo -e "$out\nCurrent Channel for $1 is not Set"
fi
}


mac_control--()
{

	mac_control_II--()
	{
	mac_dev=
	mac_devII=
	rand=
	var_II=
	sam= ## Variable for SoftAP MAC address
	clear
	echo -e "$wrn\n
                              ***WARNING***$ins
       Do not attempt to directly change a Virtual Device (Monitor Mode NIC)
This script requires Physical and Virtual devices to have matching MAC Addresses$wrn
                              ***WARNING***\n\n\n\n\n\n"
	sleep 1
	echo -e "$inp\nNIC to Change?   (\033[1;32mLeave Blank to Return to Previous Menu$inp)"
	read mac_dev
	if [[ -z $mac_dev ]];then
		mac_control--
	else
		dev_check_var=$mac_dev
		dev_check--
		if [[ $dev_check == "fail" ]];then
			mac_control--
		fi

	fi

	while [[ -z $rand ]];do
		echo -e "$inp\nRandom MAC? (y or n)"
		read rand
		case $rand in
			y|Y) ;;

			n|N) while [[ -z $sam ]];do
				echo -e "$inp\nDesired MAC Address for $out$mac_dev$inp?   (\033[1;32mi.e. aa:bb:cc:dd:ee:ff$inp)"
				read sam
			done;;

			*) rand= ;;
		esac

	done

	while [[ $var_II != "x" ]];do
		echo -e "$inp\nDoes $out$mac_dev$inp have a Monitor Mode NIC associated with it? (y or n)"
		read var
		case $var in
			n|N|y|Y) var_II="x" ;;
			*) var_II= ;;
		esac

	done

	case $var in
		y|Y) case $rand in
			y|Y) while [[ -z $mac_devII ]];do
				echo -e "$inp\nMonitor Mode NIC name?"
				read mac_devII
				dev_check_var=$mac_devII
				dev_check--
				if [[ $dev_check == "fail" ]];then
					mac_devII=
				fi

			done

			ifconfig $mac_dev down
			ifconfig $mac_devII down
			clear
			echo -e "$out\n--------------------\nChanging MAC Address\n--------------------"
			echo -e "$out\n$mac_dev `macchanger -r $mac_dev`"
			if [[ $? -ne 0 ]];then
				echo -e "$wrn\nThe Attempt was Unsuccessful, Try Again"
				ifconfig $mac_dev up
				sleep .7
				mac_control--
			else
				rand_mac=$(ifconfig $mac_dev | awk '{print $5}')
				rand_mac=$(echo $rand_mac | awk '{print $1}')
				echo -e "$out\n$mac_devII `macchanger -m $rand_mac $mac_devII`"
				if [[ $? -ne 0 ]];then
					echo -e "$wrn\nThe Attempt was Unsuccessful, Try Again"
					ifconfig $mac_devII up
					sleep .7
					mac_control--
				else
					ifconfig $mac_dev up
					ifconfig $mac_devII up
					echo -e "$ins\n\n\n\nPress Enter to Continue"
					read
					mac_control--
				fi

			fi;;

			n|N) mac_devII=
			while [[ -z $mac_devII ]];do
				echo -e "$inp\nMonitor Mode NIC name?"
				read mac_devII
				dev_check_var=$mac_devII
				dev_check--
				if [[ $dev_check == "fail" ]];then
					mac_devII=
				fi

			done

			ifconfig $mac_dev down
			ifconfig $mac_devII down
			clear
			echo -e "$out\n--------------------\nChanging MAC Address\n--------------------"
			echo -e "$out\n$mac_dev `macchanger -m $sam $mac_dev`"
			if [[ $? -ne 0 ]];then
				echo -e "$wrn\nThe Attempt was Unsuccessful, Try Again"
				ifconfig $mac_dev up
				sleep .7
				mac_control--
			else
				echo -e "$out\n$mac_devII `macchanger -m $sam $mac_devII`"
				if [[ $? -ne 0 ]];then
					echo -e "$wrn\nThe Attempt was Unsuccessful, Try Again"
					ifconfig $mac_devII up
					sleep .7
					mac_control--
				else
					ifconfig $mac_dev up
					ifconfig $mac_devII up
					echo -e "$ins\n\n\n\nPress Enter to Continue"
					read
					mac_control--
				fi

			fi;;

		esac;;

		n|N) case $rand in
			y|Y) ifconfig $mac_dev down
			clear
			echo -e "$out\n--------------------\nChanging MAC Address\n--------------------"
			echo -e "$out\n$mac_dev `macchanger -r $mac_dev`"
			if [[ $? -ne 0 ]];then
				echo -e "$wrn\nThe Attempt was Unsuccessful, Try Again"
				ifconfig $mac_dev up
				sleep .7
				mac_control--
			else
				ifconfig $mac_dev up
				echo -e "$ins\n\n\n\nPress Enter to Continue"
				read
				mac_control--
			fi;;

			n|N) ifconfig $mac_dev down
			clear
			echo -e "$out\n--------------------\nChanging MAC Address\n--------------------"
			echo -e "$out\n$mac_dev `macchanger -m $sam $mac_dev`"
			if [[ $? -ne 0 ]];then
				echo -e "$wrn\nThe Attempt was Unsuccessful, Try Again"
				ifconfig $mac_dev up
				sleep .7
				mac_control--
			else
				ifconfig $mac_dev up
				echo -e "$ins\n\n\n\nPress Enter to Continue"
				read
				mac_control--
			fi;;

		esac;;

	esac
	}

clear
echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      --MAC Address Options--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) List Available NICs

2) MAC Address Change

P)revious Menu

G)oto Main Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
read var
case $var in
	1) nics--
	mac_control--;;

	2) mac_control_II--;;

	p|P) case $init_var in
		6) init_setup--;;
		*) init_var=
		setups--;;
	esac;;

	g|G) main_menu--;;

	*) mac_control--;;
esac
}

dev_check--()
{
ifconfig $dev_check_var > /dev/null
if [[ $? -ne 0 ]];then
	clear
	echo -e "$wrn\nDevice does NOT exist"
	sleep 1
	dev_check="fail"
else		for (( i = 1 ; i < 5 ; i++ ));do
			column=$(echo $var | cut -d . -f$i)
			if [[ $column -lt 0 || $column -gt 255 ]];then
				ip_mac="fail"
				break
			else
				ip_mac=
			fi

		done

		clear
	dev_check=
fi
}


monitormode--()
{
var=
km= ## Device to kill
clear
echo -e "$out"
airmon-ng
# var_II=$(ifconfig -a | grep --color=never wlan | awk '{print $1}' | cut -d: -f1)
# for var_II in $var_II; do
# 	echo -e "$out\n$var_II"
# 	ifconfig $var_II | grep --color=never wlan | awk '{print $5}' | cut -c1-17 | tr [:upper:] [:lower:] | sed 's/-/:/g'
# done
#
# var_II=$(ifconfig -a | grep --color=never mon | awk '{print $1}')
# for var_II in $var_II; do
# 	echo -e "$out\n$var_II"
# 	ifconfig $var_II | grep --color=never mon | awk '{print $5}' | cut -c1-17 | tr [:upper:] [:lower:] | sed 's/-/:/g'
# done

sleep 1
if [[ $kill_mon == "kill" ]];then
	echo -e "$wrn\n
                              ***WARNING***$ins
       Do not attempt to directly disable Monitor Mode on a Physical Device
        The script will ask for the associated Physical Device when ready$wrn
                              ***WARNING***"
	sleep 1
		echo -e "$inp\nMonitor Mode Device to Kill?"
		read km
		dev_check_var=$km
		dev_check--
		if [[ $dev_check == "fail" ]];then
			return
		fi

		if [[ -z $km ]];then
			return
		fi

	while [[ -z $var ]];do
		echo -e "$inp\nWhat interface is $out$km$inp Associated With?"
		read var
		dev_check_var=$var
		dev_check--
		if [[ $dev_check == "fail" ]];then
			var=
		fi

	done

	echo -e "$out"
	airmon-ng stop $km && airmon-ng stop $var
	pii=
	echo -e "$ins\n\nPress Enter to Continue"
	read
else
	echo -e "$inp\nInterface to Enable Monitor Mode on?"
	read phys_dev
	if [[ -z $phys_dev ]];then
		return
	fi

	dev_check_var=$phys_dev
	dev_check--
	if [[ $dev_check == "fail" ]];then
		return
	fi

	echo -e "$out"
	var=$(airmon-ng start $phys_dev | tee /tmp/airmon_output | grep enabled | awk '{print $9}' | sed 's/)//g' | cut -d] -f2)
	clear
	cat /tmp/airmon_output
	sleep 2.5
	shred -u /tmp/airmon_output
	pii=$var
fi
}


naming--()
{
clear
echo -e "$wrn\n
                        ***WARNING***$ins
Proceeding further will erase all NIC variable names for this script
Doing so requires that you rename them for this script to work properly$wrn
                        ***WARNING***

$inp\nDo you wish to continue? (y) or (n)\n"
read var
case $var in
	y|Y) ie=
	pii=
	init_setup--;;

	n|N) setups--;;

	*) naming--;;
esac
}


nics--()
{
clear
echo -e "$out"
airmon-ng
var=$(ifconfig -a | grep --color=never HWaddr | awk '{print $1}')
for var in $var; do
	echo -e "$out\n$var"
	ifconfig $var | grep --color=never HWaddr | awk '{print $5}' | cut -c1-17 | tr [:upper:] [:lower:] | sed 's/-/:/g'
done

echo -e "$ins\n\nPress Enter to Continue"
read
}


no_dev--()
{
case $1 in
	monitor)
	clear
	echo -e "$out\nMonitor Mode NIC not defined\n$inp\nWould You Like to Define it Now? (y or n)"
	read no_dev
	case $no_dev in
		y|Y)
		echo -e "$inp\nMonitor Mode NIC?"
		read pii
		dev_check_var=$pii
		dev_check--
		case $dev_parent in
			venue--)
			if [[ $dev_check == "fail" ]];then
				pii=
				var=
			fi

			sm=$(ifconfig $pii | grep --color=never HWaddr | awk '{print $5}' | cut -c1-17 | tr [:upper:] [:lower:] | sed 's/-/:/g');;

			routing--)
			if [[ $dev_check == "fail" ]];then
				pii=
				rte_choice=
			fi;;

		esac;;

		*)
		case $dev_parent in
			venue--)
			var= ;;

			routing--)
			rte_choice= ;;
		esac;;

	esac;;

	managed)
	clear
	echo -e "$out\nInternet Connected NIC not defined\n$inp\nWould You Like to Define it Now? (y or n)"
	read no_dev
	case $no_dev in
		y|Y)
		echo -e "$inp\nInternet Connected NIC?"
		read ie
		dev_check_var=$ie
		dev_check--
		case $dev_parent in
			routing--)
			if [[ $dev_check == "fail" ]];then
				ie=
				rte_choice=
			fi;;

		esac;;

		*)
		case $dev_parent in
			routing--)
			rte_choice= ;;
		esac;;

	esac;;

esac }


tchan--()
{
#tc= ## tgt channel
echo -e "$inp\nTgt Channel? (1-14)"
read tc
case $tc in
	1|2|3|4|5|6|7|8|9|10|11|12|13|14) ;;

	*) tc=
	echo -e "$wrn\nYou Must Enter a Legitimate Channel to Proceed"
	sleep 1.5
	clear;;
esac

case $parent_IV in
	dump) dump--;;
esac

case $parent_III in
	rtech) parent_III= ## Nulled to prevent repeat looping that is NOT wanted!
	rtech_II--;;
esac

case $parent_VI in
	ctech) ctech_II--;;
esac
}
