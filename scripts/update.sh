#!/bin/bash


echo Stopping prairie service...
sudo systemctl stop prairie


echo Updating...
cd ~/prairie-raspi
git checkout .
git pull

if [[ "$HOSTNAME" == *"portal"* ]]; then
    echo "Updating portal arduino"
    arduino-cli compile --fqbn adafruit:samd:adafruit_feather_m4 portal.ino
    arduino-cli upload -p /dev/ttyACM0 --fqbn adafruit:samd:adafruit_feather_m4 portal.ino
sudo systemctl start prairie
    /home/moonlight/prairie-raspi/portal.py
fi
if [[ "$HOSTNAME" == *"booth"* ]]; then
    echo "Updating booth arduino"
    arduino-cli compile --fqbn arduino:avr:nano booth.ino
    arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:nano booth.ino
   /home/moonlight/prairie-raspi/booth.py
fi
