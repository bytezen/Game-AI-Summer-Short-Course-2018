import pygame

class GameWorld:
    _instance = None
    
    def __init__(self, width, height):
        self.dimensions = pygame.Rect(0,0,width,height)

    @property
    def right(self):
        return self.dimensions.right
    @property
    def left(self):
        return self.dimensions.left
    @property
    def top(self):
        return self.dimensions.top
    @property
    def bottom(self):
        return self.dimensions.bottom
