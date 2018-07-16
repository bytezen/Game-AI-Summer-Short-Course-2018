from fsm import BaseGameEntity,StateMachine
from wife_states import DoHouseWork, WifeGlobalState
from constants import Location

class Wife(BaseGameEntity):
    
    def __init__(self,name='wife',wid=None,location=Location.shack):
        super().__init__()

        if wid != None:
            #override the assigned id
            self.id = wid
            
        self.name = name
        self.location = location
        self.cooking = False
        self.state_machine = StateMachine(self)
        self.state_machine.current_state = DoHouseWork.instance()
        self.state_machine.global_state = WifeGlobalState.instance()

    def change_location(self, new_location):
        self.location = new_location

    def update(self):
        self.state_machine.update()

    def handle_message(self,msg):
        return self.state_machine.handle_message(msg)
                

    def __repr__(self):
        return self.name

if __name__ =='__main__':

    elsa = Wife()
    print(elsa.id)
    elsa.state_machine.current_state.enter(elsa)
    elsa.state_machine.current_state.execute(elsa)
    
