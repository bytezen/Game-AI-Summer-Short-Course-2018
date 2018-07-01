#
# BaseGameEntity
#
# This is the base class for all entities
#
from pgzero.actor import Actor

class BaseGameEntity(Actor):
    m_id = 0
    ##TODO: Enum for entity types
    def __init__(self,img,entity_type="food",pos=(0,0),scale=(1,1),boundingRadius=0):

        
        self._id = self.next_id()
        self._entity_type = entity_type
        self._pos = pos
        self._scale = scale
        self._boundingRadius = boundingRadius
        self._tag = False
        
        super().__init__(img,center=pos,anchor=('center','center'))        
        
    @classmethod
    def next_id(self):
        id = BaseGameEntity.m_id
        BaseGameEntity.m_id += 1
        return id
    
    @property
    def id(self):
        return self._id

    @property
    def entity_type(self):
        return self._entity_type

    @entity_type.setter
    def entity_type(self,entity_type):
        self._entity_type = entity_type

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self,pos):
        self._pos = pos

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self,scale):
        self._scale = scale

    @property
    def boundingRadius(self):
        return self._boundingRadius

    @boundingRadius.setter
    def boundingRadius(self,boundingRadius):
        self._boundingRadius = boundingRadius

    @property
    def tag(self):
        return self._tag

    def is_tagged(self):
        return self._tag
    
    def tag(self):
        self._tag = True
        
    def untag(self):
        self._tag = False

    def update(self, time_elapsed):
        raise NotImplementedError("please override this method in your entity class")

    def render(self):
        raise NotImplementedError("please override this method in your entity class")

    def handle_message(self, msg):
        return False

    def write(self, fh):
        return None

    def read(self, fh):
        return None
            
    def __repr__(self):
        return "entity{{{id}({type})}}".format(id=self.id,type=self.entity_type)


if __name__ == "__main__":
    #import pygame as pg
    import pgzrun
    import pygame.time
    print("testing Base Game Entity")


    WIDTH = 500
    HEIGHT = 500

    baddie = BaseGameEntity("target")
    baddie.x = 0.5*WIDTH
    baddie.y = 0.5*HEIGHT
    baddie_ctr = baddie.center

    alien = Actor("alien")
    alien_ctr = alien.center
    print(baddie.topleft)

    def draw():
        screen.clear()
        baddie.draw()
        screen.draw.circle((250,250),5,(255,200,200))

    def update():
        baddie.angle += 15
        baddie.center = baddie_ctr

    pgzrun.go()
