from entity import MovingEntity
from model import Model

from pygame.math import Vector2
import math
import random
import geometry
##import daten

def time_to_cover_distance(obj, a, b, force, friction):
    """calculate the time to travel between 2 points assuming the obj has an initial speed of 0.

    Args:
        obj (assert obj.mass > 0) : the object that is moving
        a (Vector2, tuple, list): the starting point
        b (Vector2, tuple, list): the ending point
        force (float) : magnitude of the force applied to the object

    Returns:
        time (float) : the time required to reach the destination point; -1 if object cannot reach
        the destination point. (Object can not overcome friction to get there )
    """
    # the speed in the next time step *if* the object applies the force
    # Note, this function assumes that speeds don't accumulate
    speed = force / obj.mass

    #final velocity at b
    #
    #  v^2 = init_v ^ 2 + 2*a*dist
    #
    # if init_v ^ 2 + 2*a*dist is negative then the final position can not be reached
    distance_to_cover = Vector2(a).distance_to(Vector2(b))

    term = speed * speed + 2.0 * distance_to_cover * friction
    if term <= 0:
        return -1
    else:
        v = sqrt(term)
        
        # final velocity - initial velocity / accel
        return (v-speed)/friction
    

def test_wall_collision(obj,walls,screen=None):
##    print('\n******\n')
    idx_closest = -1
    if obj.velocity.length() < 0.0000001:
##        print('\t velocity is 0 ...returning')
        return
    
    normal_vel= obj.velocity.normalize()
    _pos = Vector2(obj.pos)
    b_radius = obj.bounding_radius
##    print('\tnormal_vel: {0},_pos: {1}, b_radius: {2}'.format(normal_vel,_pos,b_radius)) 

    intersection_pt = Vector2()
    collision_pt = Vector2()

    distance_to_intersection = 100000000


    for i,w in enumerate(walls):
        _collision = _pos - ( w.normal * b_radius)
##        if _debug:
##            print('\t',i,' pos: ', _pos, '  collision: ', _collision,' normal ', str(w.normal * b_radius), end='')


        #if the collision point is behind the plane
        #then calculate exactly where it will intersect the wall
##        if _debug:
##            where_is_pt = geometry.where_is_point(_collision, w.b, w.normal)
##            print(' pt(front,on,behind): ', where_is_pt)
        if geometry.where_is_point(_collision, w.b, w.normal) == geometry.plane_backside:
##            print('\t\t --on backside --',end='')
            dist_to_wall = geometry.distance_to_ray_plane_intersection(_collision,
                                                                       w.normal,
                                                                       w.a,
                                                                       w.normal)
            intersection_point = _collision + (dist_to_wall * w.normal)

##            if screen != None:
##                obj.display_list.append((screen.draw.filled_circle, [intersection_point,5,'yellow']) )           
            
        else:
            dist_to_wall = geometry.distance_to_ray_plane_intersection(_collision,
                                                                       normal_vel,
                                                                       w.a,
                                                                       w.normal)
            intersection_point = _collision +  (dist_to_wall * normal_vel)
##            if screen != None:
##                obj.display_list.append((screen.draw.circle, [intersection_point,5,'red']) )               

        on_line_segment = False

        if geometry.line_intersection(w.b, w.a,
                                      _collision - w.normal * 20.0,
                                      _collision + w.normal * 20.0
                                      ):
##            obj.display_list.append( (screen.draw.line, [_collision - w.normal * 20.0,
##                                                          _collision + w.normal * 20.0,
##                                                         'purple']))
            on_line_segment = True
##            print('\t**\t*** on line segment ***** \n')

        # now check to see if the collision point is within the range of the velocity vector
        # and if it is the closest hit found so far.
        # If it is that means the ball will collide with the wall sometime
        # between this time step and the next one
        dist = _collision.distance_squared_to(intersection_point)

        if dist < obj.velocity.length_squared() \
            and dist < distance_to_intersection \
            and on_line_segment:                
                dist_to_intersection = dist
                idx_closest = i
                _collision = intersection_point 
        
    # to prevent having to calculate the exact time of collision we can just check if the velocity
    # is opposite to the wall normal before reflecting it. This prevents the case where there is overshoot
    # and th ball gets reflected back over the line before it has completely reentered the playing area
    if idx_closest >= 0 and normal_vel.dot(walls[idx_closest].normal) < 0:
##        print('....reflecting!!!!! ')
        obj.velocity.reflect_ip( walls[idx_closest].normal)
    

class Ball(MovingEntity):
    def __init__(self,boundary,**kwargs):
        super().__init__('ball',**kwargs)
        print(kwargs)
        self.pitch_boundary = boundary
        self.model = kwargs['model']

        #testing
        ##        self.predicted_position = None
        ##        self.display_list = []
    def __call__(self):
        return Vector2(self.pos)


    def update(self):
        #debug
        if _paused:
            return
        test_wall_collision(self,self.pitch_boundary,screen)
        
        # debug - reset predicted position so we don't render it
##        if self.speed == 0:
##            self.predicted_position = None

        self.prev_pos = self.pos


        # if we are moving fast enough to overcome friction
        if self.velocity.length_squared() > self.model.friction * self.model.friction:
            friction_force = self.model.friction 
            friction_force = friction_force * self.heading
            self.velocity += friction_force 
            self.pos += self.velocity



    def draw(self):
        super().draw()
##        if self.predicted_position != None:
##            screen.draw.filled_circle( self.predicted_position, 5, 'white')
        
##        if len(self.display_list) > 0:
##            for f,ps in self.display_list:
##                f(*ps)
                                    
        
    def kick(self, direction, force):
        accel = Vector2(direction).normalize() * force / self.mass
        # update the velocity
        self.velocity = accel
##        print('{kick} vel = ', self.velocity)
        
        self.predicted_position = self.future_position(180)
        

    
    def handle_message(self,msg):
        return false

    def time_to_cover_distance(self, a, b, force):
        """calculate the time to travel between 2 points assuming the obj has an initial speed of 0.

        Args:
            obj (assert obj.mass > 0) : the object that is moving
            a (Vector2, tuple, list): the starting point
            b (Vector2, tuple, list): the ending point
            force (float) : magnitude of the force applied to the object

        Returns:
            time (float) : the time required to reach the destination point; -1 if object cannot reach
            the destination point. (Object can not overcome friction to get there )
        """
        # the speed in the next time step *if* the object applies the force
        # Note, this function assumes that speeds don't accumulate
        speed = force / self.mass

        #final velocity at b
        #
        #  v^2 = init_v ^ 2 + 2*a*dist
        #
        # if init_v ^ 2 + 2*a*dist is negative then the final position can not be reached
        distance_to_cover = Vector2(a).distance_to(Vector2(b))

        term = speed * speed + 2.0 * distance_to_cover * self.model.friction
        if term <= 0:
            return -1
        else:
            v = sqrt(term)
            
            # final velocity - initial velocity / accel
            return (v-speed)/friction    


    def future_position(self, time):
        # using the equation d = ut + 1/2at^2, where d = distance, a = friction,
        # u = start velocity, t=change in time

        if self.speed == 0:
            print('{future_position} no speed returning position')
            return self.pos

        ut = self.velocity * time

        half_at_sq = (0.5 * self.model.friction * time * time) 

        half_at_sq = half_at_sq * self.heading

        # this is the magnitude of the distance traveled
        # multiply it times the heading to get the distance and direction
        d = ut + half_at_sq


        return self.pos + d


    def trap(self):
        self.velocity *= 0

    def place_at_position(self, value):
        self.prev_pos = self.pos
        self.pos = Vector2(value)
        self.vel *= 0

    def add_noise_to_kick(self, ball_pos, ball_target):
        displacement = 360.0 * (1.0 - model.player_kick_accuracy) * random.uniform(-1,1)
        toTarget = ball_target - ball_pos
        toTarget.rotate_ip(displacement)
        return toTarget + ball_pos
        
        pass

if __name__ == '__main__':
    import pgzrun
    from pygame import Rect
    import wall

    

    boundary = Rect(10,10,380,380)
    WIDTH = 400
    HEIGHT = 400

    KICK_FORCE = 3

    walls = wall.walls_from_rect(boundary)
    b = Ball(walls,model=Model.instance())
    b.pos = Vector2(WIDTH *0.5, HEIGHT * 0.5)

    mouse_pos = None
    #debug
    _paused = _debug = False
    
    def update():
        b.update()
        
    def draw():
        if _paused:           
            return
        
        screen.fill('darkgreen')

        for w in walls:
            w.draw(screen.surface, True)

        #debug render direction vector
        if mouse_pos != None:
            dist = Vector2(mouse_pos[0] - b.pos[0], mouse_pos[1] - b.pos[1])
            dist.normalize_ip()
            dist *= 20
            
            screen.draw.line(b.pos,
                             (b.pos[0] + dist.x, b.pos[1] + dist.y),
                             (200,200,0))            
            
        b.draw()

    def on_mouse_move(pos):
        global mouse_pos
        mouse_pos = pos


    def on_mouse_up(pos):
        dist = (pos[0] - b.pos[0], pos[1] - b.pos[1])
        b.kick(dist, KICK_FORCE ) 


    def on_key_down(key):
        print(key)
        if key == keys.P:
            global _paused
            _paused = not _paused
        elif key == keys.D:
            global _debug
            _debug = not _debug



        
    pgzrun.go()

        


        
        
