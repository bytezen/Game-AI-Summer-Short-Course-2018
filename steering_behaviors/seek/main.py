from actors import Vehicle, Crosshair
from pygame.math import Vector2
from steering import Behavior

import pgzrun
    
WIDTH = 800
HEIGHT = 600

MASS = 1.0
MAX_SPEED = 100 # pixels / second
MAX_FORCE = 200 # pixels / second^2
MAX_TURN_RATE = 50 # degrees / second
INIT_VEL = (50,0)

def create_agents():
    world.agents = []
    vehicle = Vehicle(world=world,center=(400,10), mass=MASS, max_speed=MAX_SPEED, max_force=MAX_FORCE, max_turn_rate=MAX_TURN_RATE, vel=INIT_VEL)
    world.agents.append(vehicle)
    

class GameWorld:
    def __init__(self,width,height):
        #TODO: read this from config file

        self._paused = False
        self._window_dim = Vector2(WIDTH,HEIGHT)
        self._crosshair = Crosshair((WIDTH*0.5, HEIGHT*0.5))

        self._show_steering_force = True
        self._show_crosshair = True

        self._behavior_flag = Behavior.SEEK

    def update(self, time_elapsed):
        if self.paused:
            return
        
        for a in self.agents:
            a.update(time_elapsed)


    def draw(self):
        for a in world.agents:
            a.draw()

        if self.show_crosshair:
            self._crosshair.draw()
        
    def render(self, surface):
        if self.render_crosshair:
            self._dirty_rect.append(target_surf.get_rect(center=self.crosshair))
            #surface.blit(target_surf, target_surf.get_rect(center=self.crosshair))

        #for agent in self.agents:
        #    agent.render(surface)

    @property
    def dirty_rect(self):
        return self._dirty_rect
    
    def handleKeyPresses(self):
        pass

    def handleMenuItems(self):
        pass
    
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

##    def seek_on(self):
##        self._behavior_flag |= Behavior.SEEK
##
##    def seek_off(self):
##        if self.behavior_on(Behavior.SEEK):
##            self._behavior_flag ^= Behavior.SEEK
##
##    def behavior_on(self, behavior):
##        return self._behavior_flag & behavior > 0

    def toggle_seek(self):
        for a in self.agents:
            a.toggle_behavior(Behavior.SEEK)




        

world = GameWorld(WIDTH,HEIGHT)

def start():
    create_agents()


def update(dt):
    for a in world.agents:
        a.update(dt)

    
def draw():
    screen.clear()
    world.draw()

def on_key_down(key):
    pass

def on_key_up(key):

    if key == keys.S:
        world.toggle_seek()
        
    elif key == keys.C:
        world.show_crosshair = not world.show_crosshair

def on_mouse_down(pos):
    # move the target
    world.crosshair = pos
    pass


start()
pgzrun.go()



    
