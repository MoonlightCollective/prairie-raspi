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
    mqtt_connection = True

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("booth")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def sendArduino(msg):
    print("sending to arduino: "+msg)
    ser.write(msg.encode('utf-8'))

#figure out whether we are an odd or even portal
host = socket.gethostname()
boothNum = int(host[-1:])  
print("running on booth "+ str(boothNum))

# Starting the mixer
mixer.init()
mixer.pre_init(44100, 16, 2, 4096)
  
# Loading the song
# mixer.music.load("audio/PortalWhispers.wav")

# Setting the volume
# mixer.music.set_volume(0.7)
  
# Start playing the song
# mixer.music.play(-1)

heartbeatSnd = pygame.mixer.Sound('audio/Booth/HbTestLoop.wav')


client = mqtt.Client(socket.gethostname())
client.on_connect = on_connect
client.on_message = on_message
mqtt_connection = False

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.reset_input_buffer()

#messages we might get from the arduino:


current_distance = 2000

def send_mqtt():
      tagsDict = { "host":socket.gethostname() }
      msgDict = { "name":"trigger", "fields":fieldDict, "tags":tagsDict, "timestamp":math.floor(time.time()) }
      json_object = json.dumps(msgDict)

      client.publish ("portal",json_object)


def distance_to_period(dist_centimeters):
  period_msecs = dist_centimeters * 3.3
  return period_msecs

last_heatbeat = time.time()

def beat_heart():
  if time.time() - last_heatbeat > distance_to_period(current_distance):
    last_heatbeat = time.time()
    heartbeatSnd.play();

last_keep_alive = time.time()

def keep_alive():
  if time.time() - last_keep_alive > 30:
  # send keep alive every 30 seconds
    last_keep_alive = time.time()

    if mqtt_connection is False:
      try:
        client.connect(host="192.168.0.202")
        client.loop_start()
      except Exception as e:
        print (e)

    fieldDict = { "sender":socket.gethostname() }
    tagsDict = { "host":socket.gethostname() }
    msgDict = { "name":"keep-alive", "fields":fieldDict, "tags":tagsDict, "timestamp":math.floor(time.time()) }
    json_object = json.dumps(msgDict)
    #client.publish ("booth",json_object) #temporarily disable keep-alive

while True:

  beat_heart()

  if ser.in_waiting > 0:
    line = ser.readline().decode('utf-8').rstrip()
    params = line.split(' ')
    print(params)

    if params[0]=="dist":

      current_distance = params[1]


  time.sleep(0.01)