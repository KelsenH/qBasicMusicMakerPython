import sys, pygame, pygame.midi
 
 # set up pygame
pygame.init()
pygame.midi.init()
 
 # list all midi devices
for x in range( 0, pygame.midi.get_count() ):
    print (pygame.midi.get_device_info(x))

inp = pygame.midi.Input(0)
 
 # run the event loop
while True:
    if inp.poll():
        print (inp.read(1000))
        pygame.time.wait(10)
