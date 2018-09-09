import message
import entity_manager

def get_class_attribute_map(cls):
    _ATTR_MAP[cls] = [prop for prop in dir(cls) if not prop.startswith('__')]
    return [ (cls, prop) for prop in dir(cls) if not prop.startswith('__') ]

def add_player(model,player):
    model.players.append(player)

class Window:
    pass

class MenuItem:
    pass


class Display:

    # display view parameters
    show_team_states = False
    show_player_states = True
    show_ids = False
    show_support_spots = False
    show_regions = True
    show_controlling_team = False
    show_supporting_player_targets = False
    show_highlight_when_threatened = False
    show_frame_rate = False
    show_steering_force = True
    steering_force_display_length = 50
    # state of the team displayed on screen
    show_team_state = True 
    show_heading = True


class Params:
    goal_width = 100
    num_sweet_spots_x = 13
    num_sweet_spots_y = 6
    spot_can_pass_score = 2
    spot_can_score_from_position_score = 1
    spot_dist_from_controlling_player_score = 1
    spot_closeness_to_supporting_player_score = 0
    spot_ahead_of_attacker_score = 0
    #how many times per second the support spots will be calculated
    support_spot_update_freq = 1
    chance_player_attempts_pot_shot = 0.005
    chance_of_using_arrive_type_receive_behavior = 0.5
    ball_size = 5.0
    ball_mass = 1.0
    friction = -0.015 #0.95 #0.015

    # goalkeeper has to be this close to the ball in order to interact with it
    keeper_in_ball_range = 10
    player_in_target_range = 10

    # the player has to be this close to the ball to be able to kick it. The higher the value this gets, the easir it gets to tackle.
    player_kicking_distance = 6.0
    player_kick_frequency = 8 

    player_mass = 3.0
    player_max_force = 1.0
    player_max_speed_with_ball = 1.2
    player_max_speed =  3.6
    player_max_turn_rate = 5 #0.4 
    player_scale = 1.0

    # when an opponent comes within this range the player will attempt to pass the ball. Players tend to pass more often, the higher the value
    player_comfort_zone = 60

    player_kicking_accuracy = 0.99

    # the number of times the soccerTeam.can_shoot method attempst to find a valid shot
    num_attempts_to_find_valid_strike = 5

    within_range_of_home = 15
    within_range_of_sweet_spot = 15
    min_pass_distance = 120

    # minumum distance a player must be from the goalkeeper before it will pass the ball
    goal_keeper_min_pass_distance = 50

    # the distance the keeper puts between the back of the net and the ball when using he interpose steering behavior
    goal_keeper_tending_distance = 20

    # when the ball comes within this distance the goalkeeper changes state to intercept the ball
    goal_keeper_intercept_range = 100

    # how close the ball must be to a receiver before he starts chasing it
    ball_within_receiving_range = 10

    player_receiving_range = 50

    player_view_distance = 100
    player_separation_coefficient = 1

class Managers:
    entity_manager = entity_manager.EntityManager.instance() 
    dispatcher = message.Dispatcher.instance(entity_manager)

class TeamModel:
    players = []


_ATTR_MAP = {}
_ATTR =  get_class_attribute_map(Display) + \
         get_class_attribute_map(Params) + \
         get_class_attribute_map(Managers) +\
         get_class_attribute_map(TeamModel)

class Model():
    _instance = None
    DELEGATED_ATTRIBUTES = _ATTR 

    def __init__(self):
        pass

    @classmethod
    def instance(klass):
        if klass._instance == None:
            klass._instance = Model()
        return klass._instance

    def __getattr__(self,prop ):
        for cls,ps in _ATTR_MAP.items():
            if prop in ps:
                return getattr(cls,prop)

        return object.__getattribute__(self, prop)

    # from lordmauve of pgzero
    def __setattr__(self, attr, value):
        for cls, ps in _ATTR_MAP.items():
            if attr in ps:
                return setattr(cls, attr, value)

        if attr in self.__dict__.keys():
            return object.__setattr__(self, attr, value)

        raise AttributeError('no property {} found'.format(attr))


initial_model = Model.instance()
