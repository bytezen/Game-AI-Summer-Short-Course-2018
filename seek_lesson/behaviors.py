from pygame.math import Vector2
import util

class Behavior:
    NONE = 0
    SEEK = 1

##    id_map = {0:'NONE',1:'SEEK'}
##    
##    def __init__(self,entity,behavior_type):
##        self.type = behavior_type
##        self.entity = entity
##
##    def calculate(self, **kwargs):
##        pass
##
##    def __repr__(self):
##        return self.id_map[self.type]
##

class SteeringBehaviors:
    """
    Class that encapsulates a host of steering behaviors that can be applied to
    an entity. Entitiies are of type Actor. See the Actor documentation for how to use
    """
    def __init__(self, entity):
        """
            Create a steering behaviors for entity. Entity is expected to be of
            type MovingEntity.
            
        """
        self.entity = entity
        self._steering_force = Vector2()
        self._flags = Behavior.NONE


    def turn_on(self, behavior):
        self._flags |= behavior
        
    def turn_off(self, behavior):
        if self.is_on(behvior):
            self._flags ^= behavior

    def is_on(self,behavior):
        return self._flags & behavior > 0
    
    def calculate(self):
        self._steering_force *= 0

        if self.is_on(Behavior.SEEK):
            self._steering_force += self.seek(self.entity.seek_target)
            

        # clamp the steering_force to the maximum if necessary
        util._clamp_vector(self._steering_force,0, self.entity.max_force)

        return self._steering_force

    
    
    def seek(self,target):
        """Compute the steering force required to seek a target

        Args:
            target (Vector2, tuple, list): The coordinates of the target

        Returns:
            force (Vector2): The steering force for this behavior
        """

        # our desired velocity is the velocity that would take us to the target
        # from our current position
        desiredVelocity = Vector2(target) - self.entity.pos

        # avoid dividing by 0 by making sure the length of the desired velocity
        # is greater than 0
        if desiredVelocity.length() > 0.0001:
            desiredVelocity.normalize_ip()
            # scale the vector by our max_speed
            desiredVelocity *= self.entity.max_speed

        # the resulting force is the difference between where we want to go
        # and our current velocity
        return desiredVelocity - self.entity.vel
            
        


        
    
