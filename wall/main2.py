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

WIDTH = 300
HEIGHT = 400

ROWS = 6
COLS = 6

dim = Vector2( WIDTH / COLS , HEIGHT / ROWS  )

def double_wall ( coord1, coord2 ):
    """ make a double sided wall
    """

    # make two walls and then offset them in the direction of their normal
    wall1 = make_wall( coord1, coord2 )
    wall2 = make_wall( coord2, coord1 )

    wall1_offset = 2.5 * wall1.normal
    wall1.point1 = wall1.point1 + wall1_offset
    wall1.point2 = wall1.point2 + wall1_offset
    wall1.center_point += wall1_offset
    
    wall2_offset = 2.5 * wall2.normal
    wall2.point1 = wall2.point1 + wall2_offset
    wall2.point2 = wall2.point2 + wall2_offset
    wall2.center_point += wall2_offset    
    
    
    return  [wall1, wall2]

    

def make_wall( coord1, coord2 ):
    """give 2 coordinates as row, column and this function
        will return a wall at those coordinates
    """
    coord1 = Vector2(coord1)
    coord2 = Vector2(coord2)
    
    return Wall( (coord1.x * dim.x, coord1.y * dim.y),
                 (coord2.x * dim.x, coord2.y * dim.y)
                 )


## Start the pygame code
pg.init()
window = pg.display.set_mode( (WIDTH,HEIGHT), SRCALPHA | HWSURFACE)
clock = pg.time.Clock()


# create a world with no walls
world = World([])

# start adding walls to the world
world.walls.extend( double_wall((1,3),
                              (0,3)) )

##world.walls.append( make_wall((1,3),
##                              (0,3)) )

##world.walls.append( make_wall((0,3),
##                              (1,3))
##                              )


##world.walls.append( make_wall((1,1),
##                              (1,2)) )
##
##world.walls.append( make_wall((2,1),
##                              (1,1)) )
##
##world.walls.append( make_wall((3,0),
##                              (3,2)) )
##
##world.walls.append( make_wall((3,0),
##                              (3,2)) )
##
##world.walls.append( make_wall((3,2),
##                              (2,2)) )





##world.walls.append( Wall( (400,10), (400,100) ) )
##world.walls.append( Wall( (200,70), (300,50) ) )
##world.walls.append( Wall( (40,200), (80,200) ) )

##boid= Boid(world)
##boid.pos = (10,250)
##boid.vel = ( 100, 0)
##boid.turn_on(Behaviors.WALL_AVOIDANCE)

fill_color = pg.Color('yellow')
magic_spot = Vector2( int(0.75 * WIDTH), int(0.5 * HEIGHT) )

while True:
    window.fill(fill_color)

    for event in pg.event.get():
        if event.type == MOUSEBUTTONUP:
##            boid.seek_target = event.pos
            
            if magic_spot.distance_squared_to( event.pos ) < 50:
                fill_color =  pg.Color('red')
            else:
                fill_color = pg.Color('white')                

        if event.type == KEYUP:
            if event.key == K_s:
                print('you pressed s')
        
        if event.type == QUIT:
            pg.display.quit()
            pg.quit()
            sys.exit()


    for wall in world.walls:
        wall.draw(window,True)

    pg.draw.circle(window, pg.Color('purple'), (int(magic_spot.x), int(magic_spot.y)), 5)

##    if boid.pos.distance_to( finish_line ) < 5 :
        # set the fill_color to something...

        
##    boid.draw(window, clock.get_time() * .001)

    
    clock.tick(60)

    pg.display.update()
