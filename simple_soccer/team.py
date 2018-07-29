from player import PlayerBase, GoalKeeper, FieldPlayer
from support_spot_calculator import SupportSpotCalculator
from fsm import StateMachine
from pygame.math import Vector2
import pygame as pg
import pgzero.screen

import sys

HOME = 'home'
AWAY = 'away'

class SoccerTeam:

    def __init__(self, display_model, pitch, side ):
        # self.model = model
        self.pitch = pitch
        self.view = View(display_model)
        self.view.model = self

        if side == HOME:
            self.color = pg.Color('red')
            self.goal = self.pitch.home_goal
            self.opponent_goal = self.pitch.away_goal
            self.init_heading = Vector2(-1,0)

        else:
            self.color = pg.Color( 'blue' )
            self.goal = self.pitch.away_goal
            self.opponent_goal = self.pitch.home_goal
            self.init_heading = Vector2(1,0)

        self.players = []
        self.opponents = []

        self._controlling_player = None
        self._supporting_player = None
        self.receiving_player = None
        self.player_closest_to_ball = None

        self.dist_sq_to_ball_from_closest_player = sys.float_info.max
        self.support_spot_calculator = SupportSpotCalculator()
        self.fsm = StateMachine(self)



    def create_players(self):

        if self.side == HOME:
            regions = [16,9,11,12,14]
        else:
            regions = [1,6,8,3,5]

        # goal keeper
        self.players.append( GoalKeeper(home=regions[0]
                                        , init_state = State.wait) )

        for region,img in regions[1:],player_images:
            player = FieldPlayer(img,
                                 region,
                                 Vector2(-1,0),
                                 Vector2(self.init_heading),
                                 init_state = State.wait 
                                 ) 

            self.model.entityManager.register_entity(player)
            self.players.append( player )


    def calculate_closest_player_to_ball(self):
        closest_so_far = sys.float_info.max

        distances = [ p.pos.distance_to( self.pitch.ball ) for p in self.players ]


    def draw(self,screen):
        for player in self.players:
            player.draw(screen)

        self.view.draw(screen)


    def update(self):
        #calculate this once per frame
        self.calculate_closest_player_to_ball()

        #the team state machine switches between attack/defense behavior. It
        #also handles the 'kick off' state where a team must return to their
        #kick off positions before the whistle is blown
        self.fsm.update()

        #update each player
        for player in players:
            player.update()


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

    def set_player_home_region(self, player, region):
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
        else:
            return 'Blue'

class View:

    WIDTH = 600
    HEIGHT = 50
    BG_COLOR = pg.Color('aliceblue')
    BORDER_COLOR = pg.Color('khaki')
    POS = Vector2(0,0)


    def __init__(self, display_model):
        self.show_model = display_model
        self.data_model = None
        self._screen = pgzero.screen.Screen(pg.Surface(( View.WIDTH, View.HEIGHT )))
        self._screen.fill((100,100,100))

        self.pos = View.POS

        rect = self._screen.surface.get_rect().inflate(-2,-2)
        # pg.draw.rect(self._screen, (100,0,0), rect, 2)
        self._screen.draw.rect(rect, (100,0,0))

    @property
    def model(self):
        pass

    @model.setter
    def model(self, model):
        self.data_model = model

    def draw(self,screen):
        _s = self._screen


        Only show the controlling, supporting and possession display stuff
        if the data_model.in_control is True

        # show the controlling team and player at the top of the display
        if self.show_model.show_controlling_team and self.data_model.in_control :
            _s.draw.text:(self.team_model.team + ' in control ')

        if self.data_model.controlling_player != None:
            _s.draw.text('Controlling Player: ' + self.data_model.controlling_player.pId)
        # show supporting players target
        if self.show_model.show_supporting_player_targets:
            if self.data_model.supporting_player != None:
                screen.draw.circle( self.data_model.support_player.steering.target, 5 )

        # render the sweet spots
        if self.show_model.show_support_spots and self.data_model.in_control():
            self.data_model.support_spot_calculator.render()


        This gets rendered if the flag is true regardless of the possession state
        of the team

        # show the team state
        if self.show_model.show_team_state:
            _s.draw.text(str(self.data_model.fsm.current_state), (30,10), color=self.data_model.color[:3])

        # self._screen.draw()
        screen.blit(self._screen.surface, self.pos)





# if __name__ == '__main__':
#     import pgzrun
#     import soccer_pitch

#     WIDTH = 800
#     HEIGHT = 600

#     mock_pitch = soccer_pitch.SoccerPitch(WIDTH,HEIGHT)

#     team = SoccerTeam( mock_pitch, HOME)

#     def draw():
#         mock_pitch.draw(screen)
#         team.draw(screen) 

#     pgzrun.go()

