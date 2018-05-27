#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root"
	exit
fi

declare -a toRemove=(
'idle*'
'scratch'
'minecraft*'
##'plank'
'simple-scan'
'youtube*'
'hexchat'
'*underbir*'
'transmission*'
'pidgin'
'libreoffice'
'atril*'
'sonic-pi'
##'sense_*'
'vlc'
)

for i in "${toRemove[@]}"; do
 apt-get -y purge --auto-remove $i
done


echo mkdir ~/Phoyo
echo cd ~/Phoyo
echo wget -P ~/Phoyo https://www.phoyosystem.com/custom/binaries/phoyo-id-crossPlatform.zip
echo unzip ~/Phoyo/phoyo-id-crossPlatform.zip -d ./
echo rm phoyo-id-crossPlatform.zip
echo cd $(ls | grep phoyo)

