from pygame.math import Vector2
from enum import IntEnum


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

    
class SteeringBehaviors:
    def __init__(self, entity):
        """
            Create a steering behaviors for entity. Entity is expected to be of
            type MovingEntity.
            
        """
        self._entity = entity
        self._steering_force = Vector2()
        self._flags = Behavior.NONE
        

    def calculate(self):
        self._steering_force *= 0

        if self.on(Behavior.SEEK):
            self._steering_force += self.seek( self._entity.world.crosshair )

        if self.on(Behavior.ARRIVE):
            self._steering_force += self.arrive( self._entity.world.crosshair)

        if self.on(Behavior.FLEE):
            self._steering_force += self.flee( self._entity.world.crosshair)
            
        if self.on(Behavior.PURSUIT):
            self._steering_force += self.pursuit( self._entity.pursuit_target )
            
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

if __name__=='__main__':
    from Vehicle import Vehicle

    foo = Vehicle(pos=(50,50),velocity=(2,2))
        
