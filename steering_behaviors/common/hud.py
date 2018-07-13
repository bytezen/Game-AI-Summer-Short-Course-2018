import pygame as pg
from pygame.math import Vector2

kvf = 'kenvector_future.ttf'
kvft = 'kenvector_future_thin.ttf'


cursor = Vector2()
slot_size = Vector2(0,20)
tab = Vector2(0,5)
header_size = 18
normal_size = 14

class Hud:
    NONE = 0
    INFO = 1
    PHYSICS = 2
    WANDER = 4
    FLOCKING = 8
    
    def __init__(self, actor):
        self._entity = actor
        self._mode = Hud.NONE

    
    def info_mode(self,on=True):
        if self._in_mode(Hud.INFO) and (not on):
            self._mode ^= Hud.INFO
        elif on:
            self._mode |= Hud.INFO

    def toggle_info_mode(self):
        self._toggle_mode(Hud.INFO)
        
##    def mode(self,m):
##        return self._in_mode(m)
    
    def _toggle_mode(self, m):
        if self._in_mode(m):
            self._mode ^= m
        else:
            self._mode_on(m)

    def _mode_on(self, m):
        self._mode |= m
        
    def _mode_off(self, m):
        if self._in_mode(m):
            self._mode ^= m
        
    def _in_mode(self,mode):        
        return (self._mode & mode) > 0

    
    def draw(self,screen):
        cursor = self._entity.exact_pos + slot_size
        entity = self._entity
        if self._in_mode(Hud.INFO):
            screen.draw.text("agent"+str(entity.id)+":",
                             tuple( cursor ),
                             fontname=kvf,
                             fontsize=header_size)

            cursor += slot_size
            cursor += tab
            screen.draw.text("velocity: " + str(entity.velocity),
                             tuple( cursor ),
                             fontname=kvft,
                             fontsize=normal_size)        
        
        pass
    
