from common.path import Path
from common.actors import Vehicle
import common.actors as Actors
from common.behavior import Behavior
import common.params as Params
from common.world import GameWorld

from pygame.math import Vector2
import random

import pgzrun


TITLE = 'Steering Behavior - Flocking'    
WIDTH = 800
HEIGHT = 600


MASS = 1.0
MAX_SPEED = 100 # pixels / second
MAX_FORCE = 1000 # pixels / second^2
MAX_TURN_RATE = 100 # degrees / second
INIT_VEL = Vector2(100,0)


world = GameWorld(WIDTH,HEIGHT)


# main Vehicle
leader = Vehicle(world=world, \
                  center=(WIDTH*0.5,HEIGHT*0.5), \
                  mass=MASS, \
                  max_speed=MAX_SPEED, \
                  max_force=MAX_FORCE, \
                  max_turn_rate=MAX_TURN_RATE, \
                  vel= 0.5 * INIT_VEL,
                  color='red')

flock = []
for i in range(10):
    vel = Vector2(1,)
    vel.rotate_ip(random.randint(0,359))
    vel *= random.randint(20,30)
    
    v = Vehicle(world=world, \
                  center=(WIDTH*0.5 + random.randint(-30,30), HEIGHT*0.6), \
                  mass=MASS, \
                  max_speed=MAX_SPEED, \
                  max_force=MAX_FORCE, \
                  max_turn_rate=MAX_TURN_RATE, \
                  vel= 0.5 * INIT_VEL,
                  color = random.choice(['blue','green','purple']))
    

    flock.append(v)


def start():
    world.add_agent(leader)

    for i in flock:
        i.wander_on()
        world.add_agent(i)

    for i in world.agents:
        i.separation_on()
##        i.wander_on()

    #make sure everything is off to begin so that we can customize
    world.display_flags_off()
    
    world.view_keys = True
    world.show_steering_force = True
    world.show_wander_circle = False


def update(dt):
    world.update(dt)


def draw():
    screen.clear()
    world.draw(screen)

def on_key_down(key):
    pass

def on_key_up(key):
    pass

def on_mouse_down(pos):
    pass


start()
pgzrun.go()

        
