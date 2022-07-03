#!/usr/bin/env python3
import serial
import time
import paho.mqtt.client as mqtt
import automationhat
import sounddevice as sd
import soundfile as sf
import sys

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Portal")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def sendArduino(msg):
    print("sending to arduino: "+msg)
    ser.write(msg.encode('utf-8'))

data, sr = sf.read("TestAudio/transition.wav")
dataW, srW = sf.read("TestAudio/whispers3.wav")

client = mqtt.Client("rasp")
client.on_connect = on_connect
client.on_message = on_message
client.connect(host="192.168.0.202")

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.reset_input_buffer()

if automationhat.is_automation_hat():
    automationhat.light.power.write(1)

playcmd1 = 'aplay -D sysdefault:CARD=Headphones audio/transition.wav'
playcmd2 = 'aplay -D sysdefault:CARD=vc4hdmi audio/transition.wav'

# we have three states... CLEAR,FORWARD,BACKWARD
# 0 = the portal is empty, no one is walking
# 1 = someone has entered the portal going forward
# 2 = someone has entered the portal going backward

# when reading the inputs, 1 = no activity (pulled high by default); 0 = path is broken (triggered low)

state = 0
last = time.time()

sd.play(dataW, srW, loop=True)

while True:
    client.loop()

    if time.time() - last > 30:
      # send keep alive every 30 seconds
      last = time.time()
      client.publish ("Portal","Portal1-Alive")

    if state == 0:
      if automationhat.input[0].read() == 0:
        # someone is going forward
        print ("forward")
        sendArduino("forward\n")
        # subprocess.run ([playcmd1],shell=True) 
        # call ([playcmd2],shell=True)
        #client.publish ("Portal","Portal1-Enter") 
        client.publish ("Booth","DoorInitialOpen")
        sd.play(data,sr)
        state = 1
        time.sleep(0.5) # add a tiny delay to avoid retriggering too often
      #elif automationhat.input[1].read() == 0:
      #  client.publish ("prairie","portal1 backward") 
      #  print ("backward")
      #  state = 2  
      #  time.sleep(0.5) # add a tiny delay to avoid retriggering too often
      else:
        time.sleep(0.1)
    if state == 1 or state == 2:
      if automationhat.input[0].read() == 1:  # and automationhat.input[1].read() == 1:
        state = 0
      else:
        time.sleep(0.1)
