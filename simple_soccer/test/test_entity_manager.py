import unittest
from unittest.mock import Mock

import entity_manager

def make_mock_object(_id=None):
    class Mock():
        def __init__(self, eId =None):
            self.id = id(self) if eId ==None else eId
    return Mock(_id)

obj1 = Mock()
obj1.id = 0
obj2 = Mock()
obj2.id = 2
obj3 = Mock()
obj3.id = 3
obj4 = Mock()
obj4.id = 4
obj5 = Mock()
obj5.id = 5
obj6 = Mock()
obj6.id = 6

class EntityManagerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.manager = entity_manager.EntityManager()

    def tearDown(self):
        self.manager = None

    def test_creating_entity_manager_instance(self):
        """manager creates an instance of EntityManager"""
        assert type( self.manager.instance() ) == entity_manager.EntityManager, \
            "instance class = %s " % type( self.manager )

    def test_singleton_manager(self):
        """only one instance of the class is created"""
        another_manager = entity_manager.EntityManager()
        assert another_manager.instance() == self.manager.instance(), "{} != {}".format(another_manager, self.manager)

    def test_class_method_construction(self):
        """calling the class method creates a singleton"""
        self.manager = None
        self.manager = entity_manager.EntityManager.instance()
        foo = entity_manager.EntityManager()

        assert foo.instance() == self.manager.instance()

    def test_register_entity(self):
        """can register an entity"""
        foo = make_mock_object(0)
        self.manager.register(foo)
        assert len( self.manager._entity_map ) == 1

    def test_fetch_entity(self):
        """can fetch an entity"""
        foo = make_mock_object(10)
        self.manager.register(foo)
        assert len( self.manager._entity_map ) == 1
        fetch = self.manager.fetch(10)

        assert foo == fetch
        assert len( self.manager._entity_map ) == 1

    def test_remove_entity(self):
        """can remove entity from manager"""
        foo = make_mock_object()
        self.manager.register(foo)
        assert len( self.manager._entity_map ) == 1
        removed = self.manager.remove(foo.id)

        assert len( self.manager._entity_map ) == 0

    def test_size(self):
        """adding and removing entities keeps accurate count"""
        assert self.manager.size == 0

        self.manager.register(obj1)
        self.manager.register(obj2)
        assert self.manager.size == 2

        self.manager.remove(obj2.id)
        assert self.manager.size == 1

        self.manager.remove(obj3.id)
        assert self.manager.size == 1

        self.manager.remove(obj1.id)
        assert self.manager.size == 0


if __name__=='__main__':
    #from:
    #https://medium.com/@vladbezden/using-python-unittest-in-ipython-or-jupyter-732448724e31
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
