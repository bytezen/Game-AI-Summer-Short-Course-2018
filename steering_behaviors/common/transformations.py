import numpy as np
from pygame.math import Vector2

class C2DMatrix:
    
    def __init__(self):
        self.identity()

    def identity(self):
        self.mat = np.eye(3)
        return self
    
    def reset(self): return self.identity() 

    def translate(self,*args):
        """
        return a matrix with a translation of x and y
        """
        if len(args) == 1:
            x,y = args[0].x, args[0].y
        else:
            x,y = args
            
        mat = np.array(([1,0,x],
                        [0,1,y],
                        [0,0,1]))

        self.mat = np.matmul(self.mat, mat)
        return self

        
    def scale(self,*args):
        if len(args) == 1:
            x,y = args[0].x, args[0].y
        else:
            x,y = args
            
        mat = np.array(( [x,0,0],
                         [0,y,0],
                         [0,0,1] ))

        self.mat = np.matmul(self.mat, mat)
        return self       

            
    def rotate(self,*args):
        if len(args) == 1:
            theta = np.radians( args[0] )
            cos, sin = np.cos( theta ), np.sin( theta)
            fwd,side = Vector2( cos, -sin ), Vector2(sin, cos) 
        else:
            fwd,side = args

        mat = np.array(( [fwd.x, fwd.y, 0],
                         [side.x, side.y, 0],
                         [0,0,1] ))

        self.mat = np.matmul(self.mat, mat)
        return self

        
    def transform(self,*args):
        if isinstance(args[0],list) :
            return self.transform_all(args[0])
        
        if len(args) == 1:
            point = args[0]
        else:
            point = Vector2(*args)
            
        pt = np.array([point.x,point.y,1]).reshape(3,1)

        tx_pt = np.matmul(self.mat, pt)

        return Vector2(tx_pt[0,0], tx_pt[1,0])
        

    def transform_all(self,points):
        return [self.transform(p) for p in points]

    def __repr__(self):
        return str(self.mat)
        
    


##
##
##
##
##
##


def point_to_world_space(point,position,fwd,side,scale=Vector2(1.0,1.0)):
    """
    given a point in object local space, the position of the object, orientation and scale
    this function transforms the vectors into world space
    """
    point = Vector2(point)
    pos = Vector2(position) if isinstance(position,tuple) else position

    print(point, pos, fwd, side, scale)
    
    mat = C2DMatrix()

    if (not (scale.x == 1.0)) or (not (scale.y == 1.0)):
        mat.scale(scale)

    print(mat)
    mat.rotate(fwd,side)
    print(mat)
    mat.translate(pos.x, pos.y)
    print(mat)
    return mat.transform( point )


def vector_to_world_space(vector, fwd, side):
    print('are we even getting here')
    mat = C2DMatrix()
    mat.rotate(fwd, side)
    print(mat)
    
    return mat.transform(vector)
        


##def world_transform(points, pos, forward, side):
##    """given points, position and orientation transform the points
##into the objects world space"""
##    pass

##def point_to_world_space(point, agent_heading, agent_side, agent_pos):
##    """transform a point from the agent's local space into world space"""
##    pass

##def vector_to_world_space(vec, agent_heading, agent_side):
##    """tranforms a vector from the agent's local space into world space"""
##    pass

def point_to_local_space(point, agent_heading, agent_side, agent_position):
    """transforms a point into the agent's local space"""

    tx = -agent_position.dot( agent_heading )
    ty = -agent_position.dot( agent_side )
    
    mat = C2DMatrix()
    mat.translate(tx,ty)
    mat.rotate(agent_heading, agent_side)

    return mat.transform(Vector2(point))

def vector_to_local_space(vec, agent_heading, agent_side):
    mat = C2DMatrix()
    mat.rotate(agent_heading, agent_side)

    return mat.transform(Vector2(vec))    


def vector_rotate_around_origin(vec, angle):
    return vec.rotate(angle)

def create_whiskers(num_whiskers, whisker_length, fov, facing, origin):
    """
    given an origin, a facing direction, a 'field of view' describing the 
    limit of the outer whiskers, a whisker length and the number of whiskers
    this method returns a vector containing the end positions of a series
    of whiskers radiating away from the origin and with equal distance between
    them. (like the spokes of a wheel clipped to a specific segment size)
    """
    pass


mat = C2DMatrix()
pos = Vector2(2.5, 4.33)
length,angle = pos.as_polar()
heading = Vector2(np.cos(np.radians(angle)),np.sin(np.radians(angle)))
side = heading.rotate(90)
print(pos,2*pos)

test = point_to_local_space(2*pos,
                     heading,
                     side,
                     pos)
print('test = \n ',test)

test2 = vector_to_local_space(2*pos, heading, side)

##mat.translate(5,5)
##mat.scale(Vector2(2,1))
##mat.translate(Vector2(-5,-5))




##
##theta = np.radians(30)
##c,s = np.cos(theta), np.sin(theta)
##R = np.array( ( (c,-s) , (s, c)  ) )
##print(R)
