#!/usr/bin/env python3
import serial
import time
import paho.mqtt.client as mqtt
import sounddevice as sd
import soundfile as sf
import sys
import json
import socket

# The callback for when the client receives a CONNACK response from the server.
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
dataEnter, srEnter = sf.read("audio/Portal/PortalEnter.wav")
dataExit, srExit = sf.read("audio/Portal/PortalExit.wav")

client = mqtt.Client("rasp")
client.on_connect = on_connect
client.on_message = on_message
try:
  client.connect(host="192.168.0.202")
  client.loop_start()
except Exception as e:
  print (e)
  pass

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.reset_input_buffer()

#messages we might get from the arduino:
# "enter" = person walks through portal going forward
# "exit" = person walks through the other direction

last = time.time()

while True:
    if time.time() - last > 30:
      # send keep alive every 30 seconds
      last = time.time()
      data = {}
      data['name'] = 'keep-alive'
      data['timestamp'] = time.time()
      data['host'] = socket.gethostname()
      client.publish ("Portal",json.dumps(data))

    if ser.in_waiting > 0:
      line = ser.readline().decode('utf-8').rstrip()
      print(line)

      if line=="enter":
        sd.play(dataEnter,srEnter)
        data = {}
        data['name'] = 'trigger'
        data['timestamp'] = time.time()
        data['host'] = socket.gethostname()
        data['direction'] = 'forward'
        client.publish ("Portal",json.dumps(data))

      if line=="exit":
        sd.play(dataExit,srExit)
        data = {}
        data['name'] = 'trigger'
        data['timestamp'] = time.time()
        data['host'] = socket.gethostname()
        data['direction'] = 'backward'
        client.publish ("Portal",json.dumps(data))
    
    time.sleep(0.1)