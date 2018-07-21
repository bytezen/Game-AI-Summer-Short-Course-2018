from pygame.math import Vector2


class Seek():
    """Seek to a target

    requires that entity have a target attribute that is a (tuple, list, or Vector2)
    """

    #we only need one instance of the behavior
    _instance = None
    
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

