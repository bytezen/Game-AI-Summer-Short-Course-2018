import pygame
from pygame import  Color

OFF_COLOR = Color('black')
LOW_COLOR = Color('lightyellow')
MED_COLOR = Color('lemonchiffon')
MEDLOW_COLOR = Color('lightgoldenrodyellow')
MEDHI_COLOR = Color('khaki')
HI_COLOR = Color('gold')
BLOWN_COLOR = OFF_COLOR
##print(BLACK, LOW, MEDLOW, MED, MEDHI, HI)

OFF = 'off'
LOW = 'low'
MEDLOW = 'medlow'
MED = 'med'
MEDHI = 'medhi'
HI = 'hi'
BLOWN = 'blown'


class State:
    """Parent class that is the base state for all other light states.

    All State classes inherit from this class. To make a light state pass in a
    light and a burn_rate for the light. 

    Attributes:
        _light (Light): the light that owns the state.
        _burn_rate (number): specifies how much the life of the light
    decreases during each update.

    """    
    def __init__(self, light, burn_rate, color):
        self._light = light
        self._burn_rate = burn_rate
        self._color = color

    def enter(self):
        pass

    def execute(self, screen=None):
        if screen != None:
            screen.fill(self._color)


    def exit(self):
        pass

    def burn(self):
        self._light.life -= self._burn_rate



class Off(State):
    """A class representing a light that is off

    Lights in this state have a burn_rate of 0
    """       
    def __init__(self,light):
        super().__init__(light,0, OFF_COLOR)
        self.name = OFF

    def enter(self):
        print('light is off')

    def execute(self, screen=None):
        if self._light.life > 0:
            self._light.change_state( Low(self._light) )
        else:
            super().execute(screen)                     

    def exit(self):
        print('Let there be light')




class Low(State):
    """A class representing a light that is at a low brightness state

    Lights in this state have a burn_rate of 0.2
    """        
    def __init__(self,light):
        super().__init__(light, 0.2,LOW_COLOR)
        self.name = LOW        

    def enter(self):
        print('turning light on low')

    def execute(self,screen=None):        
        self.burn()
        if self._light.life < 1:
            self._light.change_state(Blown(self._light))
        else:
            super().execute(screen)                        

    def exit(self):
        print('leaving low')
    


class MedLow(State):
    """A class representing a light that is at a medium low brightness state

    Lights in this state have a burn_rate of 0.4
    """            
    def __init__(self,light):
        super().__init__(light, 0.4,MEDLOW_COLOR)
        self.name = MEDLOW        

    def enter(self):
        print('turning light on medlow')

    def execute(self,screen=None):        
        self.burn()
        if self._light.life < 1:
            self._light.change_state(Blown(self._light))
        else:
            super().execute(screen)                        

    def exit(self):
        print('leaving medlow')


class Med(State):
    """A class representing a light that is at a medium brightness state

    Lights in this state have a burn_rate of 0.6
    """            
    def __init__(self,light):
        super().__init__(light, 0.6,MED_COLOR)
        self.name = MED        

    def enter(self):
        print('turning light on med')

    def execute(self,screen=None):        
        self.burn()
        if self._light.life < 1:
            self._light.change_state(Blown(self._light))
        else:
            super().execute(screen)            

    def exit(self):
        print('leaving med')


class MedHi(State):
    """A class representing a light that is at a medium high brightness state

    Lights in this state have a burn_rate of 0.8
    """                
    def __init__(self,light):
        super().__init__(light, 0.8,MEDHI_COLOR)
        self.name = MEDHI        

    def enter(self):
        print('turning light on med hi')

    def execute(self,screen=None):        
        self.burn()
        if self._light.life < 1:
            self._light.change_state(Blown(self._light))
        else:
            super().execute(screen)

    def exit(self):
        print('leaving med hi')


class Hi(State):
    """A class representing a light that is at a high brightness state

    Lights in this state have a burn_rate of 1.0
    """                
    def __init__(self,light):
        super().__init__(light, 1.0,HI_COLOR)
        self.name = HI        

    def enter(self):
        print('turning light on hi')

    def execute(self,screen=None):        
        self.burn()
        if self._light.life < 1:
            self._light.change_state(Blown(self._light))
        super().execute(screen)            

    def exit(self):
        print('leaving hi')


class Blown(State):
    """A class representing a light that is blow
    """                
    def __init__(self,light):
        super().__init__(light, 0,BLOWN_COLOR)
        self.name = BLOWN        

    def enter(self):
        print('the light Blew! You need to change the light' )

    def execute(self,screen=None):
        super().execute(screen)        

    def exit(self):
        print('you finally change the light...Let there be light!')

