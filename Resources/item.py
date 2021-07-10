import Resources.imports as res
import Resources.connection as con
import Resources.spells as spl
class Item:
    def __init__(self, Dictionary):
        self.globalID = Dictionary.get("globalID", None)
        self.ID = Dictionary.get("ID", None)
        self.ModelID = Dictionary.get("modelID", None)
        self.Name = Dictionary.get("name", None)
        self.Rarity = Dictionary.get("rarity", None)
        self.Flavor = Dictionary.get("flavor", None)
        self.Value = Dictionary.get("value", None)
        self.Bound = Dictionary.get("bound", None)
        self.Level = Dictionary.get("level", None)
        self.Stamina = Dictionary.get("stamina", "0")
        self.Armor = Dictionary.get("armor", "0")
        self.Stat = Dictionary.get("stat", "0")
        self.Damage = Dictionary.get("damage", None)
        self.Type = Dictionary.get("type", None)
        self.Class = Dictionary.get("class", None)
        self.Slot = Dictionary.get("slot", None)
        self.Colors = Dictionary.get("colors", None)
        self.Spells = Dictionary.get("spells", None)
        self.SpellAttrs = Dictionary.get("spellattrs", None)
        self.ShowHair = Dictionary.get("showHair", None)
        self.Charges = Dictionary.get("charges", None)
        self.Reagents = Dictionary.get("reagents", None)

    def exists(self):
        if self.Name == None:
            return False
        return True
    def returnItemString(self):
        globalid = self.globalID if self.globalID else "F"
        id = self.ID if self.ID else "F"
        bound = self.Bound if self.Bound else "F"
        charges = self.Charges if self.Charges else "F"
        spells = ""
        if self.Spells:
            for i in self.Spells:
                spells += i.ID + "&"
        else:
            spells = "F"
        string = globalid + "-" + id + "-" + id + "-" + bound + "-" + spells + "-" + charges
        return string
    def returnFullItemName(self):
        rarityColor = "0,0,0"
        if self.Rarity == "Common":
            rarityColor = "255,255,255"
        elif self.Rarity == "Uncommon":
            rarityColor = "30,255,0"
        elif self.Rarity == "Rare":
            rarityColor = "0,112,221"
        elif self.Rarity == "Epic":
            rarityColor = "163,53,238"
        elif self.Rarity == "Legendary":
            rarityColor = "255,128,0"
        return "%ITEM" + rarityColor + " [" + self.Name + "]"
    def ItemStringWithNewGlobalID(self):
        globalID = str(self.incrementGlobalItemId())
        id = self.ID if self.ID else "F"
        bound = self.Bound if self.Bound else "F"
        charges = self.Charges if self.Charges else "F"
        spells = ""
        if self.Spells:
            print (self.Spells)
            for i in self.Spells:
                print (i)
                spells += i.ID + "&"
        else:
            spells = "F"
        string = globalID + "-" + id + "-" + id + "-" + bound + "-" + spells + "-" + charges
        return string

    @staticmethod
    def createItem(ID, modelID, name, rarity, flavor, value, bound, level, stamina, armor, stat, damage, Type, Class, slot, colors, spells, showHair, charges):
        Dictionary = {
            "ID": ID,
            "modelID": modelID,
            "name": name,
            "rarity": rarity,
            "flavor": flavor,
            "value": value,
            "bound": bound,
            "level": level,
            "stamina": stamina,
            "armor": armor,
            "stat": stat,
            "damage": damage,
            "type": Type,
            "class": Class,
            "slot": slot,
            "colors": colors,
            "spells": spells,
            "showHair": showHair,
            "charges": charges
        }
        return Dictionary

    @staticmethod
    def returnItem(name, ID = None):
        value = Item({})
        if ID != None:
            for i in Items:
                if i.ID == ID:
                    value = i
        else:
            for i in Items:
                if i.Name == name.title():
                    value = i
        return value
    

    @staticmethod
    def incrementGlobalItemId():
        with open("Resources/database/config",'r') as f:
            a = f.read().splitlines()
        a[0] = int(a[0]) + 1
        with open("Resources/database/config",'w') as f:
            for i in a:
                if a[-1] == i:
                    f.write(str(i))
                else:
                    f.write(str(i) + "\n")
        return a[0]
 
Items = {
    Item({
        "name": "Barbaric Chainmail Helmet",
        "ID": "1",
        "rarity": "Common",

        "modelID": "1",
        "colors": "117 117 117, 158 158 158, 191 54 12, 255 60 0",
        "showHair": "no",

        "slot": "Helmet",
        "type": "Mail",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Barbaric Chainmail Shoulderguards",
        "ID": "2",
        "rarity": "Common",

        "modelID": "2",
        "colors": "117 117 117, 158 158 158",

        "slot": "Shoulders",
        "type": "Mail",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Barbaric Chainmail Armor",
        "ID": "3",
        "rarity": "Common",

        "modelID": "3",
        "colors": "117 117 117, 158 158 158",

        "slot": "Chest",
        "type": "Mail",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Barbaric Chainmail Gloves",
        "ID": "4",
        "rarity": "Common",

        "modelID": "4",
        "colors": "117 117 117, 158 158 158, 191 54 12, 255 60 0",

        "slot": "Gloves",
        "type": "Mail",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Barbaric Chainmail Waistguard",
        "ID": "5",
        "rarity": "Common",

        "modelID": "5",
        "colors": "191 54 12, 255 60 0",

        "slot": "Waist",
        "type": "Mail",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Barbaric Chainmail Legguards",
        "ID": "6",
        "rarity": "Common",

        "modelID": "6",
        "colors": "117 117 117, 158 158 158",

        "slot": "Legs",
        "type": "Mail",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Barbaric Chainmail Sabatons",
        "ID": "7",
        "rarity": "Common",

        "modelID": "7",
        "colors": "117 117 117, 158 158 158",

        "slot": "Feet",
        "type": "Mail",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Heroic Chainmail Helmet",
        "ID": "27",
        "rarity": "Common",

        "modelID": "1",
        "colors": "117 117 117, 158 158 158, 63 81 181, 83 108 254",
        "showHair": "no",

        "slot": "Helmet",
        "type": "Mail",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Heroic Chainmail Shoulderguards",
        "ID": "28",
        "rarity": "Common",

        "modelID": "2",
        "colors": "117 117 117, 158 158 158",

        "slot": "Shoulders",
        "type": "Mail",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Heroic Chainmail Armor",
        "ID": "29",
        "rarity": "Common",

        "modelID": "3",
        "colors": "117 117 117, 158 158 158, 63 81 181, 83 108 254",

        "slot": "Chest",
        "type": "Mail",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Heroic Chainmail Gloves",
        "ID": "30",
        "rarity": "Common",

        "modelID": "4",
        "colors": "117 117 117, 158 158 158, 191 54 12, 255 60 0",

        "slot": "Gloves",
        "type": "Mail",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Heroic Chainmail Waistguard",
        "ID": "31",
        "rarity": "Common",

        "modelID": "5",
        "colors": "26 35 126, 83 108 254",

        "slot": "Waist",
        "type": "Mail",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Heroic Chainmail Legguards",
        "ID": "32",
        "rarity": "Common",

        "modelID": "6",
        "colors": "117 117 117, 158 158 158",

        "slot": "Legs",
        "type": "Mail",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Heroic Chainmail Sabatons",
        "ID": "33",
        "rarity": "Common",

        "modelID": "7",
        "colors": "117 117 117, 158 158 158",

        "slot": "Feet",
        "type": "Mail",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Broken Wooden Sword",
        "ID": "8",
        "rarity": "Common",

        "modelID": "8",
        "colors": "128 85 72,93 64 55",

        "slot": "Mainhand",
        "type": "Sword",
        "value": "1",
        "damage": "2 - 4",
        "class": "warrior"
    }),
    Item({
        "name": "Wooden Buckler",
        "ID": "9",
        "rarity": "Common",

        "modelID": "9",
        "colors": "93 64 55, 128 85 72",

        "slot": "Offhand",
        "type": "Shield",
        "value": "1",
        "armor": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Neophyte Hat",
        "ID": "10",
        "rarity": "Common",

        "modelID": "10",
        "colors": "207 59 48, 244 67 54",
        "showHair": "no",

        "slot": "Helmet",
        "type": "Cloth",
        "value": "1",
        "armor": "1",
        "class": "mage"
    }),
    Item({
        "name": "Neophyte Shoulderpads",
        "ID": "11",
        "rarity": "Common",

        "modelID": "11",
        "colors": "207 59 48, 244 67 54",

        "slot": "Shoulders",
        "type": "Cloth",
        "value": "1",
        "armor": "1",
        "class": "mage"
    }),
    Item({
        "name": "Neophyte Robe",
        "ID": "12",
        "rarity": "Common",

        "modelID": "12",
        "colors": "207 59 48, 244 67 54",

        "slot": "Chest",
        "type": "Cloth",
        "value": "1",
        "armor": "1",
        "class": "mage"
    }),
    Item({
        "name": "Neophyte Gloves",
        "ID": "13",
        "rarity": "Common",

        "modelID": "13",
        "colors": "103 58 183, 86 49 153",

        "slot": "Gloves",
        "type": "Cloth",
        "value": "1",
        "armor": "1",
        "class": "mage"
    }),
    Item({
        "name": "Neophyte Sash",
        "ID": "14",
        "rarity": "Common",

        "modelID": "14",
        "colors": "103 58 183, 86 49 153",

        "slot": "Waist",
        "type": "Cloth",
        "value": "1",
        "armor": "1",
        "class": "mage"
    }),
    Item({
        "name": "Neophyte Pants",
        "ID": "15",
        "rarity": "Common",

        "modelID": "15",
        "colors": "207 59 48, 244 67 54",

        "slot": "Legs",
        "type": "Cloth",
        "value": "1",
        "armor": "1",
        "class": "mage"
    }),
    Item({
        "name": "Neophyte Slippers",
        "ID": "16",
        "rarity": "Common",

        "modelID": "16",
        "colors": "103 58 183, 86 49 153",

        "slot": "Feet",
        "type": "Cloth",
        "value": "1",
        "armor": "1",
        "class": "mage"
    }),
    Item({
        "name": "Neophyte Rod",
        "ID": "17",
        "rarity": "Common",

        "modelID": "17",
        "colors": "121 85 72, 244 67 54",

        "slot": "Mainhand",
        "type": "Staff",
        "value": "1",
        "damage": "1-1",
        "class": "mage"
    }),
    Item({
        "name": "Wizard Hat",
        "ID": "37",
        "rarity": "Common",

        "modelID": "10",
        "colors": "30 132 204, 33 150 243",
        "showHair": "no",

        "slot": "Helmet",
        "type": "Cloth",
        "value": "1",
        "armor": "1",
        "class": "mage"
    }),
    Item({
        "name": "Wizard Shoulderpads",
        "ID": "38",
        "rarity": "Common",

        "modelID": "11",
        "colors": "30 132 204, 33 150 243",

        "slot": "Shoulders",
        "type": "Cloth",
        "value": "1",
        "armor": "1",
        "class": "mage"
    }),
    Item({
        "name": "Wizard Robe",
        "ID": "39",
        "rarity": "Common",

        "modelID": "12",
        "colors": "30 132 204, 33 150 243",

        "slot": "Chest",
        "type": "Cloth",
        "value": "1",
        "armor": "1",
        "class": "mage"
    }),
    Item({
        "name": "Wizard Gloves",
        "ID": "40",
        "rarity": "Common",

        "modelID": "13",
        "colors": "156 39 176, 144 36 163",

        "slot": "Gloves",
        "type": "Cloth",
        "value": "1",
        "armor": "1",
        "class": "mage"
    }),
    Item({
        "name": "Wizard Sash",
        "ID": "41",
        "rarity": "Common",

        "modelID": "14",
        "colors": "156 39 176, 144 36 163",

        "slot": "Waist",
        "type": "Cloth",
        "value": "1",
        "armor": "1",
        "class": "mage"
    }),
    Item({
        "name": "Wizard Pants",
        "ID": "42",
        "rarity": "Common",

        "modelID": "15",
        "colors": "30 132 204, 33 150 243",

        "slot": "Legs",
        "type": "Cloth",
        "value": "1",
        "armor": "1",
        "class": "mage"
    }),
    Item({
        "name": "Wizard Slippers",
        "ID": "43",
        "rarity": "Common",

        "modelID": "16",
        "colors": "156 39 176, 144 36 163",

        "slot": "Feet",
        "type": "Cloth",
        "value": "1",
        "armor": "1",
        "class": "mage"
    }),
    Item({
        "name": "Wizard Rod",
        "ID": "44",
        "rarity": "Common",

        "modelID": "17",
        "colors": "121 85 72, 33 150 243",

        "slot": "Mainhand",
        "type": "Staff",
        "value": "1",
        "damage": "1-1",
        "class": "mage"
    }),
    
    Item({
        "name": "Thief Helmet",
        "ID": "18",
        "rarity": "Common",

        "modelID": "18",
        "colors": "107 71 62, 121 85 72",
        "showHair": "no",

        "slot": "Helmet",
        "type": "Leather",
        "value": "1",
        "armor": "2",
        "class": "rogue"
    }),
    Item({
        "name": "Thief Shoulders",
        "ID": "19",
        "rarity": "Common",

        "modelID": "19",
        "colors": "107 71 62, 121 85 72",

        "slot": "Shoulders",
        "type": "Leather",
        "value": "1",
        "armor": "2",
        "class": "rogue"
    }),
    Item({
        "name": "Thief Jerkin",
        "ID": "20",
        "rarity": "Common",

        "modelID": "20",
        "colors": "107 71 62, 121 85 72",

        "slot": "Chest",
        "type": "Leather",
        "value": "1",
        "armor": "2",
        "class": "rogue"
    }),
    Item({
        "name": "Thief Gloves",
        "ID": "21",
        "rarity": "Common",

        "modelID": "21",
        "colors": "107 71 62, 121 85 72",

        "slot": "Gloves",
        "type": "Leather",
        "value": "1",
        "armor": "2",
        "class": "rogue"
    }),
    Item({
        "name": "Thief Buckle",
        "ID": "22",
        "rarity": "Common",

        "modelID": "22",
        "colors": "61 41 35, 82 56 49, 61 61 61",

        "slot": "Waist",
        "type": "Leather",
        "value": "1",
        "armor": "2",
        "class": "rogue"
    }),
    Item({
        "name": "Thief Pants",
        "ID": "23",
        "rarity": "Common",

        "modelID": "23",
        "colors": "107 71 62, 121 85 72",

        "slot": "Legs",
        "type": "Leather",
        "value": "1",
        "armor": "2",
        "class": "rogue"
    }),
    Item({
        "name": "Thief Boots",
        "ID": "24",
        "rarity": "Common",

        "modelID": "24",
        "colors": "107 71 62, 121 85 72",

        "slot": "Feet",
        "type": "Leather",
        "value": "1",
        "armor": "2",
        "class": "rogue"
    }),
    Item({
        "name": "Thief Dagger",
        "ID": "25",
        "rarity": "Common",

        "modelID": "25",
        "colors": "133 133 133, 107 107 107, 179 18 7",

        "slot": "Mainhand",
        "type": "Dagger",
        "value": "1",
        "damage": "1-3",
        "class": "rogue"
    }),
    Item({
        "name": "Thief Shiv",
        "ID": "26",
        "rarity": "Common",

        "modelID": "26",
        "colors": "133 133 133, 107 107 107, 179 18 7",

        "slot": "Offhand",
        "type": "Dagger",
        "value": "1",
        "damage": "1-3",
        "class": "rogue"
    }),

    #Tier 1 craftable items
    Item({
        "name": "Copper Helmet",
        "ID": "45",
        "rarity": "Uncommon",
        "reagents": "4-copper,",

        "modelID": "1",
        "colors": "201 128 60, 144 90 40, 105 105 105, 50 50 50",
        "showHair": "no",

        "slot": "Helmet",
        "type": "Mail",
        "value": "3",
        "armor": "6",
        "stamina": "2",
        "class": "warrior"
    }),
    Item({
        "name": "Copper Shoulderguards",
        "ID": "46",
        "rarity": "Uncommon",
        "reagents": "4-copper,",

        "modelID": "2",
        "colors": "201 128 60, 144 90 40",

        "slot": "Shoulders",
        "type": "Mail",
        "value": "3",
        "armor": "6",
        "stamina": "1",
        "stat": "1",
        "class": "warrior"
    }),
    Item({
        "name": "Copper Armor",
        "ID": "47",
        "rarity": "Uncommon",
        "reagents": "4-copper,",

        "modelID": "3",
        "colors": "201 128 60, 144 90 40, 105 105 105, 50 50 50",

        "slot": "Chest",
        "type": "Mail",
        "value": "3",
        "armor": "6",
        "stamina": "2",
        "class": "warrior"
    }),
    Item({
        "name": "Copper Gloves",
        "ID": "48",
        "rarity": "Uncommon",
        "reagents": "4-copper,",

        "modelID": "4",
        "colors": "201 128 60, 144 90 40, 105 105 105, 50 50 50",

        "slot": "Gloves",
        "type": "Mail",
        "value": "3",
        "armor": "6",
        "stat": "1",
        "class": "warrior"
    }),
    Item({
        "name": "Copper Waistguard",
        "ID": "49",
        "rarity": "Uncommon",
        "reagents": "4-copper,",

        "modelID": "5",
        "colors": "181 108 40, 104 35 1",

        "slot": "Waist",
        "type": "Mail",
        "value": "3",
        "armor": "6",
        "stamina": "1",
        "class": "warrior"
    }),
    Item({
        "name": "Copper Legguards",
        "ID": "50",
        "rarity": "Uncommon",
        "reagents": "4-copper,",

        "modelID": "6",
        "colors": "201 128 60, 144 90 40",

        "slot": "Legs",
        "type": "Mail",
        "value": "3",
        "armor": "6",
        "stamina": "2",
        "class": "warrior"
    }),
    Item({
        "name": "Copper Sabatons",
        "ID": "51",
        "rarity": "Uncommon",
        "reagents": "4-copper,",

        "modelID": "7",
        "colors": "201 128 60, 144 90 40",

        "slot": "Feet",
        "type": "Mail",
        "value": "3",
        "armor": "6",
        "stat": "1",
        "class": "warrior"
    }),
    Item({
        "name": "Copper Sword",
        "ID": "52",
        "rarity": "Uncommon",
        "reagents": "4-copper,",

        "modelID": "52",
        "colors": "201 128 60, 164 95 61",

        "slot": "Mainhand",
        "type": "Sword",
        "value": "3",
        "stat": "2",
        "damage": "2 - 5",
        "class": "warrior"
    }),
    Item({
        "name": "Copper Buckler",
        "ID": "53",
        "rarity": "Uncommon",
        "reagents": "4-copper,",

        "modelID": "52",
        "colors": "201 128 60, 164 95 61",

        "slot": "Offhand",
        "type": "Shield",
        "value": "3",
        "armor": "6",
        "stamina": "2",
        "class": "warrior"
    }),

    Item({
        "name": "Linen Hat",
        "ID": "54",
        "rarity": "Uncommon",
        "reagents": "4-linen,",

        "modelID": "10",
        "colors": "220 210 200, 250 240 230",
        "showHair": "no",

        "slot": "Helmet",
        "type": "Cloth",

        "stat": "1",

        "value": "1",
        "armor": "2",
        "class": "mage"
    }),
    Item({
        "name": "Linen Shoulderpads",
        "ID": "55",
        "rarity": "Uncommon",
        "reagents": "4-linen,",

        "modelID": "11",
        "colors": "220 210 200, 250 240 230",

        "slot": "Shoulders",
        "type": "Cloth",

        "stamina": "1",
        "stat": "1",

        "value": "1",
        "armor": "2",
        "class": "mage"
    }),
    Item({
        "name": "Linen Robe",
        "ID": "56",
        "rarity": "Uncommon",
        "reagents": "4-linen,",

        "modelID": "12",
        "colors": "220 210 200, 250 240 230",

        "slot": "Chest",
        "type": "Cloth",

        "stat": "2",

        "value": "1",
        "armor": "2",
        "class": "mage"
    }),
    Item({
        "name": "Linen Gloves",
        "ID": "57",
        "rarity": "Uncommon",
        "reagents": "4-linen,",

        "modelID": "13",
        "colors": "225 216 207, 195 186 187",

        "slot": "Gloves",
        "type": "Cloth",

        "stat": "1",

        "value": "1",
        "armor": "2",
        "class": "mage"
    }),
    Item({
        "name": "Linen Sash",
        "ID": "58",
        "rarity": "Uncommon",
        "reagents": "4-linen,",

        "modelID": "14",
        "colors": "195 186 187, 225 216 207, 100 100 100",

        "slot": "Waist",
        "type": "Cloth",

        "stamina": "1",

        "value": "1",
        "armor": "2",
        "class": "mage"
    }),
    Item({
        "name": "Linen Pants",
        "ID": "59",
        "rarity": "Uncommon",
        "reagents": "4-linen,",

        "modelID": "15",
        "colors": "220 210 200, 250 240 230",

        "slot": "Legs",
        "type": "Cloth",

        "stat": "2",

        "value": "1",
        "armor": "2",
        "class": "mage"
    }),
    Item({
        "name": "Linen Slippers",
        "ID": "60",
        "rarity": "Uncommon",
        "reagents": "4-linen,",

        "modelID": "16",
        "colors": "195 186 187, 225 216 207",

        "slot": "Feet",
        "type": "Cloth",

        "stat": "1",

        "value": "1",
        "armor": "2",
        "class": "mage"
    }),
    Item({
        "name": "Linen Rod",
        "ID": "60",
        "rarity": "Uncommon",
        "reagents": "4-linen,",

        "modelID": "17",
        "colors": "121 85 72, 225 216 207",

        "slot": "Mainhand",
        "type": "Staff",

        "stat": "2",

        "value": "1",
        "damage": "1-1",
        "class": "mage"
    }),

    Item({
        "name": "Embossed Cap",
        "ID": "61",
        "rarity": "Uncommon",
        "reagents": "4-light,",

        "modelID": "18",
        "colors": "107 71 62, 121 85 72",
        "showHair": "no",

        "slot": "Helmet",
        "type": "Leather",
        "value": "3",
        "armor": "4",
        "stamina": "1",
        "stat": "1",
        "class": "rogue"
    }),
    Item({
        "name": "Embossed Shouldercap",
        "ID": "62",
        "rarity": "Uncommon",
        "reagents": "4-light,",

        "modelID": "19",
        "colors": "107 71 62, 121 85 72",

        "slot": "Shoulders",
        "type": "Leather",
        "value": "3",
        "armor": "4",
        "stamina": "1",
        "stat": "1",
        "class": "rogue"
    }),
    Item({
        "name": "Embossed Jacket",
        "ID": "63",
        "rarity": "Uncommon",
        "reagents": "4-light,",

        "modelID": "20",
        "colors": "107 71 62, 121 85 72",

        "slot": "Chest",
        "type": "leather",
        "value": "3",
        "armor": "4",
        "stamina": "1",
        "stat": "1",
        "class": "rogue"
    }),
    Item({
        "name": "Embossed Gloves",
        "ID": "64",
        "rarity": "Uncommon",
        "reagents": "4-light,",

        "modelID": "21",
        "colors": "107 71 62, 121 85 72",

        "slot": "Gloves",
        "type": "leather",
        "value": "3",
        "armor": "4",
        "stat": "1",
        "class": "rogue"
    }),
    Item({
        "name": "Embossed Buckle",
        "ID": "49",
        "rarity": "Uncommon",
        "reagents": "4-light,",

        "modelID": "65",
        "colors": "61 41 35, 82 56 49, 61 61 61",

        "slot": "Waist",
        "type": "leather",
        "value": "3",
        "armor": "4",
        "stamina": "1",
        "class": "rogue"
    }),
    Item({
        "name": "Embossed Pants",
        "ID": "66",
        "rarity": "Uncommon",
        "reagents": "4-light,",

        "modelID": "23",
        "colors": "107 71 62, 121 85 72",

        "slot": "Legs",
        "type": "leather",
        "value": "3",
        "armor": "4",
        "stamina": "1",
        "stat": "1",
        "class": "rogue"
    }),
    Item({
        "name": "Embossed Boots",
        "ID": "67",
        "rarity": "Uncommon",
        "reagents": "4-light,",

        "modelID": "24",
        "colors": "107 71 62, 121 85 72",

        "slot": "Feet",
        "type": "leather",
        "value": "3",
        "armor": "4",
        "stat": "1",
        "class": "rogue"
    }),
    Item({
        "name": "Embossed Dagger",
        "ID": "68",
        "rarity": "Uncommon",
        "reagents": "4-light,",

        "modelID": "25",
        "colors": "133 133 133, 107 107 107, 179 18 7",

        "slot": "Mainhand",
        "type": "Dagger",
        "value": "3",
        "stat": "1",
        "stamina": "1",
        "damage": "2 - 4",
        "class": "rogue"
    }),
    Item({
        "name": "Embossed Shiv",
        "ID": "69",
        "rarity": "Uncommon",
        "reagents": "4-light,",

        "modelID": "52",
        "colors": "201 128 60, 164 95 61",

        "slot": "Offhand",
        "type": "Dagger",
        "value": "3",
        "damage": "2 - 4",
        "stamina": "1",
        "stat": "1",
        "class": "rogue"
    }),

    #Deadmines loot
    Item({
        "name": "Sentry Helmet",
        "ID": "70",
        "rarity": "Rare",

        "modelID": "70",
        "colors": "201 128 60, 144 90 40, 105 105 105, 50 50 50",
        "showHair": "no",
        "level":"10",

        "slot": "Helmet",
        "type": "Mail",
        "value": "3",
        "armor": "9",
        "stamina": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Sentry Shoulderguards",
        "ID": "71",
        "rarity": "Rare",

        "modelID": "71",
        "colors": "201 128 60, 144 90 40",
        "level":"10",

        "slot": "Shoulders",
        "type": "Mail",
        "value": "3",
        "armor": "9",
        "stamina": "2",
        "stat": "1",
        "class": "warrior"
    }),
    Item({
        "name": "Sentry Armor",
        "ID": "72",
        "rarity": "Rare",

        "modelID": "72",
        "colors": "201 128 60, 144 90 40, 105 105 105, 50 50 50",
        "level":"10",

        "slot": "Chest",
        "type": "Mail",
        "value": "3",
        "armor": "9",
        "stamina": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Sentry Gloves",
        "ID": "73",
        "rarity": "Rare",

        "modelID": "73",
        "colors": "201 128 60, 144 90 40, 105 105 105, 50 50 50",
        "level":"10",

        "slot": "Gloves",
        "type": "Mail",
        "value": "3",
        "armor": "9",
        "stat": "2",
        "class": "warrior"
    }),
    Item({
        "name": "Sentry Waistguard",
        "ID": "74",
        "rarity": "Rare",

        "modelID": "74",
        "colors": "181 108 40, 104 35 1",
        "level":"10",

        "slot": "Waist",
        "type": "Mail",
        "value": "3",
        "armor": "9",
        "stamina": "2",
        "class": "warrior"
    }),
    Item({
        "name": "Sentry Legguards",
        "ID": "75",
        "rarity": "Rare",

        "modelID": "75",
        "colors": "201 128 60, 144 90 40",
        "level":"10",

        "slot": "Legs",
        "type": "Mail",
        "value": "3",
        "armor": "9",
        "stamina": "3",
        "class": "warrior"
    }),
    Item({
        "name": "Sentry Sabatons",
        "ID": "76",
        "rarity": "Rare",

        "modelID": "76",
        "colors": "201 128 60, 144 90 40",
        "level":"10",

        "slot": "Feet",
        "type": "Mail",
        "value": "3",
        "armor": "9",
        "stamina":"2",
        "class": "warrior"
    }),
    Item({
        "name": "Sentry Sword",
        "ID": "77",
        "rarity": "Rare",

        "modelID": "77",
        "colors": "201 128 60, 164 95 61",
        "level":"10",

        "slot": "Mainhand",
        "type": "Sword",
        "value": "3",
        "stat": "3",
        "damage": "4 - 7",
        "class": "warrior"
    }),
    Item({
        "name": "Sentry Buckler",
        "ID": "78",
        "rarity": "Rare",

        "modelID": "78",
        "colors": "201 128 60, 164 95 61",
        "level":"10",

        "slot": "Offhand",
        "type": "Shield",
        "value": "3",
        "armor": "9",
        "stamina": "3",
        "class": "warrior"
    }),

    Item({
        "name": "Apothecary Hat",
        "ID": "79",
        "rarity": "Rare",

        "modelID": "79",
        "colors": "220 210 200, 250 240 230",
        "showHair": "no",
        "level":"10",

        "slot": "Helmet",
        "type": "Cloth",

        "stat": "3",
        "value": "1",
        "armor": "3",
        "class": "mage"
    }),
    Item({
        "name": "Apothecary Shoulderpads",
        "ID": "80",
        "rarity": "Rare",

        "modelID": "80",
        "colors": "220 210 200, 250 240 230",
        "level":"10",

        "slot": "Shoulders",
        "type": "Cloth",

        "stamina": "1",
        "stat": "2",

        "value": "1",
        "armor": "3",
        "class": "mage"
    }),
    Item({
        "name": "Apothecary Robe",
        "ID": "81",
        "rarity": "Rare",

        "modelID": "81",
        "colors": "220 210 200, 250 240 230",
        "level":"10",

        "slot": "Chest",
        "type": "Cloth",

        "stat": "3",

        "value": "1",
        "armor": "3",
        "class": "mage"
    }),
    Item({
        "name": "Apothecary Gloves",
        "ID": "82",
        "rarity": "Rare",

        "modelID": "82",
        "colors": "225 216 207, 195 186 187",
        "level":"10",

        "slot": "Gloves",
        "type": "Cloth",

        "stat": "2",

        "value": "1",
        "armor": "3",
        "class": "mage"
    }),
    Item({
        "name": "Apothecary Sash",
        "ID": "83",
        "rarity": "Rare",

        "modelID": "83",
        "colors": "195 186 187, 225 216 207, 100 100 100",
        "level":"10",

        "slot": "Waist",
        "type": "Cloth",

        "stamina": "2",

        "value": "1",
        "armor": "3",
        "class": "mage"
    }),
    Item({
        "name": "Apothecary Pants",
        "ID": "84",
        "rarity": "Rare",

        "modelID": "84",
        "colors": "220 210 200, 250 240 230",
        "level":"10",

        "slot": "Legs",
        "type": "Cloth",

        "stat": "3",

        "value": "1",
        "armor": "3",
        "class": "mage"
    }),
    Item({
        "name": "Apothecary Slippers",
        "ID": "85",
        "rarity": "Rare",

        "modelID": "85",
        "colors": "195 186 187, 225 216 207",
        "level":"10",

        "slot": "Feet",
        "type": "Cloth",

        "stat": "2",

        "value": "1",
        "armor": "3",
        "class": "mage"
    }),
    Item({
        "name": "Apothecary Staff",
        "ID": "86",
        "rarity": "Rare",

        "modelID": "86",
        "colors": "121 85 72, 225 216 207",
        "level":"10",

        "slot": "Mainhand",
        "type": "Staff",

        "stat": "3",

        "value": "1",
        "damage": "1-1",
        "class": "mage"
    }),

    Item({
        "name": "Bandit's Cap",
        "ID": "87",
        "rarity": "Rare",

        "modelID": "87",
        "colors": "107 71 62, 121 85 72",
        "showHair": "no",
        "level":"10",

        "slot": "Helmet",
        "type": "Leather",
        "value": "3",
        "armor": "6",
        "stamina": "2",
        "stat": "1",
        "class": "rogue"
    }),
    Item({
        "name": "Bandit Shouldercap",
        "ID": "88",
        "rarity": "Rare",

        "modelID": "88",
        "colors": "107 71 62, 121 85 72",
        "level":"10",

        "slot": "Shoulders",
        "type": "Leather",
        "value": "3",
        "armor": "6",
        "stamina": "1",
        "stat": "2",
        "class": "rogue"
    }),
    Item({
        "name": "Bandit's Jacket",
        "ID": "89",
        "rarity": "Rare",

        "modelID": "89",
        "colors": "107 71 62, 121 85 72",
        "level":"10",

        "slot": "Chest",
        "type": "leather",
        "value": "3",
        "armor": "6",
        "stamina": "2",
        "stat": "1",
        "class": "rogue"
    }),
    Item({
        "name": "Bandit's Gloves",
        "ID": "90",
        "rarity": "Rare",

        "modelID": "90",
        "colors": "107 71 62, 121 85 72",
        "level":"10",

        "slot": "Gloves",
        "type": "leather",
        "value": "3",
        "armor": "6",
        "stat": "2",
        "class": "rogue"
    }),
    Item({
        "name": "Bandit's Buckle",
        "ID": "91",
        "rarity": "Rare",

        "modelID": "91",
        "colors": "61 41 35, 82 56 49, 61 61 61",
        "level":"10",

        "slot": "Waist",
        "type": "leather",
        "value": "3",
        "armor": "6",
        "stamina": "2",
        "class": "rogue"
    }),
    Item({
        "name": "Bandit's Pants",
        "ID": "92",
        "rarity": "Rare",

        "modelID": "92",
        "colors": "107 71 62, 121 85 72",
        "level":"10",

        "slot": "Legs",
        "type": "leather",
        "value": "3",
        "armor": "6",
        "stamina": "1",
        "stat": "2",
        "class": "rogue"
    }),
    Item({
        "name": "Bandit's Boots",
        "ID": "93",
        "rarity": "Rare",

        "modelID": "93",
        "colors": "107 71 62, 121 85 72",
        "level":"10",

        "slot": "Feet",
        "type": "leather",
        "value": "3",
        "armor": "6",
        "stat": "1",
        "stamina": "1",
        "class": "rogue"
    }),
    Item({
        "name": "Bandit's Dagger",
        "ID": "94",
        "rarity": "Rare",

        "modelID": "94",
        "colors": "133 133 133, 107 107 107, 179 18 7",
        "level":"10",

        "slot": "Mainhand",
        "type": "Dagger",
        "value": "3",
        "stat": "3",
        "damage": "3 - 6",
        "class": "rogue"
    }),
    Item({
        "name": "Bandit's Shiv",
        "ID": "95",
        "rarity": "Rare",

        "modelID": "95",
        "colors": "201 128 60, 164 95 61",
        "level":"10",

        "slot": "Offhand",
        "type": "Dagger",
        "value": "3",
        "damage": "3 - 6",
        "stamina": "3",
        "class": "rogue"
    }),

    Item({
        "name": "Brotherhood Medallion",
        "ID": "96",
        "rarity": "Rare",

        "modelID": "95",
        "colors": "201 128 60, 164 95 61",
        "level":"10",

        "slot": "Trinket",
        "value": "3",
        "class": "all",
        "spells": [spl.Spell.findByID("4"), spl.Spell.findByID("5")],
        "spellattrs": [{"A":"A"}, {"B":"B"}],
        
        "flavor":"Engraved on the bottom you can see, 'E.V. + V.C.'"
    }),



    
    Item({
        "name": "Elementium Helmet",
        "ID": "400",
        "rarity": "Epic",
        "reagents": "5-copper,4-bronze,3-iron,2-mithril,1-thorium",

        "modelID": "1",
        "colors": "201 128 60, 144 90 40, 105 105 105, 50 50 50",
        "showHair": "no",

        "slot": "Helmet",
        "type": "Mail",
        "value": "30",
        "armor": "60",
        "stamina": "30",
        "stat": "10",
        "class": "warrior"
    }),
    Item({
        "name": "Mooncloth Hat",
        "ID": "500",
        "rarity": "Epic",
        "reagents": "5-linen,4-wool,3-silk,2-mageweave,1-runecloth",

        "modelID": "1",
        "colors": "201 128 60, 144 90 40, 105 105 105, 50 50 50",
        "showHair": "no",

        "slot": "Helmet",
        "type": "Cloth",
        "value": "30",
        "armor": "10",
        "stamina": "30",
        "stat": "60",
        "class": "mage"
    }),
    Item({
        "name": "Cured Hood",
        "ID": "600",
        "rarity": "Epic",
        "reagents": "5-light,4-medium,3-heavy,2-thick,1-rugged",

        "modelID": "1",
        "colors": "201 128 60, 144 90 40, 105 105 105, 50 50 50",
        "showHair": "no",

        "slot": "Helmet",
        "type": "Leather",
        "value": "30",
        "armor": "40",
        "stamina": "30",
        "stat": "40",
        "class": "rogue"
    }),
    Item({
        "name": "Minor Health Potion",
        "ID": "1000",
        "rarity": "Common",
        "spells":[spl.Spell.findByID("6")],
        "spellattrs": [{"health":30}],
        "class": "all"
    }),


    Item({
        "name": "Key To The Deadmines",
        "ID": "10001",
        "rarity": "Rare",
        "spells": [spl.Spell.findByID("1")],
        "spellattrs": [{"dungeon":"DMVC"}],
        "charges":"1"
    }),
    Item({
        "name": "Fragmented Key Blade",
        "ID": "10000",
        "rarity": "Rare",
        "flavor":"These fragments are ethereal, broken beyond repair. Perhaphs there is someone who can help you fix it."
    }),
    Item({
        "name": "Fragmented Key Bow",
        "ID": "10002",
        "rarity": "Rare",
        "flavor":"These fragments are ethereal, broken beyond repair. Perhaphs there is someone who can help you fix it."
    }),
    Item({
        "name": "Essence Of Karazhan",
        "ID": "10003",
        "rarity": "Rare",
        "flavor":"Holding onto this makes gives you the chills. It's presence creates the winds of Deadwind Pass. Perhaphs there is someone who can make use of this"
    }),
    Item({
        "name": "Key To Karazhan",
        "ID": "10004",
        "rarity": "Epic",
        "spells": [spl.Spell.findByID("2")],
        "spellattrs": [{"dungeon":"KARA"}],
        "charges":"1"
    })
}


#Item.incrementGlobalItemId()
#Items Formatting
# 102 10 10 2 3 1
# (10-10-F-FF), (102-FF-1-FF-)
#  X - XX - X - XX - X - X
#  ^GlobalID
#      ^Stat ID
#           ^ Appearance ID
#                ^ Bound status
#                    ^ Spells
#                        ^ Charges
# GlobalID - ItemID - Model ID - AppearanceID - Bound Status - Spells - Charges
# F = no value
# 01-05-B-F
# Chain helmet made to look like alliance variant, bound with no enchantment