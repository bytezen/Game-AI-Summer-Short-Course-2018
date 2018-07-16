from miner import Miner
from wife import Wife
import time

rounds = 20
bob = Miner(name='bob')
elsa = Wife(name='elsa')

for i in range(rounds):
    bob.update()
    elsa.update()
    time.sleep(.8)
    

