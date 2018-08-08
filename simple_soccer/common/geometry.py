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

    

