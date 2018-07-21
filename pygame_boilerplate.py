import pygame as pg
from pygame.locals import *
from pygame.math import Vector2
from boid import Boid
import random
##from game_world import *

import sys
##import game_world as world

BOID_NUMBER = 20

pg.init()
window = pg.display.set_mode((500,500), SRCALPHA | HWSURFACE)
clock = pg.time.Clock()


# load some images of boids
##boid_orig_surface = pg.image.load('images/boid1_small.png').convert_alpha()
##boid_surface = pg.transform.rotozoom(boid_orig_surface, -45, 1.0)
##offset = Vector2(-boid_orig_surface.get_width() * 0.5,
##                 -boid_orig_surface.get_height() * 0.5)
##offset.rotate_ip(-45)


# load the target image
target = pg.image.load('images/target.png').convert_alpha()
target_pos = (250,250)


boids = []
for i in range(BOID_NUMBER):
    boid = Boid(color=random.choice(['red','blue','green','purple']))
    boid.pos = (random.randint(0, 500), random.randint(0,500))
    boid.max_speed = random.randint(100,100)
    boid.seek_target = target_pos
    boid.seek_on()

    boids.append(boid)

frame = 0
while True:
    window.fill(pg.Color('white'))

    for event in pg.event.get():
        if event.type == MOUSEBUTTONUP:
            target_pos = event.pos
            for b in boids:
                b.seek_target = target_pos
        
        if event.type == QUIT:
            pg.display.quit()
            pg.quit()
            sys.exit()

    # draw the target on the screen
    window.blit(target,target.get_rect(center=target_pos))

    # update and draw the agent on the screen
    for b in boids:
        b.update(clock.get_time() * .001)
        b.draw(window)

    
    clock.tick(60)

    pg.display.update()
