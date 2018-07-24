class Window:
    pass

class MenuItem:
    pass


class Display:

    # display view parameters
    show_states = False
    show_ids = False
    show_support_spots = False
    show_regions = False
    show_controlling_team = False
    show_targets = False
    show_highlight_when_threatened = False
    show_frame_rate = False


class Params:
    player_kicking_accuracy = 0.99
    friction = 0.95 #0.015
    
class Model(object):
    _instance = None

    def __init__(self):
        pass
        
    @classmethod
    def instance(klass):
        if klass._instance == None:
            klass._instance = Model()
        return klass._instance

    def __getattribute__(self,prop ):
        res = None
        try: # look in display
            res = object.__getattribute__(Display, prop)
        except:
            pass

        if res != None:
            return res

        try:
            res = object.__getattribute__(Params, prop)
        except:
            pass

        if res == None:
            raise AttributeError ('uknown model attribute: {0}'.format(prop))
        else:
            return res
            


        return res
        

        
    

initial_model = Model.instance()
