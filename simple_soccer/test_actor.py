import pgzero
from pygame.math import Vector2
from math import atan2, radians, cos, sin, pi, tau, degrees

half_pi = 0.5 * pi

class Heading:
    def __init__(self,angle):
        self._angle = angle

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self,value):
        self._angle = value

    @property
    def heading(self):
        #clamp angle
        # angle = self.angle % 360

        # convert to range of [-180,180]
        # angle = (angle - 360) if angle > 180 else angle

        rads = radians(self.angle)

        return Vector2(cos(rads), -sin(rads))

    def __repr__(self):
        return str( self.heading )

    

player = Actor('redshirt0')
heading = Heading(0)
player.pos = 200,200
player.angle = 50
Heading.angle = player.angle



WIDTH = 400
HEIGHT = 400
mx,my,targetx,targety = 0,0,0,0

frame = 0
def draw():
    screen.fill((200,200,200))
    if frame % 30 == 0:
        dy = targety - player.pos[1]
        dx = targetx - player.pos[0]
        print(dx,dy)
        player.angle = degrees( -atan2(dy, dx) )
        # player.angle += 5
        heading.angle = player.angle
        # print('angle = {}({})  heading = {}'.format(player.angle,
                                                    # radians(player.angle),
                                                    # heading))
    player.draw()

    screen.draw.line( player.pos,
                      ( (Vector2(player.pos) + 20 * heading.heading) ),
                      (200,0,0))

    screen.draw.filled_circle((targetx, targety),10,(200,0,0))

def update():
    global frame
    frame += 1
    pass

def on_mouse_move(pos):
    global mx, my
    mx,my = pos

def on_mouse_down(pos):
    global targetx, targety
    targetx,targety = pos
