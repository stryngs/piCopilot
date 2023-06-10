# Background
One day I came across a thread on the new [PMKID](https://hashcat.net/forum/thread-7717.html) attack.  I wanted to shorten the steps needed to obtain the data to run [hashcat](https://hashcat.net/hashcat/) and built this tool.

# Gist
pmkid2hashcat does not inject if the outcome is already known.  Once you have a captured string that is the input for hashcat, there is no sense in making duplicates, nor interacting with the same ESSID again.  This simplicity also means that if you miss a PMKID due to something such as perhaps a channel switch; pmkid2hashcat will not retry.

pmkid2hashcat does not control or care about channel hopping.  An easy way to hop channels without too much work is simply utilizing airodump-ng at the same time.  Let airodump-ng control the hops and pmkid2hashcat prepare the hashes for hashcat intake without having to do a conversion that a tool like hcxdumptool requires.

The simplistic nature of pmkid2hashcat is by design.  Be seen the least amount of times as possible.

hashes.file is for hashcat, hashes.log is for humans.  Both logs are appended to and never overwritten.

# How-to
Spin up a Python3 virtual env and then:
```
git clone https://github.com/stryngs/packetEssentials
git clone https://github.com/stryngs/easy-thread
git clone https://github.com/stryngs/quickset

python3 -m pip install packetEssentials/RESOURCEs/*.tar.gz
python3 -m pip install easy-thread/*.tar.gz
python3 -m pip install quickset/lib/SRC/quickset*
```

Create the input for hashcat:
```
python3 ./pmkid2hashcat.py -i <Monitor Mode NIC>
```

Run hashcat:
```
hashcat -m 22000 hashes.file <wordlist>
```
