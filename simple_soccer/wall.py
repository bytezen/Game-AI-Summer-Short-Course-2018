from pygame.math import Vector2
import pygame as pg
from pygame import Color

class Wall2D:
    def __init__(self, ptA, ptB, color = 'white'):
        self.a = Vector2(ptA)
        self.b = Vector2(ptB)
        self.normal = (self.b - self.a).rotate(90)
        self.normal.normalize_ip()
        self.center = (self.b + self.a) * 0.5
        self._color = Color(color)
        pass

    def draw(self, screen, show_normal = False):
        pg.draw.line(screen,
                     self._color,
                     self.a,
                     self.b,
                     2)

        if show_normal:
            pg.draw.line(screen,
                         Color('darkgoldenrod'),
                         self.center,
                         self.center + 10 * self.normal,
                         2)
                         
                     
def walls_from_rect(rect, color ='white'):
    boundary = [None]*4
    boundary[0] = Wall2D(rect.topleft, rect.topright, color)
    boundary[1] = Wall2D(rect.topright, rect.bottomright, color)
    boundary[2] = Wall2D(rect.bottomright, rect.bottomleft, color)
    boundary[3] = Wall2D(rect.bottomleft, rect.topleft, color)

    return boundary

if __name__=='__main__':
    wall1 = Wall2D( Vector2(10,10), Vector2(200,10))
    print(wall1.a, wall1.b, wall1.normal)

    
    
