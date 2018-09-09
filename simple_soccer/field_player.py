import model
from pygame.math import Vector2
from fsm import StateMachine
import player_states as PState
from entity import MovingEntity
from steering_behaviors import SteeringBehaviors, BehaviorType
import util
import math
from config import Config

class BasePlayer(MovingEntity):
      # max_speed_with_ball = None
      # receiving_range = None

      # @classmethod
      # def initialize_class_parameters(cls,**kwargs):
      #       cls.max_speed_with_ball = kwargs['max_speed_with_ball']
      #       cls.receiving_range = kwargs['receiving_range']

      def __init__(self,image, pitch, team, home, heading, model = model.initial_model, **kwargs): 
            super().__init__('redshirt0') #image,  **kwargs)

            self.max_turn_rate = model.player_max_turn_rate
            self.max_force = model.player_max_force
            self.max_speed = model.player_max_speed

            #register with the entity_manager
            model.entity_manager.register(self)

            self.home = Vector2(home)
            self.pos = Vector2(home)
            self.mass = model.player_mass
            # self.velocity = Vector2()
            # self.heading = Vector2(heading)
            _,self.angle = Vector2(heading).as_polar() 

            print('...creating player{}: @ position {}, angle {}'.format(self.id,self.pos,self.angle ))

            # in case the velocity is zero
            if self.speed < 0.00001:
                  self.angle = 0.0
                  # self.set_orientation(Vector2(heading))

            self.model = model
            self.max_speed_with_ball = model.player_max_speed_with_ball
            self.receiving_range = model.ball_within_receiving_range
            self.role = None
            self.pitch = pitch
            self.team = team

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


            #apply braking if there is no steering force but there is velocity
            if self.steering.steering_force.length() < 0.0001 and (self.velocity.length_squared() > 0.001):
                  braking_rate = 0.8
                  self.velocity *= braking_rate

            # first calculate the speed change due to the force

            #FORWARD COMPONENT CALC
            # get the components now because updating the angle and
            # velocity will change the computations
            forward_component = self.steering.forward_component()
            side_component = self.steering.side_component()

            # first calculate the velocity change due to turning

            dAngle = (side_component * self.max_turn_rate)
            # this will adjust the heading...
            self.angle -= dAngle

            speed = abs(forward_component) * self.max_speed
            self.velocity = (speed / self.mass) * self.heading


            #FORWARD COMPONENT CALC
            # accel = self.heading *  forward_component/ self.mass 
            # self.velocity += accel

            # self.exact_pos += self.velocity

            # self.exact_pos +=  speed * self.heading #self.velocity
            self.exact_pos = self.exact_pos + self.velocity

            # if debug_output:
            #       print('   prevPos = {}  position={}'.format(self.prev_pos, self.exact_pos))
            #       print('---END UPDATE\n\n')

      def draw(self,screen):
            super().draw()

            #
            # Show Rendering Aids - Steering_Force
            #

            #DEBUG
            screen.draw.circle( self.home, 10, (255,0,0) )
            # if self.at_home():

            #print ID
            screen.draw.text(str(self.id), self.exact_pos + Vector2(0,-20))


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

            if self.model.show_heading:
                   screen.draw.line(self.exact_pos,
                                    self.exact_pos + 50 * self.heading,
                                    (0,255,0))
                   screen.draw.line(self.exact_pos,
                                    self.exact_pos + 50 * self.side,
                                    (0,0,255))



      def ball_within_receiving_range(self):
            return self.exact_pos.distance_to(self.ball()) < self.receiving_range

      def track_ball(self):
            return self.rotate_heading_to_face_position(self.ball())

      def is_controlling_player(self):
            return False

      def at_home(self):
            return self.at_target(self.home) 
            # return self.exact_pos.distance_to(self.home) < 0.001

      def at_target(self, target):
            if self.id == 1:
                  print('[FieldPlayer.at_target] pos: {}, target: {}, dist: {} '.format(self.exact_pos,target,self.exact_pos.distance_to(Vector2(target))))
                  print('    vel= {}, speed= '.format(self.velocity,self.speed))
            return self.exact_pos.distance_to(Vector2(target)) < 1.0

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
