#!/bin/bash
#add telegraf source
wget -q https://repos.influxdata.com/influxdb.key
echo '23a1c8836f0afc5ed24e0486339d7cc8f6790b83886c4c96995b88a061c5bb5d influxdb.key' | sha256sum -c && cat influxdb.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdb.gpg > /dev/null
echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdb.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list
rm influxdb.key

#install packages
sudo apt update
sudo apt upgrade -y
sudo apt install -y mosquitto-clients libasound-dev python3 libportaudio2 libsndfile1 python3-numpy libfl2 telegraf python3-pip screen
sudo pip install sounddevice pyserial paho-mqtt soundfile

#install arduino cli
cd ~
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
echo "export PATH=\$PATH:/home/moonlight/bin">> ~/.bashrc
~/bin/arduino-cli config init
sed -i -e "s/additional_urls: \[\]/additional_urls: \n    \[https:\/\/adafruit.github.io\/arduino-board-index\/package_adafruit_index.json\]/g" ~/.arduino15/arduino-cli.yaml
~/bin/arduino-cli core update-index
~/bin/arduino-cli core install adafruit:samd
~/bin/arduino-cli core install arduino:avr
~/bin/arduino-cli lib install FastLED

#enable serial terminal
echo "enable_uart=1" | sudo tee -a /boot/config.txt

#install prairie service
sudo cp /home/moonlight/prairie-raspi/scripts/prairie.service /etc/systemd/system
sudo systemctl enable prairie
sudo systemctl start prairie 
