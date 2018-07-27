from soccer_pitch import Goal, SoccerPitch
from player import PlayerBase, GoalKeeper, FieldPlayer
from support_spot_calculator import SupportSpotCalculator
from fsm import StateMachine

import sys

HOME = 'home'
AWAY = 'away'

class SoccerTeam:
    
    def __init__(self, pitch, side ):
        if side == HOME:
            self.color = 'red'
            self.goal = self.pitch.home_goal
            self.opponent_goal = self.pitch.away_goal
            
        else:
            self.color = 'blue'
            self.goal = self.pitch.away_goal
            self.opponent_goal = self.pitch.home_goal

        self.players = []
        self.opponents = []

        self._controlling_player = None
        self._supporting_player = None
        self.receiving_player = None
        self.player_closest_to_ball = None

        self.dist_sq_to_ball_from_closest_player = sys.float_info.max
        self.support_spot_calculator = SupportSpotCalculator()


    def create_players(self):

        if self.side == HOME:
            regions = [16,9,11,12,14]
        else:
            regions = [1,6,8,3,5]

        # goal keeper
        self.players.append( GoalKeeper(home=regions[0]
                                        , init_state = State.wait) )

        for region in regions[1:]:
            player = FieldPlayer(home=region,
                                             init_state = State.wait,
                                             heading = Vector2(-1,0),

                                             ,) )
                                             ,) )
                                             ,) )
                                             ,) )

            self.model.entityManager.register_entity(player)
            self.players.append( player )


    def calculate_closest_player_to_ball(self):
        pass

    def draw(self,screen):
        pass

    def update(self):
        pass

    def return_all_field_players_home(self):
        pass

    def can_shoot(self, ball_pos, power, shot_target = Vector2()):
        pass

    def find_pass(self, passer, receiver, pass_target, power, min_passing_distance):
        pass

    def get_best_pass_to_receiver(self, passer, receiver, pass_target, power):
        pass

    def is_pass_safe_from_opponent(self, phrom, target, receiver, opp, passing_force):
        pass

    def is_pass_safe_from_all_opponents(self, phrom, target, receiver, passing_force):
        pass

    def is_opponent_within_radius(self, pos, radius):
        pass

    def request_pass(self, requester):
        pass

    def determine_best_supporting_attacker(self):
        pass

    def get_support_spot(self):
##        return self.support_spot_calculater.get_best_spot()
        pass    

    def get_player_from_id(self, player_id):
        pass

    def set_player_home_region(self, player, region)
        pass

    def determine_best_supporting_position(self):
        return self.support_spot_calculator.determine_best_supportin
        pass

    def update_targets_of_waiting_players(self):
        pass

    def all_players_at_home(self):
        pass
    
    @property
    def in_control(self):
        return self.controlling_player != None

    @property
    def controlling_player(self):
        return self._controlling_player

    @controlling_player.setter
    def controlling_player(self, player):
        self._controlling_player = player
            
    @property
    def supporting_player(self):
        return self._supporting_player

    @supporting_player.setter
    def supporting_player(self, player):
        self._supporting_player = player
        self.opponents.lost_control()

    

    def __repr__(self):
        if self.color == 'red':
            return 'Red'
        else self.color == 'blue'
            return 'Blue'
        

    


            
        
