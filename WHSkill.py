import WHUtls.py

class WHSkill:
    def __init__(self, name, description, attribute, level=0, isAdvanced=False):
        self.name = name
        self.description = description
        self.attribute = attribute
        self.isAdvanced = isAdvanced
        self.level = level

    def GetBonus(self):
        return self.level

    def SetLevel(self, level):
        self.level = level

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
        else:
            return 999

    def LevelUp(self):
        self.level += 1

     