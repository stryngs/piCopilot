envir--()
{
wrn="\033[31m"   ## Warnings / Infinite Loops
ins="\033[1;32m" ## Instructions
out="\033[1;33m" ## Outputs
hdr="\033[1;34m" ## Headers
inp="\033[36m"   ## Inputs
}


greet--()
{
clear
echo -e "$hdr\n\n\n\n\n\n\n
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 QuickSet - A Quick Way to Setup a Wired/Wireless Hack
   Version $out$current_ver$hdr (\033[1;33m$rel_date$hdr)
   -- stryngs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
sleep 2.5
ap_check=
init_setup--
}


trap--()
{
echo -e "$wrn\nPlease Exit Out of The Script Properly"
sleep 2
main_menu--
}


usage--()
{
clear
echo -e "$ins\nUsage: ./quickset.sh"
}
