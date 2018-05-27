#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root"
	exit
fi

declare -a toRemove=(
'idle*'
'scratch'
'minecraft*'
'simple-scan'
'youtube*'
'hexchat'
'*underbir*'
'transmission*'
'pidgin'
'libreoffice'
'atril*'
'sonic-pi'
'vlc'
)

for i in "${toRemove[@]}"; do
 apt-get -y purge --auto-remove $i
done

##needed for printer driver 
sudo apt install gcc libtool libssl-dev libc-dev \
libjpeg-turbo8-dev libpng12-dev libtiff5-dev cups


echo mkdir ~/PhoyoLinux
echo cd ~/PhoyoLinux
echo wget -P ~/PhoyoLinux https://www.phoyosystem.com/custom/binaries/PhoyoLinux.tar.gz
echo tar xfz PhoyoLinux.tar.gz -C ~/PhoyoLinux
echo rm PhoyoLinux.tar.gz
echo ./PhoyoLinux
