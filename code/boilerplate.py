# Pygame Boilerplate Code

import pygame, sys
# constant variables MOUSEMOTION, KEYUP, QUIT
from pygame.locals import *

WHITE = (255,255,255)
BLACK = (0,0,0)

def main():
    global DISPLAYSURF

    pygame.init()    

    DISPLAYSURF = pygame.display.set_mode((1200,800))
    pygame.display.set_caption("Programming AI")


    # load background for the game
    bgImg = pygame.image.load("../assets/pitch_1200.jpeg")
    
    while True:
        DISPLAYSURF.fill( WHITE )
        
        checkForQuit()

        #draw background
        DISPLAYSURF.blit(bgImg, (0,0) )

        # handle events
        for event in pygame.event.get():
            print(event.type)

        pygame.display.update()        


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
        
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)                

def terminate():
    pygame.quit()
    sys.exit()
    
if __name__ == '__main__':
    main()
