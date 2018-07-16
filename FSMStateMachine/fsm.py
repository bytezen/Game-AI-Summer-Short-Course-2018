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

class MessageType(Enum):
    HiHoneyImHome = 1
    StewReady = 2

    def __repr__(self):
        if self == MessageType.HiHoneyImHome:
            return "hi honey im home"
        elif self == MessageType.StewReady:
            return "stew ready"
        else:
            return "unknown message"


class Message:
    def __init__(self,frm,to,info,msg_type):
        self.receiver_id = to
        self.sender_id = frm
        self.info = info
        self.dispatch_time = when
        self.msg_type

class MessageDispatcher:
    _instance = None
    
    def __init(self):
        self.priority_q = None

    def discharge(self, receiver, msg):
        if not receiver.handle_message(msg):
            print('message not handled: ',msg)
            

    def dispatch_message(self, sender_id, receiver_id=None, msg=None, info=0, delay=0, ):
        receiver = EntityManager.instance().get_entity(receiver_id)
        
        if receiver == None:
            print('I do not have know a receiver with this id: ', receiver_id, ' message not delivered: ', msg)
            return

        telegram = Message(sender_id, receiver_id, msg, info)

        if delay <= 0.0:
            self.discharge(receiver, telegram)
        else:
            telegram.dispatch_time = current_time + delay
            self.priority_q.add(telegram)
        
        
        pass

    def dispatch_delayed_msg(self):
        pass

    @classmethod
    def instance(cls):
        if cls._instance == None:
            _instance = MessageDispatcher()

        return _instance


class EntityManager:
    pass 
    

if __name__ == '__main__':

    s = State()
    print('state id=', s.id)
    
    sm = StateMachine(None)
    sm.current_state = "this is something else"
    print(sm.current_state_name())
    
    
    
    
    
        
