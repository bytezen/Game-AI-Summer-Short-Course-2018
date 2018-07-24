from BaseGameEntity import BaseGameEntity
import pygame
from pygame.math import Vector2
#from pygame.math.Vector2 import *
from math import radians, degrees

class MovingEntity(BaseGameEntity):

    def __init__(self,img):
        self._velocity = None
        self._heading = None
        self._normal = None
        self._mass = None
        self._max_speed = None
        self._max_force = None
        self._max_turn_rate = None

        self._rect = None

        super().__init__(img,entity_type="moving")        


    def speed(self):
        return self.velocity.magnitude
    
    def speed_sq(self):
        return self.velocity.magnitude_squared

    def is_speed_maxed_out(self):
        return self.speed >= self.max_speed

    def rotate_heading_to_face_position(self, target):
        # vector to where we want to face
        to_target = (target - self.pos).normalize_ip

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
        self.heading.rotate_ip( degrees(angle) )
        self._normal = self.heading.rotate( 90 )

        return False
        

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self,vec):
        self._velocity = Vector2(vec)
        
    @property
    def heading(self):
        return self._heading

    @heading.setter
    def heading(self,vector):
        v = Vector2(vector)
        length = v.length()
        assert length > 0.0001, "trying to set heading to vector with length 0" 
        self._heading = ( ( v / length ) ).normalize()
        self._normal = self._heading.rotate( 90 )
        
    @property
    def normal(self):
        return self._normal
        
    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self,val):
        self._mass = val

    @property
    def max_speed(self):
        return self._max_speed

    @max_speed.setter
    def max_speed(self,val):
        self._max_speed = val

    @property
    def max_force(self):
        return self._max_force

    @max_force.setter
    def max_force(self,val):
        self._max_force = val        

    @property
    def max_turn_rate(self):
        return degrees(self._max_turn_rate)

    @max_turn_rate.setter
    def max_turn_rate(self,val):
        self._max_turn_rate = radians(val)        



if __name__ == "__main__":
    import pgzrun
    
    foo = MovingEntity('player')
    foo.max_turn_rate = 10
    foo.heading = (1,0)
    foo.x = 200
    foo.y = 100
    fo0_ctr = foo.center
    
    WIDTH = 400
    HEIGHT = 400

    def draw():
        screen.fill("aliceblue")
        foo.draw()

    def update():
        foo.x += 2        
        _ctr = foo.center
        foo.angle += 1
        foo.center = _ctr


        pass

    pgzrun.go()
