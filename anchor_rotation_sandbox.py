import pgzrun
import pygame as pg

WIDTH = 400
HEIGHT = 400
TITLE = 'Anchor Rotation Test'

boid = Actor('boid3',center=(200,200), anchor=('left','center'))
boid2 = Actor('boid3', center=(200,100), anchor=('left','center'))
imgw, imgh = boid2._orig_surf.get_size()

scaled_boid = pg.transform.scale(boid2._orig_surf, (200, 50))
                                      
anchor = boid.midleft
anchor2 = boid2.midleft
def draw():
    screen.fill((175,175,175))
    screen.draw.circle(anchor, 5, 'yellow')
    screen.draw.circle(anchor2, 5, 'yellow')
    screen.blit(scaled_boid, (0,0))
    boid.draw()
    boid2.draw()
    pass

def update(dt):
    boid.angle += 10
pgzrun.go()
