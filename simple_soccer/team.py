from field_player import GoalKeeper, FieldPlayer

import player_states as PState
import team_state as TeamState
from soccer_pitch import SoccerPitch
from support_spot_calculator import SupportSpotCalculator
from fsm import StateMachine
from pygame.math import Vector2
import pygame as pg
import pgzero.screen

import model 

import sys

HOME = 'HOME'
AWAY = 'AWAY'

class View:

    WIDTH = 600
    HEIGHT = 50
    BG_COLOR = pg.Color('aliceblue')
    BORDER_COLOR = pg.Color('khaki')
    POS = Vector2(100,0)

    def __init__(self, display_model):
        self.show_model = display_model
        self.data_model = None
        self._screen = pgzero.screen.Screen(pg.Surface(( 600, 50 )))
        self._screen.surface.get_rect().center = (400, 30)
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
        c = 'blue' if self.data_model.home_team else 'red'

        # Only show the controlling, supporting and possession display stuff
        if self.data_model.in_control is True:

            # show the controlling team and player at the top of the display
            if self.show_model.show_controlling_team and self.data_model.in_control :
                _s.draw.text(self.team_model.team + ' in control ')

            if self.data_model.controlling_player != None:
                _s.draw.text('Controlling Player: ' + self.data_model.controlling_player.pId, color=c)
            # show supporting players target
            if self.show_model.show_supporting_player_targets:
                if self.data_model.supporting_player != None:
                    screen.draw.circle( self.data_model.support_player.steering.target, 5,color=c  )

            # render the sweet spots
            if self.show_model.show_support_spots:
                self.data_model.support_spot_calculator.render()


        # show the team state
        if self.show_model.show_team_state:
            _s.draw.text('team state: ' + str(self.data_model.fsm.current_state),
                         (30,10),
                         color=c)

        # self._screen.draw()
        screen.blit(self._screen.surface, self.pos)


class SoccerTeam:

    def __init__(self, side, pitch, display_model=model.initial_model, entity_manager=model.initial_model.entity_manager, dispatcher=model.initial_model.dispatcher):
        # self.model = model
        self.pitch = pitch
        self.view = View(display_model)
        self.view.model = self
        self.side = side
        self._entity_manager = entity_manager
        self._dispatcher = dispatcher

        if side == HOME:
            self.color = pg.Color('red')
            self.goal = self.pitch.home_goal
            self.opponent_goal = self.pitch.away_goal
            self.init_heading = Vector2(-1,0)

        elif side == AWAY:
            self.color = pg.Color( 'blue' )
            self.goal = self.pitch.away_goal
            self.opponent_goal = self.pitch.home_goal
            self.init_heading = Vector2(1,0)

        else:
            raise ValueError ( "side must be either 'HOME' or 'AWAY' " )

        self.players = self.create_players()
        self.opponent = None

        self._controlling_player = None
        self._supporting_player = None
        self._receiving_player = None
        self.player_closest_to_ball = None

        self.dist_sq_to_ball_from_closest_player = sys.float_info.max
        self.support_spot_calculator = SupportSpotCalculator()
        self.fsm = StateMachine(self)
        self.fsm.current_state = TeamState.prepare_for_kickoff
        self.fsm.previous_state = TeamState.prepare_for_kickoff
        self.fsm.global_state = None 

    def __call__(self):
        return self.players

    def create_players(self):
        players = []

        if self.home_team:
            regions = [self.pitch.pos_from_region(region) for region in [11,16,15,4,3] ]
        else:
            regions = [self.pitch.pos_from_region(region) for region in [1,6,8,3,5] ]

        # goal keeper
        if self.side == HOME:
            image_file = 'redshirt'
        else:
            image_file = 'blueshirt'


        players.append( GoalKeeper(image_file+'0',
                                   self.pitch,
                                   team = self,
                                   home = regions[0],
                                   heading = self.init_heading
                                   ) )

        # rest of the team
        for idx, region in enumerate(regions[1:]):
            player = FieldPlayer(image_file + str(idx),
                                 self.pitch,
                                 team = self,
                                 home= region,
                                 heading=self.init_heading
                                 ) 

            players.append( player )
            if idx == 0:
                player.pos = (400, 300)

        return players



    def calculate_closest_player_to_ball(self):
        closest_so_far = sys.float_info.max
        print('distances to closes player', self.players)

        print('this is the ball position: ', self.pitch.ball() )
        distances = [ p.exact_pos.distance_to( self.pitch.ball() ) for p in self.players ]

        return min(distances)

    def draw(self,screen):
        for player in self.players:
            player.draw()

        self.view.draw(screen)


    def update(self,dt):
        #calculate this once per frame
        self.calculate_closest_player_to_ball()

        #the team state machine switches between attack/defense behavior. It
        #also handles the 'kick off' state where a team must return to their
        #kick off positions before the whistle is blown
        self.fsm.update()

        #update each player
        for player in self.players:
            player.update(dt)


    def return_all_field_players_home(self):
        for player in self.players:
            dispatcher.dispatch_message(Message.SEND_MSG_IMMEDIATELY,
                                        -1,player.id,Message.GO_HOME,None)

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
        return all( [p.at_home for p in self.players])

    
    @property
    def home_team(self):
        return self.side == HOME

    @property
    def away_team(self):
        return self.side == AWAY

    @property
    def in_control(self):
        return self.controlling_player != None

    @property
    def receiving_player(self):
        return self._receiving_player

    @receiving_player.setter
    def receiving_player(self, player):
        self._receiving_player = player

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




if __name__ == '__main__':
    import pgzrun
    import soccer_pitch
    import team
    import model as Model
    import field_player

    WIDTH = 800
    HEIGHT = 600

    #initialize the parameters
    model = Model.initial_model

    field_player.BasePlayer.initialize_class_parameters(max_speed_with_ball = model.player_max_speed_with_ball,
                                                        receiving_range = model.player_receiving_range)

    mock_pitch = soccer_pitch.SoccerPitch(WIDTH,HEIGHT)

    home_team = team.SoccerTeam( HOME, mock_pitch )
    away_team = team.SoccerTeam( AWAY, mock_pitch )
    home_team.opponent = away_team
    away_team.opponent = home_team

    def update(dt):
        home_team.update(dt)

    def draw():
        mock_pitch.draw(screen)
        home_team.draw(screen) 

    pgzrun.go()

