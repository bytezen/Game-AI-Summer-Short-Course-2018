from miner import Miner
from wife import Wife
from entity_manager import EntityManager

import time
import random

##random.seed(10)

rounds = 20
entity_mgr = EntityManager()

bob = Miner('bob')
elsa = Wife('elsa')

entity_mgr.register_entry(bob)
entity_mgr.register_entry(elsa)


for i in range(rounds):
    bob.update()
    elsa.update()
    time.sleep(.1)
    

