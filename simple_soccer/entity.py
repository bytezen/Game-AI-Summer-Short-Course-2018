#
# BaseGameEntity
#
# This is the base class for all entities
#
import pygame as pg
from pgzero.actor import Actor

from pygame.math import Vector2
#from pygame.math.Vector2 import *
from math import radians, degrees
from enum import IntEnum



class EntityType(IntEnum):
    DEFAULT = -1
    pass

    

## ---------------------------------------------------
## BaseEntity
## 
##   
class BaseEntity(Actor):
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
        self.id = BaseEntity._ID
        BaseEntity._ID +=1

        self.entity_type = EntityType.DEFAULT


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
        print('....before angle = ', self.pos, ' ', self._anchor_value)
        self._angle = angle
        pos = self.pos
        self._surf = pg.transform.rotate(self._orig_surf, angle)
        self.width, self.height = self._surf.get_size()
        self._calc_anchor()
        self.pos = pos

        print('....after angle = ', self.pos)

    def update(self, time_elapsed):
        raise NotImplementedError("please override this method in your entity class")

    def render(self):
        raise NotImplementedError("please override this method in your entity class")

    def handle_message(self, msg):
        return False        
        

## ---------------------------------------------------
## MoviingEntity
## 
## 
class MovingEntity(BaseEntity):
    def __init__(self,image,
                     velocity=(0,0),
                     max_speed = -1,
                     max_force = -1,
                     max_turn_rate = -1,
                     *args,**kwargs):
        super().__init__(image,*args,**kwargs)
        
        self._heading = Vector2()
        self._side = Vector2()
        self._init_moving_props(**kwargs)
        self.prev_pos = self.pos



    def _init_moving_props(self,**kwargs):
        # velocity
        try: self.velocity = Vector2(kwargs['velocity'])
        except: self.velocity = Vector2(0,0)

        # max_speed
        try: self.max_speed = kwargs['max_speed']
        except: self.max_speed = -1

        # max_force
        try: self.max_force = kwargs['max_force']
        except: self.max_force = -1

        # mass
        try: self.mass = kwargs['mass']
        except: self.mass = 1

        # max_turn_rate
        try: self.max_turn_rate = kwargs['max_turn_rate']
        except: self.max_turn_rate = -1     


    def rotate_heading_to_face_position(self, target):
        # vector to where we want to face
        to_target = (target - self.pos).normalize_ip()

        # angle that we need to turn to get there
        angle = self.heading.angle_to( to_target )

        # are we pretty much there??
        if angle < 0.00001:
            return True 

        # we aren't there so change the angle but make sure it is
        # not bigger than we are allowed to turn
        if angle > self.max_turn_rate:
            angle = self.max_turn_rate

        # turn us and also update our side vector
        self._heading.rotate_ip( degrees(angle) )
        self._side = self._heading.rotate( 90 )

        return False

    def set_orientation(self, vec):
        """ sets the heading and side vector based on vec
        """
        if vec.length() > 0:
            self._heading = vec.normalize()
            self._side = self._heading.rotate( 90 )

    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, value):
        """also set the heading and the side
        """
        self._velocity = Vector2(value)

        if self._velocity.length() > 0:
            # print(self._velocity, self._velocity.normalize(), type(self._velocity))
            # print(self.set_direction)
            # n = self._velocity.normalize()
            # self.set_direction(n)
 
            self.set_orientation( self._velocity )
            # self._heading = self._velocity.normalize()
            # self._side = self._heading.rotate(90)
        else:
            self._heading *= 0
            self._side *= 0

    @property
    def speed(self):
        return self._velocity.length()

    @property
    def speed_sq(self):
        return self._velocity.length_sq()
    
    @property
    def heading(self):
        return self._heading

    @heading.setter
    def heading(self, value):
        if abs(1.0 - value.length()) > 0.00001:
            self._heading = value.normalize()
        else:
            self._heading = value

        self._side = self._heading.rotate(90)

    @property
    def side(self):
        return self._side
        
    # @property
    # def exact_pos(self):
        # return Vector2(self.pos)

    # @exact_pos.setter
    # def exact_pos(self,vec):
        # self.pos = tuple(vec)

if __name__ == "__main__":
    #import pygame as pg
    import pgzrun
    import pygame.time
    print("testing Base Game Entity")


    WIDTH = 500
    HEIGHT = 500

    baddie = BaseEntity("target")

    alien = Actor("boid1_small")
    alien_ctr = alien.center

    foo = MovingEntity('boid1_small')
    print(foo.velocity)
    
    

    def draw():
        pass
        screen.clear()
        baddie.draw()
        screen.draw.circle((250,250),5,(255,200,200))

    def update(dt):
        pass

    pgzrun.go()
