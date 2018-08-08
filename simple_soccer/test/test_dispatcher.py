import unittest
from unittest.mock import Mock

import time

import message
import entity_manager

def mock_sender():
     pass

def mock_receiver():
     pass

def mock_message():
     pass

def mock_entity_manager():
     return entity_manager.EntityManager.instance()

def mock_message_handler(*args):
     return True

obj80 = Mock()
obj80.id = 80
obj5 = Mock()
obj5.id = 5
obj45 = Mock()
obj45.id = 45

class DispatcherTest(unittest.TestCase):

     def setUp(self):
          self.dispatcher = message.Dispatcher(mock_entity_manager())

          mock_entity_manager().clear()
          mock_entity_manager().register(obj80)
          mock_entity_manager().register(obj5)
          mock_entity_manager().register(obj45)


     def tearDown(self):
          if self.dispatcher != None:
               self.dispatcher = None

     def test_creating_dispatcher_instance(self):
          """dispatcher creates an instance of Dispatcher"""
          dispatcher = message.Dispatcher(mock_entity_manager)
          assert type( dispatcher.instance() ) == message.Dispatcher 

     def test_singleton_dispatcher(self):
          """only one instance of the class is created"""
          message.Dispatcher._instance = None 
          assert message.Dispatcher._instance == None
          another_dispatcher = message.Dispatcher.instance(mock_entity_manager)
          yet_another_dispatcher = message.Dispatcher.instance()
          assert another_dispatcher.instance() == yet_another_dispatcher.instance()

     def test_constructor_singleton_creation(self):
          """can create dispatcher from construtor"""
          dispatcher1 = message.Dispatcher(mock_entity_manager)
          dispatcher2 = message.Dispatcher(mock_entity_manager)

          assert dispatcher1.instance() == dispatcher2.instance()

     def test_send_message(self):
          """message can be sent and received bewtween two entities that exist """

          self.dispatcher.dispatch_message(obj80.id,obj45.id,message.Test,0,info=100)
          obj45.handle_message.assert_called()


     def test_send_to_unknown_recipient(self):
          """sending message to an unknow receipient fails but does not crash"""
          # assert False
          pass

     def test_unknown_sender_fails(self):
          """sending message from an unknown sender fails but does not crash"""
          # assert False
          pass

     def test_delayed_message(self):
          """a delayed message is sent at the appropriate time"""
          self.dispatcher.dispatch_message(obj5.id, obj45.id,'from 5 to 45',delay = 2)
          self.dispatcher.dispatch_message(obj45.id, obj5.id,'from 45 to 5',delay = 5)
          self.dispatcher.dispatch_message(obj80.id, obj45.id,'from 80 to 45',delay = 1)

          expected_msg_order = [(obj80.id, obj45.id),
                                (obj5.id, obj45.id),
                                (obj45.id,obj5.id)]

          q_order = [(msg.sender_id, msg.receiver_id) for msg in self.dispatcher._priority_q ]
          assert expected_msg_order == q_order, \
               "priority_queue: %s \n expected_order %s" % ( self.dispatcher._priority_q, expected_msg_order )

     def test_resolve_receiver_id_from_receiver(self):
          """given an object return the object or id attribute"""

          class Empty:
               pass

          _id = message.self_or_id(obj80)
          assert _id == 80

          _next_id = message.self_or_id(obj80.id)
          assert _id == 80

          bar = Empty()
          _next_next_id = message.self_or_id(bar)
          assert _next_next_id == bar, ( "_next_next_id = %s, %s" % (_next_next_id,bar) )

          bar.__dict__['id'] = 1001
          _next_next_id = message.self_or_id(bar)
          assert _next_next_id == bar.id, ( "_next_next_id.id = %s, %s" % (_next_next_id.id,bar.id) )

     def test_dispatch_delay(self):
          """a delayed message is handled after the appropriate delay"""


          # self.dispatcher.dispatch_message(obj80.id,obj5.id,'TEST',delay=3)
          self.dispatcher.dispatch_message(obj80,obj5,'TEST',delay=3)
          obj5.handle_message.assert_not_called()
          count = 6
          for i in range(count):
               self.dispatcher.dispatch_delayed_message()
               if i < 3:
                    obj5.handle_message.assert_not_called()
               else:
                    obj5.handle_message.assert_called_once()

               time.sleep(1)


          self.dispatcher.dispatch_message(obj5,obj80,'TEST',delay=3)
          self.dispatcher.dispatch_message(obj5,obj45,'TEST',delay=1)
          for count in range(count):
               self.dispatcher.dispatch_delayed_message()
               time.sleep(1)
               if count < 1:
                    obj45.handle_message.assert_not_called()
               if count < 3:
                    obj80.handle_message.assert_not_called()


          obj80.handle_message.assert_called_once()
          obj45.handle_message.assert_called_once()



if __name__=='__main__':
     unittest.main() 




