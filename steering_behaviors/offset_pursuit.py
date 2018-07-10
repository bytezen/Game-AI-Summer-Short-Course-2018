from common.path import Path
from common.actors import Vehicle
import common.actors as Actors
from common.behavior import Behavior
import common.params as Params
from common.world import GameWorld

from pygame.math import Vector2


import pgzrun


TITLE = 'Steering Behavior - Offset Pursuit'    
WIDTH = 800
HEIGHT = 600


MASS = 1.0
MAX_SPEED = 100 # pixels / second
MAX_FORCE = 200 # pixels / second^2
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
                  color='purple')

follower = Vehicle(world=world, \
                  center=(WIDTH*0.5,HEIGHT*0.15), \
                  mass=MASS, \
                  max_speed=MAX_SPEED, \
                  max_force=MAX_FORCE, \
                  max_turn_rate=MAX_TURN_RATE, \
                  vel= INIT_VEL)


def start():    
    follower.offset_pursuit_on();
    leader.wander_on()
    follower.leader = leader    
    world.add_agent(follower,leader)

    world.display_flags_off()
    world.view_keys = True
    world.show_steering_force = True


def update(dt):
    world.update(dt)


def draw():
    screen.clear()
    world.draw(screen.surface)

def on_key_down(key):
    pass

def on_key_up(key):
    pass

def on_mouse_down(pos):
    pass


start()
pgzrun.go()

        
