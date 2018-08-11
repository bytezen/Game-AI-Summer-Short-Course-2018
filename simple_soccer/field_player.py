import model 
from pygame.math import Vector2
from fsm import StateMachine
import player_states as PState
from entity import MovingEntity
from steering.steering import SteeringBehaviors
from steering.behaviortypes import Behavior

from config import Config

class BasePlayer(MovingEntity):
      max_speed_with_ball = None
      receiving_range = None

      @classmethod
      def initialize_class_parameters(cls,**kwargs):
            cls.max_speed_with_ball = kwargs['max_speed_with_ball']
            cls.receiving_range = kwargs['receiving_range']

      def __init__(self,image, pitch, team, home, heading, model = model.initial_model, **kwargs): 
            # super().__init__(image, pitch, team, home, heading, model, **kwargs)
            # super().__init__(image, **kwargs)
            super().__init__(image,
                             mass = model.player_mass,
                             max_force = model.player_max_force,
                             max_speed = model.player_max_speed,
                             max_turn_rate = model.player_max_turn_rate,
                             **kwargs)

            #register with the entity_manager
            model.entity_manager.register(self)

            self.home = Vector2(home)
            self.pos = Vector2(home)
            self.velocity = Vector2()

            # in case the velocity is zero
            if self.speed < 0.00001:
                  self.set_orientation(Vector2(heading))

            self.model = model
            self.role = None
            self.pitch = pitch
            self.team = team
            self.receiving_range = BasePlayer.receiving_range

            self.steering = SteeringBehaviors(self)
            self.steering.separation_on()

            self.state = PState.wait
            self.fsm = StateMachine(self)
            self.fsm.current_state = self.state
            self.fsm.previous_state = self.state
            self.fsm.global_state = PState.global_player
            self.fsm.current_state.enter(self)

            # TODO: implement and test regulator
            # self.kick_limiter = Regulator(self.model.player_kick_frequency)

      def update(self,dt):
            self.fsm.update()

            self.steering.calculate()

            if self.steering.force.length() < 0.0001:
                  braking_rate = 0.8
                  self.velocity *= braking_rate

            turning_force = util.clamp_vector( self.steering.side_component,
                                               -self.max_turn_rate,
                                               self.max_turn_rate)
            self.heading.rotate_ip(turning_force)

            self.velocity = self.heading * self.speed

      def ball_within_receiving_range(self):
            return self.exact_pos.distance_to(self.pitch.ball()) < self.receiving_range

      def is_controlling_player(self):
            return False

      def at_home(self):
            vpos = Vector2(self.pos)
            return vpos.distance_to(self.home) < 0.001

      def at_target(self, target):
            return self.exact_pos.distance_to(Vector2(target)) < 0.001

      def arrive_on(self):
            self.steering.on( Behavior.ARRIVE )

      def arrive_off(self):
            self.steering.off( Behavior.ARRIVE )


class GoalKeeper(BasePlayer):
      def __init__(self, image, pitch, team, home, heading, model = model.initial_model, **kwargs):
            super().__init__(image, pitch, team, home, heading, model, **kwargs)

            # super().__init__(image,
            #                  mass = model.player_mass,
            #                  max_force = model.player_max_force,
            #                  max_speed = model.player_max_speed,
            #                  max_turn_rate = model.player_max_turn_rate,
            #                  **kwargs)

            # self.home = Vector2(home)
            # self.pos = Vector2(home)
            # self.velocity = Vector2()

            # # in case the velocity is zero
            # if self.speed < 0.00001:
            #       self.set_orientation(Vector2(heading))


            # self.state = PState.Wait.instance()
            # self.model = model
            # self.role = None
            # self.fsm = StateMachine(self)

            # if self.state != None:
            #       self.fsm.current_state = self.state
            #       self.fsm.previous_state = self.state
            #       self.fsm.global_state = PState.global_player

            #       self.fsm.current_state.enter(self)

            # self.steering = SteeringBehaviors(self)
            # self.steering.separation_on()

            # TODO: implement and test regulator
            # self.kick_limiter = Regulator(self.model.player_kick_frequency)



class FieldPlayer(BasePlayer):
      def __init__(self, image, pitch, team, home, heading, model = model.initial_model,**kwargs):
            super().__init__(image, pitch, team, home, heading, model, **kwargs)

            # super().__init__(image, **kwargs)
            # super().__init__(image,
            #                  mass = model.player_mass,
            #                  max_force = model.player_max_force,
            #                  max_speed = model.player_max_speed,
            #                  max_turn_rate = model.player_max_turn_rate,
            #                  **kwargs)

            # self.home = Vector2(home)
            # self.pos = Vector2(home)
            # self.velocity = Vector2()

            # # in case the velocity is zero
            # if self.speed < 0.00001:
            #       self.set_orientation(Vector2(heading))

            # self.model = model
            # self.role = None

            # self.state = PState.wait
            # self.fsm = StateMachine(self)
            # self.fsm.current_state = self.state
            # self.fsm.previous_state = self.state
            # self.fsm.global_state = PState.global_player
            # self.fsm.current_state.enter(self)

            # self.steering = SteeringBehaviors(self)
            # self.steering.separation_on()

            # TODO: implement and test regulator
            # self.kick_limiter = Regulator(self.model.player_kick_frequency)


if __name__ == '__main__':
      import pgzrun
      import config
      from soccer_pitch import SoccerPitch
      import random

      WIDTH = 400
      HEIGHT = 400

      pitch = SoccerPitch(WIDTH,HEIGHT)
      # player = Actor('playerredshirt0',pos=(300,200))
      # player = FieldPlayer('playerredshirt0',home_region = 0, heading=Vector2(-1,0), pos=(300,50))

      home =pitch.pos_from_region(11) 
      player = FieldPlayer('redshirt0',pitch, team=None, home=home, heading=Vector2(-1,0) )
      player.team = None
      player.pos = Vector2(random.randint(10,WIDTH), random.randint(10,HEIGHT))

      def draw():
            screen.fill('white')
            pitch.draw(screen)
            player.draw()
            
      # player.velocity = Vector2(10,25)

      # def update(dt):
            # player.update(dt)
      pgzrun.go()
