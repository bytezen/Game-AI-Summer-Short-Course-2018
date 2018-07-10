import pygame as pg
from pygame.math import Vector2

kvf = 'kenvector_future.ttf'
kvft = 'kenvector_future_thin.ttf'
bump = Vector2(0,15)
class Hud:
    def __init__(self, actor):
        self._entity = actor        

    def draw(self,screen):
        screen.draw.text("hello world", tuple( self._entity.exact_pos + bump), fontname=kvf, fontsize=32)
        pass
    
