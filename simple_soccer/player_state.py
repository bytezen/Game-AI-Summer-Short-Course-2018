class GlobalPlayerState:
      _instance = None

      @classmethod
      def instance(klass):
            if klass._instance == None:
                 klass._instance = klass()
            return klass._instance

class ChaseBall:
      _instance = None

      @classmethod
      def instance(klass):
            if klass._instance == None:
                 klass._instance = klass()
            return klass._instance


class SupportAttacker:
      _instance = None

      @classmethod
      def instance(klass):
            if klass._instance == None:
                 klass._instance = klass()
            return klass._instance


class ReturnToHomeRegion:
      _instance = None

      @classmethod
      def instance(klass):
            if klass._instance == None:
                 klass._instance = klass()
            return klass._instance


class Wait:
      _instance = None

      @classmethod
      def instance(klass):
            if klass._instance == None:
                 klass._instance = klass()
            return klass._instance

class KickBall:
      _instance = None

      @classmethod
      def instance(klass):
            if klass._instance == None:
                 klass._instance = klass()
            return klass._instance


class Dribble:
      _instance = None

      @classmethod
      def instance(klass):
            if klass._instance == None:
                 klass._instance = klass()
            return klass._instance


class ReceiveBall:
      _instance = None

      @classmethod
      def instance(klass):
            if klass._instance == None:
                 klass._instance = klass()
            return klass._instance


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
