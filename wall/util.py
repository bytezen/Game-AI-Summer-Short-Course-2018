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
    

def _create_whiskers(pos,heading,length=20,angle=50):
    """return a list of 3 whiskers

    Args:
        pos (Vector2) : origin for the whiskers
        direction( Vector2 ): what is the unrotated direction the whiskers
                            should point towards
        length (number) : the length of the whiskers
        angle (number) : absolute value of the rotation angle for the whiskers.
                         Default = +/- 50 degrees

    Returns:
        a list of two whiskers
    """
    feelers = [None]*3
    
    feelers[0] = pos + length * heading
    # 0.95 shortens the length to make the angled whiskers look better
    feelers[1] = pos + (length * 0.95) * heading.rotate(-angle)
    # 0.95 shortens the length to make the angled whiskers look better
    feelers[2] = pos + (length * 0.95) * heading.rotate(angle) 
    
    return feelers


def _line_intersection_components(a,b,c,d):
    r_top =   (a.y - c.y)*(d.x - c.x) - (a.x - c.x)*(d.y - c.y)
    s_top =   (a.y - c.y)*(b.x - a.x) - (a.x - c.x)*(b.y - a.y)
    bot  = (b.x - a.x)*(d.y - c.y) - (b.y - a.y)*(d.x - c.x)

    return r_top,s_top,bot


def line_intersection_get_distance_point(a,b,c,d):
    """
    return a tuple that states if the lines intersect
    and the distance the intersection occurs along AB
    and the point of intersection
    returns False, None,None if the lines do not intersect
    """
    
    r_top,s_top,bot = _line_intersection_components(a,b,c,d)

    if bot == 0:
        if r_top == 0 or s_top == 0: #parallel lines
            return False,None,None # what is the difference between these branches
        else:
            return False,None,None

    r = r_top/bot
    s = s_top/bot

    if r > 0 and r < 1 and s > 0 and s < 1:
        dist = a.distance_to(b) * r
        point = a + r * (b - a)
        return True,dist,point
    else:
        return False,None,None
