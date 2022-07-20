#!/bin/bash

cd ~/prairie-raspi
pwd


#echo Updating...
#git checkout .
#git pull

if [[ "$HOSTNAME" == *"portal"* ]]; then
    echo "Running portal script"
    ./portal.py
fi
