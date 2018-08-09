import model 
from pygame.math import Vector2
from fsm import StateMachine
import player_states as PState
from entity import MovingEntity
from steering.steering import SteeringBehaviors

from config import Config

class BasePlayer(MovingEntity):
      def __init__(self,image, pitch, home, heading, model = model.initial_model, **kwargs): 
            # super().__init__(image, **kwargs)
            super().__init__(image,
                             mass = model.player_mass,
                             max_force = model.player_max_force,
                             max_speed = model.player_max_speed,
                             max_turn_rate = model.player_max_turn_rate,
                             **kwargs)

            self.home = Vector2(home)
            self.pos = Vector2(home)
            self.velocity = Vector2()

            # in case the velocity is zero
            if self.speed < 0.00001:
                  self.set_orientation(Vector2(heading))

            self.model = model
            self.role = None
            self.pitch = pitch

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




class GoalKeeper(MovingEntity):
      def __init__(self, image, pitch, home, heading, model = model.initial_model, **kwargs):
            super().__init__(image,
                             mass = model.player_mass,
                             max_force = model.player_max_force,
                             max_speed = model.player_max_speed,
                             max_turn_rate = model.player_max_turn_rate,
                             **kwargs)

            self.home = Vector2(home)
            self.pos = Vector2(home)
            self.velocity = Vector2()

            # in case the velocity is zero
            if self.speed < 0.00001:
                  self.set_orientation(Vector2(heading))


            self.state = PState.Wait.instance()
            self.model = model
            self.role = None
            self.fsm = StateMachine(self)

            if self.state != None:
                  self.fsm.current_state = self.state
                  self.fsm.previous_state = self.state
                  self.fsm.global_state = PState.global_player

                  self.fsm.current_state.enter(self)

            self.steering = SteeringBehaviors(self)
            self.steering.separation_on()

            # TODO: implement and test regulator
            # self.kick_limiter = Regulator(self.model.player_kick_frequency)



class FieldPlayer(BasePlayer):
      def __init__(self, image, pitch, home, heading, model = model.initial_model,**kwargs):
            super().__init__(image, pitch, home, heading, model, **kwargs)

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


if __name__ == '__main__':
      import pgzrun
      import config
      from soccer_pitch import SoccerPitch

      WIDTH = 400
      HEIGHT = 400

      pitch = SoccerPitch(WIDTH,HEIGHT)
      # player = Actor('playerredshirt0',pos=(300,200))
      # player = FieldPlayer('playerredshirt0',home_region = 0, heading=Vector2(-1,0), pos=(300,50))
      player = FieldPlayer('playerredshirt0',pitch, home=pitch.pos_from_region(11), heading=Vector2(-1,0) )

      def draw():
            screen.fill('white')
            pitch.draw(screen)
            player.draw()
            
      # player.velocity = Vector2(10,25)

      # def update(dt):
            # player.update(dt)
      pgzrun.go()
