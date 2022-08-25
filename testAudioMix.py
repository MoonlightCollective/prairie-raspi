#!/usr/bin/env python3
import pygame
from pygame import mixer
  
# Starting the mixer
mixer.init()
  
# Loading the song
mixer.music.load("TestAudio/PortalWhispers.wav")

# Setting the volume
mixer.music.set_volume(0.7)
  
# Start playing the song
mixer.music.play(-1)

portalSnd = pygame.mixer.Sound('audio/Portal/PortalEnter.wav')
  
# infinite loop
while True:
    print("press 'p' to play portal sound")
    print("Press 'e' to exit the program")
    query = input("  ")
    if query == '1':
        hbSnd.set_volume(1.0)
    elif query == '0':
        hbSnd.set_volume(0.5)
    elif query == 'p':
        portalSnd.set_volume(0.6)
        portalSnd.play(0);
    elif query == 'e':
        mixer.music.stop()
        break