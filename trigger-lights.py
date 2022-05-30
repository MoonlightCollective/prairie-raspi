#!/usr/bin/env python3
import serial
import time
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("prairie")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.payload == b"portal1 forward":
        sendArduino("forward\n")
    elif msg.payload == b"portal1 backward":
        sendArduino("backward\n")

def sendArduino(msg):
    print("sending to arduino: "+msg)
    ser.write(msg.encode('utf-8'))

client = mqtt.Client("rasp2")
client.username_pw_set("moonlight","collective")
client.on_connect = on_connect
client.on_message = on_message
client.connect(host="73.254.192.189",port=41799)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

while True:
  client.loop()
