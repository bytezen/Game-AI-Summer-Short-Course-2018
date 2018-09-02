from pygame.math import Vector2
from enum import IntEnum
import random
from math import sqrt, pi
import model as Model
import util

# from common.geometry import line_intersection_get_distance_point

import common.transformations as Tx
# import pygame as pg

class Decelaration(IntEnum):
    SLOW = 3.0,
    NORMAL = 2.0,
    FAST = 1.0

class BehaviorType(IntEnum):
    NONE = 0,
    SEEK = 2,
    ARRIVE = 8,
    SEPARATION = 16,
    PURSUIT = 32,
    INTERPOSE = 64

class SteeringBehaviors:
    """
    Class that encapsulates a host of steering behaviors that can be applied to
    an player. Entitiies are of type Actor. See the Actor documentation for how to use
    """
    _model = None

    def __init__(self, player):
        """
            Create a steering behaviors for player. player is expected to be of
            type MovingEntity.
        """
        if SteeringBehaviors._model == None:
            SteeringBehaviors._model = Model.initial_model

        self.player = player
        self.flags = BehaviorType.NONE
        self.separation_multiplier = self._model.player_separation_coefficient
        self.tagged = False
        self.view_distance = self._model.player_view_distance
        self.ball = player.ball
        self.interpose_distance = 0.0
        #unused in original Buckland code
        # self.antenna = [Vector2()] * 5

        # Steering force should always be normalized!!!
        self.steering_force = Vector2()
        self._target = None

    ##                                      ##
    ##                                      ##
    #     convenience methods                #
    ##    to turn on behaviors              ##
    ##                                      ##

    def is_seek_on(self): return self.is_on(BehaviorType.SEEK)
    def seek_on(self) : self.on(BehaviorType.SEEK)
    def seek_off(self) : self.off(BehaviorType.SEEK)

    def is_arrive_on(self): return self.is_on(BehaviorType.ARRIVE)
    def arrive_on(self) : self.on(BehaviorType.ARRIVE)
    def arrive_off(self) : self.off(BehaviorType.ARRIVE)

    def is_separation_on(self): return self.is_on(BehaviorType.SEPARATION)
    def separation_on(self) : self.on(BehaviorType.SEPARATION)
    def separation_off(self) : self.off(BehaviorType.SEPARATION)

    def is_pursuit_on(self): return self.is_on(BehaviorType.PURSUIT)
    def pursuit_on(self) : self.on(BehaviorType.PURSUIT)
    def pursuit_off(self) : self.off(BehaviorType.PURSUIT)

    def is_interpose_on(self): return self.is_on(BehaviorType.INTERPOSE)
    def interpose_on(self) : self.on(BehaviorType.INTERPOSE)
    def interpose_off(self) : self.off(BehaviorType.INTERPOSE)


    ##                                      ##
    ##                                      ##
    #     general turn behaviors on/off      #
    ##                                      ##
    ##                                      ##

    def on(self, behavior):
        self.flags |= behavior

    def off(self, behavior):
        if self.is_on(behavior):
            self.toggle_behavior(behavior)

    def all_off(self):
        self.flags = BehaviorType.NONE

    def is_on(self, behavior):
        return self.flags & behavior > 0

    def toggle_behavior(self, behavior):
        self.flags ^= behavior


    ##                                      ##
    ##                                      ##
    #              Neighbors                 #

    def find_neighbors(self):
        tagged = []
        for player in self._model.players:
            player.steering.untag()
            to = self.player.exact_pos.distance_squared_to( player.exact_pos)

            # print('[steering_behavior.find_neighbors] -- {} {}'.format(player,to),end=' ')

            if to <= ( self.view_distance * self.view_distance ):
                # print('...tagging')
                player.steering.tag()
                tagged.append(player)

        return tagged


    def tag(self):
        self.tagged = True

    def untag(self):
        self.tagged = False

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self,value):
        self._target = Vector2(value)

    ##                                      ##
    ##                                      ##
    #              Force components          #
    ##                                      ##
    ##                                      ##

    def forward_component(self):
        # make sure vector is not zero
        if self.steering_force.length() < 0.001:
            return 0

        norm_steering_force = self.steering_force.normalize()
        fwd = self.player.heading
        # dotprod = norm_steering_force.dot(fwd)
        dotprod = self.steering_force.dot(fwd)

        # print('[SteeringBehaviors.forward_component] side, steering_force ',self.player.heading, self.steering_force)
        
        return dotprod #self.player.heading.dot(self.steering_force.normalize())

    def side_component(self):
        # make sure vector is not zero
        if self.steering_force.length() < 0.001:
            return 0

        norm_steering_force = self.steering_force.normalize()
        side = self.player.side
        dotprod = norm_steering_force.dot(side)

        # print('[SteeringBehaviors.side_component] side . steering_force = {} . {} {}'.format(side, norm_steering_force, dotprod))

        return dotprod

    ##                                      ##
    ##                                      ##
    #              Force Calcuations         #
    ##                                      ##
    ##                                      ##

    def calculate(self):
        self.steering_force *= 0
        self.steering_force = self.sum_forces()


        util.clamp_vector(self.steering_force, 0, self.player.max_force)

        return self.steering_force

    def sum_forces(self):
        force = Vector2()

        if self.is_on(BehaviorType.SEPARATION):
            force += self.separation() * self.separation_multiplier

            print('got here...')
            #DEBUG
            # if self.player.id == 1:
            #     print('[sum_forces]: summing separation force: {}'.format(force.length()))

            if not self.accumulate_force(force):
                #DEBUG
                print('    ...returning separation force because we are over the accumulation limit')

                return self.steering_force

        if self.is_on(BehaviorType.SEEK):
            force += self.seek( self.target )

            if not self.accumulate_force(force):
                return self.steering_force

        if self.is_on(BehaviorType.ARRIVE):
            force += self.arrive( self.target, decelaration = Decelaration.FAST)

            #DEBUG
            # if self.player.id == 1:
            #     print('[sum_forces]: summing arrive force: {}'.format(force.length()))

            if not self.accumulate_force(force):
                #DEBUG
                print('    ...returning arrive force because we are over the accumulation limit')

                return self.steering_force

        if self.is_on(BehaviorType.PURSUIT):
            force += self.pursuit( self.ball())

            if not self.accumulate_force(force):
                return self.steering_force

        if self.is_on(BehaviorType.INTERPOSE):
            force += self.interpose( self.ball(), self.target, self.interpose_distance)

            if not self.accumulate_force(force):
                return self.steering_force

        return force


    def accumulate_force(self, force_to_add):
        magnitude_so_far = self.steering_force.length()
        magnitude_remaining = self.player.max_force - magnitude_so_far

        if magnitude_remaining <= 0.0 :
            return False

        magnitude_to_add = min(force_to_add.length(), magnitude_remaining)

        if magnitude_to_add > 0:
            self.steering_force += force_to_add.normalize() * magnitude_to_add

        return True

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
        desiredVelocity = target - self.player.exact_pos

        if desiredVelocity.length() > 0.0001:
            desiredVelocity.normalize_ip()
            desiredVelocity *= self.player.max_speed

        return desiredVelocity - self.player.velocity


    ## ---------------------------------------------------
    ## Arrive
    ##
    ##
    ##
    def arrive(self,target, decelaration=Decelaration.NORMAL):
        toTarget = target - self.player.exact_pos
        dist = toTarget.length()
        # print('[steering.arrive] distance = ',dist )
        if (dist * dist) > 1.0 :
            decelarationTweak = 0.3
            speed = dist * (decelaration * decelarationTweak )

            # print('[steering.arrive] speed = {}'.format( speed ),end='   ')
            speed = min(speed, self.player.max_speed)
            # print(' clamped speed = {}'.format(speed))

            desiredVelocity = toTarget * ( speed / dist )
            return desiredVelocity - self.player.velocity
        else:
            return Vector2()


    ## ---------------------------------------------------
    ## Pursuit
    ## 
    ##
    ##  
    def pursuit(self, target):
        # vector from us to the evader
        to_target = target.exact_pos - self.player.exact_pos

        # how similar are our headings?
        relative_heading = self.player.heading.dot(target.heading)

        # are we pointed towards the evader?
        is_headed_towards = to_evader.dot(self.player.heading) > 0

        # if we are headedTowards them and they are coming towards them
        # go to their position
        # acos(0.95)= 18 degrees
        if is_headed_towards and relative_heading < -0.95:
            return self.seek(target.exact_pos)

        # if we are here then the evader is not ahead of us
        # we will try to anticipate where they are with a lookahead time
        # the lookahead time is proportional to the distance between the evader
        # and us; (the further we are from one another the further in the future we want
        # to look in order to predict where the evader is going to be
        # it is inversely proportional to the sum of our speed and the evader's speed:
        # the faster we are both moving the shorter the lookahead time (because we
        # will cover more distance in a shorter time since we are going faster.)

        look_ahead_time = to_target.length() / ( self.player.max_speed + target.speed )
        return self.seek(target.exact_pos + target.velocity * look_ahead_time)
 



    ## ---------------------------------------------------
    ## Separation
    ##
    ##
    ##
    def separation(self):
        steering_force = Vector2()
        neighbors = self.find_neighbors()

        #filter out neighbors that are us, or not tagged, or someone that we should be evading
        for n in [n for n in neighbors if n.id != self.player.id and n.tagged]:
                to = self.player.exact_pos - n.exact_pos
                # make the force inversely proportional to the distance squared
                # if the distance is small then distance * distance will be even smaller
                # divide a constant by this distance squared factor number to get the force
                d = to.length_squared()
                if d > 0:
                    steering_force +=  to * ( self._model.player_separation_coefficient /  to.length_squared() )

        return steering_force

    ## ---------------------------------------------------
    ## Interpose
    ## 
    ##
    ##       
    def interpose(self, target1, target2, dist_from_target):
        
        # first we need to figure out where the two agents are going to be at time T in the future.
        # This is approximated by determining the time taken to reach the mid way point at the
        # current time at max speed

        mid_point = (target1.exact_pos + target2.exact_pos ) * 0.5
        time_to_reach_mid_point =   (player.exact_pos.distance_to( mid_point) ) / player.max_speed

        future1 = target1.exact_pos + target1.velocity * time_to_reach_mid_point
        future2 = target2.exact_pos + target2.velocity * time_to_reach_mid_point

        mid_point = (future1 + future2) * 0.5

        return self.arrive(mid_point,Decelaration.FAST)


    def render_aids(self,surface):
        player = self.player

        # Render Steering Force
        if world.show_steering_force:
            pass

