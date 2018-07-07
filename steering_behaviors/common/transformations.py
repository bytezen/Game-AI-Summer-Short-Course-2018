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
            
        mat = np.array(([1,0,0],
                        [0,1,0],
                        [x,y,1]))

        self.mat = np.matmul(self.mat, mat)
        return self

        
    def scale(self,*args):
        #if you pass in one argument it is assumed to be a Vector2 or a number
        # if it is a number then the matrix will set Sx = Sy = argument
        if len(args) == 1:
            if isinstance(args[0],Vector2):
                x,y = args[0].x, args[0].y
            else:
                x = y = args[0]
        else:
            x,y = args
            
        mat = np.array(( [x,0,0],
                         [0,y,0],
                         [0,0,1] ))

        self.mat = np.matmul(self.mat, mat)
        return self       

            
    def rotate(self,*args):
        """
        construct a rotation matrix that transforms a point into
        local space
        """
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
            
        pt = np.array([point.x,point.y,1])

        #this is the kicker...we are assuming row vector transformations
        #with how we setup the matrices
        tx_pt = np.matmul(pt,self.mat)

        return Vector2(tx_pt[0], tx_pt[1])
        

    def transpose(self):
        self.mat = self.mat.transpose()
        return self.mat
    
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
    given a point (or list of points) in object local space, the position of the object, orientation and scale
    this function transforms the vectors into world space
    """

    # if we have a list of points then recursively call this function one individual point
    if isinstance(point,list):
        return [ point_to_world_space(p, position, fwd, side,scale) for p in point ]

    #copy the parameters so we don't manipulate them
    temp_point = Vector2(point)
    temp_position = Vector2(position) 
    
    mat = C2DMatrix()

    if (not (scale.x == 1.0)) or (not (scale.y == 1.0)):
        mat.scale(scale)

    mat.rotate(fwd,side)
    
    mat.translate(temp_position.x, temp_position.y)
    
    return mat.transform( temp_point )


def vector_to_world_space(vector, fwd, side):
    mat = C2DMatrix()
    mat.rotate(fwd, side)
    
    return mat.transform(vector)
        


def point_to_local_space(point, agent_heading, agent_side, agent_position):
    """transforms a point into the agent's local space"""

    tx = -agent_position.dot( agent_heading )
    ty = -agent_position.dot( agent_side )
    
    mat = C2DMatrix()
    mat.mat[0,0] = agent_heading.x
    mat.mat[1,0] = agent_heading.y
    mat.mat[2,0] = tx 

    mat.mat[0,1] = agent_side.x
    mat.mat[1,1] = agent_side.y
    mat.mat[2,1] = ty 

    return mat.transform(Vector2(point))

def vector_to_local_space(vec, agent_heading, agent_side):
    mat = C2DMatrix()

    mat.mat[0,0] = agent_heading.x
    mat.mat[1,0] = agent_heading.y


    mat.mat[0,1] = agent_side.x
    mat.mat[1,1] = agent_side.y

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


##
##points = [(1,1),(1,4),(12,0)]
##foo = point_to_world_space(points, Vector2(3,-3), Vector2(.707,.707), Vector2(-.707,.707))
##for p,f in zip(points, foo):
##    print(p,f)






##
##mat = C2DMatrix()
##pos = Vector2(2.5, 4.33)
##length,angle = pos.as_polar()
##heading = Vector2(np.cos(np.radians(angle)),np.sin(np.radians(angle)))
##side = heading.rotate(90)
##print(pos,2*pos)
##
##test = point_to_local_space(2*pos,
##                     heading,
##                     side,
##                     pos)
##print('test = \n ',test)
##
##test2 = vector_to_local_space(2*pos, heading, side)
