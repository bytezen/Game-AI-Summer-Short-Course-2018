from actors import Vehicle, Crosshair
from pygame.math import Vector2
from steering import Behavior

import pgzrun



def create_agents():
    world.agents = []

    vehicle = Vehicle(world=world,center=(400,200), mass=MASS, max_speed=MAX_SPEED, max_force=MAX_FORCE, max_turn_rate=MAX_TURN_RATE, vel=INIT_VEL)
    vehicle.toggle_behavior(BEHAVIOR)
    vehicle.pursuit_target = runner
    
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

    def update(self, time_elapsed):
        if self.paused:
            return
        
        for a in self.agents:
            a.update(time_elapsed)

        runner.update(time_elapsed)

    def draw(self):
        for a in world.agents:
            a.draw()

        runner.draw()
        
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



TITLE = 'Steering Behavior - Pursuit'    
WIDTH = 800
HEIGHT = 600

MASS = 1.0
MAX_SPEED = 100 # pixels / second
MAX_FORCE = 200 # pixels / second^2
MAX_TURN_RATE = 50 # degrees / second
INIT_VEL = (50,0)
BEHAVIOR = Behavior.PURSUIT
        

world = GameWorld(WIDTH,HEIGHT)


# target
runner = Vehicle(world=world,                   \
                 center=(0,30),               \
                 mass=MASS,                     \
                 max_speed=MAX_SPEED,           \
                 max_force=MAX_FORCE,           \
                 max_turn_rate=MAX_TURN_RATE,   \
                 vel=INIT_VEL)




def start():
    create_agents()


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



    
