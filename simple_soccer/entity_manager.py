from enum import Enum

## singleton class design from
## https://gist.github.com/pazdera/1098129
##
class EntityManager:
    __instance  = None

    def __init__(self):
        self._entity_map = {}
        if EntityManager.__instance == None:
            EntityManager.__instance = self

    def register(self, new_entity):
        if new_entity.id in self._entity_map.keys():
            print("id for {0} already exists in manager".format(new_entity))
            return

        self._entity_map[new_entity.id] = new_entity

    def fetch(self, anId):
        """ this is the entity from id documentation"""
        try:
            assert (anId in self._entity_map.keys())
            return self._entity_map[anId]
        except:
            print('{} not found in EntityManager'.format(anId))
            return None

    ## remove and entity from the manager if it exists
    def remove(self, anId):
        try:
            del self._entity_map[anId]
        except:
            pass

    def clear(self):
        self._entity_map.clear()
    

    @property
    def size(self):
        return len(self._entity_map)

    @property
    def map(self):
        return self._entity_map

    @classmethod
    def instance(cls):
        if EntityManager.__instance == None:
            EntityManager.__instance = EntityManager() 

        return EntityManager.__instance



