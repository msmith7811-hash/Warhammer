import random


def RollDice(die=10):
    return random.randint(1,die)

def RollPercentage():
    return random.randint(1,100)

def CheckForDoubles(number):
    if (number>100):
        print("too big")
        return False
    elif (number < 1):
        print("too small")
        return False
    elif (number==100):
        print("double zeros!")
        return True
    elif (int(number/10)==int(number%10)):
        print("first die:", int(number/10))
        print("second die:", int(number%10))
        return True
    else:
        return False
    
    
