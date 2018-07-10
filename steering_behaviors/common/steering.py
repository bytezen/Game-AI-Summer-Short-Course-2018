from pygame.math import Vector2
from enum import IntEnum
from random import random
from math import sqrt, pi
import sys

from common.params import ObstacleAvoidanceParams, WallAvoidanceParams, WanderParams, BehaviorParams
from common.behavior import Behavior
from common.geometry import line_intersection_get_distance_point

import common.transformations as Tx
import pygame as pg

import pygame.gfxdraw
import pgzrun

##class Behavior(IntEnum):
##    NONE = 0,
##    SEEK = 2,
##    FLEE = 4,
##    ARRIVE = 8,
##    WANDER = 16,
##    COHESION = 32,
##    SEPARATION = 64,
##    ALIGNMENT = 128,
##    OBSTACLE_AVOIDANCE = 256,
##    WALL_AVOIDANCE = 512,
##    FOLLOW_PATH = 1024,
##    PURSUIT = 2048,
##    EVADE = 4096,
##    INTERPOSE = 8192,
##    HIDE = 16384,
##    FLOCK = 32768,
##    OFFSET_PURSUIT = 65536
    
class Decelaration(IntEnum):
    SLOW = 3.0,
    NORMAL = 2.0,
    FAST = 1.0

##class Params:
##    jitter = 5.0
##    radius = 50.0
##    distance = 50.0
##    target = Vector2(0,-1)
    
class SteeringBehaviors:
    def __init__(self, entity):
        """
            Create a steering behaviors for entity. Entity is expected to be of
            type MovingEntity.
            
        """
        self._entity = entity
        self._steering_force = Vector2()
        self._flags = Behavior.NONE

        self.wander_params = WanderParams()
        self.obstacle_params = ObstacleAvoidanceParams()
        self.wall_params = WallAvoidanceParams()
        self.behavior_params = BehaviorParams()

        self.feelers = [0,0,0]
        self.path = None
        

    def calculate(self):
        self._steering_force *= 0

        if self.is_on(Behavior.SEEK):
            self._steering_force += self.seek( self._entity.world.crosshair )

        if self.is_on(Behavior.ARRIVE):     
            self._steering_force += self.arrive( self._entity.world.crosshair)

        if self.is_on(Behavior.FLEE):             
            self._steering_force += self.flee( self._entity.world.crosshair)
            
        if self.is_on(Behavior.PURSUIT):                  
            self._steering_force += self.pursuit( self._entity.pursuit_target )
            
        if self.is_on(Behavior.EVADE):             
            self._steering_force += self.evade( self._entity.evade_target )

        if self.is_on(Behavior.WANDER):                  
            self._steering_force += self.wander()

        if self.is_on(Behavior.OBSTACLE_AVOIDANCE):
            self._steering_force += self.obstacle_avoidance( self._entity.world.obstacles )
            
        if self.is_on(Behavior.WALL_AVOIDANCE):
            self._steering_force += self.wall_avoidance( self._entity.world.walls )

        if self.is_on(Behavior.INTERPOSE):
            self._steering_force += self.interpose( *self._entity.targets )

        if self.is_on(Behavior.HIDE):
            self._steering_force += self.hide( self._entity.hunter, self._entity.world.obstacles )

        if self.is_on(Behavior.FOLLOW_PATH):
            self._steering_force += self.follow_path( self.path )
            
        return self._steering_force

    def on(self, behavior):
        self._flags |= behavior

    def off(self, behavior):
        if self.is_on(behavior):
            self.toggle_behavior(behavior)

    def all_off(self):
        self._flags = Behavior.NONE
            
    def is_on(self, behavior):
        return self._flags & behavior > 0
        
    def toggle_behavior(self, behavior):
        self._flags ^= behavior


    ##                                      ##
    ##                                      ##
    #             Behavior methods           #
    ##                                      ##
    ##                                      ##
    

    ## ---------------------------------------------------
    ## Seek
    ## 
    ##
    ##      
    def seek(self,target):
        desiredVelocity = target - self._entity.exact_pos
        
        if desiredVelocity.length() > 0.0001:
            desiredVelocity.normalize_ip()
            desiredVelocity *= self._entity.max_speed

        return desiredVelocity - self._entity.velocity


    ## ---------------------------------------------------
    ## Arrive
    ## 
    ##
    ##  
    def arrive(self,target, decelaration=Decelaration.NORMAL):
        toTarget = target - self._entity.exact_pos
        dist = toTarget.length()
##        print(dist * dist)
        if (dist * dist) > 1.0 :
            decelarationTweak = 0.3
            speed = dist * (decelaration * decelarationTweak )

            speed = min(speed, self._entity.max_speed)

            desiredVelocity = toTarget * ( speed / dist )
            return desiredVelocity - self._entity.velocity
        else:
            return Vector2()



    ## ---------------------------------------------------
    ## Flee
    ## 
    ##
    ##  
    def flee(self,target):
        desiredVelocity = self._entity.exact_pos - target
        
        if desiredVelocity.length() > 0.0001:
            desiredVelocity.normalize_ip()
            desiredVelocity *= self._entity.max_speed

        return desiredVelocity - self._entity.velocity
        

    ## ---------------------------------------------------
    ## Pursuit
    ## 
    ##
    ##  
    def pursuit(self, evader):
        # vector from us to the evader
        to_evader = evader.exact_pos - self._entity.exact_pos

        # how similar are our headings?
        relative_heading = self._entity.heading.dot(evader.heading)

        # are we pointed towards the evader?
        is_headed_towards = to_evader.dot(self._entity.heading) > 0

        # if we are headedTowards them and they are coming towards them
        # go to their position
        # acos(0.95)= 18 degrees
        if is_headed_towards and relative_heading < -0.95:
            return self.seek(evader.exact_pos)

        # if we are here then the evader is not ahead of us
        # we will try to anticipate where they are with a lookahead time
        # the lookahead time is proportional to the distance between the evader
        # and us; (the further we are from one another the further in the future we want
        # to look in order to predict where the evader is going to be
        # it is inversely proportional to the sum of our speed and the evader's speed:
        # the faster we are both moving the shorter the lookahead time (because we
        # will cover more distance in a shorter time since we are going faster.)

        look_ahead_time = to_evader.length() / ( self._entity.max_speed + evader.speed )
        return self.seek(evader.exact_pos + evader.velocity * look_ahead_time)

    ## ---------------------------------------------------
    ## Evade
    ## 
    ##
    ##  
    def evade(self, pursuer):
        entity = self._entity
        to_pursuer = pursuer.exact_pos - entity.exact_pos

        #Threat Range; uncomment to have agent only pursue entities within range
        threat_range = BehaviorParams.threat_scan_distance or 10000
        
        if to_pursuer.length_squared() > (threat_range * threat_range):
            return Vector2()

        look_ahead_time = to_pursuer.length() / ( entity.max_speed + pursuer.speed )
        return self.flee( pursuer.pos + ( pursuer.velocity * look_ahead_time ) )



    ## ---------------------------------------------------
    ## Wander
    ## 
    ##
    ##   
    def wander(self):
        entity = self._entity

        params = self.wander_params

        ## from M.Buckland:
        ## this behavior is dependent on the update rate, so this line must
        ## be included when using time independent framerate.        
##        jitter_this_time_slice = params.jitter * entity.time_elapsed

        jitter_this_time_slice = params.jitter
        
        randomVec = Vector2( (random()*2.0-1.0) * jitter_this_time_slice, \
                             (random()*2.0-1.0) * jitter_this_time_slice )

        params.target += randomVec

        # project the target onto a point on the unit circle
        params.target.normalize_ip()

        # increase the length of the vector to the same radius
        # of the wander circle
        params.target *= params.radius

        
        # move the wander circle in front of us
        target = params.target + Vector2(params.distance,0)

        # tramsform the target into world coordinates
        target.rotate_ip(entity.angle)


        return target


    ## ---------------------------------------------------
    ## Obstacle Avoidance
    ## 
    ##
    ##       
    def obstacle_avoidance(self, obstacles):
        params = self.obstacle_params
        entity = self._entity
        steering_force = Vector2()
        
        self.d_box_length = params.min_detection_box_length
        # the scale of the box length is dependent on our max_speed ratio
        speed_ratio = entity.speed / entity.max_speed
        self.d_box_length = self.d_box_length + speed_ratio * self.d_box_length

        #tag obstacles that are within range of our detection box
        entity.world.tag_obstacles_in_view_range( entity, obstacles, self.d_box_length )

##        closest_intersecting_obstacle
        closest_obstacle = None
        
        # track the distance to the cib
        dist_to_closest_intersection_point = 1000000

        local_pos_of_closest_obstacle = Vector2()

        for o in entity.world.obstacles:
            if o.tagged:
##                point, agent_heading, agent_side, agent_position):                
                local_pos = Tx.point_to_local_space(o.exact_pos,
                                                    entity.heading,
                                                    entity.side,
                                                    entity.exact_pos)

                # if local_pos is less than 0 it is behind us so we can ignore it
                if local_pos.x >= 0:
                    # if the distance from the x axis to the object's position is
                    # less than its radius + half the width of the detection box then
                    # there is a potential intersection
                    expanded_radius = o.bounding_radius + entity.bounding_radius

                    if abs(local_pos.y) < expanded_radius:
                        # now do a line/circle intersection test. The center of the circle
                        # is (cx,cy) The intersection points are
                        # given by the formula x = cx +/- sqrt(r^2 - cy^2) for y = 0.
                        # We only need to look at the smallest positive value of x because
                        # that will be the closest point of intersection
                        cx = local_pos.x
                        cy = local_pos.y                        
                        sqrt_part = sqrt(expanded_radius * expanded_radius - cy * cy)

                        ip = cx - sqrt_part

                        if ip <= 0.0:
                            ip = cx + sqrt_part

                        # if this intersection point is smaller thatn our current closest
                        # then update our tracking variables with the information for this
                        # obstacle
                        if ip < dist_to_closest_intersection_point:
                            dist_to_closest_intersection_point = ip
                            closest_obstacle = o
                            local_pos_of_closest_obstacle = local_pos


        # if we have an object that is closest (i.e. within range)
        if  closest_obstacle != None:
            # the closer the actor is to the object, the stronger the
            # steering force should be
            multiplier = 1.0 + ( self.d_box_length - local_pos_of_closest_obstacle.x) / self.d_box_length

            #calculate the lateral force
            steering_force.y = multiplier * \
                               (closest_obstacle.bounding_radius - local_pos_of_closest_obstacle.y)

            #apply a braking force proportional to the obstacle's distance from the vehicle
            braking_weight = 0.2

            steering_force.x = braking_weight * \
                               (closest_obstacle.bounding_radius - local_pos_of_closest_obstacle.x)

        #convert the steering force from local to world space
        return Tx.vector_to_world_space(steering_force, entity.heading, entity.side)

    ## ---------------------------------------------------
    ## Wall Avoidance
    ## 
    ##
    ##       
    def wall_avoidance(self, walls):
        self.create_feelers()
        entity = self._entity
        ## variables for keeping track of the information as we
        ## iterate through the list of walls
        # dist to intersection point
        dist_ip = 0
        dist_to_closest_ip = 1000000

        closest_wall = None

        steering_force = Vector2()
        point = Vector2()
        closest_point = Vector2()


        # for each feeler
        # find the closest wall
##        intersecting_walls = [ wall for feeler, wall in feelers,walls if line_intersection()]

        for feeler in self.feelers:
            for wall in walls:
                intersecting,_dt,_pt = line_intersection_get_distance_point(entity.exact_pos,
                                                                            feeler,
                                                                            wall.phrom,
                                                                            wall.to)

                if intersecting:
                    if _dt < dist_to_closest_ip:
                        dist_to_closest_ip = _dt
                        closest_wall = wall
                        closest_point = _pt
            # if we found a wall then calculate a steering force based on how far
            # the feeler cut into the wall
            if closest_wall != None:
                over_shoot = feeler - closest_point
                steering_force = wall.normal * over_shoot.length() * self.wall_params.repel_multiplier
        
        return steering_force

    ## ---------------------------------------------------
    ## Interpose
    ## 
    ##
    ##       
    def interpose(self, *agents):
        assert len(agents) >= 2, 'need to pass in at least 2 agents, suckah' + str(len(agents))
        target1,target2 = agents[:2]
        entity = self._entity
        
        # first we need to figure out where the two agents are going to be at time T in the future.
        # This is approximated by determining the time taken to reach the mid way point at the
        # current time at max speed

        mid_point = (target1.exact_pos + target2.exact_pos ) * 0.5
        time_to_reach_mid_point =   (entity.exact_pos.distance_to( mid_point) ) / entity.max_speed

        future1 = target1.exact_pos + target1.velocity * time_to_reach_mid_point
        future2 = target2.exact_pos + target2.velocity * time_to_reach_mid_point

        mid_point = (future1 + future2) * 0.5

        return self.arrive(mid_point,Decelaration.FAST)


    ## ---------------------------------------------------
    ## Hide
    ## 
    ##
    ##       
    def hide(self, hunter, obstacles):
        entity = self._entity
        world = self._entity.world

        # record keeping variables
        dist_to_closest = sys.float_info.max
        best_hiding_spot = None
        closest_obstacle = None

        for o in world.obstacles:
            hiding_spot = self.get_hiding_position( o.exact_pos, o.bounding_radius, hunter.exact_pos )
            dist = entity.exact_pos.distance_to( hiding_spot )
            if dist < dist_to_closest:
                best_hiding_spot = hiding_spot
                closest_obstacle = o
                dist_to_closest = dist

        if dist_to_closest == sys.float_info.max:
            return self.evade(hunter)

        return self.arrive(best_hiding_spot,Decelaration.FAST)


    def get_hiding_position(self, blocking_obj_pos, blocking_obj_bounding_radius, baddie_pos, spacing_from_obj = 30): 
        """
        Given the position of a hunter, and position and bounding radius of an obstacle, this method
        finds the position that puts the boundary between its location and the hunter
        """
        # calculate the spacing 
        dist_away = blocking_obj_bounding_radius + spacing_from_obj

        # calculate the heading from the object to the hunter
        to = (blocking_obj_pos - baddie_pos).normalize()
        
        # scale the distance
        return (blocking_obj_pos) + to * dist_away



    ## ---------------------------------------------------
    ## Follow Path
    ## 
    ##
    ##       
    def follow_path(self, path):
        entity = self._entity
        if entity.exact_pos.distance_to( self.path.current_way_point ) < \
            BehaviorParams.path_follow_scan_distance:

                self.path.next()

        if self.path.at_end():
            return self.seek(self.path.current_way_point)
        else:
            return self.arrive(self.path.current_way_point, Decelaration.NORMAL)
        
    
    ## ---------------------------------------------------
    ## Create Feelers
    ## 
    ##       
    def create_feelers(self):
        entity = self._entity
        fl = self.wall_params.detection_feeler_length
        
        self.feelers[0] = entity.exact_pos + fl * entity.heading
        
        temp = entity.heading.rotate( -50) #3.5 * 0.5 * pi)
        self.feelers[1] = entity.exact_pos + fl * 0.95 * temp
        
        temp = entity.heading.rotate( 50 ) #0.5 * pi)
        self.feelers[2] = entity.exact_pos + fl * 0.95 * temp
        
        

    

    def render_aids(self,surface):
        entity = self._entity
        world = entity.world

        # Render Steering Force
        if world.show_steering_force:
            pass

        # Render Wander if relevant     
        if world.show_wander_circle \
           and self.is_on(Behavior.WANDER):

            params = self.wander_params

            #get the wander circle center in world coordinates
            wander_center = Vector2(params.distance,0)
            wander_center.rotate_ip(self._entity.angle)
            wander_center += self._entity.exact_pos
                        
            # draw the wander cirle
            pygame.gfxdraw.aacircle(surface, \
                                    int(wander_center.x),
                                    int(wander_center.y),
                                    int(self.wander_params.radius),
                                    (255,0,0))
        

            #draw the wander target
            wander_target = self.wander_params.target.rotate(self._entity.angle)
            wander_target += wander_center #self._entity.exact_pos
            pygame.gfxdraw.filled_circle(surface,
                                         int(wander_target.x),
                                         int(wander_target.y),
                                         5,
                                         (255,255,0))

        # Render Detection Box if relevant

        #only for main vehicle
        if entity.is_behavior_on(Behavior.OBSTACLE_AVOIDANCE) and world.show_detection_box: # and self.id == 0:
            minLen = ObstacleAvoidanceParams.min_detection_box_length
            # the length is a function of how fast we are going
            # the closer we get to maximum speed the longer the length

            # calculate the verts for the detection box in local space coordinates, relative
            # to the vehicle of interest
            if entity.max_speed > 0:
                speed_ratio = entity.speed / entity.max_speed
            else:
                speed_ratio = 1.0
                
            length = minLen + (minLen * speed_ratio )
            tl = Vector2( 0, -entity.bounding_radius )
            tr = tl + Vector2(length, 0)
            br = tr + Vector2(0, 2 * entity.bounding_radius)
            bl = br - Vector2(length, 1)
            close = bl + Vector2(0,-2 * entity.bounding_radius)

            #get rectangle in world space coordinates for rendering

                        
            rect_verts_world_space = Tx.point_to_world_space([tl,tr,br,bl],
                                                             entity.exact_pos,
                                                             entity.heading,
                                                             entity.side
                                                             )
                
            pygame.gfxdraw.aapolygon( surface, rect_verts_world_space, (0,200,0))


        # wall_avoidance aids
        if entity.is_behavior_on(Behavior.WALL_AVOIDANCE):
            if world.show_feelers:
                for feeler in self.feelers:
                    pygame.gfxdraw.line( surface,
                                           int(entity.exact_pos.x),
                                           int(entity.exact_pos.y),
                                           int(feeler.x),
                                           int(feeler.y),
                                           pg.Color("orange"))
        
            if world.show_walls:
                for wall in world.walls:
                    if world.show_wall_normals:
                        wall.draw_with_normals(surface)
                    else:
                        wall.draw(surface)

        if entity.is_behavior_on(Behavior.FOLLOW_PATH):
            if world.show_path:
                self.path.draw(surface)



                    
