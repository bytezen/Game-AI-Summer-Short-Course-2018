from fsm import State,StateMachine,MessageType
from constants import Location

import random
import time

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
        if random.random() < 0.1 and not wife.state_machine.is_in_state(VisitBathroom.instance()):
            wife.state_machine.change_state(VisitBathroom.instance())

    def on_message(self, wife, msg):
        if msg == Message.HiHoneyImHome:
            time = [str(x) for x in [now.hour,now.minute,now.second]]
            print("\nmessage handled by: {0} at time: {1}".format(miner,":".join(time)))

            print("\n{0}: Hi Honey. Let m emake you some of mah fine country stew".format(wife))
            wife.state_machine.change_state(CookStew.instance())

            return True

        return false

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
        print("\n{0}: Time to do some housework".format(wife))
        

    def execute(self, wife):
        chore = random.choice(["Moppin' the floor",
                           "Washin' the dishes",
                           "Makin' the bed"])
        
        print("\n{0}: {1} ".format(wife,chore))


    def exit(self, wife):
        pass        


    def on_message(self, miner, msg):
        """
        The GlobalState for the miner will handle messages
        """
        return False        


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
        print("\n{0}: Leavin' the Jon".format(wife))


    def on_message(self, miner, msg):
        """
        The GlobalState for the miner will handle messages
        """
        return False

## --------------------------------------------
## CookStew 
##
##
##
##
class CookStew(State):
    _instance = None
    
    def __init__(self):
        super().__init__()


    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()

        return cls._instance

    def enter(self,wife):
        if wife.cooking:
            print("\n{0}: Putting the stew in the oven")

            dispatch.dispatch_message(delay=1.5,
                                      sender=wife.id,
                                      receiver=wife.id,
                                      msg=MessageType.StewReady,
                                      info=MessageInfo.NO_ADDITIONAL_INFO)
            wife.cooking = True

    def execute(self,wife):
        print("\n{0}: Fussin' over food".format(wife))

    def exit(self,wife):
        print("\n{0}: Puttin the stew on the table ".format(wife))        
        pass

    def on_message(self, wife, msg):
        if msg == Message.StewReady:
            time = [str(x) for x in [now.hour,now.minute,now.second]]
            print("\nmessage handled by: {0} at time: {1}".format(miner,":".join(time)))

            print("\n{0}: Stew Ready! Lets eat ".format(wife))

            #Let hubby know the stew is ready
            dispatch.dispatch_message(delay=SEND_MSG_IMMEDIATELY,
                                      sender=wife.id,
                                      receiver=ent_miner_bob,
                                      msg=MessageType.StewReady,
                                      info=MessageInfo.NO_ADDITIONAL_INFO)
            
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
