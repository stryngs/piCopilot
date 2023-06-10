atk_menu--()
{
clear
echo -e "$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                  --Attack Menu--
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$inp
1) Arpspoof

2) DNSspoof

3) Ferret

4) Hamster

5) SSLstrip

M)ain Menu
$ins
--> All Attacks launched in `pwd`$hdr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n$inp"
read var
case $var in
	1) arpspoof--;;

	2) dnsspoof--;;

	3) ferret--;;

	4) if [[ -f hamster.txt ]];then
		Eterm -b black -f white --pause --title "Hamster" -e hamster &
		atk_menu--
	else
		echo -e "$wrn\n\nhamster.txt MUST exist to run hamster"
		sleep 1.5
		atk_menu--
	fi;;

	5) strip_em--;;

	m|M) main_menu--;;

	*) atk_menu--;;
esac
}
