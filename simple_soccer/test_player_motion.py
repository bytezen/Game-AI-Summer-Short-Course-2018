import pgzrun
import soccer_pitch
import team
import model as Model
import field_player
import math

WIDTH = 800
HEIGHT = 600
#initial mouse position
mx,my = (0,0)
targetx,targety = (0,0)

#initialize the parameters
model = Model.initial_model

mock_pitch = soccer_pitch.SoccerPitch(WIDTH,HEIGHT)
test_team = team.SoccerTeam( team.HOME, mock_pitch )

# for testing purposes let's only keep 1 player
del test_team.players[1:]
player = test_team.players[0]

# test_team.players[0].angle = -180
# test_team.players[0].velocity = (-10,0)
# test_team.players[0].home = (50,300)

# player.arrive_on()
# player.steering.target = mx,my

#TODO: this is clunky and should be handled by the API
for p in test_team.players:
    Model.add_player(model, p)

#TEST 
test_team.players[0].exact_pos = (400,280)
print('Starting Player {} position = {} home ={}'.format(test_team.players[0].id, test_team.players[0].exact_pos, test_team.players[0].home))


test_actor = Actor('blueshirt0')
test_actor.pos = 600,300
steering_force = (0,0)
turn_force = (0,0)
side_component = 0
max_turn_rate = 0.15
turn_rate = 5.0 

def draw():
    mock_pitch.draw(screen)
    #draw target
    screen.draw.circle((mx,my), 10, (200,0,0))
    screen.draw.filled_circle((targetx,targety), 10, (200,0,0))
    screen.draw.line(tuple(player.exact_pos),
                     tuple(player.exact_pos + steering_force),
                     (200,200,0))

    test_team.draw(screen)
    # test_actor.angle = player.angle
    # test_actor.draw()

def update(dt):
    global steering_force, turn_force

    test_team.update(dt)
    player.steering.target = targetx,targety
    steering_force = player.steering.target - player.exact_pos

    side_component = player.side.dot(steering_force.normalize())
    _turn = -side_component * turn_rate

    # player.angle = math.degrees(ang + rot_angle)
    if abs(_turn) < 0.2 :
        player.angle = -steering_force.as_polar()[1]
    else:
        player.angle += _turn

    # print('steering.side = ', side_component, '  turn = ', _turn, '  curr_ang = ', player.angle)


def on_mouse_move(pos):
    global mx, my
    mx,my = pos

def on_mouse_down(pos):
    global targetx, targety
    targetx,targety = pos
pgzrun.go()
