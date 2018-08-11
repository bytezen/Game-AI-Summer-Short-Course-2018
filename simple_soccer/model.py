import message
import entity_manager

def get_class_attribute_map(cls):
    _ATTR_MAP[cls] = [prop for prop in dir(cls) if not prop.startswith('__')]
    return [ (cls, prop) for prop in dir(cls) if not prop.startswith('__') ]

class Window:
    pass

class MenuItem:
    pass


class Display:

    # display view parameters
    show_states = False
    show_ids = False
    show_support_spots = False
    show_regions = True
    show_controlling_team = False
    show_supporting_player_targets = False
    show_highlight_when_threatened = False
    show_frame_rate = False
    # state of the team displayed on screen
    show_team_state = True 


class Params:
    player_kicking_accuracy = 0.99
    friction = -0.015 #0.95 #0.015
    player_mass = 3.0
    player_max_speed = 30
    player_max_force = 30
    player_kick_frequency = 8 
    player_max_turn_rate = 15 
    player_max_speed_with_ball = 15
    player_receiving_range = 50

class Managers:
    entity_manager = entity_manager.EntityManager.instance() 
    dispatcher = message.Dispatcher.instance(entity_manager)


_ATTR_MAP = {}
_ATTR =  get_class_attribute_map(Display) + \
         get_class_attribute_map(Params) + \
         get_class_attribute_map(Managers)

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
