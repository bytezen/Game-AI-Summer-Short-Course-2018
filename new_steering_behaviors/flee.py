from pygame.math import Vector2


class Flee():

    #we only need one instance of the behavior
    _instance = None
    
    @classmethod
    def instance(klass):
        if klass._instance == None:
            klass._instance = Flee()
        return klass._instance


    @classmethod
    def calc(cls,pos,velocity,target,max_speed):        
        desiredVelocity = pos - target
        
        if desiredVelocity.length() > 0.0001:
            desiredVelocity.normalize_ip()
            desiredVelocity *= max_speed

        return desiredVelocity - velocity

        
    def calculate(self, entity):
        return self.__class__.calc(Vector2(entity.pos),
                                   Vector2(entity.velocity),
                                   Vector2(entity.flee_target),
                                   entity.max_speed)

FLEE = Flee.instance()
