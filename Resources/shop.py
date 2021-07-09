class Shop:
    def __init__(self, Dictionary):
        self.ID = Dictionary.get("ID", None)
        self.Name = Dictionary.get("name", None)
        self.Merchant = Dictionary.get("merchant", None)
        self.Dialogue = Dictionary.get("dialogue", None)
        self.Thank = Dictionary.get("thank", None)
        self.Poor = Dictionary.get("poor", None)
        self.Bye = Dictionary.get("bye", None)
        self.Items = Dictionary.get("items", None)
        self.Prices = Dictionary.get("prices", None)
    @staticmethod
    def findShop(name, ID = None):
        if ID:
            for i in Shops:
                if i.ID == ID:
                    return i
        else:
            for i in Shops:
                if i.Name.title() == name.title():
                    return i

Shops = [
    Shop({
        "ID":"1",
        "name":"Deadmines",
        "merchant":"Defias Profiteer",
        "dialogue":"The shifty-eyed merchant whispers in your direction, looking all around to make sure you're alone. \n \n%NPC Defias Profiteer ) : Pssst, you! Commere! I'm not supposed ta be tellin\' ya this, but this mornin\' down at the docks, I overheard that dirty scoundrel VanCleef sayin\' that he dared anyone to enter his mines without a weapon \n \n\'Nobody in these parts is strong enough to defeat me with his own bare hands,\' he says. \n \nSo whaddya say, pal? Think ya can prove him wrong? \n \nRegardless, have a look at my wares and good luck, Hero. Or should I say... good riddance?\" \nThe merchant taunts, laughing manically with betrayal in his eyes.",
        "thank":"A pleasure doin\' business with ye!\"",
        "poor":"The merchant looks at you and cackles \n\"Yer not buying that with a coin purse that light!\"",
        "bye":"Hope to be seein' you around! Hopefully as a corpse!",
        "items": [10001, 10000, 51, 52, 53, 10, 14],
        "prices": [100, 1000, 10, 10, 10, 10, 10]
    })
]