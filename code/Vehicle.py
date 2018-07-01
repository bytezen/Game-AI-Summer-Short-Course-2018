from MovingEntity import MovingEntity
from SteeringBehaviors import SteeringBehaviors

from math import sin,cos,radians,atan2,degrees
from Util import truncate_ip

import pygame as pg
from pygame.math import Vector2


class Vehicle(MovingEntity):
    vehicle_surf = None
    vehicle_image_path = "../assets/player.png"
    
    def __init__(self,pos=(0,0), velocity=(0,0), rotation=0.0, mass=1.0, max_force=1.0, max_speed=50.0, max_turn_rate=10):        
        super().__init__()
        self._pos = Vector2(pos)
        self.velocity = velocity
        self.mass = mass
        self.max_force = max_force
        self.max_speed = max_speed
        self.max_turn_rate = max_turn_rate
        self.heading = (cos(radians(rotation)), sin(radians(rotation)))
        self.rotation = rotation

        self._steering_behavior = SteeringBehaviors(self)
        
        if self.__class__.vehicle_surf == None:
            klass = self.__class__
            klass.vehicle_surf = pg.image.load(klass.vehicle_image_path)

        self.image_rect = self.__class__.vehicle_surf.get_rect()

    def render(self,surface):
        rotated,rect = self.update_display()
        surface.blit( rotated, rect)
#       pygame.draw.circle(surface, (255,0,0), (50,50) , 10, 0)

    def update_display(self):
        rotated,rect = myRotate( self.vehicle_surf, self.image_rect, self.rotation)
        rect.center = self.pos
        self.image_rect = rect

        return rotated, self.image_rect
               
    def update(self,dtime):
        oldpos = self.pos
        steering_force = self._steering_behavior.calculate()
        #print("{{Vehicle.update}} steering_force = {0}; mass ={1}".format(steering_force, self.mass))
        accel = steering_force / self.mass
        self.velocity += accel * dtime
        #print("velocity before truncate = %s" % self.velocity)
        truncate_ip(self.velocity,self.max_speed)
        #print("velocity after truncate = %s\n\n" % self.velocity)        
        self.pos += self.velocity * dtime

        if self._velocity.length_squared() > 0.000001:
               self.set_heading_and_normal = self.velocity.normalize()

        #update the space partitioning cell if space partitioning is on
    

    @property
    def steering_behavior(self):
        return self._steering_behavior

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self,val):
        self._pos = Vector2(val)

    def __repr__(self):
        s = super().__repr__()
        s = s + "{pos:%s; vel:%s}" % (self.pos, self.velocity)
        return s


def map(x,a,b,c,d):
    alpha = (float(x) - a)/(b - a)
    
    return (1.0 - alpha) * d + alpha * c

def myRotate(image, rect, angle):
    """Rotate the image while keeping its center.
        source = https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
        """
    # Rotate the original image without modifying it.
    new_image = pg.transform.rotozoom(image, angle,1)
    # Get a new rect with the center of the old rect.
    rect = new_image.get_rect(center=rect.center)
    return new_image, rect



if __name__ == '__main__':
    import pygame as pg, sys
    from pygame.locals import *
    from pygame.transform import *
    from pygame.math import Vector2
    import math
    
    foo = Vehicle(pos=(150,150), rotation= -45) #Vehicle(pos=(1,0), mass=1.0, rotation=0.0, velocity=0.0, max_force=2.0, max_speed=5.0, max_turn_rate=10)

    print(foo)
    
    pg.init()
    SURF = pg.display.set_mode((500,400))
    SURF.fill((255,255,255))

    # load boid
    boidSurf = pg.image.load("../assets/player.png")
    rect = boidSurf.get_rect()
    
    new_image = pg.transform.rotate(boidSurf, -90)
    rect = new_image.get_rect(center=rect.center)
    new_image,rect = myRotate(boidSurf, rect, -100)
    mousex,mousey = 0,0
    while True:
        SURF.fill((255,255,255))
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

        mousex, mousey = pg.mouse.get_pos()
        
#        print("{alpha}".format(alpha=map(mousex,0,500,,1)))
#        alpha=map(mousex,0,500,-90,90)
        dpos = Vector2(mousex,mousey) - foo.pos

        foo.rotation = -degrees( math.atan2(dpos.y,dpos.x) )
#        new_image,rect = myRotate(boidSurf,rect, alpha)
        
#        SURF.blit( new_image, rect)

        foo.render(SURF)
        pg.display.update()
