from fsm import BaseGameEntity
from miner_states import GoHomeAndSleepTilRested
from constants import Location

class Miner(BaseGameEntity):
    COMFORT_LEVEL = 5
    MAX_NUGGETS = 3
    THIRST_LEVEL = 5
    TIREDNESS_THRESHOLD = 5
    
    def __init__(self,name='anonymous'):
        super().__init__()

        self.location = Location.saloon
        self.gold_carried = 0
        self.money_in_bank = 0
        self.thirst = 0
        self.fatigue = 0
        self.current_state = GoHomeAndSleepTilRested.instance()
        self.name = name

##    def change_state(self, new_state):
##        self.current_state.exit( self )
##        self.current_state = new_state
##        self.current_state.enter(self)

    def add_to_gold_carried(self, val):
        self.gold_carried += val
        self.gold_carried = max(0, self.gold_carried)

    def add_to_wealth(self, val):
        self.money_in_bank += val
        self.money_in_bank = max(0, self.money_in_bank)

    def thirsty(self):
        return self.thirst >= self.THIRST_LEVEL

    def fatigued(self):
        return self.fatigue >= self.TIREDNESS_THRESHOLD

    def pockets_full(self):
        return self.gold_carried >= self.MAX_NUGGETS

    def buy_and_drink_whiskey(self):
        self.thirst = 0
        self.money_in_bank -= 2

    def change_location(self,new_location):
        self.location = new_location

    def increase_fatigue(self):
        self.fatigue += 1

    def decrease_fatigue(self):
        self.fatigue -= 1

    def wealth(self):
        return self.money_in_bank

    def update(self):
        self.thirst += 1

        if self.current_state:
            self.current_state.execute(self)

    def __repr__(self):
        return self.name

if __name__ =='__main__':

    bob = Miner()
    print(bob.id)
    bob.current_state.enter(bob)
    
