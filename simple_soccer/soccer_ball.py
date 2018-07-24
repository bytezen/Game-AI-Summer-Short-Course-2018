from entity import MovingEntity
from model import Model

from pygame.math import Vector2
import math
import random
import geometry


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
##            print('  dist_to_wall= ', dist_to_wall, '  intersection_pt = ', intersection_point)
            if screen != None:
                obj.display_list.append((screen.draw.filled_circle, [intersection_point,5,'yellow']) )           
            
        else:
            dist_to_wall = geometry.distance_to_ray_plane_intersection(_collision,
                                                                       normal_vel,
                                                                       w.a,
                                                                       w.normal)
            intersection_point = _collision +  (dist_to_wall * normal_vel)
            if screen != None:
                obj.display_list.append((screen.draw.circle, [intersection_point,5,'red']) )               

        on_line_segment = False

        if geometry.line_intersection(w.b, w.a,
                                      _collision - w.normal * 20.0,
                                      _collision + w.normal * 20.0
                                      ):
            obj.display_list.append( (screen.draw.line, [_collision - w.normal * 20.0,
                                                          _collision + w.normal * 20.0,
                                                         'purple']))
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
        print('....reflecting!!!!! ')
        obj.velocity.reflect_ip( walls[idx_closest].normal)
    

class Ball(MovingEntity):
    def __init__(self,boundary,**kwargs):
        super().__init__('ball',**kwargs)
        print(kwargs)
        self.pitch_boundary = boundary
        self.model = kwargs['model']

        self.display_list = []

    def update(self,dt):
        if _paused:
            return

        del self.display_list[:]
        self.prev_pos = self.pos

##        test_wall_collision(self,self.pitch_boundary,screen)

        if self.velocity.length_squared() > self.model.friction * self.model.friction:
            self.velocity -= self.velocity * self.model.friction * dt
            self.pos += self.velocity

        test_wall_collision(self,self.pitch_boundary,screen)            

    def draw(self):
        super().draw()
        if len(self.display_list) > 0:
            for f,ps in self.display_list:
                f(*ps)
                                    
        
    def kick(self, direction, force):
        accel = Vector2(direction).normalize() * force / self.mass
        # update the velocity
        self.velocity = accel

    
    def handle_message(self,msg):
        return false

    def time_to_cover_distance(time, phrom, to, force):
        pass

    def future_position(self, time):
        pass

    def trap(self):
        self.velocity *= 0

    def place_at_position(self, value):
        self.pos = value

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

    walls = wall.walls_from_rect(boundary)
    b = Ball(walls,model=Model.instance())
    b.pos = Vector2(WIDTH *0.5, HEIGHT * 0.5)

    mouse_pos = None
    _paused = _debug = False
    
    def update(dt):
        b.update(dt)
        
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
        b.kick(dist, 5 ) 
        print(pos)

    def on_key_down(key):
        print(key)
        if key == keys.P:
            global _paused
            _paused = not _paused
        elif key == keys.D:
            global _debug
            _debug = not _debug



        
    pgzrun.go()

        


        
        
