import random
class Spell:
    def __init__(self, Dictionary):
        self.ID = Dictionary.get("ID", None)
        self.Name = Dictionary.get("name", None)
        self.Description = Dictionary.get("description", None)
        self.Type = Dictionary.get("type", None)
        self.Function = Dictionary.get("function")
    @staticmethod
    def findByID(id):
        for i in Spells:
            if i.ID == id:
                return i
        return None
def restoreHealth(**kwargs):
    user = kwargs.get('user', None)
    health = kwargs.get('health', None)
    user.modifyHealth(health,health)
    return " \n \nYou restored " + str(health) + " health."

def attune(**kwargs):
    user = kwargs.get('user', None)
    dungeon = kwargs.get('dungeon', None)
    temp = user.Lockouts.split(",")
    lockout = ""
    for i in temp:
        if dungeon in i:
            lockout = i
    newlock = lockout[:1] + "=" + lockout[2:]
    temptwo = user.Lockouts.replace(lockout, newlock)
    user.updateSelf("Lockouts", temptwo)
    msg = " \n \nCongratulations, you are now attuned to "
    if dungeon == "DMVC":
        msg += "the Deadmines!"
    elif dungeon == "KARA":
        msg += "Karazhan!"
    return msg

def immune(**kwargs):
    return "immune"

def medallion(**kwargs):
    user = kwargs.get('user', None)
    item = user.Trinket
    itemSplit = item.split("-")
    spellSplit = itemSplit[4].split("&")
    i = 0
    while i < len(spellSplit):
        #cut
        if spellSplit[i] == "4":
            if int(user.Health) < 100:
                return " \n \nThe medallion cannot be used right now."
            else:
                user.modifyHealth(-100, -100)
                spellSplit[i] = "5"
                itemSplit[4] = "&".join(spellSplit)
                user.updateSelf("trinket", "-".join(itemSplit))
                return " \n \nThe medallion cuts deep, draining 100 of your health."
        #restore
        elif spellSplit[i] == "5":
            spellSplit[i] = "4"
            itemSplit[4] = "&".join(spellSplit)
            user.updateSelf("trinket", "-".join(itemSplit))
            user.modifyHealth(100, 100)
            return " \n \nYou reabsorb the life force in the medallion, restoring 100 health."
        i += 1

def medallionPassive(**kwargs):
    user = kwargs.get('user', None)
    mob = kwargs.get('mob', None)
    item = user.Trinket
    itemSplit = item.split("-")

def fireball1(**kwargs):
    user = kwargs.get('user', None)
    mob = kwargs.get('mob', None)
    if mob and user:
        roll = random.randint(0, 100)
        if roll < 50:
            mob.mobhealth -= 10


Spells = [
    Spell({
        "ID":"1",
        "name":"attune-dmvc",
        "description": "Attunes you to Deadmines.",
        "type":"active",
        "function": attune
    }),
    Spell({
        "ID":"2",
        "name":"attune-kara",
        "description": "Attunes you to Karazhan.",
        "type":"active",
        "function": attune
    }),
    Spell({
        "ID":"3",
        "name":"stunimmune",
        "description": "Makes you resilient against stuns.",
        "type":"onhit",
        "function": immune
    }),
    Spell({
        "ID":"4",
        "name":"vctrinketdrain",
        "description": "Cut the medallion deep into your arm, draining 100 health and storing it within the medallion.",
        "type":"active",
        "function": medallion
    }),
    Spell({
        "ID":"7",
        "name":"vctrinketrestore",
        "description": "Taking fatal damage will instead break open the medallion, causing you to heal for 100 health instead.",
        "type":"onhit",
        "function": medallionPassive
    }),
    Spell({
        "ID":"5",
        "name":"vctrinketrestore",
        "description": "Drain the medallion, restoring the health stored.",
        "type":"active",
        "function": medallion
    }),
    Spell({
        "ID":"6",
        "name":"mhp",
        "description": "Restore 30 health.",
        "type":"active",
        "function": restoreHealth
    }),
    Spell({
        "ID":"8",
        "name":"fire weapon",
        "description": "Shoot a fireball at the target, dealing 10 damage.",
        "type":"proc",
        "function": fireball1
    }),
]