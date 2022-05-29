#!/usr/bin/env python3

import time
import paho.mqtt.client as mqtt
import automationhat

client =mqtt.Client("rasp1")
client.username_pw_set("moonlight","collective")
client.connect(host="73.254.192.189",port=41799)

if automationhat.is_automation_hat():
    automationhat.light.power.write(1)

# we have three states... CLEAR,FORWARD,BACKWARD
# 0 = the portal is empty, no one is walking
# 1 = someone has entered the portal going forward
# 2 = someone has entered the portal going backward

# when reading the inputs, 1 = no activity (pulled high by default); 0 = path is broken (triggered low)

state = 0
last = time.time()

while True:
    if time.time() - last > 30:
      # send keep alive every 30 seconds
      last = time.time()
      client.publish ("prairie","portal1 alive")

    if state == 0:
      if automationhat.input[0].read() == 0:
        # someone is going forward
        client.publish ("prairie","portal1 forward") 
        print ("forward")
        state = 1
        time.sleep(0.5) # add a tiny delay to avoid retriggering too often
      elif automationhat.input[1].read() == 0:
        client.publish ("prairie","portal1 backward") 
        print ("backward")
        state = 2  
        time.sleep(0.5) # add a tiny delay to avoid retriggering too often
      else:
        time.sleep(0.1)
    if state == 1 or state == 2:
      if automationhat.input[0].read() == 1 and automationhat.input[1].read() == 1:
        state = 0
      else:
        time.sleep(0.1)
