import random

class Dungeon:
    def __init__(self, Rooms, Dictionary):
        self.rooms = Rooms
        self.intro = Dictionary.get("intro", None)
        self.attunefail = Dictionary.get("attunefail", None)
        self.cPoS = Rooms[0]
    def returnValidMoves(self):
        validMoves = {}
        if self.cPoS.back:
            validMoves["back"] = self.cPoS.back.back
        if self.cPoS.left:
            validMoves["left"] = self.cPoS.left
        if self.cPoS.right:
            validMoves["right"] = self.cPoS.right
        if self.cPoS.forward:
            validMoves["forward"] = self.cPoS.forward
        return validMoves
    def move(self, direction):
        if self.cPoS.back and direction == "back":
            self.cPoS = self.cPoS.back
        elif self.cPoS.left and direction == "left":
            self.cPoS = self.cPoS.left
        elif self.cPoS.right and direction == "right":
            self.cPoS = self.cPoS.right
        elif self.cPoS.forward and direction == "forward":
            self.cPoS = self.cPoS.forward

class Boss:
    def __init__(self, Dictionary):
        self.ID = Dictionary.get("ID", None)
        self.name = Dictionary.get("name", None)
        self.level = Dictionary.get("level", None)
        self.chance = Dictionary.get("chance", None)
        self.health = Dictionary.get("health",None)
        self.damage = Dictionary.get("damage",None)
        self.loot = Dictionary.get("loot", None)
        self.killquote = Dictionary.get("killquote",None)
        self.diequote = Dictionary.get("diequote",None)

        #Rares 
        self.type = Dictionary.get("type",None)
        self.chance = Dictionary.get("chance", None)
        self.suprise = Dictionary.get("suprise", None)

        #Challenge mode
        self.cmodecheck = Dictionary.get("cmodecheck", None)
        self.cmode = Dictionary.get("cmode", None)
        self.cmkill = Dictionary.get("cmkill", None)
        self.cmdie = Dictionary.get("cmdie", None)
        self.cmloot = Dictionary.get("cmloot", None)

        #hardmode
        self.hardmodecheck = Dictionary.get("hardmodecheck", None)
    def rollLoot(self, cmode):
        val = 0
        roll = random.randint(0, 100)
        loot = self.cmloot if cmode else self.loot
        for i in loot:
            val += loot[i]
            if roll < val:
                return i

class Treasure:
    def __init__(self, Dictionary):
        self.ID = Dictionary.get("ID", None)
        self.loot = Dictionary.get("loot", None)
        self.req = Dictionary.get("req", None)
        self.success = Dictionary.get("success", None)
        self.failure = Dictionary.get("failure", None)
    def rollLoot(self):
        val = 0
        roll = random.randint(0, 100)
        loot = self.loot
        for i in loot:
            val += loot[i]
            if roll < val:
                return i

class Interactable:
    def __init__(self, Dictionary):
        self.ID = Dictionary.get("ID", None)
        self.name = Dictionary.get("name", None)
        self.restriction = Dictionary.get("restriction", None)
        self.req = Dictionary.get("req", None)
        self.success = Dictionary.get("success", None)
        self.failure = Dictionary.get("failure", None)

class Room:
    def __init__(self, Dictionary):
        self.ID = Dictionary.get("ID", None)
        self.name = Dictionary.get("name", None)
        self.description = Dictionary.get("description", None)
        self.clear = Dictionary.get("clear", None)
        self.boss = Dictionary.get("boss", None)
        self.rare = Dictionary.get("rare", None)
        self.treasure = Dictionary.get("treasure", None)
        self.interactable = Dictionary.get("interactable", None)
        self.forward = None
        self.back = None
        self.left = None
        self.right = None

#Key Reference