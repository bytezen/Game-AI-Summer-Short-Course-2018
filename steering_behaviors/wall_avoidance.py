from common.actors import Vehicle, Crosshair, Obstacle
import common.actors as Actors
from common.behavior import Behavior
import common.params as Params
from common.world import GameWorld


import pgzrun


TITLE = 'Steering Behavior - Obstacle Avoidance'    
WIDTH = 800
HEIGHT = 600

MASS = 1.0
MAX_SPEED = 100 # pixels / second
MAX_FORCE = 200 # pixels / second^2
MAX_TURN_RATE = 50 # degrees / second
INIT_VEL = (100,0)
BEHAVIOR = Behavior.NONE
        

world = GameWorld(WIDTH,HEIGHT)


# main Vehicle
vehicle = Vehicle(world=world, \
                  center=(WIDTH*0.05,HEIGHT*0.5), \
                  mass=MASS, \
                  max_speed=MAX_SPEED, \
                  max_force=MAX_FORCE, \
                  max_turn_rate=MAX_TURN_RATE, \
                  vel=INIT_VEL)


#evade in this case
vehicle.toggle_behavior(BEHAVIOR)


def start():
    world.add_agent(vehicle)

    world.show_walls = True
    vehicle.wall_avoidance_on()
    world.show_feelers = True
    world.create_walls()
    


def update(dt):
    world.update(dt)
##    for a in world.agents:
##        a.update(dt)



def draw():
    screen.clear()
    world.draw(screen.surface)

def on_key_down(key):
    pass

def on_key_up(key):

##    if key == keys.B:
##        world.toggle_behavior()

    #show Crosshair shortcut 'C'        
    if key == keys.C:
        world.show_crosshair = not world.show_crosshair

    #obstacle avoidance shortcut 'O'
    elif key == keys.O:
        world.show_obstacles = not world.show_obstacles
        if world.show_obstacles:
            world.create_obstacles()
            for a in world.agents:
                a.obstacle_avoidance_on()
        else:
            del world.obstacles[:]
            for a in world.agents:
                a.obstacle_avoidance_off()

    elif key == keys.W:
        world.show_walls = not world.show_walls
        if world.show_walls:
            world.create_walls()
            world.behavior_on(Behavior.WALL_AVOIDANCE)
        else:
            world.behavior_off(Behavior.WALL_AVOIDANCE)

def on_mouse_down(pos):
    # move the target
    world.crosshair = pos
    pass


start()
pgzrun.go()



    
