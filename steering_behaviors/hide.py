from common.actors import Vehicle, Crosshair, Obstacle
import common.actors as Actors
from common.behavior import Behavior
import common.params as Params
from common.world import GameWorld


import pgzrun


TITLE = 'Steering Behavior - Hide'    
WIDTH = 800
HEIGHT = 600

MASS = 1.0
MAX_SPEED = 100 # pixels / second
MAX_FORCE = 200 # pixels / second^2
MAX_TURN_RATE = 100 # degrees / second
INIT_VEL = (100,0)
BEHAVIOR = Behavior.NONE
        

world = GameWorld(WIDTH,HEIGHT)


# main Vehicle
hunter = Vehicle(world=world, \
                  center=(WIDTH*0.5,HEIGHT*0.5), \
                  mass=MASS, \
                  max_speed=(MAX_SPEED * 0.5), \
                  max_force=MAX_FORCE, \
                  max_turn_rate=MAX_TURN_RATE, \
                  vel= (INIT_VEL[0]*0.05,0))

hider1 = Vehicle(world=world, \
                  center=(WIDTH*0.25,HEIGHT*0.25), \
                  mass=MASS, \
                  max_speed=MAX_SPEED, \
                  max_force=MAX_FORCE, \
                  max_turn_rate=MAX_TURN_RATE, \
                  boid = 'purple',
                  vel=INIT_VEL)


hider2 = Vehicle(world=world, \
                  center=(WIDTH*0.75,HEIGHT*0.75), \
                  mass=MASS, \
                  max_speed=MAX_SPEED, \
                  max_force=MAX_FORCE, \
                  max_turn_rate=MAX_TURN_RATE, \
                  boid = 'purple',
                  vel=INIT_VEL)


def create_obstacles():
    o1 = Obstacle(pos=(0.23*WIDTH, 0.23*HEIGHT))
    o2 = Obstacle(pos=(0.66*WIDTH, 0.5*HEIGHT))    
    o3 = Obstacle(pos=(0.43*WIDTH, 0.76*HEIGHT))
    
    return [o1,o2,o3]


def start():
    world.add_agent(hunter)
    world.add_agent(hider1)
    world.add_agent(hider2)

##    world.create_obstacles(3) #obstacles = create_obstacles()
    world.obstacles = create_obstacles()
    
    hider1.hunter = hunter
    hider2.hunter = hunter

    hunter.wander_on(); #hunter.obstacle_avoidance_on()

    hider1.hide_on(); #hider1.obstacle_avoidance_on()
    hider2.hide_on(); #hider2.obstacle_avoidance_on()    

    
    world.display_flags_off()
    world.view_keys = True
    world.show_steering_force = True
    world.show_obstacles = True
    


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



    
