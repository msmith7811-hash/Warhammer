
import random
import WHCharacter
import WHUtils
import WHCombat

CharacterList = []
index = 0

while True:
        MainMenu=input("Do you want to 'M'anage Characters, 'C'heck things or 'Fight'? 'Q' to quit ").strip().lower()
        if MainMenu=='m':
                while True:
                        NewCharYN=input("Are you 1-creating a New character or 2-Loading an existing character? 9 to return to previous menu.  ").strip().lower()
                        if NewCharYN=='1':
                            print("Creating a new Character!")
                            #new character creation
                            Character = WHCharacter.Monster() 
                            CharacterList.append(Character)
                            Character.create()
                            Character.showLong()
                            index += 1
                        elif NewCharYN=='2':
                            print("Loading an existing Character!")
                            CharacterName = input("Enter the name of the character to load: ")
                            Character = WHCharacter.Monster()
                            CharacterList.append(Character)
                            Character.load(CharacterName)
                            Character.showLong()
                            index += 1
                        elif NewCharYN=='9':
                            break
                        else:
                            print("please select 1,2, or 9")      
        elif MainMenu=='f':
                print("Fight! Fight! Fight!")
                WHCombat.Combat(CharacterList[0], CharacterList[1])
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
            
        
            
        
            
