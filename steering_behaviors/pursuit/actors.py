
from pygame import transform
from pygame.math import Vector2
from pgzero.actor import Actor
from steering import SteeringBehaviors
from math import cos,sin,degrees,radians

class Actor2(Actor):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._angle = 0.0
        self._orig_surf = self._surf

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
        self.heading = Vector2(cos(radians(angle)), sin(radians(angle)))

    
class Vehicle(Actor2):
    IMG_FILE = 'player'

    # Document the constructor. Essentially what we are doing here
    # is handling all of the vehicle specific args as positional parameters
    # everything passed in is wrapped up as kwargs and passed into the pgzero
    # Actor superclass. Look at the Actor class documentation to see what the valid
    # args are for this.
    #
    # This class will also handle the image for the Vehicle internally.
    def __init__(self,world,vel,mass,max_speed,max_turn_rate,max_force,**kwargs):

        self._velocity = Vector2(vel)
        self.max_speed = max_speed
        self._max_turn_rate = max_turn_rate
        self._max_force = max_force
        self.mass = mass
        self._target_actor = None

        # create a reference to steering behavior and
        # pass a reference of ourselves to it
        self._steering = SteeringBehaviors(self)

        self._world = world

        super().__init__(Vehicle.IMG_FILE, **kwargs)

        #TODO: Check that we have a position in kwargs
        #if  not ('pos' in kwargs):
         #   raise ValueError("you must specify a pos arg. See pygamezero Actor documentation")
        
        self.exact_pos = Vector2(self.pos)
        self.angle = self.velocity.as_polar()[1]


    def update(self,dt):
        steering_force = self._steering.calculate()

        accel = steering_force / self.mass
        self.velocity += accel * dt
        truncate_ip( self.velocity, self.max_speed) 
        self.exact_pos += self.velocity * dt

        if self.speed > 0.0001:
            self.heading = self._velocity.normalize()
            self.side = self.heading.rotate(90)
            
        self.pos = self.exact_pos
        self.angle = -self.velocity.as_polar()[1]

    def toggle_behavior(self,behavior):
        self._steering.toggle_behavior(behavior)


    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self,vec):
        self._velocity = Vector2(vec)
        self.heading = Vector2(cos(radians(self.angle)), sin(radians(self.angle)))
        self.side = self.heading.rotate(90)

    @property
    def speed(self): return self.velocity.length()
    
    @property
    def world(self): return self._world

    @property
    def pursuit_target(self):
        return self._target_actor
    
    @pursuit_target.setter
    def pursuit_target(self, agent):
        self._target_actor = agent

        
        

        
    


class Crosshair(Actor):
    IMG_FILE = 'target'
    
    def __init__(self, *args,**kwargs):
        super().__init__(Crosshair.IMG_FILE,*args,**kwargs)

        
    


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
