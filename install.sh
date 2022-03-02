#! /bin/bash

#
# install.sh 
#
# Install script for downloading and installing the vivpi system and associated services
#

# Variables
installLocation="/etc/vivpi"

# Initialisation
echo ""
echo " =================="
echo " Vivpi Installation"
echo " =================="
echo ""

if [ $(id -u) -ne 0 ]
  then echo "! Please run as root to ensure install completes correctly!"
  exit
fi

# Check if script is downloaded or is curled into sh
tempDir=$(mktemp -d)
localDir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
if [ -f "$localDir/test.sh" ]
then
  cp -r $localDir $tempDir
 else 
  git clone --depth 1 https://github.com/Chalmrah/vivpi.git $tempDir
fi

origDir=$(pwd)
cd "$tempDir"

if [ readlink -e $installLocation ] && [ systemctl is-active --quiet vivpi.timer ]
then
  echo "> First time install"
  echo "> Prerequisites"
  apt install python3 python3-pip python-dev -y
  pip3 install -y -r $tempDir/requirements.txt
  mkdir $installLocation
else
  echo "> Upgrade mode"
fi

echo "> Copying files"
cp -ur vivpi/ $installLocation

echo "> Installing services"
for service in `ls -d $tempDir/services/*`; do
  sed -i "s#install_Location#${installLocation}#g" $service
  cp -u $service /etc/systemd/system/
  serviceName=$(basename $service)
  systemctl enable /etc/systemd/system/$serviceName
done

echo "> Reloading systemctl"
systemctl daemon-reload

cd "$origDir"

echo "> Cleaning up temp directory"
rm -r $tempDir

echo ""
echo " ======================"
echo " Installation Complete!"
echo " ======================"