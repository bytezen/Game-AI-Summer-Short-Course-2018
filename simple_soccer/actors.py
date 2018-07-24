
from pygame import transform
from pygame.math import Vector2
from pgzero.actor import Actor
import pygame.gfxdraw as gfxdraw
import pygame as pg

from common.steering import SteeringBehaviors
from common.behavior import Behavior
from common.path import Path
from common.hud import Hud
from math import cos,sin,degrees,radians
import random



def tag_neighbors(actor, objs, dist):
    """ all actors(objs) that are within range(dist) of x are tagged"""
##    print('ATTEMPT to tag_neighbors')
    #clear tags
    for o in objs:
        o.untag()

        if actor == o:
            continue
        
        to = o.exact_pos - actor.exact_pos
        #account for the bounding radius of the other object search range
        rng = dist + o.bounding_radius
        
##        print('{tag_neighbors.to} ', to, str(to.length_squared()),str(rng*rng) )

        if to.length_squared() < ( rng * rng ):
            o.tag()

## ---------------------------------------------------
## Actor2
## 
##   
class Actor2(Actor):
    _ID = 0
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._angle = 0.0
        self._orig_surf = self._surf
        self._tag = False
        # bounding radius
        # assume that the dimensions of the image are the dimensions
        # of the actor
        self.bounding_radius = 0.5 * max(self._orig_surf.get_width(),
                                         self._orig_surf.get_height())
        self.exact_pos = Vector2(self.pos)        
##        print('Actor2 init: ',args)

        #Assign a unique ID and update the ID store for the next Actor
        self.id = Actor2._ID
        Actor2._ID +=1 


    def tag(self):
        self._tag = True
        
    def untag(self):
        self._tag = False

    @property
    def tagged(self):
        return self._tag
    
    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self,angle):
        self._angle = angle
        pos = self.pos
        self._surf = transform.rotate(self._orig_surf, angle)
        self.width, self.height = self._surf.get_size()
        self._calc_anchor()
        self.pos = pos
        

## ---------------------------------------------------
## Vehicle
## 
##       
class Vehicle(Actor2):
    IMG_FILE = 'player'

##    BOID_IMG = { 'red':'boid1', 'blue':'boid2', 'green':'boid3', 'purple': 'boid4'}
    BOID_IMG = { 'red':'boid1_small', 'blue':'boid2_small', 'green':'boid3_small', 'purple': 'boid4_small'}
    
    #Target indices for different behaviors that require additional actors
    HUNTER_INDEX = 4
    LEADER_INDEX = 3

    # Document the constructor. Essentially what we are doing here
    # is handling all of the vehicle specific args as positional parameters
    # everything passed in is wrapped up as kwargs and passed into the pgzero
    # Actor superclass. Look at the Actor class documentation to see what the valid
    # args are for this.
    #
    # This class will also handle the image for the Vehicle internally.
    def __init__(self,world,vel,mass,max_speed,max_turn_rate,max_force,boid=None,**kwargs):

    
        # this will also initialize our heading and our side vector
        self.velocity = Vector2(vel)
        self.max_speed = max_speed
        self._max_turn_rate = max_turn_rate
        self.max_force = max_force
        self.mass = mass
        self._target_actor = None
        self.steering_force = Vector2()
        self.targets = [None,None,None,None,None]

        # create a reference to steering behavior and
        # pass a reference of ourselves to it
        self._steering = SteeringBehaviors(self)

        self._world = world

        if not(boid in Vehicle.BOID_IMG.keys()):
            boid = random.choice(list(Vehicle.BOID_IMG.values()))
        else:
            boid = Vehicle.BOID_IMG[boid]                
            
        super().__init__(boid, **kwargs)

        #TODO: Check that we have a position in kwargs
        #if  not ('pos' in kwargs):
         #   raise ValueError("you must specify a pos arg. See pygamezero Actor documentation")
        
##        self.exact_pos = Vector2(self.pos)
        self.angle = -self.heading.as_polar()[1]

        self.time_elapsed = 0.0

        self.hud = Hud(self)
        self.hud.info_mode()

    def update(self,dt):
        #some behaviors need to know the time since the last update
        self.time_elapsed = dt
        
        self.steering_force = self._steering.calculate()

        truncate_ip(self.steering_force, self.max_force)
        
##        print('***** STEERING FORCE = ', steering_force)

        accel = self.steering_force / self.mass
##        print("      VElocity before accel = ", self.velocity)
        
        self.velocity += accel * dt
##        if self.id == 2 :
##            print("     entity{0}: VElocity AFTER accel = ".format(self.id), self.velocity * dt)
        
        truncate_ip( self.velocity, self.max_speed)
##        print("      VElocity AFTER truncate = ", self.velocity)                
        self.exact_pos += self.velocity * dt

        # handle off screen position by wrapping
        if self.exact_pos.x > self._world.width:
            self.exact_pos.x = 0 #self.bounding_radius
            
        if self.exact_pos.x < 0:
            self.exact_pos.x = self._world.width - self.bounding_radius

        if self.exact_pos.y < 0:
            self.exact_pos.y = self._world.height - self.bounding_radius

        if self.exact_pos.y > self._world.height:
            self.exact_pos.y = 0 # self.bounding_radius

        if self.speed > 0.0001:
            self.heading = self._velocity.normalize()
            self.side = self.heading.rotate(90)
            
        self.pos = self.exact_pos

        # positive is counterclockwise,but we want to rotate clockwise for positive
        self.angle = -self.heading.as_polar()[1]


    def seek_on(self):
        self.behavior_on(Behavior.SEEK)

    def seek_off(self):
        self.behavior_off(Behavior.SEEK)
        
    def arrive_on(self):
        self.behavior_on(Behavior.ARRIVE)

    def arrive_off(self):
        self.behavior_off(Behavior.ARRIVE)
        
    def flee_on(self):
        self.behavior_on(Behavior.FLEE)

    def flee_off(self):
        self.behavior_off(Behavior.FLEE)
              
    def pursuit_on(self):
        self.behavior_on(Behavior.PURSUIT)

    def pursuit_off(self):
        self.behavior_off(Behavior.PURSUIT)
              
    def evade_on(self):
        self.behavior_on(Behavior.EVADE)

    def evade_off(self):
        self.behavior_off(Behavior.EVADE)        
              
    def wander_on(self):
        self.behavior_on(Behavior.WANDER)

    def wander_off(self):
        self.behavior_off(Behavior.WANDER)

    def obstacle_avoidance_on(self):
        self.behavior_on(Behavior.OBSTACLE_AVOIDANCE)

    def obstacle_avoidance_off(self):
        self.behavior_off(Behavior.OBSTACLE_AVOIDANCE)

    def wall_avoidance_on(self):
        self.behavior_on(Behavior.WALL_AVOIDANCE)

    def wall_avoidance_off(self):
        self.behavior_off(Behavior.WALL_AVOIDANCE)

    def interpose_on(self):
        self.behavior_on(Behavior.INTERPOSE)

    def interpose_off(self):
        self.behavior_off(Behavior.INTERPOSE)
        
    def hide_on(self):
        self.behavior_on(Behavior.HIDE)

    def hide_off(self):
        self.behavior_off(Behavior.HIDE)

    def path_follow_on(self):
        self.behavior_on(Behavior.FOLLOW_PATH)

    def path_follow_off(self):
        self.behavior_off(Behavior.FOLLOW_PATH)        

    def offset_pursuit_on(self):
        self.behavior_on(Behavior.OFFSET_PURSUIT)

    def offset_pursuit_off(self):
        self.behavior_off(Behavior.OFFSET_PURSUIT)              

    def alignment_on(self):
        self.behavior_on(Behavior.ALIGNMENT)

    def alignment_off(self):
        self.behavior_off(Behavior.ALIGNMENT)            

    def separation_on(self):
        self.behavior_on(Behavior.SEPARATION)

    def separation_off(self):
        self.behavior_off(Behavior.SEPARATION)        
        
    def cohesion_on(self):
        self.behavior_on(Behavior.COHESION)

    def cohesion_off(self):
        self.behavior_off(Behavior.COHESION)        
        
    def behavior_on(self, behavior):
        print('turning on behavior: ', Behavior.str(behavior))
        self._steering.on(behavior)

    def is_behavior_on(self, behavior):
        return self._steering.is_on(behavior)
        
    def behavior_off(self, behavior):
        print('turning off behavior: ', Behavior.str(behavior))        
        self._steering.off(behavior)

    def behavior_all_off(self):
        print('turning off all behaviors: ')        
        self._steering.all_off()
        
    def is_behavior_off(self, behavior):
        return not self.is_behavior_on(behavior)
        

    def toggle_behavior(self, behavior):
        self._steering.toggle_behavior(behavior)


    def add_target(self, actor):
        self.targets.append(actor)
##    def toggle_behavior(self,behavior):
##        self._steering.toggle_behavior(behavior)

##    def obstacle_avoidance_on(self): self._steering.

    def draw(self,screen):
        surface = screen.surface
        super().draw()

        if self._world.view_keys:
            self._steering.render_aids(surface)

            #show heading and side
            if self._world.show_heading:
                gfxdraw.line(surface,
                             int(self.exact_pos.x),
                             int(self.exact_pos.y),
                             int(self.exact_pos.x + 20 * self.heading.x),
                             int(self.exact_pos.y + 20 * self.heading.y),
                             pg.Color(200,200,200))
            #steering_force
            if self._world.show_steering_force:
                f = self.steering_force / self.max_force
                f *= 100
                gfxdraw.line(surface,
                             int(self.exact_pos.x),
                             int(self.exact_pos.y),
                             int(self.exact_pos.x + f.x),
                             int(self.exact_pos.y + f.y),
                             pg.Color(200,0,0))
            #hud
            if self._world.show_hud:
                self.hud.draw(screen)
                             
                             

    @property
    def behavior(self):
        return self._steering._flags    

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self,vec):
        self._velocity = Vector2(vec)
##        if self._velocity.length() > 0.001:
        self.heading = self.velocity.normalize()
        self.side = self.heading.rotate(90)
##        else:
            

    @property
    def heading(self):
        return self._heading
    
    @heading.setter
    def heading(self,*args):
        self._heading = Vector2(*args)
        
    @property
    def speed(self): return self.velocity.length()
    
    @property
    def world(self): return self._world

    @property
    def pursuit_target(self):
        return self._target_actor
##        return self.targets[0]
    
    @pursuit_target.setter
    def pursuit_target(self, actor):
        self._target_actor = actor
##        self.targets[0] = actor

    @property
    def evade_target(self):
        return self._target_actor
##        return self.targets[1]

    @evade_target.setter
    def evade_target(self, actor):
        self._target_actor = actor
##        self.targets[1] = actor

    @property
    def hunter(self):
        return self.targets[self.HUNTER_INDEX]

    @hunter.setter
    def hunter(self,actor):
        self.targets[self.HUNTER_INDEX] = actor

    @property
    def leader(self):
        return self.targets[self.LEADER_INDEX]

    @leader.setter
    def leader(self, actor):
        self.targets[self.LEADER_INDEX] = actor

    @property
    def path(self):
        return self._steering.path

    @path.setter
    def path(self, path):
        self._steering.path = path

    
## ---------------------------------------------------
## Crosshair
## 
##   
class Crosshair(Actor2):
    IMG_FILE = 'target'
    
    def __init__(self, *args,**kwargs):
        super().__init__(Crosshair.IMG_FILE,*args,**kwargs)


## ---------------------------------------------------
## Obstacle
## 
##   
class Obstacle(Actor2):
    IMG_FILE = 'obstacle'

    def __init__(self,*args,**kwargs):
        file = Obstacle.img_file()
        super().__init__( Obstacle.img_file() ,*args, **kwargs)

    @classmethod
    def img_file(cls):
        return Obstacle.IMG_FILE + str(random.choice(range(9)))





def truncate_ip(vec,limit):
    if vec.length_squared() > (limit * limit):
        vec.normalize_ip()
        vec.scale_to_length(limit)
    else:
        vec

if __name__ == '__main__':
    import pgzrun
    
    MASS = 1.0
    MAX_SPEED = 10 # pixels / second
    MAX_FORCE = 200 # pixels / second^2
    MAX_TURN_RATE = 50 # degrees / second
    INIT_VEL = (0,30)

    WIDTH = 500
    HEIGHT = 500
    
    class dummyWorld:
        def __init__(self,w,h):
            self.w = w
            self.h = h

        @property    
        def crosshair(self):
            return Vector2(self.w * 0.5, self.h * 0.5)

    test = Vehicle(world=dummyWorld(300,300) ,center=(0,50), mass=MASS, max_speed=MAX_SPEED, max_force=MAX_FORCE, max_turn_rate=MAX_TURN_RATE, vel=INIT_VEL)
    crosshair = Crosshair((150,150))


    def draw():
        screen.fill("white")        
        crosshair.draw()

#    pgzrun.go()
