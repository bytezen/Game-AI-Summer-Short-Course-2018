import common.actors as Actors
from common.actors import Vehicle, Crosshair, Obstacle
from common.behavior import Behavior
import common.params as Params
from common.wall import Wall

import pygame as pg
import pygame.gfxdraw
from pygame.math import Vector2

import random

    

class GameWorld:
    def __init__(self,width,height):
        #TODO: read this from config file

        self._paused = False
        self._window_dim = Vector2(width,height)
        self._crosshair = Crosshair((self.width * 0.5,
                                     self.height * 0.5))
        
##        self.display_params = Params.DisplayParams()
        self.wander_params = Params.WanderParams()
        self.obstacle_params = Params.ObstacleParams()
        self.obstacles = []
        self.agents = []
        self.walls = []

        #display flags
        self.view_keys = True
        
        self.show_walls = True
        self.show_wall_normals = True
        self.show_obstacles = True
        self.show_path = False
        self.show_wander_circle = False
        self.show_steering_force = True
        self.show_heading = False
        self.show_feelers = False
        self.show_detection_box = False
        self.render_neighbors = False
        self.show_tagged = True


        self.show_cell_space_info = False
        self.show_crosshair = False


    def display_flags_off(self):
        self.view_keys = False
        
        self.show_walls = False
        self.show_wall_normals = False
        self.show_obstacles = False
        self.show_path = False
        self.show_wander_circle = False
        self.show_steering_force = False
        self.show_heading = False
        self.show_feelers = False
        self.show_detection_box = False
        self.render_neighbors = False
        self.show_tagged = False


        self.show_cell_space_info = False
        self.show_crosshair = False

    def add_agent(self, *agents):
        if len(agents) > 1:
            for agent in agents:
                self.agents.append(agent)
        else:
            self.agents.append(agents[0])
        
    def create_obstacles(self, count = None):
        max_trys = 2000

        count = count or self.obstacle_params.number
        #create a dictionary to store obstacles
        #we will add obstacles to this dictionary if they do not collide with
        #anything in the dictionary
        
        obstacleDict = {}
        
        def add_obstacle(o):
            obstacleDict[(o.left,o.top,o.width,o.height)] = obstacle_rect(o).inflate_ip(20,20)

        def obstacle_rect(obstacle):
            return pg.Rect(obstacle.left,obstacle.top,obstacle.width,obstacle.height)
        
        #build dictionary from existing obstacles (should be empty initially)
        for o in self.obstacles:
            add_obstacles(o)
        
        for i in range( count ):
            num_trys = 0
            overlapped = True

            #create an obstacle
            tryme = Obstacle(pos = (random.randint(0.05*self.width ,0.95*self.width),
                                    random.randint(0.05*self.height, 0.95*self.height))
                             )
##            tryme = Obstacle(pos = (0.25* WIDTH, 0.5* HEIGHT))            
                            
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

    def create_walls(self):
        if len(self.walls) > 0:
            return

        self.walls.append(Wall((50,50),(300,450)))

    def behavior_on(self, behavior):
        for a in self.agents:
            a.behavior_on(behavior)

    def behavior_off(self, behavior):
        for a in self.agents:
            a.behavior_off(behavior)

                          
    def tag_obstacles_in_view_range(self, actor, objs, search_range):
        #TODO: use cell space partitioning for this
        Actors.tag_neighbors(actor, objs , search_range)


    def update(self, time_elapsed):
        if self.paused:
            return
        
        for a in self.agents:
            a.update(time_elapsed)


    def draw(self,screen):
        surface = screen.surface
##        display = self.display_params

        if self.show_walls:
            for w in self.walls:
                w.draw(surface)

        if self.show_obstacles:
            for o in self.obstacles:
                o.draw()

                if self.show_tagged and o.tagged:
                    pygame.gfxdraw.aacircle(surface,
                                            int(o.exact_pos.x),
                                            int(o.exact_pos.y),
                                            int(o.bounding_radius),
                                            (200,200,0)) 


        # render the agents
        for a in self.agents:
            a.draw(screen)
##            if a.on(Behavior.WANDER) and display.show_wander_config:
##                grab wander params from steering and params file
##                use pygame.gfx to draw to screen


            if self.show_cell_space_info:
                pass
            
                    
        if self.show_crosshair:
            self._crosshair.draw()


    @property
    def width(self): return self._window_dim.x

    @property
    def height(self): return self._window_dim.y
    
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



