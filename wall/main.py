import pygame as pg
from pygame.locals import *
from pygame.math import Vector2
from boid import Boid, Behaviors
import random
from world import World
from wall import Wall

##from game_world import *

import sys
##import game_world as world

WIDTH = 500
HEIGHT = 500

pg.init()
window = pg.display.set_mode( (WIDTH,HEIGHT), SRCALPHA | HWSURFACE)
clock = pg.time.Clock()

world = World([])

w  = Wall( ( 0.85 * WIDTH, 0.10 * HEIGHT ),
           (0.85 * WIDTH, 0.90 * HEIGHT) )

world.walls.append( w )

##world.walls.append( Wall( (400,10), (400,100) ) )
##world.walls.append( Wall( (200,70), (300,50) ) )
##world.walls.append( Wall( (40,200), (80,200) ) )

boid= Boid(world)
boid.pos = (10,250)
boid.vel = ( 100, 0)
boid.turn_on(Behaviors.WALL_AVOIDANCE)
# load some images of boids
##boid_orig_surface = pg.image.load('images/boid1_small.png').convert_alpha()
##boid_surface = pg.transform.rotozoom(boid_orig_surface, -45, 1.0)
##offset = Vector2(-boid_orig_surface.get_width() * 0.5,
##                 -boid_orig_surface.get_height() * 0.5)
##offset.rotate_ip(-45)


# load the target image
##target = pg.image.load('images/target.png').convert_alpha()
##target_pos = (250,250)


##boids = []
##for i in range(BOID_NUMBER):
##    boid = Boid(color=random.choice(['red','blue','green','purple']))
##    boid.pos = (random.randint(0, 500), random.randint(0,500))
##    boid.max_speed = random.randint(100,100)
##    boid.seek_target = target_pos
##    boid.seek_on()
##
##    boids.append(boid)

##frame = 0
while True:
    window.fill(pg.Color('white'))

    for event in pg.event.get():
        if event.type == MOUSEBUTTONUP:
##            target_pos = event.pos
##            for b in boids:
##                b.seek_target = target_pos
            print(event.pos)
            boid.seek_target = event.pos

        if event.type == KEYUP:
            if event.key == K_s:
                print('you pressed s')
        
        if event.type == QUIT:
            pg.display.quit()
            pg.quit()
            sys.exit()

    # draw the target on the screen
##    window.blit(target,target.get_rect(center=target_pos))

    # update and draw the agent on the screen
##    for b in boids:
##        boid.update(clock.get_time() * .001)

    for wall in world.walls:
        wall.draw(window,True)
        
    boid.draw(window, clock.get_time() * .001)

    
    clock.tick(60)

    pg.display.update()
