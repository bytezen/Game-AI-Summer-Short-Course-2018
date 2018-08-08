
def get_class_attribute_map(cls):
    _ATTR_MAP[cls] = [prop for prop in dir(cls) if not prop.startswith('__')]
    return [ (cls, prop) for prop in dir(cls) if not prop.startswith('__') ]

class Paths:
    home_goal_keeper = 'playerredshirt0.png'
    home_player_1 = 'playerredshirt1.png'
    home_player_2 = 'playerredshirt2.png'
    home_player_3 = 'playerredshirt3.png'
    home_player_4 = 'playerredshirt4.png'

    away_goal_keeper = 'playerredshirt0.png'
    away_player_1 = 'playerredshirt1.png'
    away_player_2 = 'playerredshirt2.png'
    away_player_3 = 'playerredshirt3.png'
    away_player_4 = 'playerredshirt4.png'


_ATTR_MAP = {}
_ATTR =  get_class_attribute_map(Paths)

class Config():
    _instance = None
    DELEGATED_ATTRIBUTES = _ATTR 

    def __init__(self):
        pass

    @classmethod
    def instance(klass):
        if klass._instance == None:
            klass._instance = Config()
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


config = Config.instance()

if __name__ == '__main__':
    c = config
    print(c.home_player_0)
