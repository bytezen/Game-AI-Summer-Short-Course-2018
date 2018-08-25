import fsm 


def change_player_home_regions(team, new_regions):
      for player,region in zip(team(), new_regions):
            team.set_player_home_region(player,region)

class Attacking(fsm.State):
      _instance = None

      name = 'Attacking'

      @classmethod
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
      home_regions = [1,6,8,3,5]
      away_regions = [16,9,11,12,14]

      @classmethod
      def instance(klass):
            if klass._instance == None:
                 klass._instance = klass()
            return klass._instance

      def enter(self, team):
           if team.side == 'HOME':
                 change_player_home_regions(team, Defending.home_regions)
           else:
                 change_player_home_regions(team, Defending.away_regions)

      def execute(self, team):
            if team.in_control:
                  team.change_state( attacking )

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
            if team.all_players_at_home and team.opponent.all_players_at_home:
                  team.fsm.change_state( defending )

      def exit(self, team):
            team.pitch.game_on = True

      def on_message(self, msg):
            return False


defending = Defending.instance()
prepare_for_kickoff = PrepareForKickoff.instance()
attacking = Attacking.instance()



if __name__=='__main__':
      foo = GlobalPlayerState.instance() 
