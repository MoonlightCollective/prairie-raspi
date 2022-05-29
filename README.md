# This folder contains all the files needed on the Raspberry PI devices 
These files assume a certain set of dependencies.
To set up a new Raspberry PI device for use in our installation:
```
sudo apt install -y mosquitto mosquitto-clients
pip3 install paho-mqtt
curl https://get.pimoroni.com/automationhat | bash
```

Also make sure the Raspberry pi has i2c interface enabled. To enable run `raspi-config` and enable interfaces/i2c.
