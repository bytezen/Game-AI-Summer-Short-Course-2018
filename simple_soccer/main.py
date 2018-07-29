import pgzrun
import soccer_pitch
import model

HEIGHT = 600
WIDTH = 800

pitch = soccer_pitch.SoccerPitch(WIDTH * .8,
                                 HEIGHT * .8,
                                 (0.1 * WIDTH, 0.1 * HEIGHT),
                                 model.initial_model)

def draw():
    screen.fill('yellow')
    pitch.draw(screen)


pgzrun.go()
