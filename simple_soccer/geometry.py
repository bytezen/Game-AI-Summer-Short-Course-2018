from pygame.math import Vector2

def _line_intersection_components(a,b,c,d):
    r_top =   (a.y - c.y)*(d.x - c.x) - (a.x - c.x)*(d.y - c.y)
    s_top =   (a.y - c.y)*(b.x - a.x) - (a.x - c.x)*(b.y - a.y)
    bot  = (b.x - a.x)*(d.y - c.y) - (b.y - a.y)*(d.x - c.x)

    return r_top,s_top,bot
    

def line_intersection(a,b,c,d):
    """
    return true if line AB intersects line CD
    """
    r_top,s_top,bot = _line_intersection_components(a,b,c,d)

    if bot == 0: return False # parallel

    r = r_top/bot
    s = s_top/bot

    if r > 0 and r < 1 and s > 0 and s < 1:
        return True
    else:
        return False


def line_intersection_get_distance(a,b,c,d):
    """
    return a tuple that states if the lines intersect
    and the distance the intersection occurs along AB
    returns False, None if the lines do not intersect
    """
    
    r_top,s_top,bot = _line_intersection_components(a,b,c,d)

    if bot == 0:
        if r_top == 0 and s_top == 0:
            return True,0
        else:
            return False, None
        
    r = r_top/bot
    s = s_top/bot

    if r > 0 and r < 1 and s > 0 and s < 1:
        dist = a.distance_to(b) * r
        return True,dist
    else:
        return False,None


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

plane_backside = -1
plane_frontside = 1
on_plane = 0

def where_is_point(point, point_on_plane, plane_normal):
    """determines if point is in front of, on, or in back of plane

    Args:
        point (Vector2, tuple, list) : the point to test
        point_on_plane (Vector2, tuple, list) : a point that is located anywhere on the plane
        planeNormal (Vector2) : the normal of the plane

    Returns:
        1, if in front of the plane, or
        0, if on the plane
        -1, if behind the plane
    """
    toPoint = Vector2(point_on_plane) - Vector2(point)

    dot = toPoint.dot(plane_normal)

    if dot < -0.000001: # in front of plane
        return 1
    elif dot > 0.000001: # in back of plane
        return -1
    else:
        return 0

def distance_to_ray_plane_intersection(ray_origin, ray_heading, plane_point, plane_normal):
    """determine how far along ray an intersection happens with a plane. if any

    Args:
        ray_origin (Vector2, tuple, list): the start of the ray
        ray_heading (Vector2, tuple, list): vector in the direction of the ray
        plane_point (Vector2, tuple, list): any point on the plane
        plane_norma (Vector2, tuple, list): the normal for the plane

    Returns:
        the distance along the ray that the intersection occurs or negative if
        the ray is parallel to the plane
    """

    d = -plane_normal.dot(plane_point)
    numer = plane_normal.dot(ray_origin) + d
    denom = plane_normal.dot(ray_heading)

    if denom < 0.000001 and denom > 0.0000001:
        return -1.0
    else:
        return -(numer / denom)
    

if __name__=='__main__':
    A = Vector2(10,0)
    B = Vector2(15,0)
    C = Vector2(16,3)
    D = Vector2(25,3)

    intersect = line_intersection(A,B,C,D)
    print(intersect)

    intersect,dist = line_intersection_get_distance(A,B,C,D)
    print(intersect,dist)
    
    intersect,dist,point = line_intersection_get_distance_and_point(A,B,C,D)    
    print(intersect,dist,point)

    

