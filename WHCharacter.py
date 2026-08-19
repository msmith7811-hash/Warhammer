import random
import json
import WHUtils as WHU

#Constants

class CharAttrib:

   AttribName = ''
   AttribBase = 0
   AttribAdvances = 0

   def __init__(self,name):
      self.AttribName = name

#get the calculated value of the Attribute
   def GetValue(self):
      return self.AttribBase+self.AttribAdvances

#set the name of the Attribute
   def SetName(self,name):
      self.AttribName = name

   def GetName(self):
      return self.AttribName

   def SetBaseValue(self,value):
      self.AttribBase = value

   def ChangeBaseValue(self,value):
      self.AttribBase += value

   def ChangeAdvancesValue(self,value):
      self.AttribAdvances += value

   def GetBonus(self):
      return int(self.GetValue()/10)

         
      
   

class Monster:
    
   CharName = ''
   CharSpecies = 'H'
   Class = 'Peasant'
   Career = 'Villager'
   WeaponSkillBase = 0
   WeaponSkillAdvances = 0
   WeaponSkillCurrent = 0
   WeaponSkillBonus = 0
   BallisticSkillBase = 0
   BallisticSkillAdvances = 0
   BallisticSkillCurrent = 0
   BallisticSkillBonus = 0
   StrengthBase = 0
   StrengthAdvances = 0
   StrengthCurrent = 0
   StrengthBonus = 0
   ToughnessBase = 0
   ToughnessAdvances = 0
   ToughnessCurrent = 0
   ToughnessBonus = 0
   InitiativeBase = 0
   InitiativeAdvances = 0  
   InitiativeCurrent = 0
   InitiativeBonus = 0
   AgilityBase = 0
   AgilityAdvances = 0  
   AgilityCurrent = 0
   AgilityBonus = 0
   DexterityBase = 0
   DexterityAdvances = 0
   DexterityCurrent = 0
   DexterityBonus = 0
   IntelligenceBase = 0
   IntelligenceAdvances = 0
   IntelligenceCurrent = 0
   IntelligenceBonus = 0
   WillPowerBase = 0
   WillPowerAdvances = 0
   WillPowerCurrent = 0
   WillPowerBonus = 0
   FellowshipBase = 0
   FellowshipAdvances = 0
   FellowshipCurrent = 0
   FellowshipBonus = 0
   WoundsMax = 0
   WoundsCurrent = WoundsMax
   Corruption = 0
   
   
   def GetWS(self):
        return self.WeaponSkillCurrent

   def GetBS(self):
        return self.BallisticSkillCurrent

   def create(self):
        self.CharName = input("Enter a name for your character: ")
        self.Class = "Peasant"
        self.Career = "Villager"
        self.WeaponSkillBase = WHU.RollDice()+WHU.RollDice()
        self.WeaponSkillAdvances = 0
        self.BallisticSkillBase = WHU.RollDice()+WHU.RollDice()
        self.BallisticSkillAdvances = 0
        self.StrengthBase = WHU.RollDice()+WHU.RollDice()
        self.StrengthAdvances = 0
        self.ToughnessBase = WHU.RollDice()+WHU.RollDice()
        self.ToughnessAdvances = 0
        self.InitiativeBase = WHU.RollDice()+WHU.RollDice()
        self.InitiativeAdvances = 0
        self.AgilityBase = WHU.RollDice()+WHU.RollDice()
        self.AgilityAdvances = 0
        self.DexterityBase = WHU.RollDice()+WHU.RollDice()
        self.DexterityAdvances = 0
        self.IntelligenceBase = WHU.RollDice()+WHU.RollDice()
        self.IntelligenceAdvances = 0
        self.WillPowerBase = WHU.RollDice()+WHU.RollDice()
        self.WillPowerAdvances = 0
        self.FellowshipBase = WHU.RollDice()+WHU.RollDice()
        self.FellowshipAdvances = 0
        
        SpeciesSelect = input("Please select 1-Human, 2-Dwarf, 3-Halfling, or 4-Elf? ".strip().lower())
            
        if (SpeciesSelect == '2'):
            self.CharSpecies = 'Dwarf'
            self.WeaponSkillBase += 30
            self.BallisticSkillBase += 20
            self.StrengthBase += 20
            self.ToughnessBase += 30
            self.InitiativeBase += 20
            self.AgilityBase += 10
            self.DexterityBase += 30
            self.IntelligenceBase += 20
            self.WillPowerBase += 40
            self.FellowshipBase += 10

        elif (SpeciesSelect == '4'):
            self.CharSpecies = 'Elf'
            self.WeaponSkillBase += 30
            self.BallisticSkillBase += 30
            self.StrengthBase += 20
            self.ToughnessBase += 20
            self.InitiativeBase += 40
            self.AgilityBase += 30
            self.DexterityBase += 30
            self.IntelligenceBase += 30
            self.WillPowerBase += 30
            self.FellowshipBase += 20

        elif (SpeciesSelect == '3'):
            self.CharSpecies = 'Halfling'
            self.WeaponSkillBase += 10
            self.BallisticSkillBase += 30
            self.StrengthBase += 10
            self.ToughnessBase += 20
            self.InitiativeBase += 20
            self.AgilityBase += 20
            self.DexterityBase += 30
            self.IntelligenceBase += 20
            self.WillPowerBase += 30
            self.FellowshipBase += 30

        else:
            self.CharSpecies = 'Human'
            self.WeaponSkillBase += 20
            self.BallisticSkillBase += 20
            self.StrengthBase += 20
            self.ToughnessBase += 20
            self.InitiativeBase += 20
            self.AgilityBase += 20
            self.DexterityBase += 20
            self.IntelligenceBase += 20
            self.WillPowerBase += 20
            self.FellowshipBase += 20

        self.WeaponSkillCurrent = self.WeaponSkillBase + self.WeaponSkillAdvances
        self.WeaponSkillBonus = int(self.WeaponSkillCurrent/10)
        self.BallisticSkillCurrent = self.BallisticSkillBase + self.BallisticSkillAdvances
        self.BallisticSkillBonus = int(self.BallisticSkillCurrent/10)
        self.StrengthCurrent = self.StrengthBase + self.StrengthAdvances
        self.StrengthBonus = int(self.StrengthCurrent/10)
        self.ToughnessCurrent = self.ToughnessBase + self.ToughnessAdvances
        self.ToughnessBonus = int(self.ToughnessCurrent/10)
        self.InitiativeCurrent = self.InitiativeBase + self.InitiativeAdvances
        self.InitiativeBonus = int(self.InitiativeCurrent/10)
        self.AgilityCurrent = self.AgilityBase + self.AgilityAdvances
        self.AgilityBonus = int(self.AgilityCurrent/10)
        self.DexterityCurrent = self.DexterityBase + self.DexterityAdvances
        self.DexterityBonus = int(self.DexterityCurrent/10)
        self.IntelligenceCurrent = self.IntelligenceBase + self.IntelligenceAdvances
        self.IntelligenceBonus = int(self.IntelligenceCurrent/10)
        self.WillPowerCurrent = self.WillPowerBase + self.WillPowerAdvances
        self.WillPowerBonus = int(self.WillPowerCurrent/10)
        self.FellowshipCurrent = self.FellowshipBase + self.FellowshipAdvances
        self.FellowshipBonus = int(self.FellowshipCurrent/10)

        self.WoundsMax = self.StrengthBonus + 2*(self.ToughnessBonus) + self.WillPowerBonus
        self.WoundsCurrent = self.WoundsMax
        self.Corruption = 0
        self.save()
        return

   def showLong(self):
        print("*****************************************************")
        print("Name: ",self.CharName)
        print("Species: ",self.CharSpecies)
        print("Class: ",self.Class)
        print("Career: ",self.Career)
        print("Weapon Skill (bonus): ",self.WeaponSkillCurrent, "(",self.WeaponSkillBonus,")" )
        print("Ballistic Skill (bonus): ",self.BallisticSkillCurrent, "(",self.BallisticSkillBonus,")")
        print("Strength (bonus): ",self.StrengthCurrent, "(",self.StrengthBonus,")")
        print("Toughness (bonus): ",self.ToughnessCurrent, "(",self.ToughnessBonus,")")
        print("Initiative (bonus): ",self.InitiativeCurrent, "(",self.InitiativeBonus,")")
        print("Agility (bonus): ",self.AgilityCurrent, "(",self.AgilityBonus,")")
        print("Dexterity (bonus): ",self.DexterityCurrent, "(",self.DexterityBonus,")")
        print("Intelligence (bonus): ",self.IntelligenceCurrent, "(",self.IntelligenceBonus,")")
        print("WillPower (bonus): ",self.WillPowerCurrent, "(",self.WillPowerBonus,")")
        print("Fellowship (bonus): ",self.FellowshipCurrent, "(",self.FellowshipBonus,")")
        print("Wounds (maximum): ",self.WoundsCurrent, "(",self.WoundsMax,")")
        print("Corruption: ",self.Corruption)
        print("*****************************************************")
        return
        
   def showShort(self):
        print("Name: ",self.CharName," Race: ",self.CharSpecies," Career: ",self.Career)
        return
   
   def save(self):
       with open(f"{self.CharName}.json", "w") as f:
           #json.dump(self.__dict__, f)
           json.dump(vars(self), f)

   def load(self, CharName):
       with open(f"{CharName}.json", "r") as f:
           data = json.load(f)
           #self.__dict__.update(data)
           vars(self).update(data)