#!/bin/bash


echo Stopping prairie service...
sudo systemctl stop prairie


echo Updating...
cd ~/prairie-raspi
git checkout .
git pull


cd ~/prairie-raspi/arduino

if [[ "$HOSTNAME" == "portal1" ]]; then
    if git diff-index --name-only HEAD | grep -e 'portal1.ino' -e `readlink portal1.ino`; then
        echo "Updating portal 1 arduino"
        arduino-cli compile --fqbn adafruit:samd:adafruit_feather_m4 portal1.ino
        arduino-cli upload -p /dev/ttyACM0 --fqbn adafruit:samd:adafruit_feather_m4 portal1.ino
    fi
fi
if [[ "$HOSTNAME" == "portal2" ]]; then
    if git diff-index --name-only HEAD | grep -e 'portal2.ino' -e `readlink portal2.ino`; then
        echo "Updating portal 2 arduino"
        arduino-cli compile --fqbn adafruit:samd:adafruit_feather_m4 portal2.ino
        arduino-cli upload -p /dev/ttyACM0 --fqbn adafruit:samd:adafruit_feather_m4 portal2.ino
    fi
fi
if [[ "$HOSTNAME" == "portal3" ]]; then
    if git diff-index --name-only HEAD | grep -e 'portal3.ino' -e `readlink portal3.ino`; then
        echo "Updating portal 3 arduino"
        arduino-cli compile --fqbn aadafruit:samd:adafruit_itsybitsy_m4  portal3.ino
        arduino-cli upload -p /dev/ttyACM0 --fqbn adafruit:samd:adafruit_itsybitsy_m4  portal3.ino
    fi
fi
if [[ "$HOSTNAME" == "portal4" ]]; then
    if git diff-index --name-only HEAD | grep -e 'portal4.ino' -e `readlink portal4.ino`; then
        echo "Updating portal 4 arduino"
        arduino-cli compile --fqbn adafruit:samd:adafruit_feather_m4 portal4.ino
        arduino-cli upload -p /dev/ttyACM0 --fqbn adafruit:samd:adafruit_feather_m4 portal4.ino
    fi
fi

if [[ "$HOSTNAME" == "booth1" ]]; then
    if git diff-index --name-only HEAD | grep -e 'booth1.ino' -e `readlink booth1.ino`; then
        echo "Updating booth 1 arduino"
        arduino-cli compile --fqbn arduino:avr:nano booth1.ino
        arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:nano booth1.ino
    fi
fi
if [[ "$HOSTNAME" == "booth2" ]]; then
    if git diff-index --name-only HEAD | grep -e 'booth2.ino' -e `readlink booth2.ino`; then
        echo "Updating booth 2 arduino"
        arduino-cli compile --fqbn arduino:avr:nano booth2.ino
        arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:nano booth2.ino
    fi
fi

echo Starting prairie service...
sudo systemctl start prairie
