#!/bin/bash

declare -a toRemove=(
'idle*'
'py*'
'scratch'
'minecraft*'
'plank'
'simple-scan'
'youtube*'
'hexchat'
'*underbir*'
'transmission*'
'pidgin'
'libreoffice'
'atril*'
'sonic-pi'
'sense_*'
'vlc'
)

for i in "${toRemove[@]}"; do
 apt-get -y remove --purge $i
done

 apt-get -y autoremove
 apt-get -y install python3

echo mkdir ~/Phoyo
echo cd ~/Phoyo
echo wget -P ~/Phoyo https://www.phoyosystem.com/custom/binaries/phoyo-id-crossPlatform.zip
echo unzip ~/Phoyo/phoyo-id-crossPlatform.zip -d ./
echo rm phoyo-id-crossPlatform.zip
echo cd $(ls | grep phoyo)

