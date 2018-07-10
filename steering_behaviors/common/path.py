from pygame.math import Vector2
import pygame as pg
from pygame.gfxdraw import line,aacircle

import math
import random

class Path:

    def __init__(self, looped = False):
        self.looped = looped
        self._current_way_point = None
        self._way_points = []
        self._cursor = 0
        

    def __iter__(self):
        return self

    def __next__(self):
        if self._cursor >= ( len(self._way_points) - 1):
            if self.looped:
                self.reset()
##            else:
##                self._current_way_point = self._way_points[-1]
##                self._cursor = len(self._way_points) - 1
                
            raise StopIteration
        
        self._current_way_point = self._way_points[self._cursor]
        self._cursor += 1
        print(self._current_way_point)
        return self.current_way_point
        

    def next(self):
        try:
            pt = self.__next__()
        except StopIteration:
            return self.current_way_point            
            pass

        return self.current_way_point

    def at_end(self):
        return self._cursor >= ( len(self._way_points) - 1)

    @classmethod
    def create_random_path(cls, points, *args):
        path = Path()
        rect = pg.Rect(args)
        center = Vector2(rect.center)
        smaller_dim = min(rect.width, rect.height)
        spacing = 360 / points
        angle = 0

        print(smaller_dim,' %%%')

        for p in range(points):
            r = (random.random() * 0.3 + 0.2) * smaller_dim
            pointer = Vector2(1,0)
            pointer *= r
            pointer.rotate_ip(angle)
            angle += spacing

            path.add_way_point(center+pointer)
            
        return path

    def add_way_point(self,point):
        self._way_points.append(Vector2(point))

    def reset(self):
        self._cursor = 0

    @property
    def current_way_point(self):
        if self._cursor < 0 or self._cursor > (len(self._way_points) - 1):
            return None
        else:
            return self._way_points[self._cursor]
    
    @property 
    def path(self):
        return self._way_points
    
    @path.setter
    def path(self, points):
        self._way_points = [Vector2(p) for p in points]

    
    def clear(self):
        del self._way_points[:]

    def draw(self, surface):
        aacircle(surface, 300, 300, 10, pg.Color('red'))
        for i,p in enumerate(self._way_points):
            aacircle(surface,
                     int(p.x), int(p.y), 5,
                     pg.Color("gold") )
            
            if (i+1) < len(self._way_points):
                p2 = self._way_points[i+1]
                line(surface,
                     int(p.x),int(p.y),
                     int(p2.x),int(p2.y),
                     pg.Color("goldenrod"))
                
                aacircle(surface,
                         int(p2.x), int(p2.y), 5,
                         pg.Color("gold") )

