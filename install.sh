#! /bin/bash

#
# install.sh 
#
# Install script for downloading and installing the vivpi system and associated services
#

# Variables
installLocation="/etc/vivpi"

# Initialisation
echo -e ""
echo -e "Vivpi Installation"
echo -e ""

if [ "$EUID" -ne 0 ]
  then echo "! Please run as root to ensure install completes correctly!"
  exit
fi

# Check if script is downloaded or is curled into sh
localDir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

if 

# Download git to temp location
tempDir=$(mktemp -d)
git clone --depth 1 https://github.com/Chalmrah/vivpi.git $tempDir

origDir=$(pwd)
cd "$tempDir"

if [ readlink -e $installLocation ] && [ systemctl is-active --quiet vivpi.timer ]
then
  echo -e "> First time install"
  echo -e ">  Prerequisites"
  apt install python3 python3-pip python-dev -y
  pip3 install -y -r $tempDir/requirements.txt
  mkdir $installLocation
else
  echo -e "> Upgrade mode"
fi

echo -e ">  Copying files"
cp -ur vivpi/ $installLocation

echo -e ">  Installing services"
for service in `ls -d $tempDir/services/*`; do
  sed -i "s#install_Location#${installLocation}#g" $service
  cp -u $service /etc/systemd/system/
  systemctl enable /etc/systemd/system/$service
done

echo -e "Reloading systemctl"4
systemctl daemon-reload

cd "$origDir"