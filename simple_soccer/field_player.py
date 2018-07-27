from model import Model
from pygame.math import Vector2
from fsm import StateMachine
import player_state as PState
from entity import MovingEntity
from steering.steering import SteeringBehaviors


class FieldPlayer(MovingEntity):
      def __init__(self, image,home_region, heading, velocity = (0,0), init_state = None, model = Model.instance(),**kwargs):
            super().__init__(image,
                             mass = model.player_mass,
                             max_force = model.player_max_force,
                             max_speed = model.player_max_speed,
                             max_turn_rate = model.player_max_turn_rate,
                             **kwargs)

            self.home = home_region
            self.velocity = Vector2(velocity)

            # in case the velocity is zero
            if self.speed < 0.00001:
                  self.set_orientation(Vector2(heading))


            self.state = init_state
            self.model = model
            self.role = None
            self.fsm = StateMachine(self)

            if self.state != None:
                  self.fsm.current_state = self.state
                  self.fsm.previous_state = self.state
                  self.fsm.global_state = PState.global_player()

                  self.fsm.current_state.enter(self)

            self.steering = SteeringBehaviors(self)
            self.steering.separation_on()

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

      WIDTH = 400
      HEIGHT = 400

      player = FieldPlayer('playerredshirt5',1,Vector2(-1,0))
      player.velocity = Vector2(10,25)

      def update(dt):
            player.update(dt)

      def draw():
            screen.fill('white')
            player.draw()

      pgzrun.go()
