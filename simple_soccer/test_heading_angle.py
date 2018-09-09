import pgzrun
from pygame.math import Vector2
import math

WIDTH = 300
HEIGHT = 300

#mouse vars
mx,my = 0,0
tx,ty = mx,my

class Character:
    def __init__(self,img):
        self.pos = Vector2()
        self.heading = Vector2(1,0)
        self.image = img
        self._actor = Actor(self.image)
        self._target = 10 * self.heading

    @property
    def exact_pos(self):
        return Vector2(self.pos)

    @exact_pos.setter
    def exact_pos(self,pos):
        self.pos = tuple(pos)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, val):
        self._target = Vector2(val)

    def draw(self,layer):
        # print('aangle = ', self._actor.angle)
        self._actor.draw()
        layer.draw.line( self.pos, self.exact_pos + 20 * self.heading, 'red')

    def update(self):
        #want to update the delegated actor's angle
        pass

    def move(self,*xs ):
        if len(xs) == 1:
            self.pos = xs
        elif len(xs) == 2:
            self.pos = xs[0],xs[1]

        self._actor.pos = self.pos


def update():
    foo.update()
    pass

def draw():
    screen.fill('white')
    foo.draw(screen)
    screen.draw.circle((mx,my),10,'purple')
    screen.draw.filled_circle((tx,ty),5,'purple')

def on_mouse_down(pos):
    global tx,ty
    tx,ty = pos

    dx = tx - foo.pos[0]
    dy = ty - foo.pos[1]
    ang = math.atan2(dy,dx)

    def _angle(a):
        angle = math.degrees(a)
        foo.heading = Vector2()
        foo.heading.from_polar(( 1.0,angle))
        foo._actor.angle = -angle
    # foo.heading = Vector2(dx,dy).normalize()
    # foo._actor.angle = -foo.heading.as_polar()[1]  #math.degrees(ang)

    _angle(ang)
    print('heading = {}  angle = {}'.format( foo.heading.as_polar()[1], foo._actor.angle))
    foo.target = tx,ty

def on_mouse_move(pos):
    global mx,my
    mx,my = pos



foo = Character('redshirt0')
foo.move(WIDTH*0.5,HEIGHT*0.5)




pgzrun.go()
