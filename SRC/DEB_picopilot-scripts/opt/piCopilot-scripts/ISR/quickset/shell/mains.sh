cleanup--()
{
## Check for DHCPD action history
## If it existed, act appropriately
if [[ -n $dhcp_svr_pid ]];then
	ps aux | grep $dhcp_svr_pid | grep -v grep > /dev/null 2>&1
	if [[ $? -eq 0 ]];then
		echo -e "$inp\nKill the DHCP Server? (y or n)"
		read var
		case $var in
			y|Y) kill -9 $dhcp_svr_pid
			echo -e "$out\nDHCP Server Successfully Killed" ;;
		esac

	fi

	test -f /tmp/dhcpd/dhcpd.pid
	if [[ $? -eq 0 ]];then
		echo -e "$inp\nRemove the DHCP Server PID file? (y or n)"
		read var
		case $var in
			y|Y) echo -e "$out"
			shred -uv /tmp/dhcpd/dhcpd.pid ;;
		esac

	fi

	test -f /tmp/dhcpd/dhcpd.leases
	if [[ $? -eq 0 ]];then
		echo -e "$inp\nRemove /tmp/dhcpd/dhcpd.leases? (y/n)"
		read var
		case $var in
			y|Y) echo -e "$out"
			shred -uv /tmp/dhcpd/dhcpd.leases ;;
		esac

	fi

	test $dhcpdconf
	if [[ $? -eq 0 ]];then
		echo -e "$inp\nRemove $dhcpdconf? (y/n)"
		read var
		case $var in
			y|Y) echo -e "$out"
			shred -uv $dhcpdconf ;;
		esac

	fi

fi

## Check for DNS Spoofing history
## If it existed, act appropriately
if [[ $dns_tmp == 1 ]];then
	var=0
	while [[ $var == 0 ]];do
		echo -e "$inp\nRemove /tmp/dns_spf? (y/n)"
		read var
		case $var in
			y|Y) shred -uv /tmp/dns_spf
			var=1 ;;

			n|N) var=1 ;;

			*) ;;
		esac

	done

fi

if [[ $wacg_check == "active" ]];then
var=0
	while [[ $var == 0 ]];do
		echo -e "$inp\nRemove temporary WACg Files? (y/n) $out{/tmp/WACg/*}"
		read var
		case $var in
			y|Y) shred -uv /tmp/WACg/*
			rm -rf /tmp/WACg
			var=1 ;;

			n|N) var=1 ;;

			*) ;;
		esac

	done

fi

reset
echo -e "\n\n\n"
exit
}


init_setup--()
{
kill_mon=
clear
echo -e "$ins\n
----------------------------------------------------------------------
 Only Certain Modes in this Script Require Both Devices to be Defined
----------------------------------------------------------------------$hdr\n
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                          Initial NIC Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Internet Connected NIC               [$out$ie$inp]

2) Monitor Mode NIC                     [$out$pii$inp]

3) Enable Monitor Mode

4) Kill Monitor Mode

5) MAC Address Options

6) List Available NICs

C)ontinue

E)xit Script$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
read init_var
case $init_var in
	1) echo -e "$inp\nDefine NIC"
	read ie
	dev_check_var=$ie
	dev_check--
	if [[ $dev_check == "fail" ]];then
		ie=
	fi

	init_setup--;;

	2) echo -e "$inp\nDefine NIC"
	read pii
	dev_check_var=$pii
	dev_check--
	if [[ $dev_check == "fail" ]];then
		pii=
	fi

	init_setup--;;

	3) monitormode--
	init_setup--
	;;

	4) kill_mon="kill"
	monitormode--
	init_setup--;;

	5) mac_control--;;

	6) nics--
	init_setup--;;

	c|C) main_menu--;;

	e|E) reset
	echo -e "\n\n"
	exit 0;;

	*) init_setup--;;
esac
}


main_menu--()
{
trap trap-- INT
clear
echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~
    QuickSet (\033[1;33m$current_ver$hdr)
     --Main Menu--
Make Your Selection Below
~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Setup Menu

2) WiFi Stuff

3) Quick Attacks

4) Routing Features

E)xit Script$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
read var
case $var in
	1) setups--;;

	2) wifi_101--;;

	3) atk_menu--;;

	4) routing--;;

	e|E) cleanup--;;

	*) main_menu--;;
esac
}


setups--()
{
clear
echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
         --Setup Menu--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) List Available NICs

2) NIC Names & Monitor Mode Setup

3) MAC Address Options

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
read var
case $var in
	1) nics--
	setups--;;

	2) naming--;;

	3) mac_control--;;

	m|M) main_menu--;;

	*) setups--;;
esac
}
