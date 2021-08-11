import Resources.item as itm

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
        self.FunctionCheck = Dictionary.get("functioncheck", None)
        self.Function = Dictionary.get("function", None)
        self.FunctionQuote = Dictionary.get("functionquote")
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
def none(user):
    return False
def reforgeKeyCheck(user):
    if user.checkIfHasItem(itm.Item.returnItem("Essence of Karazhan")) and user.checkIfHasItem(itm.Item.returnItem("Fragmented Key Bow")) and user.checkIfHasItem(itm.Item.returnItem("Fragmented Key Blade")):
        return "🔑"
    return False
def reforgeKey(user):
    one = user.checkIfHasItem(itm.Item.returnItem("Essence of Karazhan"))
    two = user.checkIfHasItem(itm.Item.returnItem("Fragmented Key Bow"))
    three = user.checkIfHasItem(itm.Item.returnItem("Fragmented Key Blade"))
    user.removeFromInventory(one[0][0])
    user.removeFromInventory(two[0][0])
    user.removeFromInventory(three[0][0])
    user.addToInventory(itm.Item.ItemStringWithNewGlobalID(itm.Item.returnItem("Key To Karazhan")))
    return True

Shops = [
    Shop({
        "ID":"1",
        "name":"Deadmines",
        "merchant":"Defias Profiteer",
        "dialogue":"The shifty-eyed merchant whispers in your direction, looking all around to make sure you're alone. \n \n%NPC Defias Profiteer ) : Pssst, you! Commere! I'm not supposed ta be tellin\' ya this, but this mornin\' down at the docks, I overheard that dirty scoundrel VanCleef sayin\' that he dared anyone to enter his mines without a weapon \n \n\'Nobody in these parts is strong enough to defeat me with his own bare hands,\' he says. \n \nSo whaddya say, pal? Think ya can prove him wrong? \n \nRegardless, have a look at my wares and good luck, Hero. Or should I say... good riddance?\" \nThe merchant taunts, laughing manically with betrayal in his eyes.",
        "thank":"%NPC Defias Profiteer ) :\"A pleasure doin\' business with ye!\"",
        "poor":"The merchant looks at you and cackles \n%NPC Defias Profiteer ) :\"Yer not buying that with a coin purse that light!\"",
        "bye":"%NPC Defias Profiteer ) : \"Hope to be seein' you around! Hopefully as a corpse!\"",
        "items": [10001],
        "prices": [500],
        "functioncheck":none
    }),
    Shop({
        "ID":"2",
        "name":"Karazhan",
        "merchant":"Archmage Alturius",
        "dialogue":"You approach an old man, hair as white as snow and a face emulsified into a fuzzy beard. \n%NPC Archmage Alturius ) : 'Are you familiar with Karazhan? It's more than a mere building. It is a portal into the nether, a beacon shining into other worlds. The possible repercussions of it falling into the wrong hands are unthinkable. This demonic intrusion must be stopped. \n \n If you want entry into Karazhan, you're going to need the key. It was fragmented by the legion forces that inhabit this tower now, but I can reforge it if you bring me the pieces. \n \nThe Essence of Karazhan can be found on one of the shades around here. On your journey, you might rarely encounter a Shade of Karazhan. \n \nThe Key's Blade was given to the city of Stormwind, but I heard it was lost when a rebelious group of masons rioted. Perhaphs they now hold onto the key. \n \nWith all that said, feel free to have a chat with Darius, and see if anything he offers can help you on your journey.",
        "thank":"A pleasure doin\' business with ye!\"",
        "poor":"The merchant looks at you and cackles \n\"Yer not buying that with a coin purse that light!\"",
        "bye":"Hope to be seein' you around! Hopefully as a corpse!",
        "items": [10004],
        "prices": [5000],
        "functioncheck":reforgeKeyCheck,
        "function":reforgeKey,
        "functionquote":"I make a de key is in bag"
    })
]


