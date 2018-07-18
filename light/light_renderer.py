

OFF = 10
class Light:
    OFF = 0
    ON = 1
    
    def __init__(self, status = OFF):
        self._state = status

    def turn_on(self):
        if self._state == Light.OFF:
            self._state = Light.ON
        else:
            self._state = Light.ON

    def turn_off(self):
        if self._state == Light.ON:
            self._state = Light.OFF
        else:
            self._state = Light.OFF

    def draw(self, screen = None):
        if not screen:
            return print(self)
        else:
            if self._state == Light.ON:
                screen.fill(Color('yellow'))
            else:
                screen.fill(Color('black'))

    def __repr__(self):
        status = 'ON' if self._state == Light.ON else 'OFF'
        return 'I am ' + status



def terminate():
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
    

if __name__ == '__main__':

    import sys
    import pygame
    from pygame.constants import HWSURFACE, SRCALPHA
    from pygame import Color
    
##    print('testing the light class')
    light = Light(status=Light.ON)
##    light.draw()

    #pygame boilerplate
    pygame.init()
    screen = pygame.display.set_mode((100,100),HWSURFACE | SRCALPHA)
    FPSCLOCK = pygame.time.Clock()

    #the game loop; keep looping and listening for events until we quit
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and \
                        event.mod & (pygame.KMOD_CTRL | pygame.KMOD_META):
                    terminate()
                if event.key == pygame.K_UP:
                    light.turn_on()
                if event.key == pygame.K_DOWN:
                    light.turn_off()

        screen.fill(Color('white'))
        
        light.draw(screen)
        
        
        pygame.display.flip()
        FPSCLOCK.tick(60)
    

    
