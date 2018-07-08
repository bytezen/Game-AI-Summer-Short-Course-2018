from pygame.math import Vector2
from pygame.gfxdraw import line
from pygame import Color

class Wall:
    def __init__(self,phrom=Vector2(),to=Vector2()):
        self._start = Vector2(phrom)
        self._end = Vector2(to)
        self.calculate_normal()


    @property
    def center(self):
        return (self.phrom + self.to ) * 0.5
    
    @property
    def phrom(self):
        return self._start
    
    @phrom.setter
    def phrom(self,vec):
        self._start = Vector2(vec)
        self.calculate_normal()

    @property
    def to(self):
        return self._end

    @to.setter
    def to(self,vec):
        self._end = Vector2(vec)
        self.calculate_normal()
    
    def draw(self,surface):
        line(surface,
             int(self.phrom.x),
             int(self.phrom.y),
             int(self.to.x),
             int(self.to.y),
             Color("magenta"))

    def draw_with_normals(self,surface):
        self.draw(surface)
        center = self.center
        line(surface,
             int(center.x),
             int(center.y),
             int(center.x + 20 * self.normal.x),
             int(center.y + 20 * self.normal.y),
             Color("white"))
        
    def calculate_normal(self):
        vec = self.to - self.phrom
        if vec.length_squared() > 0.0001:
            vec.normalize_ip()
            vec.rotate_ip(90)
            self.normal = vec
        else:
            self.normal = vec



        
