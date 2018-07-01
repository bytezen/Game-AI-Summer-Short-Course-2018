from pygame.math import Vector2
from configparser import ConfigParser
import io
import random

from Vehicle import *

def config(file):
# Load the configuration file
    with open(file) as f:
        sample_config = f.read()
    config = ConfigParser() #(allow_no_value=True)
    config.read(file)
    #config.readfp(io.BytesIO(sample_config))

    # List all contents
    print("List all contents")
    for section in config.sections():
        print("Section: %s" % section)
        for options in config.options(section):
            print("x %s:::%s:::%s" % (options,
                                      config.getint(section, options) * 1.4,
                                      str(type(options))))

    # Print some contents
    #print("\nPrint some contents")
    #print(config.get('other', 'use_anonymous'))  # Just get the value
    #print(config.getboolean('other', 'use_anonymous'))  # You know the datatype?    


target_file = "../assets/target.png"
target_surf = None

class GameWorld:
    def __init__(self,width,height):
        #TODO: read this from config file        
        self._vehicles = [Vehicle(pos=(0.25*w,0.25*h),velocity=(40,0))] #[ Vehicle(pos=(0,0)) for v in range(2) ]
        self._obstacles = []
        self._walls = []

        self._paused = False
        self._window_dim = Vector2(width,height)
        self._crosshair = Vector2(width*0.5, height*0.5)

        self._show_walls = True
        self._show_obstacles = True
        self._show_path = True
        self._show_steering_force = True
        self._show_crosshair = True

        self._dirty_rect = []

    def _create_obstacles(self):
        pass

    def _create_walls(self):
        pass

    def update(self, time_elapsed):
        if self.paused:
            return

        del self._dirty_rect[:]
        
        for a in self.agents:
            a.update(time_elapsed)
            self._dirty_rect.append(a.image_rect)
            img, rect = a.update_display()
            self._dirty_rect.append(rect)

    def draw(self, surface):
        surface.blit(target_surf, target_surf.get_rect(center=self.crosshair) )
        
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
    def walls(self):
        return self._walls

    @property
    def agents(self):
        return self._vehicles

    @property
    def obstacles(self):
        return self._obstacles

    @property
    def crosshair(self):
        return self._crosshair
    
    @crosshair.setter
    def crosshair(self,args):
        self._crosshair = Vector2(args)

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
    def render_crosshair(self):
        return self._show_crosshair





if __name__ == '__main__':
    from pygame.math import Vector2
    import pygame as pg
    import sys
    import random
    
    from pygame.locals import *
    
    w = 800
    h = 600
    # config("steering.ini")

    
    pg.init()

    FPS = 30
    fpsClock = pg.time.Clock()
    
    SURF = pg.display.set_mode((w,h))
    SURF.fill((255,255,255))

    target_surf = pg.image.load(target_file)
    
    game = GameWorld(w,h)
    game.draw(SURF)
    pg.display.update()
    
    while True:
        #SURF.fill((255,255,255))
        
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    game.crosshair = event.pos
                    print("button = %s %s " % (event.button, str(event.pos)))

            #foo.crosshair = pg.mouse.get_pos()

        dt = fpsClock.get_time() * 0.001
        print("fps=%f" % fpsClock.get_fps())
        game.update(dt)
        game.render(SURF)
        #print(game.agents[0])
        #print("dirties = %d " % len(game.dirty_rect))
        pg.display.update()
        fpsClock.tick(FPS)
                

    

    

