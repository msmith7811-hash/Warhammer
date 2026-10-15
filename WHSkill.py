import WHUtils
from dataclasses import dataclass

@dataclass
class WHSkill:
    def __init__(self, name="skill", description="To pay the bills", attribute="Fellowship", level=0, isAdvanced=False):
        self.name = name
        self.description = description
        self.attribute = attribute
        self.isAdvanced = isAdvanced
        self.level = level

    def GetBonus(self):
        return self.level

    def SetLevel(self, level):
        self.level = level

    def IsUsable(self):
        if not self.isAdvanced:
            return True
        elif self.level > 0:
            return True
        else:
            return False

    def XPToLevel(self, xp):
        if self.level<=5:
            return 10
        elif self.level<=10:
            return 15
        elif self.level<=15:
            return 20
        elif self.level<=20:
            return 30
        elif self.level<=25:
            return 40
        elif self.level<=30:
            return 60
        elif self.level<=35:
            return 80
        elif self.level<=40:
            return 110
        elif self.level<=45:
            return 140
        elif self.level<=50:
            return 180
        elif self.level<=55:
            return 220
        elif self.level<=60:
            return 270   
        elif self.level<=65:
            return 320
        elif self.level<=70:
            return 380
        else:
            return 440

    def LevelUp(self):
        self.level += 1

       