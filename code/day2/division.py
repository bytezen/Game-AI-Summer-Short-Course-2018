
class Divider:
    """
        This is a class that computes the quotient and remainder of 2 numbers
    """
    def __init__(self):
        self.dividend = None
        self.divisor = None


    def div(self):
        print('{Divider.div method is running}')
        
        if self.dividend != None and self.divisor != None:
            p = 0

            q = self.dividend            

            while q >= self.divisor:
                q = q - self.divisor
                p = p + 1
            return p,q            

class Divider2:
    """
        This is a class that computes the quotient and remainder of 2 numbers
    """
    def __init__(self,a,b):
        self.dividend = a
        self.divisor = b


    def div(self):
        print('{Divider2.div method is running}')
        
        if self.dividend != None and self.divisor != None:
            p = 0

            q = self.dividend            

            while q >= self.divisor:
                q = q - self.divisor
                p = p + 1
            return p,q            


class Divider3:
    """
        This is a class that computes the quotient and remainder of 2 numbers
    """
    def __init__(self,dividend=None,divisor=None):
        self.dividend = dividend
        self.divisor = divisor


    def div(self):
        print('{Divider2.div method is running}')
        
        if self.dividend != None and self.divisor != None:
            p = 0

            q = self.dividend            

            while q >= self.divisor:
                q = q - self.divisor
                p = p + 1
            return p,q  

def div(a,b):
    """
    function that computes division via
    a series of substractions
    """
    # counter for the number of times we have subtracted the divisor
    p = 0
    #initialize the quotient to the dividend
    q = a

    # run this loop while we have enough divisor to substract from
    while q >= b:
        #substract the divisor from the dividend
        q = q - b
        # increment the counter
        p = p + 1

    # if we are here then we can't take any more away from the quotient
    # we will return the number of times that we subtracted the divisor
    # and any amount that we have left over
    return p,q

# --------
# Main function
#
#
#
def main():
    print(" Hey, I have a cool way to divide something..give it a try\n ")

    dividend = int(input('enter a number that you would like to divide\n...'))
    divisor = int(input('\nwhat would you like to divide the number by\n...'))

    input('\n...press enter to use my custon division machine...')

    q,r = div(dividend,divisor)

    print('\n\t***', dividend, 'divided by ', divisor, ' is equal to ',q,' with ', r,' left over ***')
    
    

## This will only run when this file is loaded as a main module

if __name__=='__main__':
    
##    print(" Hey, I have a cool way to divide something..give it a try\n ")
##
##    dividend = int(input('enter a number that you would like to divide\n...'))
##    divisor = int(input('\nwhat would you like to divide the number by\n...'))
##
##    input('\n...press enter to use my custon division machine...')
##
##    q,r = div(dividend,divisor)
##
##    print('\n\t***', dividend, 'divided by ', divisor, ' is equal to ',q,' with ', r,' left over ***')
##    
    pass
