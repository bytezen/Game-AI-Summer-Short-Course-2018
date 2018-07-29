import fsm 


def change_player_home_regions(team, new_regions):
      for player,region in zip(team, new_regions):
            team.set_player_home_region(player,region)

class Attacking(fsm.State):
      _instance = None

      name = 'Attacking'

      @classmethod
      def instance(klass):
            if klass._instance == None:
                 klass._instance = klass()
            return klass._instance

      def instance(klass):
            if klass._instance == None:
                 klass._instance = klass()
            return klass._instance

      def enter(self, team):
            pass

      def execute(self, team):
            pass

      def exit(self, team):
            pass

      def on_message(self, msg):
            return False



class Defending(fsm.State):
      _instance = None

      name = 'Defending'

      @classmethod
      def instance(klass):
            if klass._instance == None:
                 klass._instance = klass()
            return klass._instance

      def instance(klass):
            if klass._instance == None:
                 klass._instance = klass()
            return klass._instance

      def enter(self, team):
            pass

      def execute(self, team):
            pass

      def exit(self, team):
            pass

      def on_message(self, msg):
            return False



class PrepareForKickoff(fsm.State):
      _instance = None
      name = 'PrepareForKickoff'

      @classmethod
      def instance(klass):
            if klass._instance == None:
                 klass._instance = klass()
            return klass._instance

      def enter(self, team):
            team.controlling_player = None
            team.supporting_player = None
            team.receiver_player = None
            team.player_closest_to_ball = None

            team.return_all_field_players_home()

      def execute(self, team):
            pass

      def exit(self, team):
            pass

      def on_message(self, msg):
            return False




global_player = GlobalPlayerState.instance()
chase_ball = ChaseBall.instance()
support_attacker = SupportAttacker.instance()
return_home = ReturnToHomeRegion.instance()
wait = Wait.instance()
kick_ball = KickBall.instance()
dribble = Dribble.instance()
receive_ball = ReceiveBall.instance




if __name__=='__main__':
      foo = GlobalPlayerState.instance() 
