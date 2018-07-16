from enum import Enum

class Location(Enum):
    shack = 0
    goldmine = 1
    bank = 2
    saloon = 3

    
class bcolors:
    purple = '\033[95m' #Purple
    blue = '\033[94m' #blue
    green = '\033[92m' #green
    yellow = '\033[93m' #yellow
    orange = '\033[91m'    #orange
    endc = '\033[0m'    #back to white
    bold = '\033[1m'    
    underline = '\033[4m' 
