from enum import Enum

class BaseGameEntity:
    _ID = 0
    def __init__(self):
        self.id = BaseGameEntity.assign_id()
        
    @classmethod
    def assign_id(cls):
        _id = cls._ID
        cls._ID += 1
        return _id
    
class State:
    def __init__(self):
        pass

    def enter(self, entity):
        raise NotImplemented

    def execute(self, entity):
        raise NotImplemented

    def exit(self, entity):
        raise NotImplemented

    def on_message(self, entity, msg):
        raise NotImplemented

    def __repr__(self):
        try:
            return self.name
        except:
            return "anonState"


class StateMachine:
    def __init__(self, owner):
        self.owner = owner
        self.current_state = None
        self.previous_state = None
        self.global_state = None

    def update(self):
        if self.global_state:
            self.global_state.execute(self.owner)

        if self.current_state:
            self.current_state.execute(self.owner)

    def handle_message(self, msg):
        if self.current_state != None and self.current_state.on_message(self.owner, msg):
            return True

        if self.global_state != None and self.global_state.on_message(self.owner, msg):
            return True

        return False

    def change_state(self, new_state):
        self.previous_state = self.current_state
        self.current_state.exit(self.owner)
        self.current_state = new_state
        self.current_state.enter(self.owner)

    def revert_to_previous_state(self):
        self.change_state(self.previous_state)

    def is_in_state(self, state):
        return self.current_state.id == state.id

    def current_state_name(self):
        return self.current_state.__class__
   

if __name__ == '__main__':

    s = State()
    print('state id=', s.id)
    
    sm = StateMachine(None)
    sm.current_state = "this is something else"
    print(sm.current_state_name())
    
    
    
    
    
        
