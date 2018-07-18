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


    def __repr__(self):
        status = 'ON' if self._state == Light.ON else 'OFF'
        return 'I am ' + status


if __name__ == '__main__':

    print('testing the light class')
    light = Light()
    print(light)

    
