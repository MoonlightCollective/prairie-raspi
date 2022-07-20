#!/bin/bash

cd ~/prairie-raspi
pwd


#echo Updating...
#git checkout .
#git pull

if [[ "$HOSTNAME" == *"portal"* ]]; then
    echo "Running portal script"
    /home/moonlight/prairie-raspi/portal.py
fi
if [[ "$HOSTNAME" == *"booth"* ]]; then
    echo "Running booth script"
    /home/moonlight/prairie-raspi/booth.py
fi
