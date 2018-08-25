import model
from pygame.math import Vector2
from fsm import StateMachine
import player_states as PState
from entity import MovingEntity
from steering_behaviors import SteeringBehaviors, BehaviorType
import util
from config import Config

class BasePlayer(MovingEntity):
      max_speed_with_ball = None
      receiving_range = None

      @classmethod
      def initialize_class_parameters(cls,**kwargs):
            cls.max_speed_with_ball = kwargs['max_speed_with_ball']
            cls.receiving_range = kwargs['receiving_range']

      def __init__(self,image, pitch, team, home, heading, model = model.initial_model, **kwargs): 
            super().__init__(image,
                             mass = model.player_mass,
                             **kwargs)

            self.max_turn_rate = model.player_max_turn_rate
            self.max_force = model.player_max_force
            self.max_speed = model.player_max_speed

            #register with the entity_manager
            model.entity_manager.register(self)

            self.home = Vector2(home)
            self.pos = Vector2(home)
            # self.velocity = Vector2()
            # self.heading = Vector2(heading)
            _,self.angle = Vector2(heading).as_polar() 

            print('...creating player{}: @ position {}, angle {}'.format(self.id,self.pos,self.angle ))

            # in case the velocity is zero
            if self.speed < 0.00001:
                  self.angle = 0.0
                  # self.set_orientation(Vector2(heading))

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

            #DEBUG
            if self.id == 1:
                  print('player{} velocity: {}'.format(self.id,self.velocity))
                  print('       steering_force = {}'.format(self.steering.steering_force))

            if self.steering.steering_force.length() < 0.0001:
                  braking_rate = 0.8
                  self.velocity *= braking_rate

            # first calculate the velocity change due to turning
            turning_rate = util.clamp(self.steering.side_component(),
                                      -self.max_turn_rate,
                                      self.max_turn_rate)
            # self.heading.rotate_ip(turning_force)
            # this will indirectly update the heading of the player
            if abs(turning_rate) > 0.001:
                  # this will automagically propogate to a new heading
                  # and side vector
                  self.angle = turning_rate
                  self.velocity = self.speed * self.heading
            # self.heading.rotate_ip(turning_force)

            accel = self.heading *  self.steering.forward_component()/ self.mass 
            self.velocity += accel

            self.exact_pos += self.velocity

      def draw(self,screen):
            super().draw()

            #
            # Show Rendering Aids - Steering_Force
            #

            if self.model.show_steering_force:
                  screen.draw.line(self.exact_pos,
                                   self.exact_pos + self.model.steering_force_display_length * self.steering.steering_force,
                                   (200,0,0))

            if self.model.show_player_states:
                  states = ""
                  if self.steering.is_seek_on():
                        states += "S"
                  if self.steering.is_arrive_on():
                        states += "A"
                  if self.steering.is_separation_on():
                        states += "Sp"
                  if self.steering.is_pursuit_on():
                        states += "P"
                  if self.steering.is_interpose_on():
                        states += "I"

                  if len(states) > 0:
                        offset = self.exact_pos + ( self.heading  * 5) + Vector2(0,5)
                        screen.draw.text(states, offset)

      def ball_within_receiving_range(self):
            return self.exact_pos.distance_to(self.ball()) < self.receiving_range

      def track_ball(self):
            return self.rotate_heading_to_face_position(self.ball())

      def is_controlling_player(self):
            return False

      def at_home(self):
            return self.exact_pos.distance_to(self.home) < 0.001

      def at_target(self, target):
            return self.exact_pos.distance_to(Vector2(target)) < 0.001

      def arrive_on(self):
            self.steering.on( BehaviorType.ARRIVE )

      def arrive_off(self):
            self.steering.off( BehaviorType.ARRIVE )

      @property
      def tagged(self):
            return self.steering.tagged

      @property
      def ball(self):
            return self.pitch.ball

      def __repr__(self):
            if 'GoalKeeper' in str( type(self) ):
                  position = '*'
            else:
                  position = ''
            return '{{[player{}{}] {}}}'.format(self.id, position, self.exact_pos)


class GoalKeeper(BasePlayer):
      def __init__(self, image, pitch, team, home, heading, model = model.initial_model, **kwargs):
            super().__init__(image, pitch, team, home, heading, model, **kwargs)


class FieldPlayer(BasePlayer):
      def __init__(self, image, pitch, team, home, heading, model = model.initial_model,**kwargs):
            super().__init__(image, pitch, team, home, heading, model, **kwargs)



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
