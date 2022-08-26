#!/usr/bin/env python3
import pygame
from pygame import mixer
import serial
import time
import paho.mqtt.client as mqtt
import sys
import json
import socket
import time
import math

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("portal")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def sendArduino(msg):
    print("sending to arduino: "+msg)
    ser.write(msg.encode('utf-8'))

# Starting the mixer
mixer.init()
mixer.pre_init(44100, 16, 2, 4096)
  
# Loading the song
# mixer.music.load("audio/PortalWhispers.wav")

# Setting the volume
# mixer.music.set_volume(0.7)
  
# Start playing the song
# mixer.music.play(-1)

enterSnd = pygame.mixer.Sound('audio/Portal/PortalEnter.wav')
exitSnd = pygame.mixer.Sound('audio/Portal/PortalExit.wav')
whisperSnd = pygame.mixer.Sound('audio/PortalWhispers.wav')

#start the sound loop
whisperSnd.play(-1)

client = mqtt.Client(socket.gethostname())
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
      fieldDict = { "sender":socket.gethostname() }
      tagsDict = { "host":socket.gethostname() }
      msgDict = { "name":"keep-alive", "fields":fieldDict, "tags":tagsDict, "timestamp":math.floor(time.time()) }
      json_object = json.dumps(msgDict)
      client.publish ("portal",json_object)

    if ser.in_waiting > 0:
      line = ser.readline().decode('utf-8').rstrip()
      print(line)

      if line=="enter":
        enterSnd.play(0);
        fieldDict = { "sender":socket.gethostname(), "direction":"forward" }
        tagsDict = { "host":socket.gethostname() }
        msgDict = { "name":"trigger", "fields":fieldDict, "tags":tagsDict, "timestamp":math.floor(time.time()) }
        json_object = json.dumps(msgDict)
        client.publish ("portal",json_object)

      if line=="exit":
        exitSnd.play(0);
        fieldDict = { "sender":socket.gethostname(), "direction":"backward" }
        tagsDict = { "host":socket.gethostname() }
        msgDict = { "name":"trigger", "fields":fieldDict, "tags":tagsDict, "timestamp":math.floor(time.time()) }
        json_object = json.dumps(msgDict)
        client.publish ("portal",json_object)
    
    time.sleep(0.1)