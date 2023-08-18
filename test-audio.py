#!/usr/bin/env python3
import pygame
from pygame import mixer

# Starting the mixer
mixer.init()

# Loading the song
#mixer.music.load("HbTestLoop.wav")
mixer.music.load("audio/Portal/PortalWhispers-Set1Only.wav")

# Setting the volume
mixer.music.set_volume(0.7)

# Start playing the song


hbSnd = pygame.mixer.Sound('audio/Portal/PortalWhispers-Set1Only.wav')
portalSnd = pygame.mixer.Sound('audio/Portal/PortalEnter.wav')
hbchan = hbSnd.play(-1);


# infinite loop
while True:
    print("press 'p' to play portal sound")
    print("press '0' to set heartbeat to half volume, press '1' to set to heartbeat to full volume")
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