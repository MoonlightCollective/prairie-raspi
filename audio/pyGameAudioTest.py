import pygame
from pygame import mixer
  
# Starting the mixer
mixer.init()
  
# Loading the song
mixer.music.load("HbTestLoop.wav")

# Setting the volume
mixer.music.set_volume(0.7)
  
# Start playing the song


hbSnd = pygame.mixer.Sound('HbTestLoop.wav')
portalSnd = pygame.mixer.Sound('Portal7.wav')
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
        # Stop the mixer
        mixer.music.stop()
        break