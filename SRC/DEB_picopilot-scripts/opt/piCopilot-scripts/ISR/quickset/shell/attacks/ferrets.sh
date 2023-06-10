ferret--()
{
#fer_dev= Device to be sniffed
#fer_type= Wifi or Wired
#wifi_check= Allowing us the conditional choice for a non default ferret setting of channel 6 if we use a wifi device

	ferret_II--()
	{
	clear
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
           --Ferret Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Device to Sniff  [$out$fer_dev$inp]

2) Type of Device   [$out$fer_type$inp]

3) List Available NICs

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read var
	case $var in
		1) echo -e "$inp\nDevice?"
		read fer_dev
		dev_check_var=$fer_dev
		dev_check--
		if [[ $dev_check == "fail" ]];then
			fer_dev=
		fi

		ferret_II--;;

		2) echo -e "$inp\n1) Wireless\n2) Wired"
		read var
		case $var in
			1) fer_type="Wireless"
			wifi_check="wireless" ;;

			2) fer_type="Wired"
			wifi_check="wired" ;;

			*) var= ;;
		esac

		ferret_II--;;

		3) nics--
		ferret_II--;;

		c|C) if [[ -z $fer_dev || -z $wifi_check ]];then
			echo -e "$wrn\nSniffing Device and Type Must be Selected to Proceed"
			sleep 1
			ferret_II--
		else
			case $wifi_check in
				wireless) var=
					chan_check-- $fer_dev
					if [[ -n $chan_res ]];then
						echo -e "$out\nCurrent Channel is: $chan_res. $inp Would You Like to Change it? (y/n)"
						read var
					else
						tchan--
					fi

					case $var in
						y|Y) tchan--;;
						n|N) tc=$chan_res ;;
						*) ferret_II--;;
					esac

				if [[ -z $tc ]];then
					ferret_II--
				fi

				Eterm -b black -f white --pause --title "Ferret" -e ferret -i $fer_dev --channel $tc &
				atk_menu--;;

				wired) Eterm -b black -f white --pause --title "Ferret" -e ferret -i $fer_dev &
				atk_menu--;;
			esac

		fi;;

		p|P) atk_menu--;;

		m|M) main_menu--;;

		*) ferret_II--;;
	esac
	}

if [[ -z $pii ]];then
	fer_dev=$ie ## Set to internet conected NIC if no monitor mode device present
else
	fer_dev=$pii
fi

fer_type="Wireless"
wifi_check="wireless"
ferret_II--
}
