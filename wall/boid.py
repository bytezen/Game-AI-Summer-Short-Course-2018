import pygame as pg
from pygame.math import Vector2
import pygame.gfxdraw
from pygame import Color
import sys
import util

pg.init()
IMAGE_PATH = 'images/'
MAX_SPEED = 100
MAX_FORCE = 1000
WALL_REPEL_FORCE = 100

class Behaviors:
    NONE = 0
    SEEK = 1
    FLEE = 2
    WALL_AVOIDANCE = 4

    
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
    SHOW_HEADING = False
    SHOW_WHISKERS = False
    
    def __init__(self, world, pos=(0,0), vel=(0,0), mass = 1.0):

        self.pos = Vector2(pos)
        self.mass = mass
        self.vel = Vector2(vel)        
        self.heading = Vector2(1,0)
        self.side = self.heading.rotate(-90)
        

##        self._orig_surface = _get_image(color)
        
        self._orig_surface = pg.image.load(IMAGE_PATH+'boid1_small.png').convert_alpha()        
        _,self.angle = self.heading.as_polar()
        
        self.behaviors = Behaviors.SEEK #| Behaviors.WALL_AVOIDANCE
        self.steering_force = Vector2()

        self.seek_target = None
        self.max_force = MAX_FORCE
        self.max_speed = MAX_SPEED


        self.world = world
        self.whiskers = []

              
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
        self.steering_force = self.calculate_steering_force()

        # accel = Force / mass
        accel = self.steering_force / self.mass

        # velocity
        # velocity = initialVelocity + acceleration * changeInTime
        self.vel = self.vel + accel * dtime

        # make sure that we don't exceed the speed limit
        util._clamp_vector(self.vel,0, self.max_speed)

        #position
        # position = positionInitial + velocity * changeInTime
        self.pos += self.vel * dtime

        #update the angle
        _,self.angle = self.vel.as_polar()

        
    def draw(self, surface, dt):
        self.update(dt)
        _surface, _rect = util._rotate(self._orig_surface,
                                            self.angle,
                                            self.pos,
                                            Vector2(0,0))
        surface.blit(_surface, _rect)

        #draw the steering force
        f = self.steering_force / self.max_force
        f *= 100
        pg.gfxdraw.line(surface,
                         int(self.pos.x),
                         int(self.pos.y),
                         int(self.pos.x + f.x),
                         int(self.pos.y + f.y),
                         pg.Color(200,0,0))

        # draw heading if desired
        if Boid.SHOW_HEADING:
            pg.draw.line( surface,
                          Color('purple'),
                          self.pos,
                          self.pos + 20 * self.heading)

        # draw feelers if desired
        if Boid.SHOW_WHISKERS:
            for whisker in self.whiskers:
                pg.draw.line( surface,
                              Color('purple'),
                              self.pos,
                              whisker)
            

    def calculate_steering_force(self):
        force = Vector2()
        
        if self.is_on(Behaviors.SEEK):
            force += self.calculate_seek(self.seek_target)

        if self.is_on(Behaviors.WALL_AVOIDANCE):
            force += self.calculate_wall_avoidance(self.world.walls)

        return force

    
    # check to see if a behavior is on for the boid
    def is_on(self, behavior):
        return self.behaviors & behavior > 0

    # turn on a behavior for the boid
    def turn_on(self, behavior):
        self.behaviors |= behavior

    # turn off a behavior for the boid
    def turn_off(self, behavior):
        if self.is_on(behavior):
            self.behaviors ^= behavior
            
            
##    def seek_on(self):
##        self.steering.turn_on(Behavior.SEEK);
##        
##    def seek_off(self):
##        self.steering.turn_off(Behavior.SEEK);


    def calculate_seek(self,target):
        """Compute the steering force required to seek a target

        Args:
            target (Vector2, tuple, list): The coordinates of the target

        Returns:
            force (Vector2): The steering force for this behavior
        """


        if target == None:
            return Vector2()
  
        # our desired velocity is the velocity that would take us to the target
        # from our current position
        desiredVelocity = Vector2(target) - self.pos

        # avoid dividing by 0 by making sure the length of the desired velocity
        # is greater than 0
        if desiredVelocity.length() > 0.0001:
            desiredVelocity.normalize_ip()
            # scale the vector by our max_speed
            desiredVelocity *= self.max_speed

        # the resulting force is the difference between where we want to go
        # and our current velocity
        return desiredVelocity - self.vel



    def calculate_wall_avoidance(self, walls):
        self.whiskers = util._create_whiskers(self.pos, self.heading)

        #variables for keep track of tallys
        distance_to_intersection_point = 0
        distance_to_closest_intersection_point = sys.float_info.max

        closest_wall = None

        force = Vector2()
        point = Vector2()
        closest_point = Vector2()

        # for each whisker find the closest wall
        for whisker in self.whiskers:
            for wall in self.world.walls:
                intersects,distance,intersecting_point = util.line_intersection_get_distance_point(Vector2(self.pos),
                                                                                                   whisker,
                                                                                                   wall.point1,
                                                                                                   wall.point2)
        
                if intersects:
                    if distance < distance_to_closest_intersection_point:
                        distance_closest_intersection_point = distance
                        closest_wall = wall
                        closest_point = intersecting_point

            # if we found a wall then calculate a steering force based on how far
            # the whisker penetrated the wall
            if closest_wall != None:
                over_shoot = whisker - closest_point
                force = wall.normal * over_shoot.length() * WALL_REPEL_FORCE
                
        return force

    

def _get_image(color):
    if color == 'green':
        return pg.image.load(IMAGE_PATH+'boid3_small.png').convert_alpha()

    if color == 'blue':
        return pg.image.load(IMAGE_PATH+'boid2_small.png').convert_alpha()

    if color == 'purple':
            return pg.image.load(IMAGE_PATH+'boid4_small.png').convert_alpha()
        
    return pg.image.load(IMAGE_PATH+'boid1_small.png').convert_alpha()    
    
