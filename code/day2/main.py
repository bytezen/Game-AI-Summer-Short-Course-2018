import sys
import light_statemachine as State
from light_statemachine import Light

import pygame as pg
from pygame import Color
from pygame.constants import HWSURFACE, SRCALPHA

# create a light
light = Light()


#create states for the light

off = State.Off(light)
low = State.Low(light)
medlow = State.MedLow(light)
med = State.Med(light)
medhi = State.MedHi(light)
hi = State.Hi(light)
blown = State.Blown(light)


# set-up pygame

pg.init()
screen = pg.display.set_mode((200,200),HWSURFACE | SRCALPHA)
CLOCK = pg.time.Clock()
FPS = 30


def terminate():
    """closes pygame and the pygame window

    Args:
        None
    Returns:
        Nothing

    """
    pg.display.quit()
    pg.quit()
    sys.exit(0)



#the game loop; keep looping and listening for events until we quit
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            terminate()
        if event.type == pg.KEYDOWN:
                
            # turn the lights up 'UP ARROW'
            if event.key == pg.K_UP:
                light.brighten()

            # turn the light down 'DOWN ARROW'
            if event.key == pg.K_DOWN:
                light.dim()

            # change the light 'c'
            if event.key == pg.K_c:
                light.change_bulb()

            #quit
            if event.key == pg.K_q and \
                    event.mod & (pg.KMOD_CTRL | pg.KMOD_META):
                terminate()            
                
                

    screen.fill(Color('white'))    
    light.update(screen)
    
    
    pg.display.flip()
    CLOCK.tick(60)
                                 


