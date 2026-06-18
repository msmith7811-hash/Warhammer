import random
import WHUtils

#Constants

class CharAttrib:

   AttribName = ''
   AttribBase = 0
   AttribAdvances = 0

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
   WeaponSkill = CharAttrib()
   WeaponSkill.SetName('WS')
   BallisticSkill = CharAttrib()
   BallisticSkill.SetName('BS')
   Strength = CharAttrib()
   Strength.SetName('S')
   Toughness = CharAttrib()
   Toughness.SetName('T')
   Initiative = CharAttrib()
   Initiative.SetName('I')
   Agility = CharAttrib()
   Agility.SetName('Ag')
   Dexterity = CharAttrib()
   Dexterity.SetName('Dex')
   Intelligence = CharAttrib()
   Intelligence.SetName('Int')
   WillPower = CharAttrib()
   WillPower.SetName('WP')
   Fellowship = CharAttrib()
   Fellowship.SetName('Fel')
   
   def GetWS(self):
        return self.WeaponSkill.GetValue()

   def GetBS(self):
        return self.BallisticSkill.GetValue()

   def create(self):
        self.CharName = input("Enter a name for your character: ")
        SpeciesSelect = input("Please select 'H'uman, 'D'warf, h'A'lfling, or 'E'lf? ".strip().lower())
        if (SpeciesSelect == 'h'):
            self.CharSpecies = 'Human'
            self.WeaponSkill.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.BallisticSkill.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Strength.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Toughness.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Initiative.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Agility.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Dexterity.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Intelligence.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.WillPower.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Fellowship.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            
        elif (SpeciesSelect == 'd'):
            self.CharSpecies = 'Dwarf'
            self.WeaponSkill.SetBaseValue(30+WHUtils.RollDice()+WHUtils.RollDice())
            self.BallisticSkill.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Strength.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Toughness.SetBaseValue(30+WHUtils.RollDice()+WHUtils.RollDice())
            self.Initiative.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Agility.SetBaseValue(10+WHUtils.RollDice()+WHUtils.RollDice())
            self.Dexterity.SetBaseValue(30+WHUtils.RollDice()+WHUtils.RollDice())
            self.Intelligence.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.WillPower.SetBaseValue(40+WHUtils.RollDice()+WHUtils.RollDice())
            self.Fellowship.SetBaseValue(10+WHUtils.RollDice()+WHUtils.RollDice())
            
        elif (SpeciesSelect == 'e'):
            self.CharSpecies = 'Elf'
            self.WeaponSkill.SetBaseValue(30+WHUtils.RollDice()+WHUtils.RollDice())
            self.BallisticSkill.SetBaseValue(30+WHUtils.RollDice()+WHUtils.RollDice())
            self.Strength.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Toughness.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Initiative.SetBaseValue(40+WHUtils.RollDice()+WHUtils.RollDice())
            self.Agility.SetBaseValue(30+WHUtils.RollDice()+WHUtils.RollDice())
            self.Dexterity.SetBaseValue(30+WHUtils.RollDice()+WHUtils.RollDice())
            self.Intelligence.SetBaseValue(30+WHUtils.RollDice()+WHUtils.RollDice())
            self.WillPower.SetBaseValue(30+WHUtils.RollDice()+WHUtils.RollDice())
            self.Fellowship.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())

        elif (SpeciesSelect == 'a'):
            self.CharSpecies = 'Halfling'
            self.WeaponSkill.SetBaseValue(10+WHUtils.RollDice()+WHUtils.RollDice())
            self.BallisticSkill.SetBaseValue(30+WHUtils.RollDice()+WHUtils.RollDice())
            self.Strength.SetBaseValue(10+WHUtils.RollDice()+WHUtils.RollDice())
            self.Toughness.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Initiative.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Agility.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Dexterity.SetBaseValue(30+WHUtils.RollDice()+WHUtils.RollDice())
            self.Intelligence.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.WillPower.SetBaseValue(30+WHUtils.RollDice()+WHUtils.RollDice())
            self.Fellowship.SetBaseValue(30+WHUtils.RollDice()+WHUtils.RollDice())

        else:
            self.CharSpecies = 'Human'
            self.WeaponSkill.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.BallisticSkill.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Strength.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Toughness.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Initiative.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Agility.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Dexterity.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Intelligence.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.WillPower.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
            self.Fellowship.SetBaseValue(20+WHUtils.RollDice()+WHUtils.RollDice())
        return

   def showLong(self):
        print("*****************************************************")
        print("Name: ",self.CharName)
        print("Species: ",self.CharSpecies)
        print("Class: ",self.Class)
        print("Career: ",self.Career)
        print("Weapon Skill (bonus): ",self.GetWS(), "(",self.WeaponSkill.GetBonus(),")" )
        #print("Weapon Skill Bonus",self.WeaponSkill.GetBonus())
        print("Ballistic Skill (bonus): ",self.GetBS(), "(",self.BallisticSkill.GetBonus(),")")
        #print("Ballistic Skill Bonus: ",self.BallisticSkill.GetBonus())
        print("Strength (bonus): ",self.Strength.GetValue(), "(",self.Strength.GetBonus(),")")
        #print("Strength Bonus: ",self.Strength.GetBonus())
        print("Toughness (bonus): ",self.Toughness.GetValue(), "(",self.Toughness.GetBonus(),")")
        #print("Toughness Bonus: ",self.Toughness.GetBonus())
        print("Initiative (bonus): ",self.Initiative.GetValue(), "(",self.Initiative.GetBonus(),")")
        print("Agility (bonus): ",self.Agility.GetValue(), "(",self.Agility.GetBonus(),")")
        print("Dexterity (bonus): ",self.Dexterity.GetValue(), "(",self.Dexterity.GetBonus(),")")
        print("Intelligence (bonus): ",self.Intelligence.GetValue(), "(",self.Intelligence.GetBonus(),")")
        print("WillPower (bonus): ",self.WillPower.GetValue(), "(",self.WillPower.GetBonus(),")")
        print("Fellowship (bonus): ",self.Fellowship.GetValue(), "(",self.Fellowship.GetBonus(),")")
        print("*****************************************************")
        return
        
   def showShort(self):
        print("Name: ",self.CharName," Race: ",self.CharSpecies," Career: ",self.Career)
        return
 
