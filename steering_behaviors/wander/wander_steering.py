from pygame.math import Vector2
from enum import IntEnum
from random import random
from params import WanderParams
import pygame.gfxdraw
import pgzrun

class Behavior(IntEnum):
    NONE = 0,
    SEEK = 2,
    FLEE = 4,
    ARRIVE = 8,
    WANDER = 16,
    COHESION = 32,
    SEPARATION = 64,
    ALIGNMENT = 128,
    OBSTACLE_AVOIDANCE = 256,
    WALL_AVOIDANCE = 512,
    FOLLOW_PATH = 1024,
    PURSUIT = 2048,
    EVADE = 4096,
    INTERPOSE = 8192,
    HIDE = 16384,
    FLOCK = 32768,
    OFFSET_PURSUIT = 65536
    
class Decelaration(IntEnum):
    SLOW = 3.0,
    NORMAL = 2.0,
    FAST = 1.0

##class Params:
##    jitter = 5.0
##    radius = 50.0
##    distance = 50.0
##    target = Vector2(0,-1)
    
class SteeringBehaviors:
    def __init__(self, entity):
        """
            Create a steering behaviors for entity. Entity is expected to be of
            type MovingEntity.
            
        """
        self._entity = entity
        self._steering_force = Vector2()
        self._flags = Behavior.NONE

        self.wander_params = WanderParams()
        

    def calculate(self):
        self._steering_force *= 0

        if self.on(Behavior.SEEK):
            print('seek on')
            self._steering_force += self.seek( self._entity.world.crosshair )

        if self.on(Behavior.ARRIVE):
            print('arrive on')            
            self._steering_force += self.arrive( self._entity.world.crosshair)

        if self.on(Behavior.FLEE):
            print('flee on')                        
            self._steering_force += self.flee( self._entity.world.crosshair)
            
        if self.on(Behavior.PURSUIT):
            print('pursuit on')                        
            self._steering_force += self.pursuit( self._entity.pursuit_target )
            
        if self.on(Behavior.EVADE):
            print('evade on')                        
            self._steering_force += self.evade( self._entity.target_actor )

        if self.on(Behavior.WANDER):
##            print('wander on')                        
            self._steering_force += self.wander()
            
        return self._steering_force

    def on(self, behavior):
        return self._flags & behavior > 0

    def seek_on(self):
        self.toggle_behavior(Behavior.SEEK)

    def seek_off(self):
        self.toggle_behavior(Behavior.SEEK)

    def arrive_on(self):
        self.toggle_behavior(Behavior.ARRIVE)

    def arrive_off(self):
        self.toggle_behavior(Behavior.ARRIVE)
        
    def toggle_behavior(self, behavior):
        self._flags ^= behavior

    #
    # Behavior methods
    #
    def seek(self,target):
        desiredVelocity = target - self._entity.exact_pos
        
        if desiredVelocity.length() > 0.0001:
            desiredVelocity.normalize_ip()
            desiredVelocity *= self._entity.max_speed

        return desiredVelocity - self._entity.velocity


    def arrive(self,target, decelaration=Decelaration.NORMAL):
        toTarget = target - self._entity.exact_pos
        dist = toTarget.length()
##        print(dist * dist)
        if (dist * dist) > 1.0 :
            decelarationTweak = 0.3
            speed = dist * (decelaration * decelarationTweak )

            speed = min(speed, self._entity.max_speed)

            desiredVelocity = toTarget * ( speed / dist )
            return desiredVelocity - self._entity.velocity
        else:
            return Vector2()


    def flee(self,target):
        desiredVelocity = self._entity.exact_pos - target
        
        if desiredVelocity.length() > 0.0001:
            desiredVelocity.normalize_ip()
            desiredVelocity *= self._entity.max_speed

        return desiredVelocity - self._entity.velocity
        

    def pursuit(self, evader):
        # vector from us to the evader
        to_evader = evader.exact_pos - self._entity.exact_pos

        # how similar are our headings?
        relative_heading = self._entity.heading.dot(evader.heading)

        # are we pointed towards the evader?
        is_headed_towards = to_evader.dot(self._entity.heading) > 0

        # if we are headedTowards them and they are coming towards them
        # go to their position
        # acos(0.95)= 18 degrees
        if is_headed_towards and relative_heading < -0.95:
            return self.seek(evader.exact_pos)

        # if we are here then the evader is not ahead of us
        # we will try to anticipate where they are with a lookahead time
        # the lookahead time is proportional to the distance between the evader
        # and us; (the further we are from one another the further in the future we want
        # to look in order to predict where the evader is going to be
        # it is inversely proportional to the sum of our speed and the evader's speed:
        # the faster we are both moving the shorter the lookahead time (because we
        # will cover more distance in a shorter time since we are going faster.)

        look_ahead_time = to_evader.length() / ( self._entity.max_speed + evader.speed )
        return self.seek(evader.exact_pos + evader.velocity * look_ahead_time)


    def evade(self, pursuer):
        entity = self._entity
        to_pursuer = pursuer.exact_pos - entity.exact_pos

        #Threat Range; uncomment to have agent only pursue entities within range
        threat_range = 100.0
        if to_pursuer.length_squared() > (threat_range * threat_range):
            return Vector2()

        look_ahead_time = to_pursuer.length() / ( entity.max_speed + pursuer.speed )
        return self.flee( pursuer.pos + ( pursuer.velocity * look_ahead_time ) )
        pass


    def wander(self):
        entity = self._entity

        params = self.wander_params

        ## from M.Buckland:
        ## this behavior is dependent on the update rate, so this line must
        ## be included when using time independent framerate.        
##        jitter_this_time_slice = params.jitter * entity.time_elapsed

        jitter_this_time_slice = params.jitter
        
        randomVec = Vector2( (random()*2.0-1.0) * jitter_this_time_slice, \
                             (random()*2.0-1.0) * jitter_this_time_slice )

        params.target += randomVec
##        print("params.target after random vec {0} = {1} ".format(randomVec,params.target))

        # project the target onto a point on the unit circle
        params.target.normalize_ip()

        # increase the length of the vector to the same radius
        # of the wander circle
        params.target *= params.radius
##        print('params.target projected onto radius', params.target)

##        print('new params target = ',params.target)
        
        # move the wander circle in front of us
        target = params.target + Vector2(params.distance,0)
##        print('target after adding distance offset', target)
        target.rotate_ip(entity.angle)

##        print('target after rotating by {0} = {1}'.format(entity.angle,target))

##        target += entity.exact_pos
##        return target - entity.exact_pos   

##        print('target after translating {0} = {1}'.format(entity.exact_pos, target))
##        print('pos = ', entity.exact_pos)
##        resVec = target - entity.exact_pos
##        print('steering vector = {0} magnitude = {1}'.format(resVec,resVec.length()))

##        print("--------- ------\n")

        return target


    def render(self,screen):
        if self._entity.world.model.render_wander_circle \
           and self.on(Behavior.WANDER):

            params = self.wander_params

            #get the wander circle center in world coordinates
            wander_center = Vector2(params.distance,0)
            wander_center.rotate_ip(self._entity.angle)
            wander_center += self._entity.exact_pos
                        
            # draw the wander cirle
            pygame.gfxdraw.aacircle(screen.surface, \
                                    int(wander_center.x),
                                    int(wander_center.y),
                                    int(self.wander_params.radius),
                                    (255,0,0))
        

            #draw the target point
            wander_target = self.wander_params.target.rotate(self._entity.angle)
            wander_target += wander_center #self._entity.exact_pos
            pygame.gfxdraw.filled_circle(screen.surface,
                                         int(wander_target.x),
                                         int(wander_target.y),
                                         5,
                                         (255,255,0))
