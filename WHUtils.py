from ast import If
import random
from dataclasses import dataclass


@dataclass
class RollResult:
    Successful: bool = False
    SuccessLevel: int = 0
    Doubles: bool = False
    Divby10: bool = False
    NaturalSuccess: bool = False
    NaturalFailure: bool = False
   

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
    
def ReverseDice(number):
    reversednumber = (number%19)*10 + int(number/10)
    return reversednumber 

def SkillTest(target, difficulty=0, reversable=False):
    Result = RollResult()
    print("Target:", target, "Difficulty:", difficulty)
    target += difficulty
    Roll = RollPercentage()
    print("Roll:", Roll)
    if reversable == True:
        if ReverseDice(Roll) < Roll:
           Roll = ReverseDice(Roll)
           print("Reversed Roll:", Roll)
    if Roll <= 5:
        Result.Successful = True
        Result.NaturalSuccess = True
        print("Natural Success!")   
    elif Roll >=96:
        Result.Successful = False
        Result.NaturalFailure = True
        print("Natural Failure!")
    elif Roll <= target:  
        Result.Successful = True
        print("Success!")
    else:
        Result.Successful = False
        print("Failure!")   
    
    Result.SuccessLevel = int((target - Roll)/10)
    print("Success Level:", Result.SuccessLevel)
    if CheckForDoubles(Roll):
        Result.Doubles = True
        print("Doubles!")
    if Roll%10 == 0:
        Result.Divby10 = True
        print("Divisible by 10!")
    
    return Result
