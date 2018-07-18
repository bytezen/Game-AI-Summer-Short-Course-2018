        
from light_states import *
##Off, Low, MedLow, Med, MedHi, Hi, Blown, OFF, LOW, MEDLOW
        
class Light:
    def __init__(self):
        self._state = Off(self)
        self.life = 100

    def brighten(self):
        if self._state.name == OFF:
            self.change_state( Low(self) )

        elif self._state.name == LOW:
            self.change_state( MedLow(self) )                        

        elif self._state.name == MEDLOW:
            self.change_state( Med(self) )            

        elif self._state.name == MED:
            self.change_state( MedHi(self) )            

        elif self._state.name == MEDHI:
            self.change_state( Hi(self) )
            
    def dim(self):
        pass

    def change_bulb(self):
        self.change_state( Off(self) )
        self.life = 100
        
    def current_state(self):
        return self._state

    def change_state(self, new_state):
        self._state.exit()
        self._state = new_state
        self._state.enter()

    def update(self,screen = None):
        self._state.execute(screen)
        
