import WHCharacter
import WHUtils

# Determine surprise
# 
# Determine initiative 

round = 0
inCombat = True
attackRollSL = WHUtils.RollResult()
defenseRollSL = WHUtils.RollResult()

def applyDamage (character, target, SuccessLevel):
   global inCombat
   damage = SuccessLevel + character.StrengthBonus - target.ToughnessBonus
   if damage < 1:
      damage = 1   
   target.WoundsCurrent -= damage  
   location = getLocation()
   print(target.CharName," was hit in the ", location, " and took ", damage, " damage")
   if target.WoundsCurrent <= 0:
      print(target.CharName, " has been killed by ", character.CharName)
      inCombat = False   

def meleeAttack(character, target):
   print(character.CharName, " is attacking ", target.CharName)
   print(character.CharName, " rolls to attack" )
   attackRollSL = WHUtils.SkillTest(character.GetWS()+character.MeleeSkill_basic.GetBonus())
   print(target.CharName, " rolls to defend" )
   defenseRollSL = WHUtils.SkillTest(target.GetWS()+target.MeleeSkill_basic.GetBonus())
   if attackRollSL.SuccessLevel > defenseRollSL.SuccessLevel:
      SuccessLevel = attackRollSL.SuccessLevel
      print(character.CharName, " hits ", target.CharName, "with a success level of", SuccessLevel)
      applyDamage(character, target, SuccessLevel)
   else:       
      print(character.CharName, " misses ", target.CharName)

def getLocation():
     locationRoll = WHUtils.RollPercentage()
     if locationRoll <= 9:
          return "Head"
     elif locationRoll <= 24:
          return "Secondary Arm"
     elif locationRoll <= 44:
          return "Primary Arm"
     elif locationRoll <= 79:
          return "Body"
     elif locationRoll <= 89:
          return "Left Leg"
     else:
          return "Right Leg"


def Combat(hero, opponent):
   global round
   global inCombat
   # determine initiative
   while inCombat:
      round += 1
      print("****************** Round: ", round, " ******************")
      print(hero.CharName, " has ", hero.WoundsCurrent, " wounds remaining")
      print(opponent.CharName, " has ", opponent.WoundsCurrent, " wounds remaining")
      action = input("What do they want to do? 1 for Attack, 2 for Quit")
      if action == '1': #### Attack
         meleeAttack(hero, opponent)
         meleeAttack(opponent, hero)
      if action == '2': #### Quit
         inCombat = False



     
#for each round
##for each character, by initiative
##select action
###if not engaged, can Walk up to walk movement
###one of the following
#### Sprint (if not engaged)
##### Make average (+20) Athletics test, monve Run + SL in yards 
#### Charge (if not engaged, replaces walk) - Sprint + melee attack at +10
#### Assess  

##### Roll to hit 
###### Opposed Melee Test, Highest SL wins
####### determine Criticals/Fumbles
####### if successful
######## Determine hit location
######## Determine Damage
######## Apply Damage
######## Apply Criticals
###### if not successful
####### apply fumbles
#### Defend 

   