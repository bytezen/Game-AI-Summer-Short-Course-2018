from fsm import State
from constants import Location


## --------------------------------------------
## GoHomeAndSleepTilRested 
##
##
##
##
class GoHomeAndSleepTilRested(State):
    _instance = None
    
    def __init__(self):
        super().__init__()


    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()

        return cls._instance

    def enter(self, miner):
        if miner.location != Location.shack:
            print("\n{0}: Walkin home".format(miner))
            miner.change_location(Location.shack)
        pass

    def execute(self, miner):
        if not miner.fatigued():
            print("\n{0}: What a Gosh darn fantastic nap! Time to find more gold.".format(miner))
            miner.change_state( EnterMineAndDigForNugget.instance() )
        else:
            miner.decrease_fatigue()

    def exit(self, miner):
        print("\n{0}: Leaving the house".format(miner))
        pass


## --------------------------------------------
## QuenchThirst 
##
##
##
##
class QuenchThirst(State):
    _instance = None
    
    def __init__(self):
        super().__init__()


    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()

        return cls._instance

    def enter(self, miner):
        if miner.location != Location.saloon:
            miner.change_location(Location.saloon)
            print("\n{0}: Boy, ah sure is thusty! Walking to the saloon".format(miner))
            
    def execute(self, miner):
        if miner.thirsty():
            miner.buy_and_drink_whiskey()
            print("\n{0}: That's mighty fine sippin liquer".format(miner))
            miner.change_state(EnterMineAndDigForNugget.instance())
        else:
            print("Error! Error! Error! Should not be at the saloon if you are not thirsty")

    def exit(self, miner):
        print("\n{0}: Leaving the saloon, feelin' good".format(miner))


## --------------------------------------------
## EnterMineAndDigForNugget 
##
##
##
##
class EnterMineAndDigForNugget(State):
    _instance = None
    
    def __init__(self):
        super().__init__()


    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()

        return cls._instance

    def enter(self, miner):
        if miner.location != Location.goldmine:
            print("\n{0}: Walkin' to the goldmine".format(miner))
            miner.change_location(Location.goldmine)

    def execute(self, miner):
        miner.add_to_gold_carried(1)
        miner.increase_fatigue()
        print("\n{0}: Pickin' up a nugget".format(miner))

        if miner.pockets_full():
            miner.change_state( VisitBankAndDepositGold.instance() )

        if miner.thirsty():
            miner.change_state( QuenchThirst.instance() )        

    def exit(self, miner):
        print("\n{0}: Ah'm leavin' the goldmine with mah pockets full o' sweet gold".format(miner))


## --------------------------------------------
## VisitBankAndDepositGold 
##
##
##
##
class VisitBankAndDepositGold(State):
    _instance = None
    
    def __init__(self):
        super().__init__()


    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()

        return cls._instance

    def enter(self, miner):
        if miner.location != Location.bank:
            print("\n{0}: Goin' to the bank. Yes siree".format(miner))
            miner.change_location(Location.bank)

    def execute(self, miner):
        miner.add_to_wealth(miner.gold_carried)

        miner.gold_carried = 0

        print("\n{0}: Depositing gold. Total savings now: {1}".format(miner, miner.wealth()) )

        if miner.wealth() >= miner.COMFORT_LEVEL:
            print("\n{0}: Woohoo! Rich enough for now. Back home to mah li'lle lady".format(miner))
            miner.change_state( GoHomeAndSleepTilRested.instance() )
        else:
            miner.change_state( EnterMineAndDigForNugget.instance() )
            

    def exit(self, miner):
        print("\n{0}: Leavin' the bank".format(miner))    



if __name__ == '__main__':
    from miner import Miner

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
