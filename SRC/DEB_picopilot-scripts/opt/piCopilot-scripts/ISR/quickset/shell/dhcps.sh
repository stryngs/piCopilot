dhcp_pre_var--()
{
dhcp_dev="at0" ## Device to setup DHCP server on
sas="192.168.10.0" ## DHCP Subnet
sair="192.168.10.100 192.168.10.200" ## DHCP IP range
dhcp_start="192.168.10.100"
dhcp_end="192.168.10.200"
dhcp_tail="Yes" ## DHCP Tail Log
dns_cus="No" ## Use custom DNS entries for DHCP server, defaulted to nameservers in /etc/resolv.conf
}


dhcp_svr--()
{
##Gives dhcpd the permissions it needs
mkdir -p /tmp/dhcpd/ > /dev/null 2>&1
echo > /tmp/dhcpd/dhcpd.pid > /dev/null 2>&1
shred -u /tmp/dhcpd/dhcpd.pid > /dev/null 2>&1
## Clear any dhcp leases that might have been left behind
echo > /tmp/dhcpd/dhcpd.leases > /dev/null 2>&1
chown -R dhcpd:dhcpd /tmp/dhcpd/
var=
dhcpdconf="/tmp/dhcpd/dhcpd.conf" ## Temp file used by dhcpd3


	dhcp_func--()
	{
	#dns_cus= Variable for determining if Custom DNS hosts are requested
	#dns_cus_array= Array for holding the custom DNS hosts IP addresses
	#dns_entry=Variable for index assignments within ${dns_cus_array[@]}
	#dns_total= Total number of indexes in the Custom DNS hosts array

		if [[ -z $ap_type ]];then
			while [[ -z $ap_type ]];do
				echo -e "$inp\n1) Wireless Vaccuum style DHCP Server

2) StickyPot style DHCP Server

3) WiFi Range Extender style DHCP Server"
				read decide
				case $decide in
					1) foo=1
					ap_type=3 ;;

					2) foo=1
					ap_type=4 ;;

					3) foo=1
					ap_type=5 ;;
				esac

			done

		fi

	case $ap_type in
		3|5) clear
		echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			--DHCP Server Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) DHCP Server Device  [$out$dhcp_dev$inp]

2) Gateway IP Address  [$out$sapip$inp]

3) IP Range            [$out$sair$inp]

4) Subnet Mask         [$out$sasm$inp]

5) Subnet              [$out$sas$inp]

6) Custom DNS Entries  [$out$dns_cus$inp]

7) Tail DHCP Log       [$out$dhcp_tail$inp]

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
		read var
		case $var in
			1) echo -e "$inp\nDHCP Server Device?"
			read dhcp_dev
			dev_check_var=$dhcp_dev
			dev_check--
			if [[ $dev_check == "fail" ]];then
				dhcp_dev=
			fi

			dhcp_func--;;

			2) echo -e "$inp\nGateway IP Address?"
			read sapip
			ip_mac-- ip $sapip
			if [[ $ip_mac == "fail" ]];then
				sapip=
			fi

			dhcp_func--;;

			3) echo -e "$inp\nIP Range? (ex. 192.168.1.100 192.168.1.200)"
			read sair
			dhcp_start=$(echo $sair | awk '{print $1}')
			dhcp_end=$(echo $sair | awk '{print $2}')
			ip_mac-- ip $dhcp_start
			if [[ $ip_mac == "fail" ]];then
				sair=
			fi

			ip_mac-- ip $dhcp_end
			if [[ $ip_mac == "fail" ]];then
				sair=
			fi

			dhcp_func--;;

			4) echo -e "$inp\nSubnet Mask?"
			read sasm
			ip_mac-- ip $sasm
			if [[ $ip_mac == "fail" ]];then
				sasm=
			fi

			dhcp_func--;;

			5) echo -e "$inp\nSubnet?"
			read sas
			ip_mac-- ip $sas
			if [[ $ip_mac == "fail" ]];then
				sas=
			fi

			dhcp_func--;;

			6) echo -e "$inp\nCreate Custom DNS Entries? (y or n)"
			read dns_cus
			case $dns_cus in
				y|Y) dns_cus="Yes"
				unset dns_cus_array
				declare -a dns_cus_array
				echo -e "$ins\nEnter the desired IP Addressess of the DNS.  End with # on a new line.\n$inp"
				while :;do
					read dns_entry
					if [[ $dns_entry != \# ]];then
						dns_cus_array=("${dns_cus_array[@]}" $dns_entry)
					else
						break
					fi

				done;;

				n|N) dns_cus="No" ;;

				*) dns_cus= ;;
			esac

			dhcp_func--;;

			7) echo -e "$inp\nCreate a Tail of the DHCP Log? (y or n)"
			read dhcp_tail
			case $dhcp_tail in
				y|Y) dhcp_tail="Yes" ;;
				n|N) dhcp_tail="No" ;;
				*) dhcp_tail= ;;
			esac

			dhcp_func--;;

			c|C) if [[ -z $dhcp_dev || -z $sapip || -z $sair || -z $sasm || -z $sas || -z $dns_cus || -z $dhcp_tail ]];then
				echo -e "$wrn\nAll Fields Must be Filled Before Proceeding"
				sleep 1
				dhcp_func--
			fi;;

			p|P) routing--;;

			m|M) main_menu--;;

			*) dhcp_func--;;
		esac;;

			4) clear
			echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			--DHCP Server Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) DHCP Server Device  [$out$dhcp_dev$inp]

2) Gateway IP Address  [$out$sapip$inp]

3) IP Range            [$out$sair$inp]

4) Subnet Mask         [$out$sasm$inp]

5) Subnet              [$out$sas$inp]

6) Custom DNS Entries  [$out$dns_cus$inp]

7) Tail DHCP Log       [$out$dhcp_tail$inp]

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
			read var
			case $var in
				1) echo -e "$inp\nDHCP Server Device?"
				read dhcp_dev
				dev_check_var=$dhcp_dev
				dev_check--
				if [[ $dev_check == "fail" ]];then
					dhcp_dev=
				fi

				dhcp_func--;;

				2) echo -e "$inp\nGateway IP Address?"
				read sapip
				ip_mac-- ip $sapip
				if [[ $ip_mac == "fail" ]];then
					sapip=
				fi

				dhcp_func--;;

				3) echo -e "$inp\nIP Range? (ex. 192.168.1.100 192.168.1.200)"
				read sair
				dhcp_start=$(echo $sair | awk '{print $1}')
				dhcp_end=$(echo $sair | awk '{print $2}')
				ip_mac-- ip $dhcp_start
				if [[ $ip_mac == "fail" ]];then
					sair=
				fi

				ip_mac-- ip $dhcp_end
				if [[ $ip_mac == "fail" ]];then
					sair=
				fi

				dhcp_func--;;

				4) echo -e "$inp\nSubnet Mask?"
				read sasm
				ip_mac-- ip $sasm
				if [[ $ip_mac == "fail" ]];then
					sasm=
				fi

				dhcp_func--;;

				5) echo -e "$inp\nSubnet?"
				read sas
				ip_mac-- ip $sas
				if [[ $ip_mac == "fail" ]];then
					sas=
				fi

				dhcp_func--;;

				6) echo -e "$inp\nCreate Custom DNS Entries? (y or n)"
				read dns_cus
				case $dns_cus in
					y|Y) dns_cus="Yes"
					unset dns_cus_array
					declare -a dns_cus_array
					echo -e "$ins\nEnter the desired IP Addressess of the DNS.  End with # on a new line.\n$inp"
					while :;do
						read dns_entry
						if [[ $dns_entry != \# ]];then
							dns_cus_array=("${dns_cus_array[@]}" $dns_entry)
						else
							break
						fi

					done;;

					n|N) dns_cus="No" ;;

					*) dns_cus= ;;
				esac

				dhcp_func--;;

				7) echo -e "$inp\nCreate a Tail of the DHCP Log? (y or n)"
				read dhcp_tail
				case $dhcp_tail in
					y|Y) dhcp_tail="Yes" ;;
					n|N) dhcp_tail="No" ;;
					*) dhcp_tail= ;;
				esac

				dhcp_func--;;

				c|C) if [[ -z $dhcp_dev || -z $sapip || -z $sair || -z $sasm || -z $sas || -z $dns_cus || -z $dhcp_tail ]];then
					echo -e "$wrn\nAll Fields Must be Filled Before Proceeding"
					sleep 1
					dhcp_func--
				fi;;

				p|P) routing--;;

				m|M) main_menu--;;

				*) dhcp_func--;;
			esac;;

		esac

		case $ap_type in
			3|5) ## Echo into and remove the file to start clean
			echo > /tmp/dhcpd/dhcpd.conf > /dev/null 2>&1
			shred -u /tmp/dhcpd/dhcpd.conf > /dev/null 2>&1
			## start dhcpd daemon with special configuration file
			echo -e "$out\nGenerating /tmp/dhcpd/dhcpd.conf"
			echo "authoritative;" >> /tmp/dhcpd/dhcpd.conf
			echo "default-lease-time 7200;">> /tmp/dhcpd/dhcpd.conf
			echo "max-lease-time 7200;" >> /tmp/dhcpd/dhcpd.conf
			echo "min-lease-time 7200;" >> /tmp/dhcpd/dhcpd.conf
			echo "ddns-update-style none;" >> /tmp/dhcpd/dhcpd.conf
			echo "log-facility local7;" >> /tmp/dhcpd/dhcpd.conf
			echo "subnet $sas netmask $sasm {" >> /tmp/dhcpd/dhcpd.conf
			echo "range $sair;" >> /tmp/dhcpd/dhcpd.conf
			echo "option routers $sapip;" >> /tmp/dhcpd/dhcpd.conf
			if [[ $dns_cus == "No" ]];then
				for dns_entry in $(grep nameserver /etc/resolv.conf | awk '{print $2}');do
					echo "option domain-name-servers $dns_entry;" >> /tmp/dhcpd/dhcpd.conf
				done
			else
				dns_total=$(echo ${#dns_cus_array[@]})
				for (( i = 0 ; i < $dns_total ; i++ ));do
					echo "option domain-name-servers "${dns_cus_array[$i]}";" >> /tmp/dhcpd/dhcpd.conf
				done
			fi

			echo "}"  >> /tmp/dhcpd/dhcpd.conf
			dhcp_tmp=1 ;; ## Variable for determining if /tmp/dhcpd/dhcpd.conf has been created

			4) 	## Echo into and remove the file to start clean
			echo > /tmp/dhcpd/dhcpd.conf > /dev/null 2>&1
			shred -u /tmp/dhcpd/dhcpd.conf > /dev/null 2>&1
			## start dhcpd daemon with special configuration file
			echo -e "$out\nGenerating /tmp/dhcpd/dhcpd.conf"
			echo "authoritative;" >> /tmp/dhcpd/dhcpd.conf
			echo "default-lease-time 7200;">> /tmp/dhcpd/dhcpd.conf
			echo "max-lease-time 7200;" >> /tmp/dhcpd/dhcpd.conf
			echo "min-lease-time 7200;" >> /tmp/dhcpd/dhcpd.conf
			echo "ddns-update-style none;" >> /tmp/dhcpd/dhcpd.conf
			echo "log-facility local7;" >> /tmp/dhcpd/dhcpd.conf
			echo "subnet $sas netmask $sasm {" >> /tmp/dhcpd/dhcpd.conf
			echo "range $sair;" >> /tmp/dhcpd/dhcpd.conf
			echo "}"  >> /tmp/dhcpd/dhcpd.conf
			dhcp_tmp=1 ;; ## Variable for determining if /tmp/dhcpd/dhcpd.conf has been created
		esac

	}

	dhcp_svr_II--()
	{

		dhcp_svr_III--()
		{
		case $rte_choice in
			3|5) route add -net $sas netmask $sasm gw $sapip;;
		esac

		case $rte_choice in
			3|5) iptables -P FORWARD ACCEPT
			iptables -t nat -A POSTROUTING -o $ie -j MASQUERADE;;
		esac

		echo -e "$out\n\n\n\nDHCP server started succesfully\n\n"
		sleep 1
		case $dhcp_tail in
			Yes) Eterm -b black -f white --pause --title "DHCP Server Tail /tmp/dhcpd/dhcpd.leases" -e tail -f /tmp/dhcpd/dhcpd.leases & ;;
		esac

		echo -e "$ins\n\n\n\nPress Enter to Return to Routing Features"
		read
		routing--
		}

	clear
	echo -e "$out"
	dhcpd3 -cf $dhcpdconf -pf /tmp/dhcpd/dhcpd.pid -lf /tmp/dhcpd/dhcpd.leases $dhcp_dev &
	for (( counter=0 ; counter < 7; counter++ ));do ## counter= Simple counting variable, nothing else..
 		dhcp_svr_pid=$(cat /tmp/dhcpd/dhcpd.pid) > /dev/null 2>&1
		if [[ -z $dhcp_svr_pid ]];then
			sleep 1
        else
			dhcpd_success="yes" ## pid_success= Variable for testing if dhcpd.pid was created
			counter="8"
			break
		fi

	done

	if [[ $dhcpd_success == "yes" ]];then
		dhcp_svr_III--
	else
		echo -e "$wrn\nThe DHCP server could not be started\nPress Enter to Return to Routing Features"
		read
		routing--
	fi
	}

if [[ -e $dhcpdconf ]] ; then
	while [[ -z $var ]];do
		echo -e "$wrn\nDHCP Server Configuration File Exists$inp\n
Create New File [\033[31mDeleting $dhcpdconf$inp] (y or n)?"
		read var
		case $var in
			y|Y) dhcp_func--
			dhcp_svr_II--;;

			n|N) echo > /tmp/dhcpd/dhcpd.leases ## Clear any dhcp leases that might have been left behind
			dhcp_svr_II--;;

			*) var= ;;
		esac

	done

else
	dhcp_func--
	dhcp_svr_II--
fi
}
