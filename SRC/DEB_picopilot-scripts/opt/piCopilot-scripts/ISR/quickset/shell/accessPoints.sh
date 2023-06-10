### Should fix this loop, but it's not too important..
ap--()
{
## MAC Address for the SoftAP
pres_mac=$(ifconfig $pii | awk '{print $5}' | awk '{print $1}' | cut -c1-17 | tr [:upper:] [:lower:] | sed 's/-/:/g')
pres_mac=$(echo $pres_mac | awk '{print $1}')
#blackhole targets every single probe request on current channel
modprobe tun
if [[ $bb == "1" ]]; then
	Eterm -b black -f white --pause --title "Blackhole AP" -e airbase-ng -c $sac -P -C 60 $pii &
	clear
## bullzeye targets specified ESSID only
elif [[ $bb == "2" ]]; then
	ssid=
	while [[ -z $ssid ]];do
		echo -e "$inp\nDesired ESSID?"
		read ssid
	done

	Eterm -b black -f white --pause --title "Bullzeye AP" -e airbase-ng -c $sac -e "$ssid" $pii &
	clear
elif [[ $bb == "3" ]];then
	private=
	ssid=
	while  [[ -z $ssid ]];do
		echo -e "$inp\nDesired ESSID?"
		read ssid
	done

	var=
	while [[ -z $var ]];do
		echo -e "$inp\nUse WEP? (y or n)"
		read var
	done

	case $var in
		y|Y) echo -e "$inp\nPassword? (a-f, 0-9) [10 Characters]"
		read wep_pword
		Eterm -b black -f white --pause --title "Wifi Extender AP" -e airbase-ng -c $sac -e "$ssid" -w $wep_pword $pii &
		clear;;

		n|N) Eterm -b black -f white --pause --title "Wifi Extender AP" -e airbase-ng -c $sac -e "$ssid" $pii & ;;

		*) ap--;;
	esac
fi

echo -e "$out\nConfiguring Devices..............\n"
## We want to give enough time before trying to down the virtual NIC for MAC changing and continuance of the script
## Need to slow quickset down for a little bit of time, or at least until at0 is created
for (( counter=0 ; counter < 13; counter++ ));do ## counter= Simple counting variable, nothing else..
	ifconfig at0 > /dev/null 2>&1
	if [[ $? -ne 0 ]];then
		sleep .5
	else
		counter="14"
		break
	fi

done

ifconfig at0 down
macchanger -m $pres_mac at0
sleep 1.5
ifconfig at0 up $sapip netmask $sasm
ifconfig at0 mtu $mtu_size
if [[ $dhcp_autol == "Yes" ]];then
	dhcp_pre_var--
	dhcp_svr--
else
	routing--
fi
}


ap_pre_var--()
{
sapip="192.168.10.1" ## SoftAP IP Address
sasm="255.255.255.0" ## SoftAP Subnet Mask
sac=6 ## SoftAP Channel
mtu_size=1500 ## MTU Size
dhcp_autol="Yes" ## DHCP Autolaunch for speed and intensity purposes
ap_check="on" ## Variable to make sure these pre-variables are called if DHCP server is done prior to SoftAP
}


ap_setup--()
{

	var_meth--()
	{
	clear
	bb=
	while [[ -z $bb ]];do
		echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
               --Method Selection--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) blackhole--> Responds to All Probe Requests

2) bullzeye--> Responds only to the specified ESSID$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
		read bb
	done

	case $bb in
		1|2) ap--;;
		*) var_meth--;;
	esac
	}

clear
echo -e "$hdr\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        --Soft AP Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) SoftAP IP Address      [$out$sapip$inp]

2) SoftAP Subnet Mask     [$out$sasm$inp]

3) SoftAP Channel         [$out$sac$inp]

4) MTU Size               [$out$mtu_size$inp]

5) DHCP Server Autolaunch [$out$dhcp_autol$inp]

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read var
case $var in
	1) echo -e "$inp\nSoftAP IP Address?"
	read sapip
	ip_mac-- ip $sapip
		if [[ $ip_mac == "fail" ]];then
			sapip=
		fi

	ap_setup--;;

	2) echo -e "$inp\nSoftAP Subnet Mask?"
	read sasm
	ip_mac-- ip $sasm
		if [[ $ip_mac == "fail" ]];then
			sasm=
		fi

	ap_setup--;;

	3) echo -e "$inp\nSoftAP Channel? (1-14)"
	read sac
	case $sac in
		1|2|3|4|5|6|7|8|9|10|11|12|13|14) ;;
		*) sac= ;;
	esac

	ap_setup--;;

	4) echo -e "$inp\nDesired MTU Size? (42-6122)"
	read mtu_size
	if [[ $mtu_size -lt 42 || $mtu_size -gt 6122 ]];then
		mtu_size=
	fi

	ap_setup--;;

	5) echo -e "$inp\nAutolaunch DHCP Server? (y or n)"
	read dhcp_autol
	case $dhcp_autol in
		y|Y) dhcp_autol="Yes" ;;
		n|N) dhcp_autol="No" ;;
		*) dhcp_autol= ;;
	esac

	ap_setup--;;

	c|C) if [[ -z $sapip || -z $sasm || -z $sac || -z $mtu_size || -z $dhcp_autol ]];then
		echo -e "$wrn\nAll Fields Must be Filled Before Proceeding"
		sleep 1
		ap_setup--
	fi;;

	p|P) routing--;;

	m|M) main_menu--;;

	*) ap_setup--;;
esac

if [[ $private == "yes" ]]; then
	bb="3"
	ap--
else
	var_meth--
fi
}
