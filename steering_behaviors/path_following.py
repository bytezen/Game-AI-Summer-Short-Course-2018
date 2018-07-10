from common.path import Path
from common.actors import Vehicle
import common.actors as Actors
from common.behavior import Behavior
import common.params as Params
from common.world import GameWorld


import pgzrun


TITLE = 'Steering Behavior - Path Following'    
WIDTH = 800
HEIGHT = 600


MASS = 1.0
MAX_SPEED = 100 # pixels / second
MAX_FORCE = 200 # pixels / second^2
MAX_TURN_RATE = 100 # degrees / second
INIT_VEL = (100,0)


world = GameWorld(WIDTH,HEIGHT)


# main Vehicle
vehicle = Vehicle(world=world, \
                  center=(WIDTH*0.5,HEIGHT*0.5), \
                  mass=MASS, \
                  max_speed=MAX_SPEED, \
                  max_force=MAX_FORCE, \
                  max_turn_rate=MAX_TURN_RATE, \
                  vel= INIT_VEL)


def start():
    world.add_agent(vehicle)

    vehicle.path = Path.create_random_path(10,(20,20),(760,500))
    vehicle.path_follow_on(); 
    
    world.display_flags_off()
    world.view_keys = True
    world.show_steering_force = True
    world.show_path = True


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

        
