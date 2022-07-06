# This folder contains all the files needed on the Raspberry PI devices 
These files assume a certain set of dependencies.
To set up a new Raspberry PI device for use in our installation:
```
sudo apt install -y mosquitto mosquitto-clients
pip3 install paho-mqtt
curl https://get.pimoroni.com/automationhat | bash
```

Also make sure the Raspberry pi has i2c interface enabled. To enable run `raspi-config` and enable interfaces/i2c.

To install the arduino tools:
- arduino-cli is included the prairi-raspi/bin folder
- just add "export PATH=$PATH:/home/moonlight/prairie-raspi/bin" to the .bashrc file


