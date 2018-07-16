from miner import Miner
import time

rounds = 20
bob = Miner()

for i in range(rounds):
    bob.update()
    time.sleep(.7)
    

