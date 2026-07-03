import WHCharacter
import WHUtils

# Determine surprise
# 
# Determine initiative 

round = 0
inCombat = True

def Combat(WHCharacter hero, WHCharacter opponent):
   global round
   global inCombat
   # determine initiative
   while inCombat:
      action = input("What does", hero.Charname," want to do? '1' for Attack, '2' for Quit")
      if action == '1': #### Attack
         meleeAttack(hero, opponent)
         meleeAttack(opponent, hero)



     
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
def meleeAttack(character, target):
   attackRoll = WHUtils.skillTest(character.GetWS())
   defenseRoll = WHUtils.skillTest(target.GetWS())
   if attackRoll > defenseRoll:
      SuccessLevel = attackRoll - defenseRoll
      print(character.Charname, " hits ", target.Charname, "with a success level of", SuccessLevel)
      applyDamage(character, target, SuccessLevel)     

def applyDamage (character, target, SuccessLevel):
   target.currentWounds -= SuccessLevel + character.StrengthBonus.GetValue() - target.ToughnessBonus.GetValue()
   if target.currentWounds <= 0:
      print(target.Charname, " has been killed by ", character.Charname)
      inCombat = False   
   