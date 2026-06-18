
import random
import WHCharacter
import WHUtils

CharacterList = []
index = 0;

while True:
        MainMenu=input("Do you want to 'M'anage Characters, 'C'heck things or 'Fight'? 'Q' to quit ").strip().lower()
        if MainMenu=='m':
                while True:
                        NewCharYN=input("Are you adding a 'N'ew character or 'L'oading an existing one? 'M' to return to previous menu.  ").strip().lower()
                        if NewCharYN=='n':
                            print("Creating a new Character!")
                            #new character creation
                            Character = WHCharacter.Monster() 
                            CharacterList.append(Character)
                            Character.create()
                            Character.showLong()
                            index += 1
                        elif NewCharYN=='l':
                            print("Loading an existing Character!")
                            #load character
                            #index += 1
                        elif NewCharYN=='m':
                            break
                        else:
                            print("please select N,E,or Q")      
        elif MainMenu=='f':
                print("Fight! Fight! Fight!")
        elif MainMenu=='c':
                percent = WHUtils.RollPercentage()
                print("you rolled a: ",percent)
                if WHUtils.CheckForDoubles(percent) == True:
                        print("which is a double")
                else:
                        print("which is not a double")
        elif MainMenu=='q':
            print("See you later!")
            quit
            break
        else:
            print("please select M,F,or Q")
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")    
        for Character in CharacterList:
            Character.showShort()    
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
            
        
            
        
            
