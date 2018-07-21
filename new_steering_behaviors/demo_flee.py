import pygame as pg
from pygame.locals import *
from boid import Boid
from game_world import GameWorld

import random
import sys


pg.init()
window = pg.display.set_mode((500,500), SRCALPHA | HWSURFACE)
clock = pg.time.Clock()


# load the target image
target = pg.image.load('images/target.png').convert_alpha()
target_pos = (250,250)

BOID_NUMBER = 20
boids = []
for i in range(BOID_NUMBER):
    boid = Boid(GameWorld(500,500), color=random.choice(['red','blue','green','purple']))
    boid.pos = (random.randint(200, 400), random.randint(200,400))
    boid.max_speed = random.randint(40,80)
    boid.flee_target = target_pos
    boid.flee_on()

    boids.append(boid)

frame = 0
while True:
    window.fill(pg.Color('white'))

    for event in pg.event.get():
        if event.type == MOUSEBUTTONUP:
            target_pos = event.pos
            for b in boids:
                b.flee_target = target_pos
        
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
