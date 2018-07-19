
ON = 'ON'
OFF = 'OFF'

light_status = OFF
light_status = False


def lightbulb():
    global light_status, ON, OFF

    # outputting what the light is now

    print('the light is: ', light_status)
    
    response = input(' do you want to flip the switch [y/n] ')
##
##    if response == 'y':
##        if light_status == ON:
##            light_status = OFF
##        else:
##            light_status = ON

    if response == 'y':
        light_status = not light_status


for i in range(10):
    lightbulb()
