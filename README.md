# This folder contains all the files needed on the Raspberry PI devices 
These files assume a certain set of dependencies.
To set up a new Raspberry PI device for use in our installation:


For a moonlight collective installation, start with a pi setup using the imaging instructions in google drive to pre-set username, password, hostname, and wifi settings
```
sudo apt install git
git clone https://github.com/MoonlightCollective/prairie-raspi
cd prairie-raspi/scripts
./setup-pi.sh
```
Customize hostname for target portal or booth: 
```
sudo raspi-config
```
Customize IP address:
```
sudo nano /etc/dhcpcd.conf
```

Compiling and updating arduino sketches to feather m4 example:
```
sudo systemctl stop prairie
arduino-cli compile --fqbn adafruit:samd:adafruit_feather_m4 palette-noise-with-interrupts
arduino-cli board list
arduino-cli upload -p /dev/ttyACM0 --fqbn adafruit:samd:adafruit_feather_m4 palette-noise-with-interrupts
sudo systemctl start prairie
```

Some audio targets are set using symlinks, update the link target using `ln -sf`
```
ln -sf path/to/target.wav PortalExit.wav
```
