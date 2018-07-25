from soccer_pitch import Goal
from player import PlayerBase, GoalKeeper, FieldPlayer
from support_spot_calculator import SupportSpotCalculator

HOME = 'home'
AWAY = 'away'

class SoccerTeam:
    
    def __init__(self, which_side):
        if which_side == HOME:
            self.color = 'red'
        else:
            self.color = 'blue'

            
        
