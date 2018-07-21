import pygame as pg
from pygame.math import Vector2


def _rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point

    Args:
        surface (pygame.Surface): The surface that is to be rotated
        angle (float): Rotate by this angle
        pivot (tuple, list, pygame.math.Vector2): The pivot point
        offset (pygame.math.Vector2): This vector is added to the pivot point after the rotation

    Returns:
        rotated image (pygame.Surface): the new rotated surface 
        rect (pygame.Rect): A rect with proper positioning for the rotated surface
    """
    #rotate the image
    rotated_image = pg.transform.rotozoom(surface, -angle, 1)
    #rotate the offset vector
    rotated_offset = offset.rotate(angle)
    #Add the rotated offset vector to the center point to shift the rectangle
    rect = rotated_image.get_rect(center = pivot + rotated_offset)

    return rotated_image , rect



def _clamp_vector(vector,min_length, max_length):
    """make sure that a vectors length is between minimum and maximum

    Args:
        vector (Vector2) - the vector to scale
        min_length (positive float) - the minimum length of the vector
        max_length (positive float) - the maximum length of the vector

    Return:
        the vector passed in is changed if necessary
    """
    length = vector.length()
    if length > .001:
        if length < min_length:
            return vector.scale_to_length(min_length)
        elif length > max_length:
            return vector.scale_to_length(max_length)
    else:
        return vector
    
    
