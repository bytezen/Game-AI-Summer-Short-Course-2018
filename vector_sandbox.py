import pgzrun
import pygame as pg
from pygame.math import Vector2
import pygame.gfxdraw
import steering_behaviors.common.transformations as Tx

class BzVector2(Vector2):    
    def __init__(self,*args):
        super().__init__(*args)

    def draw_vector(self,surface,v,pos):
        vector = Vector2(v)

        norm = vector.normalize()
        side = norm.rotate(90)

    ##    print(vector.as_polar(), norm, norm.as_polar(), side, side.as_polar())
        l = vector.length()
        
        _thickness = 30

        rect = Rect(pos[0],pos[1]-_thickness,int(vector.length()),2*_thickness)
        pygame.gfxdraw.filled_polygon(surface,
                                 [rect.topleft,
                                  rect.topright,
                                  rect.bottomright,
                                  rect.bottomleft],
                                  (255,255,0))

        tx_rect = Tx.point_to_world_space([(0,-_thickness),
                                           (l, -_thickness),
                                           (l,_thickness),
                                           (0,_thickness)],
                                           pos,
                                           norm,
                                           side)

    ##    print('TX =======>>>>     ', tx_rect)
        pygame.gfxdraw.filled_polygon(surface,
                                      tx_rect,
                                      (255,0,0))

                         
def draw_vector(surface,v,pos):
    vector = Vector2(v)

    norm = vector.normalize()
    side = norm.rotate(90)

##    print(vector.as_polar(), norm, norm.as_polar(), side, side.as_polar())
    l = vector.length()
    
    _thickness = 30

    rect = Rect(pos[0],pos[1]-_thickness,int(vector.length()),2*_thickness)
    pygame.gfxdraw.filled_polygon(surface,
                             [rect.topleft,
                              rect.topright,
                              rect.bottomright,
                              rect.bottomleft],
                              (255,255,0))

    tx_rect = Tx.point_to_world_space([(0,-_thickness),
                                       (l, -_thickness),
                                       (l,_thickness),
                                       (0,_thickness)],
                                       pos,
                                       norm,
                                       side)

##    print('TX =======>>>>     ', tx_rect)
    pygame.gfxdraw.filled_polygon(surface,
                                  tx_rect,
                                  (255,0,0))


foo = BzVector2(50,-100)




def draw():
    screen.fill('goldenrod')
    draw_vector(screen.surface, Vector2(150,150), (50,100))
    foo.draw_vector(screen.surface,foo, (100,250))    
##    foo.draw(screen)
    

def update():
    pass

def on_key_up(key):
    if key == keys.U:
        foo.angle += 10
    elif key == keys.D:
        foo.angle -= 10
    elif key == keys.S:
        foo._scale = 1.2
        foo.scale()
    elif key == keys.T:
        foo._scale = 0.8
        foo.scale()
        
##        clock.schedule_unique(restore_surf(),3.0)


def restore_surf():
    foo.restore_surf()

WIDTH = 400
HEIGHT = 400
TITLE = 'Vector Drawing'



pgzrun.go()

