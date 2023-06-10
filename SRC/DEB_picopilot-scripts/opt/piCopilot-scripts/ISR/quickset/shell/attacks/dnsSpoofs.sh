dnsspoof--()
{
#dspoof_dev= Device to listen on
#d_hosts= Variable to check if user wants to use custom hosts file for dnsspoof

	dnsspoof_II--()
	{
	#dns_spf_array= Array for holding the custom DNS spoof inputs
	#dns_spf_entry= Variable for index assignments within ${dns_spf_array[@]}
	#dns_spf_total= Total number of indexes in the DNS Spoof array
	clear
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
           --DNSspoof Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Listening NIC    [$out$dspoof_dev$inp]

2) Custom Hostfile  [\033[1;33m$d_hosts\033[36m]

2) List Available NICs

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read var
	case $var in
		1) echo -e "$inp\nNIC?"
		read dspoof_dev
		dev_check_var=$dspoof_dev
		dev_check--
		if [[ $dev_check == "fail" ]];then
			dspoof_dev=
		fi

		dnsspoof_II--;;

		2) echo -e "\033[36m\nUse Custom DNS Hosts File? (y or n)$inp"
		read d_hosts
		case $d_hosts in
			y|Y) d_hosts="Yes"
			shred -u /tmp/dns_spf > /dev/null 2>&1
			unset dns_spf_array
			declare -a dns_spf_array
			echo -e "$ins\nEnter each line of desired dnsspoof hostsfile\n(i.e. 192.168.1.1 foo.com).\nEnd with # on a new line.\n$inp"
			while :;do
				read dns_spf_entry
				if [[ $dns_spf_entry != \# ]];then
					dns_spf_array=("${dns_spf_array[@]}" "$dns_spf_entry")
				else
					break
				fi

			done

			dns_spf_total=$(echo ${#dns_spf_array[@]})
			for (( i = 0 ; i < $dns_spf_total ; i++ ));do ## $i is a simple counter
				echo ${dns_spf_array[$i]} >> /tmp/dns_spf
			done

			dns_tmp=1 ;; ## Variable for determining if /tmp/dns_spf has been created

			n|N) d_hosts="No" ;;

			*) d_hosts= ;;
		esac

		dnsspoof_II--;;

		3) nics--
		ferret_II--;;

		c|C) if [[ -z $dspoof_dev || -z $d_hosts ]];then
			echo -e "$wrn\nAll Fields Must be Filled Before Proceeding"
			sleep 1
			dnsspoof_II--
		else
			fcheck--
			case $d_hosts in
				Yes) Eterm -b black -f white --pause --title "DNSspoof" -e dnsspoof -i $dspoof_dev -f /tmp/dns_spf &
				atk_menu--;;

				No) Eterm -b black -f white --pause --title "DNSspoof" -e dnsspoof -i $dspoof_dev &
				atk_menu--;;
			esac

		fi;;

		p|P) atk_menu--;;

		m|M) main_menu--;;

		*) ferret_II--;;
	esac
	}

dspoof_dev=$ie
d_hosts="No"
dnsspoof_II--
}
