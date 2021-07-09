class Spell:
    def __init__(self, Dictionary):
        self.ID = Dictionary.get("ID", None)
        self.Name = Dictionary.get("attune", None)
        self.Description = Dictionary.get("description", None)
        self.Function = Dictionary.get("function")
    @staticmethod
    def findByID(id):
        for i in Spells:
            if i.ID == id:
                return i
        return None

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
    return msg

Spells = [
    Spell({
        "ID":"1",
        "name":"attune-dmvc",
        "description": "Attunes you to Deadmines.",
        "function": attune
    })
]