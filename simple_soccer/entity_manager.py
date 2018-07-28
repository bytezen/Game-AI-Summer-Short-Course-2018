from enum import Enum

##def ent_miner_bob():
##    mgr = EntityManager().instance()
##    entity_from


class EntityManager:
    _instance  = None
    
    def __init__(self):
        self.entity_map = {}

    def register_entry(self, new_entity):
        if new_entity.id in self.entity_map.keys():
            print("id for {0} already exists in manager".format(new_entity))
            return
        
        self.entity_map[new_entity.id] = new_entity
        pass

    def entity_from_id(self, anId):
        """ this is the entity from id documentatio"""
        assert (anId in self.entity_map.keys())
        return self.entity_map[anId]

    ## remove and entity from the manager if it exists
    def remove_entity(self, anId):
        try:
            del self.entity_map[anId]
        except:
            pass

    @classmethod
    def instance(cls):
        if cls._instance == None:
            _instance = MessageDispatcher()

        return _instance
    

class Entities(Enum):
    ent_miner_bob = 0
    ent_elsa = 1


foo = EntityManager()
foo.       
