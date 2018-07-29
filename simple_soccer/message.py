
class MessageType():
    GoHome = 'go_home'


class Message:
    def __init__(self,frm,to,info,msg_type):
        self.receiver_id = to
        self.sender_id = frm
        self.info = info
        self.dispatch_time = when
        self.msg_type

class Dispatcher:
    _instance = None
    
    def __init(self, entity_manager):
        self.priority_q = None
        self.entity_manager = entity_manager

    def discharge(self, receiver, msg):
        if not receiver.handle_message(msg):
            print('message not handled: ',msg)
            

    def dispatch_message(self, sender_id, receiver_id=None, msg=None, info=0, delay=0, ):
        receiver = entity_manager.get_entity(receiver_id)
        
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
            _instance = Dispatcher()

        return _instance

GO_HOME = MessageType.GoHome
