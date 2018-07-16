from fsm import State
from constants import Location

import random
## --------------------------------------------
## WifeGlobalState 
##
##
##
##
class WifeGlobalState(State):
    _instance = None
    
    def __init__(self):
        super().__init__()


    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()

        return cls._instance


    def execute(self, wife):
        if random.random() < 0.1:
            wife.state_machine.change_state(VisitBathroom.instance())

## --------------------------------------------
## DoHouseWork 
##
##
##
##
class DoHouseWork(State):
    _instance = None
    
    def __init__(self):
        super().__init__()


    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()

        return cls._instance

    def enter(self, wife):
        pass

    def execute(self, wife):
        chore = random.choice(["Moppin' the floor",
                           "Washin' the dishes",
                           "Makin' the bed"])
        
        print("\n{0}: {1} ".format(wife,chore))


    def exit(self, wife):
        pass        
        


## --------------------------------------------
## VisitBathroom 
##
##
##
##
class VisitBathroom(State):
    _instance = None
    
    def __init__(self):
        super().__init__()


    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()

        return cls._instance

    def enter(self, wife):
        print("\n{0}:  Walkin' to the can. Need to powda mah pretty li'lle nose".format(wife))


    def execute(self, wife):
        print("\n{0}:  Ahhhhhh! Sweet relief!".format(wife))
        wife.state_machine.revert_to_previous_state()

    def exit(self, wife):
        pass



if __name__ == '__main__':
    from wife import Wife

    bob = Miner()
##    state = GoHomeAndSleepTilRested.instance()
##    state.enter(bob)
##    state.execute(bob)
##    state.exit(bob)
    
    state = EnterMineAndDigForNugget.instance()
    state = VisitBankAndDepositGold.instance()
    state = QuenchThirst.instance()    
    
    print(state)
    bob.change_state( state )
    bob.current_state.execute( bob )
    bob.current_state.exit( bob )
