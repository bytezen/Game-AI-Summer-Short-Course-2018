#
# BaseGameEntity
#
# This is the base class for all entities
#
import pygame as pg
from pgzero.actor import Actor

from pygame.math import Vector2
#from pygame.math.Vector2 import *
import math 
from enum import IntEnum

HALF_PI = math.pi * 0.5
TAU = math.pi * 2.0

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
        # self.exact_pos = Vector2(self.pos)        
##        print('Actor2 init: ',args)

        #Assign a unique ID and update the ID store for the next Actor
        self.id = BaseEntity._ID
        BaseEntity._ID +=1

        self.entity_type = EntityType.DEFAULT

    @property
    def exact_pos(self):
        return Vector2(self.pos)
    @exact_pos.setter
    def exact_pos(self,value):
        self.prev_pos = Vector2(self.pos)
        self.pos = tuple(value)

    def tag(self):
        self._tag = True

    def untag(self):
        self._tag = False

    @property
    def tagged(self):
        return self._tag

    @property
    def angle(self):
        assert False
        return self._angle

    @angle.setter
    def angle(self,angle):
        assert False
        self._angle = angle
        pos = self.pos
        self._surf = pg.transform.rotate(self._orig_surf, angle)
        self.width, self.height = self._surf.get_size()
        self._calc_anchor()
        self.pos = pos

    def _rotate_surface(self, phi):
        """rotate the surface by phi around the anchor"""

        #save the position to readjust after the rotation
        pos = self.pos

        #rotate the surface
        self._surf = pg.transform.rotate(self._orig_surf, phi)

        #update the width and height to reflect the changed bounding rect
        self.width, self.height = self._surf.get_size()

        #update the anchors for rendering as rotation around the anchor point
        self._calc_anchor()

        #restore the position
        self.pos = pos


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
                     mass = 1,
                     *args,**kwargs):

        print('MovingEntity.__init__ : image = ' , image)
        super().__init__(image,*args,**kwargs)

        self.prev_pos = self.pos
        self.exact_pos = self.pos
        self._velocity = Vector2(velocity)

        # check for zero velocity
        if self._velocity.length_squared() < 0.001:
            self._heading = Vector2(1,0)
        else:
            self._heading = self._velocity.normalize()

        self.max_speed = max_speed
        self.max_force = max_force
        self.max_turn_rate = max_turn_rate
        self.mass = mass


    def rotate_heading_to_face_position(self, target):
        # vector to where we want to face
        to_target = (target - self.exact_pos).normalize()

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
        # this should not be necessary since heading and side are derived
        # from angle now

        # self._heading.rotate_ip( math.degrees(angle) )
        # self._side = self._heading.rotate( 90 )

        return False

    # def set_orientation(self, vec):
        """ sets the heading and side vector based on vec
        """
        # if vec.length() > 0:
            # self._heading = vec.normalize()
            # self._side = self._heading.rotate( 90 )

    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, value):
        """also set the heading and the side
        """
        self._velocity = Vector2(value)

        # if the velocity is zero then we will not adjust the angle
        # of the player. We will leave them facing the same position
        if self._velocity.length() > 0:
            self.heading = self._velocity

    @property
    def speed(self):
        return self._velocity.length()

    @property
    def speed_sq(self):
        return self._velocity.length_sq()

    @property
    def angle(self):
        return self._angle
        # return self.heading.as_polar()[1]

    @angle.setter
    def angle(self,value):
        """changes the heading to reflect a direction of value degrees"""

        self._angle = value
        #set the angle of the heading
        self._heading.from_polar((1.0, -value))

        #now rotate object to the new angle
        self._rotate_surface(value)

    @property
    def heading(self):
        return self._heading
        # rads = math.radians(self.angle)

        #have to flip the heading positive rotation is counter-clockwise
        #but up is negative in y direction
        # return Vector2(math.cos(rads), -1 * math.sin(rads)) 

    @heading.setter
    def heading(self, value):
        self._heading = Vector2(value)
        self._heading.normalize_ip()

        #heading and angle use different rotation directions for positive
        self.angle = -self._heading.as_polar()[1]
    # @heading.setter
    # def heading(self, value):
    #     """ set the heading by passing a Vector2 or a float angle"""
    #     try:
    #         _,ang = value.as_polar()
    #         self.angle = ang
    #     except:
            # self.angle = value

    @property
    def side(self):
        return self.heading.rotate(90) 
 
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

    ball = MovingEntity('ball')

    # baddie = BaseEntity("target")

    # alien = Actor("boid1_small")
    # alien_ctr = alien.center

    # foo = MovingEntity('boid1_small')
    # print(foo.velocity)


    def draw():
        pass
        screen.clear()
        # baddie.draw()
        # screen.draw.circle((250,250),5,(255,200,200))

    def update(dt):
        pass

    pgzrun.go()
