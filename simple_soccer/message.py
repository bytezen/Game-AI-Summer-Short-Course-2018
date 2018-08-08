import numbers
from datetime import datetime, timedelta


def self_or_id(obj):
    if hasattr(obj,'id'):
        return obj.id
    else:
        return obj

class MessageType():
    GoHome = 'go_home'

class Message:
    def __init__(self,frm,to,msg_type,delay=0,info=None):
        self.sender_id = self_or_id(frm)
        self.receiver_id = self_or_id(to)
        self.info = info
        self.create_time = datetime.now()
        self.delay = delay
        self.dispatch_time = self.create_time + timedelta(seconds=self.delay)
        self.msg_type = msg_type

    def __repr__(self):
        if self.delay > 0:
            return '{{delay:%d; dispatch: %s; from:%d; to:%d; type:%s; info:%s;}}' \
                % ( self.delay, self.dispatch_time, self.sender_id, self.receiver_id, self.msg_type, str(self.info) )
        else:
            return '{{delay:%d; dispatch: %s; from:%d; to:%d; type:%s; info:%s;}}' \
                % ( self.delay, self.dispatch_time, self.sender_id, self.receiver_id, self.msg_type, str(self.info) )


class Dispatcher:
    _instance = None

    @classmethod
    def instance(cls,entity_manager=None):
        if Dispatcher._instance == None:
            if entity_manager != None:
                Dispatcher._instance = Dispatcher(entity_manager)
            else:
                raise ValueError("a dispatcher needs an EntityManager" )

        return Dispatcher._instance

    def __init__(self, entity_manager=None):
        if Dispatcher._instance == None:
            if entity_manager == None:
                raise ValueError('a dispatcher needs an EntityManager')
            else:
                Dispatcher._instance = self

        self._priority_q = [] 
        self._entity_manager = entity_manager

    def discharge(self, receiver, msg):
        if not receiver.handle_message(msg):
            print(' receiver{} did not handle message: {}'.format(receiver.id,msg) )

    def dispatch_message(self, sender_id, receiver_id, msg,delay=0,info=None):
        adjusted_receiver_id =  self_or_id(receiver_id)
        receiver = self._entity_manager.fetch(adjusted_receiver_id)
        if receiver == None:
            raise KeyError('receiver_id: %s entities: %s' % (receiver_id, [em for em in self._entity_manager._entity_map]))

        if delay <= 0.0:
            telegram = Message(sender_id, receiver_id, msg,0, info)
            self.discharge(receiver, telegram)
        else:
            telegram = Message(sender_id, receiver_id, msg,delay,info)
            print('created a delayed message: ', telegram)
            self.add_to_queue(telegram)

    def dispatch_delayed_message(self):
        current_time = datetime.now()
        print('...dispatch message called with current_time= ', current_time)
        for message in self._priority_q:
            print('\t message.dispatch_time = ', message.dispatch_time,'\n')
            if current_time >= message.dispatch_time:
                #dispatch the message 
                receiver = self._entity_manager.fetch(message.receiver_id)
                if receiver == None:
                    print('I do not have know a receiver with this id: ', receiver_id, ' message not delivered and removed from the queue: ', msg)
                    return
                else:
                    print('...dispatching a delayed message...')
                    self.discharge(receiver, message)
            else:
                #the queue is sorted so we can stop checking once we get to the first
                #future message
                break

        #now remove all of the old messages
        self.remove_old_queue_messages(current_time)

    def remove_old_queue_messages(self, time):
        self._priority_q[:] = [ message for message in self._priority_q if time < message.dispatch_time]

    def add_to_queue(self, msg):
        self._priority_q.append(msg)
        self._priority_q = sorted(self._priority_q, key=lambda i: i.dispatch_time)
#
# Message constants
#
GO_HOME = MessageType.GoHome
Test = 'this is a test message'
