import pygame as pg
from pygame.math import Vector2
import pygame.gfxdraw
import steering as Behavior
import util


pg.init()
IMAGE_PATH = 'images/'
MAX_SPEED = 100
MAX_FORCE = 1000



class Boid:
    """Class representing a game agent that can move

    Attrs:
        color ('red',''purple','green','blue') - color of the agent
        pos (Vector2) - the position of the agent
        mass (float) - the mass of the agent
        vel (Vector2) - velocity of the agent
        heading (Vector2) - heading of the agent
        side(Vector2) - the vector perpendicular to the agent
        
        max_force (float) - the maximum force that can be exerted on the agent
        max_speed (float) - the maximum speed that the agent can attain

        steering (Steering Behavior) - manages the behavior of the agent
        steering_force (Vector2) - the force resulting from the behaviors that
                                    are controlling the agent

    Mehtods:
        update(dtime) - updates the agents position using the time since the last update
                        as the time value for the physics calculations

        draw(surface) - renders the agent to the screen
        
        seek_on () - turns seek behavior on
        seek_off () - turns seek behavior off
        
    """
    _ID = 0
    
    def __init__(self, pos=(0,0), vel=(0,0), mass = 1.0, color='red'):

        self.pos = Vector2(pos)
        self.mass = mass
        self.velocity = Vector2(vel)        
        self.heading = Vector2(1,0)
        self.side = self.heading.rotate(-90)
        

        self._orig_surface = _get_image(color)
        
        
        _,self.angle = self.heading.as_polar()
        
        self.steering = []
        self.steering_force = Vector2()
        self.seek_target = Vector2(100,100)
        self.max_force = MAX_FORCE
        self.max_speed = MAX_SPEED

              
    @property
    def vel(self):
        return self._vel
    
    @vel.setter
    def vel(self,value):
        """sets the velocity, heading and side vectors

        copies the value to the velocity vector. If the value
        is the zero vector then heading and side are set to
        zero vectors too.
        """
        self._vel = Vector2(value)
        #calculate the heading angle from the velocity
        _,self.angle = self._vel.as_polar()
        if self._vel.length() > 0.001:
            #calculate the heading from the velocity
            self.heading = self._vel.normalize()
            #calculate the side vector (perpendicular to the heading)
            self.side = self.heading.rotate(90)
        else:
            self.heading = Vector2()
            self.side = Vector2()


    def update(self, dtime):
        # get the steering force
        self.steering_force = self._calculate_steering_force()

        # accel = Force / mass
        accel = self.steering_force / self.mass

        # velocity
        # velocity = initialVelocity + acceleration * changeInTime
        self.velocity = self.velocity + accel * dtime

        # make sure that we don't exceed the speed limit
        util._clamp_vector(self.velocity,0, self.max_speed)

        #position
        # position = positionInitial + velocity * changeInTime
        self.pos += self.velocity * dtime

        #update the angle
        _,self.angle = self.velocity.as_polar()

        
    def draw(self, surface):
        _surface, _rect = util._rotate(self._orig_surface,
                                            self.angle,
                                            self.pos,
                                            Vector2(0,0))
        surface.blit(_surface, _rect)

        #draw the steering force
        f = self.steering_force / self.max_force
        f *= 50
        pg.gfxdraw.line(surface,
                         int(self.pos.x),
                         int(self.pos.y),
                         int(self.pos.x + f.x),
                         int(self.pos.y + f.y),
                         pg.Color(200,0,0))

    def _calculate_steering_force(self):
        steering_force = Vector2()
        for behavior in self.steering:
            steering_force += behavior.calculate(self)

        return steering_force
            
    def seek_on(self):
        # TODO: make self.steering a set
        if any([ b == Behavior.SEEK for b in self.steering]):
            return

        self.steering.append(Behavior.SEEK) 
        
    def seek_off(self):
        try:
            self.steering.remove( Behavior.SEEK )
        except:
            pass


def _get_image(color):
    if color == 'green':
        return pg.image.load(IMAGE_PATH+'boid3_small.png').convert_alpha()

    if color == 'blue':
        return pg.image.load(IMAGE_PATH+'boid2_small.png').convert_alpha()

    if color == 'purple':
            return pg.image.load(IMAGE_PATH+'boid4_small.png').convert_alpha()
        
    return pg.image.load(IMAGE_PATH+'boid1_small.png').convert_alpha()    
    
