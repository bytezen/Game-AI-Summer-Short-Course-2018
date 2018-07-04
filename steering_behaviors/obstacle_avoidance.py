from common.actors import Vehicle, Crosshair, Obstacle
from common.steering import Behavior
import common.params as Params

from pygame.math import Vector2
import pygame.gfxdraw
import random
##from wander_steering import Behavior

import pgzrun


class Model():
    render_wander_circle = True
    show_steering_force = False
    

def create_agents():
    world.agents = []

##    vehicle = Vehicle(world=world,center=(400,200), mass=MASS, max_speed=MAX_SPEED, max_force=MAX_FORCE, max_turn_rate=MAX_TURN_RATE, vel=INIT_VEL)
##    vehicle.toggle_behavior(BEHAVIOR)
##    vehicle.pursuit_target = runner
    
    world.agents.append(vehicle)
    

class GameWorld:
    def __init__(self,width,height):
        #TODO: read this from config file

        self._paused = False
        self._window_dim = Vector2(WIDTH,HEIGHT)
        self._crosshair = Crosshair((WIDTH*0.5, HEIGHT*0.5))

        self._show_steering_force = True
        self._show_crosshair = True

        self._behavior_flag = BEHAVIOR
        self.model = Model()
        
        self.display_params = Params.DisplayParams()
        self.wander_params = Params.WanderParams()
        self.obstacle_params = Params.ObstacleParams()
        self.obstacles = []


    def create_obstacles(self):
        max_trys = 2000

        #create a dictionary to store obstacles
        #we will add obstacles to this dictionary if they do not collide with
        #anything in the dictionary
        
        obstacleDict = {}
        
        def add_obstacle(o):
            obstacleDict[(o.left,o.top,o.width,o.height)] = obstacle_rect(o)

        def obstacle_rect(obstacle):
            return pygame.Rect(obstacle.left,obstacle.top,obstacle.width,obstacle.height)
        
        #build dictionary from existing obstacles (should be empty initially)
        for o in self.obstacles:
            add_obstacles(o)
        
        for i in range(self.obstacle_params.number):
            num_trys = 0
            overlapped = True

            #create an obstacle
            tryme = Obstacle(pos = (random.randint(0.05*WIDTH ,0.95*WIDTH),
                                    random.randint(0.05*HEIGHT, 0.95*HEIGHT)))
            
                            
            while overlapped == True:
                num_trys += 1
                
                # have we tried to many times?
                if num_trys > max_trys: break

                # do we intersect any existing obstacles
                intersections = obstacle_rect(tryme).collidedict( obstacleDict )
                
                if intersections == None:
                    self.obstacles.append(tryme)
                    add_obstacle(tryme)
                    break
                
        
    def update(self, time_elapsed):
        if self.paused:
            return
        
        for a in self.agents:
            a.update(time_elapsed)


    def draw(self):
        display = self.display_params
        
        for a in world.agents:
            a.draw()
##            if a.on(Behavior.WANDER) and display.show_wander_config:
##                grab wander params from steering and params file
##                use pygame.gfx to draw to screen
            if display.show_steering:
                a._steering.render(screen)

            if display.show_bounding_radius:
                pygame.gfxdraw.aacircle(screen.surface, \
                                        int(a.exact_pos.x),
                                        int(a.exact_pos.y),
                                        int(a.bounding_radius),
                                        (50,0,255))

            if display.show_obstacles:
                for o in self.obstacles:
                    o.draw()
                    
        if self.show_crosshair:
            self._crosshair.draw()

                    
            
    @property
    def agents(self):
        return self._agents

    @agents.setter
    def agents(self,agents):
        self._agents = agents
        
    @property
    def crosshair(self):
        return self._crosshair.pos
    
    @crosshair.setter
    def crosshair(self,args):
        self._crosshair.pos = Vector2(args)

    @property
    def paused(self):
        return self._paused
    
    @paused.setter
    def paused(self,flag):
        self._paused = flag
        
    @property
    def window_dim(self):
        return self._window_dim

    @property
    def render_steering_force(self):
        return self._show_steering_force

    @property
    def show_crosshair(self):
        return self._show_crosshair

    @show_crosshair.setter
    def show_crosshair(self, val):
        self._show_crosshair = val

    def toggle_behavior(self):
        for a in self.agents:
            a.toggle_behavior(BEHAVIOR)



TITLE = 'Steering Behavior - Evade'    
WIDTH = 800
HEIGHT = 600

MASS = 1.0
MAX_SPEED = 10 # pixels / second
MAX_FORCE = 100 # pixels / second^2
MAX_TURN_RATE = 50 # degrees / second
INIT_VEL = (10,0)
BEHAVIOR = Behavior.WANDER
        

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
    create_agents()
    world.create_obstacles()


def update(dt):
    world.update(dt)
##    for a in world.agents:
##        a.update(dt)



def draw():
    screen.clear()
    world.draw()

def on_key_down(key):
    pass

def on_key_up(key):

    if key == keys.B:
        world.toggle_behavior()
        
    elif key == keys.C:
        world.show_crosshair = not world.show_crosshair

def on_mouse_down(pos):
    # move the target
    world.crosshair = pos
    pass


start()
pgzrun.go()



    
