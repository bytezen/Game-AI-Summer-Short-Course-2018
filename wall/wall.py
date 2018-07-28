import pygame
from pygame.math import Vector2
from pygame import Color


class Wall:
    def __init__(self, pt1, pt2, default_color = 'red'):
        self.point1 = Vector2(pt1)
        self.point2 = Vector2(pt2)
        self.color = Color(default_color)
        self.normal = (self.point2 - self.point1).normalize().rotate(90)
        self.center_point = (self.point2 + self.point1) * 0.5

    def draw(self, screen, show_normal = False):
        pygame.draw.line(screen, self.color, self.point1, self.point2)

        if show_normal:
            pygame.draw.line(screen,
                             self.color,
                             self.center_point,
                             self.center_point + 10 * self.normal)
                             

    #this is a way to get a custom string representation of our wall
    def __repr__(self):
        return '[' + str(self.point1) + '::' + str(self.point2) +']'
