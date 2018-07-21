from enum import IntEnum
from pygame.math import Vector2
from abc import ABC, abstractmethod


class BehaviorType(IntEnum):
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


def has_all(obj, attrs):
    return all( [ hasattr(obj,a) for a in attrs] )    

    
class BaseBehavior:
    """base class for Behaviors

    This class checks to make sure tht the required attributes
    are present on an entity trying to invoke the behaviors calculation
    """
    def __init__(self,b_type):
        self._type = b_type

    @property
    def type(self):
        return self._type
        
class SeekInterface(ABC):
    @abstractmethod
    def target(self):
        pass

class Seek(BaseBehavior):
    """Seek to a target

    requires that entity have a target attribute that is a (tuple, list, or Vector2)
    """

    #we only need one instance of the behavior
    _instance = None
    
    def __init__(self):
        super().__init__(BehaviorType.SEEK)

    @classmethod
    def instance(klass):
        if klass._instance == None:
            klass._instance = Seek()
        return klass._instance

    @classmethod
    def calc(cls,pos,velocity,target,max_speed):
        """calculate the steering force required to seek to the target position

        Attrs:
            entity (hasattr == [max_speed(float), pos(Vector2)]) object that will be seeking
            target (Vector2,tuple, or list) the position to seek to

        Return:
            the force needed to seek to the target ( Vector2 )
        """
        #ideally we want to get from our position to the target ...
        desiredVelocity = target - pos

        #what is the fastest that we can travel in the direction to the desired target??
        if desiredVelocity.length() > 0.0001:
            desiredVelocity.normalize_ip()
            desiredVelocity *= max_speed

        #the force is the difference between the vector that would get us to the target and
        #our current velocity
        return desiredVelocity - velocity        

        
    def calculate(self, entity):
        return self.__class__.calc(Vector2(entity.pos),
                                   Vector2(entity.velocity),
                                   Vector2(entity.seek_target),
                                   entity.max_speed)


SEEK = Seek.instance()  


if __name__ =='__main__':
    class Dummy(SeekInterface):
        def __init__(self):
            pass
        def target(self):
            pass
        
    boo = Dummy()
    seek = Seek()
