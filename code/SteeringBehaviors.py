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
            self._steering_force += seek( entity.world.crosshair )

        return self._steering_force

    def on(self, behavior):
        return self._flags & behavior > 0

    def seek_on(self):
        self._toggleBehavior(Behavior.SEEK)

    def seek_off(self):
        self._toggleBehavior(Behavior.SEEK)

    def _toggleBehavior(self, behavior):
        self._flags ^= behavior

    #
    # Behavior methods
    #
    def seek(self,target):
        desiredVelocity = target - entity.pos()
        desiredVelocity.normalize_ip()
        desiredVelocity *= entity.max_speed

        return desiredVelocity - entity.velocity



if __name__=='__main__':
    from Vehicle import Vehicle

    foo = Vehicle(pos=(50,50),velocity=(2,2))
        
