# piCopilot
piCopilot is an ecosystem for autonomous workflows.  It has been tailored for the world of unmanned Intelligence, Surveillance and Reconnaissance.  Whether acting as an assistant during air, land or sea missions, tracking Wi-Fi and Bluetooth signals, optical monitoring, or some other interesting integration; piCopilot stands ready to assist the operator with whatever may come.

The Wi-Fi and Bluetooth monitoring capabilities of piCopilot may not be legal for use in every Country or locality.  Ensure that you check the rules and regulations for where you will be operating prior to use.  The operator is responsible for any legal and/or civil issues that may arise from their usage of piCopilot.

piCopilot is 100% feedback driven.  If you like piCopilot and wish to contribute, simply fork and PR; or raise an issue.

## Unmanned Vehicle Operations
The picopilot-unmanned package was pre-installed as part of the 20200824 release.  The following files are of interest to anyone who wants to have the core services turned on at boot:
* /etc/supervisor/conf.d/gsPrep.conf
* /etc/supervisor/conf.d/motionPrep.conf
* /etc/systemd/system/mavproxy.service

piCopilot works best in conjunction with the [CubePilot Ecosystem](https://www.cubepilot.com/#/cube/features).  The unmanned package works seamlessly with either QGroundControl or Mission Planner.  For further information on both Ground Control Systems, please refer to their respective websites:
* http://qgroundcontrol.com/
* https://ardupilot.org/planner/

piCopilot expects the GCS to have a statically set IP Address of 192.168.10.10/24 for UAV purposes.  Changing the IP address for the web applications is fairly straight forward.  From the root directory of this repository perform the following and you will see where the hardcoded IP exists for both the Raspberry PI (.254) and the GCS (.10):
```
grep -RHn -e '192.168.10.10' -e '192.168.10.254'
```

**Benefits of integrating with piCopilot**

*Swarm/Battalion Formation Management*</br>
Useful in a multitude of operations to include large-scale agricultural monitoring, or environmental surveys where handling large groups of unmanned vehicles in synchronized formations is a must.

*Cross-Platform*
Operating system agnostic and provides broad applicability across different hardware platforms.

*GPS-Denied Operation Solutions*
Provides solutions for operations in places where denial or spoofing is likely, ensuring uninterrupted missions in challenging terrains or adversarial conditions.

*Enhanced SIGINT Capabilities*
Advanced Signals Intelligence capabilities for effective surveillance and reconnaissance across the RF spectrum.

*Flexible Hardware Compatibility*
Supports a wide range of hardware and various PC configurations allowing for deployment on existing infrastructure, reducing the need for specialized equipment.

*Improved Data Visualization and Analysis*
Enhanced integration with data visualization tools like Grafana and plotly; beneficial for command and control centers needing to make quick and informed decisions.

## Core packages
* piCopilot
  * The ecosystem
* piCopilot-idrop
  * Intrusion Detection Reaction Observation Platform
* piCopilot-scripts
  * Useful scripts for piCopilot usage across the ecosystem
* piCopilot-unmanned
  * Pi powered Copilot for Unmanned Systems
* piCopilot-wifi
  * WiFi meta-package for piCopilot

## Definitions
* ecosystem
  * Any objects in memory, files, folders or system processes which make up how piCopilot operates
* kBlue
  * The underlying framework for Ubertooth and PostgreSQL interaction
* kSnarf
  * The underlying framework for 802.11 sniffing and PostgreSQL interaction
* pipeline network
  * The IPv4 network between the user and the ecosystem
  * Built on an 802.11 model
  * Can be 802.3 based with minor modifications
  * Responsible for all interactions with piCopilot
    * 3000 - Grafana
    * 8000 - piCopilot-unmanned control panel
    * 8001 - kSnarf and kBlue control panel
    * 8765 - Motioneye
    * 9001 - Supervisor
    * 9090 - idrop visuals

## Getting started
1. Create the piCopilot image for the Raspberry Pi
* Refer to notes in RELEASE
* Minimum 8GB SD card required
* Burn the image
* Boot the Raspberry Pi

2. When piCopilot first boots it will be running in hostapd mode.
* Connect to the wifi ESSID called myPi
* The password is piCopilotAP

3. Verify piCopilot-idrop is running and setup external USB NIC for 802.11
* Ports 8001 and 9001 should now be in use
* Plug in USB NIC
* Open a browser and proceed to http://192.168.10.254:8001/
* Select NIC prep
* The system will shutdown

4. Power back on and go

## Why does most of the system run as root!?
piCopilot expects a secured network.  It is not recommended to connect the pipeline network to any network where untrusted users are present or have the ability to manipulate or sniff traffic.

"Pick one thing and do it well".

Support is available using the FOSS model if you need assistance with modifications on some of the lower level aspects of piCopilot usage.

## Performance boosts (Recommended - Required for kBlue)
For SD card preservation, dphys-swapfile is disabled.  It is preferable to offload any swapping to a USB:
1. Become root:
```
sudo -s
# The password is ~~> notraspberry
```

2. Plug a USB thumb-drive of ideally at least 4GB in size into the Raspberry Pi and then do:
```
parted -s /dev/sda mklabel msdos
parted -s /dev/sda mkpart primary 0% 50%
parted -s /dev/sda mkpart primary 51% 100%
mkswap /dev/sda1
mkfs.ext4 /dev/sda2 -m 0
```

3. Setup /etc/fstab for mounts:
```
mkdir -p /mnt/usb_storage
echo '/dev/sda1 swap swap defaults 0 0' >> /etc/fstab
echo '/dev/sda2 /mnt/usb_storage ext4 noauto,nofail,x-systemd.automount,x-systemd.idle-timeout=2,x-systemd.device-timeout=2' >> /etc/fstab
```

4. Turn on swap and storage:
```
swapon /dev/sda1
mount /dev/sda2
```

5. You may now plug in an Ubertooth

## GPS integration
piCopilot has the ability to notate GPS location.  Depending on the USB devices plugged into piCopilot you may need to tweak /etc/default/gpsd.  The GPS is enabled by way of opening a shell and then:
```
systemctl enable gpsd
systemctl start gpsd
```

## Grafana visualizations
Setup Grafana and visualize your findings
```
sudo -s
# The password is ~~> notraspberry
systemctl enable grafana-server
systemctl start grafana-server
```
* Proceed to http://192.168.10.254:3000/login
* Login with admin:admin
* Change the default Grafana password if wanted
* Connect grafana to the postgresql database
  * Settings
  * Data Sources
  * Add Data Source
    * PostgreSQL
      * Host     --> localhost:5432
      * Database --> idrop
      * User     --> root
      * Password --> idrop
      * SSL Mode --> disable
* A sample dashboard for idrop is waiting on you

## Tuning idrop
To activate the k9 module notate out the MACs in question in the file /opt/piCopilot-idrop/targets.lst.  Each MAC is separated by a new line and an optional descriptor.  Upon running idrop will parse targets.lst and then update the targets table accordingly.  Each row within targets is constrained by by the mac and optional descriptor.  Thus, you may have the MAC of aa:bb:cc:dd:ee:ff multiple times, but only if the optional descriptor is different.

In the current version only notations in targets.lst will be notated.  Future planning will allow the user to optionally include all MACs listed in the targets table.

targets.lst is case-insensitive for the MAC.  An example targets.lst is as follows:
```
aa:bb:cc:dd:ee:ff My lost cell phone
11:22:AA:Bb:CD:ef That laptop I lost in the woods
```

## Connecting piCopilot to the Internet
* Give /etc/resolv.conf a nameserver
* run modWLAN and then reboot
  ```
  #modWLAN 'yourNetwork' 'yourPassword' 'Static IP for the Pi' 'netmask' 'gateway'
  modWLAN 'myHome' 'password' '192.168.73.202' '255.255.255.0' '192.168.73.1'
  ```

## Changing the self-hosted Access Point
By default piCopilot runs on channel 11 using a 192.168.10.254.  If you have used modWLAN or want to simply change the AP settings run modHOSTAPD and then reboot.
  ```
  #modHOSTAPD 'essid' 'psk' 'mode' 'channel' 'address' 'netmask' 'gateway' 'first ip' 'last ip'
  modHOSTAPD 'myPi' 'piCopilotAP' 'g' '11' '192.168.10.254' '255.255.255.0' '192.168.10.254' '192.168.10.2' '192.168.10.249'
  ```

## Upgrading (Known to break things)
* New image releases can be sporadic
* Interim updates are maintained by the DEBs folder
* How to determine what versions came the image:
```
dpkg --list | grep picopilot
```
* If the numbers above are lower than the files in DEBs, you have an available upgrade.
* It is recommended to purge piCopilot from the system prior to any upgrade.
* Perform a reboot, ensure there are no .deb files within the current directory and then do:
```
apt-get purge -y picopilot*
```
* Once complete verify that /opt now contains only 2 folders; pigpio and vc.
```
ls /opt
```
* Download the updates for piCopilot
```
git clone https://github.com/stryngs/piCopilot.git
cd piCopilot/DEBs
dpkg -i *.deb
```
* Prep the database
    * Database schema changes may occur during upgrades and without warning
    * Backup the data if it matters
    * DROP tables is our friend:
    ```
    psql idrop
    DROP TABLE IF EXISTS blue;
    DROP TABLE IF EXISTS k9;
    DROP TABLE IF EXISTS main;
    DROP TABLE IF EXISTS probes;
    DROP TABLE IF EXISTS targets;
    DROP TABLE IF EXISTS timer;
    DROP TABLE IF EXISTS uniques;
    \q
    ```

## Known bug(s)
* For the page on /, the idrop Service gets confused by the presence of kBlue and how sh.sysMode is used.  When enabling kBlue and returning to the main menu, the idrop Service will now read as kBlue.  This will be worked out in later releases.
    * To force it proper, cycle the idrop service off and then back on.  It will correct by virtue of sh.sysMode flipping through the original idrop logic.
* When downloading idrop logs, the cache gets hung.
    * Clear the cache in history as a workaround.
* kBlue can cause ubertooth hangs with multiple on/off calls.
    * Reboot is easiest, but "killall -9 ubertooth-btle" works for the ssh

## Lessons learned from tools like piCopilot
1.Keep Wireless and Bluetooth off when not in use, seriously.  Yes, really.

Your device is noisy because it is always looking for the next best thing.  By turning off Wireless and Bluetooth when not in use you will reduce the unique signatures that can be associated with a common device in 2021 that has the ability to leverage Wireless or Bluetooth.  Tracking of those signatures is already in use by various advertising companies and potentially, Governmental agencies around the world.  Why make yourself a bigger target just for the sake of convenience?

2. Work from home took on a whole new meaning.

For about $35 worth of gear the world around you changes into 0s, 1s and patterns.  No longer does one have to wait until working hours are over to see a new ESSID on the off-chance an employee brought their laptop home from work.  The Internet as we have it in 2021 proved one thing, baked-in needs to be the new bolt-on.  Did you know a Bank moved in next door?  How about a Law firm?  That dentist too.  idrop surely will.

3. Keep your list of "Remembered Networks" empty or at a minimum.  Your device can be fooled into giving out details of where it has tried to, or successfully connected to a Network Name (ESSID).  Statistics can paint quite the vivid picture if you know what you seek.

Advertising the ESSID of your great aunt Sally is not something to be desired, please excuse.  Keep Sally's business to Sally.

4. Know just how far your home network reaches.

Don't know?  Take your phone out, pick a random direction and keep walking; all the while looking for your home wireless.  When you cannot see it anymore, chalk out your 360, you have reached your bubble's end.

Reduce your power output if able.  Take a moment and login to that router of yours.  Go through the settings and see if there is a way to reduce the power output of the radio transmitter inside of it.  While maximum effect seems nice, it just may give Johnny across the way access to more than you bargained for.

Protect the very knowledge of your bubbles and change them up at random when you can.

Friends don't let friends keep ESSIDs for extended times.

5. Realize that there is no anonymity with Wireless or Bluetooth, to a point.  The best of softwares have bugs, people hunt those bugs.  Sometimes you keep your bug squishing techniques to yourself.  Sometimes you share.

The very backbone of how it works would snap in half if you tried to truly make yourself invisible to others.  Who would they talk to if not you?  Using Wireless or Bluetooth tells anyone within roughly 100 yards of your position, "I am here".

6. Build a piCopilot and learn just how all of this works.

Anyone can code.  Anyone in 2021 has the unique opportunity to learn how these common everyday protocols work.  Even if they'll never see it again, nor hear of it again; at least the seed was planted and maybe they'll remember.  The possibilities for modules like idrop and the like are endless and yet very well common; you just didn't know it.  You found this page didn't you?

7. Press the communities like Motorola, Apple, ABC, Google, etc; press them that your security and privacy matter.  The current model has none of that and it should rather be widespread and far-flung.  If your phone doesn't have a way to randomize your MAC, you should be asking why.  If you think your current randomization is good enough, boot up, run idrop and be surprised.
