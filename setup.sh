#!/bin/bash

##check for privileges
if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root"
	exit
fi

##create array with apps to remove
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

##remove apps in array -> debloating
for i in "${toRemove[@]}"; do
 apt-get -y purge --auto-remove $i
done

##needed packages for printer driver 
sudo apt install gcc libtool libssl-dev libc-dev \
libjpeg-turbo8-dev libpng12-dev libtiff5-dev cups

##install printer driver
mkdir ~/gutenprint
wget -P ~/gutenprint https://sourceforge.net/projects/gimp-print/files/gutenprint-5.2/5.2.14/gutenprint-5.2.14.tar.bz2
tar xjvf gutenprint-5.2.14.tar.bz2 -C ~/gutenprint
~/gutenprint/configure
cd ~/gutenprint
make clean
make
sudo make install

#download and extract photobooth software
echo mkdir ~/PhoyoLinux
echo cd ~/PhoyoLinux
echo wget -P ~/PhoyoLinux https://www.phoyosystem.com/custom/binaries/PhoyoLinux.tar.gz
echo tar xfz PhoyoLinux.tar.gz -C ~/PhoyoLinux
echo rm PhoyoLinux.tar.gz
echo ./PhoyoLinux
