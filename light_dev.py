

class Light:
    Off = 'OFF'
    Blown = 'BLOWN'
    Low = 'LOW'
    Med = 'MED'
    MedLow = 'MEDLOW'
    MedHi = 'MEDHI'
    Hi = 'HI'
    
    # this creates our light
    def __init__(self):
         self.health = 1000
         self.status = Light.Off

    # this brightens the light
    @property
    def brighten(self):
        if self.status == Light.Off:
            self.status = Light.Low

        elif self.status == Light.Low:
            self.status = Light.MedLow

        elif self.status == Light.MedLow:
            self.status = Light.Med

        elif self.status == Light.Med:
            self.status = Light.MedHi

        elif self.status == Light.MedHi:
            self.status = Light.Hi

        return self.status

    # this will dim the light
    @property
    def dim(self):
        if self.status == Light.Low:
            self.status = Light.Off

        elif self.status == Light.MedLow:
            self.status = Light.Low

        elif self.status == Light.Med:
            self.status = Light.MedLow

        elif self.status == Light.MedHi:
            self.status = Light.Med

        elif self.status == Light.Hi:
            self.status = Light.MedHi
        
        return self.status

## ------   END OF CLASS  -----

#this is the hunter special lazy man code shortcut
def up():
    print(light.brighten)

def down():
    print(light.dim)
    


if __name__ == '__main__':

    # now lets test the code

    # let's create a test light here
    light = Light()
    print(light.status)

    # let's brighten it twice
##    light.brighten()
##    light.brighten()

    # let print the light status
    print(light.status)





    
##light = Light()
##
##print( light.status )  # Off, Low, MedLow, Med, Medium High, High .... Blown...
##
##light.brighthen()
##light.dim()
##light.off()
##light.how_much_life()
##




       
