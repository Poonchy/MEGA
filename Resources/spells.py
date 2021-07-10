class Spell:
    def __init__(self, Dictionary):
        self.ID = Dictionary.get("ID", None)
        self.Name = Dictionary.get("attune", None)
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
    print ("success")
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
            if int(user.Health) < 30:
                return " \n \nThe medallion cannot be used right now."
            else:
                user.modifyHealth(-30, -30)
                spellSplit[i] = "5"
                itemSplit[4] = "&".join(spellSplit)
                user.updateSelf("trinket", "-".join(itemSplit))
                return " \n \nThe medallion cuts deep, draining 30 of your health."
        #restore
        elif spellSplit[i] == "5":
            spellSplit[i] = "4"
            itemSplit[4] = "&".join(spellSplit)
            user.updateSelf("trinket", "-".join(itemSplit))
            user.modifyHealth(30, 30)
            return " \n \nYou reabsorb the life force in the medallion, restoring 30 health."
        i += 1

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
        "type":"passive",
        "function": immune
    }),
    Spell({
        "ID":"4",
        "name":"vctrinketdrain",
        "description": "Cut the medallion deep into your arm, draining 30 health and storing it within the medallion.",
        "type":"active",
        "function": medallion
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
]