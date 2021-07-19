from posixpath import split
import Resources.imports as res
import Resources.connection as con
import Resources.item as itm
import Resources.spells as spl
class Character:
    def __init__(self, Dictionary):
        #Character specific
        self.ID = Dictionary.get("ID", None)
        self.Name = Dictionary.get("name", None)
        self.Race = Dictionary.get("race", None)
        self.Class = Dictionary.get("class", None)
        self.Inventory = Dictionary.get("inventory", "")
        self.Resources = Dictionary.get("resources", "")

        #Equipment
        self.Helmet = Dictionary.get("helmet", "F-F-F-F-F-F")
        self.Shoulders = Dictionary.get("shoulders", "F-F-F-F-F-F")
        self.Chest = Dictionary.get("chest", "F-F-F-F-F-F")
        self.Gloves = Dictionary.get("gloves", "F-F-F-F-F-F")
        self.Waist = Dictionary.get("waist", "F-F-F-F-F-F")
        self.Legs = Dictionary.get("legs", "F-F-F-F-F-F")
        self.Feet = Dictionary.get("feet", "F-F-F-F-F-F")
        self.Trinket = Dictionary.get("trinket", "F-F-F-F-F-F")
        self.Mainhand = Dictionary.get("mainhand", "F-F-F-F-F-F")
        self.Offhand = Dictionary.get("offhand", "F-F-F-F-F-F")
        self.Buffs = Dictionary.get("buffs", "")

        #Stats
        self.Stamina = Dictionary.get("stamina", None)
        self.Armor = Dictionary.get("armor", None)
        self.Stat = Dictionary.get("stat", None)
        self.Health = Dictionary.get("health", None)
        self.Exp = Dictionary.get("exp", None)
        self.Level = Dictionary.get("level", None)
        self.Gold = Dictionary.get("gold", None)

        #Misc
        self.Lockouts = Dictionary.get("lockouts", "0X>DMVC-AAAAAAAAAAAA")
        self.Remainder = Dictionary.get("remainder", None)
        self.Updated = Dictionary.get("updated", res.calendar.timegm(res.time.gmtime()))

    #Functions user can perform
    def exists(self):
        if self.Level == None:
            return False
        return True
    def updateHealth(self):
        #Set the time and some other initial variables
        timeNow = res.calendar.timegm(res.time.gmtime())
        currentHealth = int(self.Health)
        maxHealth = int(self.Stamina) * 10
        remainder = float(self.Remainder)
        updated = int(self.Updated)
        #Restore health based on formula
        if currentHealth < maxHealth:
            timerUsed = 3600 / (maxHealth * .25) #150
            healthToRegen = 0
            timeSinceLast = timeNow - updated
            remainder = remainder + timeSinceLast #490

            #While there's time remaining
            while remainder >= timerUsed:
                remainder -= timerUsed
                healthToRegen += 1

            #Add health and normalizes the number to max
            currentHealth += healthToRegen
            if currentHealth >= maxHealth:
                currentHealth = maxHealth
                remainder = 0
        else:
            remainder = 0
        #Update the table with new values
        self.updateSelf("health", str(str(currentHealth)))
        self.updateSelf("updated", str(timeNow))
        self.updateSelf("remainder", str(remainder))
    def returnEquipment(self):
        equipped = []
        equipped.append(self.Helmet) if self.Helmet.split("-")[0] != "F" else None
        equipped.append(self.Shoulders) if self.Shoulders.split("-")[0] != "F" else None
        equipped.append(self.Chest) if self.Chest.split("-")[0] != "F" else None
        equipped.append(self.Gloves) if self.Gloves.split("-")[0] != "F" else None
        equipped.append(self.Waist) if self.Waist.split("-")[0] != "F" else None
        equipped.append(self.Legs) if self.Legs.split("-")[0] != "F" else None
        equipped.append(self.Feet) if self.Feet.split("-")[0] != "F" else None
        equipped.append(self.Mainhand) if self.Mainhand.split("-")[0] != "F" else None
        equipped.append(self.Offhand) if self.Offhand.split("-")[0] != "F" else None
        equipped.append(self.Trinket) if self.Trinket.split("-")[0] != "F" else None
        return equipped

    #Gear functions
    def equip(self, itemList):
        item = itm.Item.returnItem(None, itemList[1])
        if item.Slot == None:
            return False, "Item cannot be equipped."
        itemInBag = self.checkIfHasItem(item)
        if not itemInBag:
            return False, "Item not found in inventory."
        if item.Level and int(item.Level) > int(self.Level):
            return "You're not high enough level to equip that item."
        itemInSlot = getattr(self, item.Slot.capitalize())
        if itemInSlot.split("-")[1] != "F":
            self.unequip(itemInSlot.split("-"))
        self.removeFromInventory(itemList[0])
        itemInBag = "-".join(itemList)
        self.updateSelf(item.Slot, itemInBag)
        self.updateSelf("Stamina",int(self.Stamina) + int(item.Stamina))
        self.updateSelf("Armor",int(self.Armor) + int(item.Armor))
        self.updateSelf("Stat",int(self.Stat) + int(item.Stat))
        self.updateSelf("Health",int(self.Health) + (int(item.Stamina) * 10))
        return True, "Succesfully equiped: " + item.returnFullItemName()
    def unequip(self, itemList):
        item = itm.Item.returnItem(None, itemList[1])
        if item.Slot == "F" or item.Slot == None:
            return False, "Item cannot be unequipped."
        itemInSlot = self.checkIfWearingItem(item)
        if not itemInSlot:
            return False, "Item not found equipped."
        self.addToInventory(itemInSlot)
        self.updateSelf(item.Slot, "F-F-F-F-F-F")
        self.updateSelf("Stamina",int(self.Stamina) - int(item.Stamina))
        self.updateSelf("Armor",int(self.Armor) - int(item.Armor))
        self.updateSelf("Stat",int(self.Stat) - int(item.Stat))
        self.updateSelf("Health",int(self.Health) - (int(item.Stamina) * 10))
        return True, "Succesfully unequiped: " + item.returnFullItemName()
    def sell(self, itemList):
        item = itm.Item.returnItem(None, itemList[1])
        if item.Slot == None:
            return False, "Item cannot be equipped."
        itemInBag = self.checkIfHasItem(item)
        if not itemInBag:
            return False, "Item not found in inventory."
        self.removeFromInventory(itemList[0])
        newGold = str(int(self.Gold) + int(item.Value))
        self.updateSelf("Gold",newGold)
        return True, "Succesfully sold " + item.returnFullItemName() + " for " + item.Value + " gold."
    def use(self, itemList):
        item = itm.Item.returnItem(None, itemList[1])
        itemInBag = self.checkIfHasItem(item)
        if item.Slot:
            if not self.checkIfWearingItem(item):
                return False, "item not found worn."
        else:
            if not itemInBag:
                return False, "Item not found in inventory."
        msg = ""
        if not item.Spells:
            return False, "Item cannot be used."
        for spell, attr in zip(itemList[4].split("&"), item.SpellAttrs):
            actualSpell = spl.Spell.findByID(spell)
            if actualSpell.Type == "active":
                attr["user"] = self
                msg += actualSpell.Function(**attr)
                if itemList[5] != "F":
                    itemList[5] = str(int(itemList[5]) - 1)
        if itemList[5] != "F" and int(itemList[5]) <= 0:
            if item.Slot:
                self.unequip(itemList)
            self.removeFromInventory(itemList[0])
        return True, "Used item " + item.returnFullItemName() + msg
    def inspect(self):
        msg = ""
        msg += "- Helmet: " + (itm.Item.returnItem(None, self.Helmet.split("-")[1]).returnFullItemName() if self.Helmet.split("-")[1] != "F" else "Empty") + " \n"
        msg += "- Shoulders: " + (itm.Item.returnItem(None, self.Shoulders.split("-")[1]).returnFullItemName() if self.Shoulders.split("-")[1] != "F" else "Empty") + " \n"
        msg += "- Chest: " + (itm.Item.returnItem(None, self.Chest.split("-")[1]).returnFullItemName() if self.Chest.split("-")[1] != "F" else "Empty") + " \n"
        msg += "- Gloves: " + (itm.Item.returnItem(None, self.Gloves.split("-")[1]).returnFullItemName() if self.Gloves.split("-")[1] != "F" else "Empty") + " \n"
        msg += "- Waist: " + (itm.Item.returnItem(None, self.Waist.split("-")[1]).returnFullItemName() if self.Waist.split("-")[1] != "F" else "Empty") + " \n"
        msg += "- Legs: " + (itm.Item.returnItem(None, self.Legs.split("-")[1]).returnFullItemName() if self.Legs.split("-")[1] != "F" else "Empty") + " \n"
        msg += "- Feet: " + (itm.Item.returnItem(None, self.Feet.split("-")[1]).returnFullItemName() if self.Feet.split("-")[1] != "F" else "Empty") + " \n"
        msg += "- Trinket: " + (itm.Item.returnItem(None, self.Trinket.split("-")[1]).returnFullItemName() if self.Trinket.split("-")[1] != "F" else "Empty") + " \n"
        msg += "- Mainhand: " + (itm.Item.returnItem(None, self.Mainhand.split("-")[1]).returnFullItemName() if self.Mainhand.split("-")[1] != "F" else "Empty") + " \n"
        msg += "- Offhand: " + (itm.Item.returnItem(None, self.Offhand.split("-")[1]).returnFullItemName() if self.Offhand.split("-")[1] != "F" else "Empty")
        return msg


    #Combat
    def train(self):
        self.updateHealth()
        damageTakenOverall, mobLevel = self.combat()
        #Check if user died
        if int(self.Health) <= 0:
            completeMsg = "Try as you might, you were too weary and collapsed during training."
            self.updateSelf("health",1)
            return False, completeMsg
        else:
            self.updateSelf("health",self.Health)
            #Dispense the gold and experience
            expCalc = round((res.math.sqrt(mobLevel) * 8) * ((.5 * mobLevel) + 1))
            expGained = self.modifyExp(expCalc, expCalc)
            goldGained = self.modifyGold(mobLevel* ((.5 * mobLevel) + 1), mobLevel * 2 * ((.5 * mobLevel) + 1))
            ifDinged = self.checkLevelUp(True)
            completeMsg = "You succesfully completed your training and lost " + str(damageTakenOverall) + " health. \n \nYou gained " + str(expGained) + " EXP and earned " + str(goldGained) + " gold. \n" + ifDinged + " \nNow standing at " + str(self.Health) + " health remaining, would you like to keep training?"
            return True, completeMsg
    
    
    
    
    def combat(self, boss = None, hardmode = False):
        #Create a dummy mob randomized by player level.
        class Mob:
            ()
        mob = Mob
        if not boss:
            mob.mobLevel = max(1, res.random.randint(int(self.Level) - 1, int(self.Level) + 1))
            mob.mobHealth = 40 + (10 * int(mob.mobLevel)) * ((.1 * mob.mobLevel) + 1)
            mob.mobDamage = [round(((.1 * mob.mobLevel) + 1) * (9 + (9 * .1 * res.math.sqrt(mob.mobLevel)))),round(((.1 * mob.mobLevel) + 1)*(14 + (14 * .1 * res.math.sqrt(mob.mobLevel))))]
        else:
            if hardmode:
                mob.mobLevel = int(boss.level)
                mob.mobHealth = round(int(boss.health) * 1.10)
                temp = boss.damage.split("-")
                mob.mobDamage = [round(int(temp[0])) * 1.10, round(int(temp[1])) * 1.10]
            else:
                mob.mobLevel = int(boss.level)
                mob.mobHealth = int(boss.health)
                temp = boss.damage.split("-")
                mob.mobDamage = [int(temp[0]), int(temp[1])]
    
        #Sets the correct main damage stat and weapon scaling
        if self.Class == "mage":
            self.wepScaling = .2
        elif self.Class == "warrior":
            self.wepScaling = 1.8
        elif self.Class == "rogue":
            self.wepScaling = 2

        #Look for if user has a weapon and retrieves it's damage
        self.mainhandDamage = self.returnWeaponDamage(self.Mainhand)
        self.offhandDamage = self.returnWeaponDamage(self.Offhand)

        #Stats tracked for when fighting a dummy.
        damageTakenOverall = 0
        procs = []
        onhits = []
        for i in self.Buffs.split(","):
            if i:
                if i.type == "proc":
                    procs.append(i)
                elif i.type == "onhit":
                    onhits.append(i)
        self.stunned = False
        mob.stunned = False
        while int(self.Health) > 0 and mob.mobHealth > 0:
            if not self.stunned:
                #Randomizes user's weapon damage
                self.wepDamage = res.random.uniform(int(self.mainhandDamage[0]), int(self.mainhandDamage[1]))
                self.ohDamage = 0
                #Calculates your weapon damage differently if you're a rogue or mage
                if self.Class == "rogue":
                    self.ohDamage = res.random.uniform(int(self.offhandDamage[0]), int(self.offhandDamage[1]))
                elif self.Class == "mage":
                    self.wepDamage += res.random.randint(round(int(self.Stat)/5),round(int(self.Stat)/3))

                #Puts your stats to scale your damage dealt
                self.statScaling = res.math.sqrt((int(self.Stat)- self.wepDamage) * (self.wepDamage * self.wepScaling))
                self.damageDealt = round(self.wepDamage * self.statScaling)

                #adds offhand damage if there was any and deal damage
                if self.ohDamage > 0:
                    self.damageDealt += .5 * round(self.ohDamage * self.statScaling)

                for i in procs:
                    i.Function({"user": self, "mob":mob})
                mob.mobHealth -= self.damageDealt
            else:
                self.stunned = False

            #Checks if mob survived the hit to retaliate
            if mob.mobHealth > 0:
                if not mob.stunned:
                    #Randomize damage dealt
                    mob.mobDamageDealt = res.random.uniform(mob.mobDamage[0], mob.mobDamage[1])

                    #Creates a modifier for damage reduction based on armor
                    self.dr = mob.mobDamageDealt / (mob.mobDamageDealt + int(self.Armor))
                    self.damageTaken = round (mob.mobDamageDealt * self.dr)
                    for i in procs:
                        i.Function({"user": self, "mob":mob})
                    self.Health = str(int(self.Health) - self.damageTaken)
                    damageTakenOverall += self.damageTaken
                else:
                    mob.stunned = False
        return damageTakenOverall, mob.mobLevel
    
    
    
    
    def returnWeaponDamage(self, item):
        if item.split("-")[1] == "F":
            return [1,1]
        weapon = itm.Item.returnItem(None, item.split("-")[1])
        if weapon.ID != None and weapon.Type != "Shield":
            damageRange = list(map(int, weapon.Damage.split("-")))
        else:
            damageRange = [1,1]
        return damageRange

    #Updates to character
    def removeFromInventory(self, globalItemID):
        for i in self.Inventory.split(","):
            itemInBag = i.split("-")
            if itemInBag[0] == globalItemID:
                newinventory = self.Inventory.replace(i+",","")
                self.Inventory = newinventory
                con.update("characters","ID",self.ID,"inventory",newinventory)
    def addToInventory(self, itemString):
        newInventory = self.Inventory + itemString + ","
        self.updateSelf("inventory",newInventory)
    def updateSelf(self, column, value):
        setattr(self,column.capitalize(),str(value))
        con.update("characters","ID",self.ID,column,str(value))
    def checkIfHasItem(self, item):
        itemString = item.returnItemString()
        itemsFound = []
        splitName = itemString.split("-")
        splitInventory = self.Inventory.replace(" ","").split(",")
        if "" in splitInventory:
            splitInventory.remove("")
        if splitInventory == []:
            return False
        for i in splitInventory:
            itemInBag = i.split("-")
            if itemInBag[1] == splitName[1]:
                itemsFound.append(itemInBag)
        if itemsFound == []:
            return False
        else:
            return itemsFound
    def checkIfWearingItem(self, item):
        itemString = item.returnItemString()
        splitName = itemString.split("-")
        itemInSlot = getattr(self, item.Slot)
        if itemInSlot.split("-")[0] == "F":
            return False
        if itemInSlot.split("-")[1] != splitName[1]:
            return False
        return itemInSlot
    def checkLevelUp(self, newLine):
        currentEXP = int(self.Exp)
        expNeeded = 10 * (res.math.floor((round((0.04*(int(self.Level)**3))+(0.8*(int(self.Level)**2))+(2*int(self.Level))))))
        newLevel = int(self.Level)
        if currentEXP >= expNeeded:
            currentEXP -= expNeeded
            newLevel += 1
            newStamina = (int(self.Stamina) + 1)
            newStat = (int(self.Stat) + 2)
            self.updateSelf("exp", str(currentEXP))
            self.updateSelf("stamina", str(newStamina))
            self.updateSelf("stat", str(newStat))
            self.updateSelf("level", str(newLevel))
            if newLine:
                return " \nDing! You leveled up! \n"
            else:
                return "Ding! You leveled up!"
        else:
            return ""
    def updateLockout(self, update, curLockout, bossID):
        temp = self.Lockouts.replace(curLockout, curLockout[:7+bossID] + update + curLockout[8+bossID:])
        self.updateSelf("Lockouts", temp)
        return curLockout[:7+bossID] + update + curLockout[8+bossID:]

    #Basic Spells
    def modifyHealth(self,min,max):
        self.updateHealth()
        healthAdded = int(res.random.uniform(min,max))
        newHealth = int(self.Health) + int(healthAdded)
        oldHealth = self.Health
        if newHealth < 0:
            newHealth = 1
        if newHealth > int(self.Stamina) * 10:
            newHealth = int(self.Stamina) * 10
        self.updateSelf("Health",newHealth)
        diff = newHealth - int(oldHealth)
        return diff
    def modifyGold(self,min,max):
        goldAdded = int(res.random.uniform(min,max))
        newGold = int(self.Gold) + int(goldAdded)
        oldGold = self.Gold
        if newGold < 0:
            newGold = 0
        self.updateSelf("Gold",newGold)
        diff = newGold - int(oldGold)
        return diff
    def modifyExp(self,min,max):
        expAdded = int(res.random.uniform(min,max))
        newExp = int(self.Exp) + int(expAdded)
        oldExp = self.Exp
        if newExp < 0:
            newExp = 0
        self.updateSelf("Exp",newExp)
        diff = newExp - int(oldExp)
        return diff
    def toggleRun(self, ID):
        if self.isRunning(ID):
            pass
        else:
            res.activeUsers.append(ID)
    def isRunning(self, ID):
        for i in res.activeUsers:
            if i == ID:
                return True
        return False
    

    #Character creation
    @staticmethod
    def insertNewCharacter(Dictionary):
        columns = ', '.join(str(x).replace('/', '_')for x in Dictionary.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in Dictionary.values())
        con.insert("Characters", columns, values)
    @staticmethod
    def createDictionary(ID, Name, Race, Class):
        #Setting variables that change based on chosen race and class
        if Class == "warrior":
            resources = "copper-0,iron-0,mithril-0,thorium-0"
            armor = "12"
            mainhand = str(itm.Item.incrementGlobalItemId()) + "-8-8-F-F-F"
            offhand = str(itm.Item.incrementGlobalItemId()) + "-9-9-F-F-F"
            if Race == "orc":
                chest = str(itm.Item.incrementGlobalItemId()) + "-3-3-F-F-F"
                legs = str(itm.Item.incrementGlobalItemId()) + "-6-6-F-F-F"
                feet = str(itm.Item.incrementGlobalItemId()) + "-7-7-F-F-F"
                stamina = "15"
                stat = "8"
                health = "150"
            elif Race == "human":
                chest = str(itm.Item.incrementGlobalItemId()) + "-29-29-F-F-F"
                legs = str(itm.Item.incrementGlobalItemId()) + "-32-32-F-F-F"
                feet = str(itm.Item.incrementGlobalItemId()) + "-33-33-F-F-F"
                stamina = "16"
                stat = "7"
                health = "160"
        elif Class == "mage":
            resources = "linen-0,silk-0,mageweave-0,runecloth-0"
            armor = "3"
            offhand = "F-F-F-F-F-F"
            if Race == "orc":
                chest = str(itm.Item.incrementGlobalItemId()) + "-12-12-F-F-F"
                legs = str(itm.Item.incrementGlobalItemId()) + "-15-15-F-F-F"
                feet = str(itm.Item.incrementGlobalItemId()) + "-16-16-F-F-F"
                mainhand = str(itm.Item.incrementGlobalItemId()) + "-17-17-F-F-F"
                stamina = "10"
                stat = "16"
                health = "100"
            elif Race == "human":
                chest = str(itm.Item.incrementGlobalItemId()) + "-39-39-F-F-F"
                legs = str(itm.Item.incrementGlobalItemId()) + "-42-42-F-F-F"
                feet = str(itm.Item.incrementGlobalItemId()) + "-43-43-F-F-F"
                mainhand = str(itm.Item.incrementGlobalItemId()) + "-44-44-F-F-F"
                stamina = "11"
                stat = "15"
                health = "110"
        elif Class == "rogue":
            resources = "light-0,heavy-0,thick-0,rugged-0"
            armor = "6"
            if Race == "orc":
                chest = str(itm.Item.incrementGlobalItemId()) + "-20-20-F-F-F"
                legs = str(itm.Item.incrementGlobalItemId()) + "-23-23-F-F-F"
                feet = str(itm.Item.incrementGlobalItemId()) + "-24-24-F-F-F"
                mainhand = str(itm.Item.incrementGlobalItemId()) + "-25-25-F-F-F"
                offhand = str(itm.Item.incrementGlobalItemId()) + "-26-26-F-F-F"
                stamina = "12"
                stat = "12"
                health = "120"
            elif Race == "human":
                chest = str(itm.Item.incrementGlobalItemId()) + "-20-20-F-F-F"
                legs = str(itm.Item.incrementGlobalItemId()) + "-23-23-F-F-F"
                feet = str(itm.Item.incrementGlobalItemId()) + "-24-24-F-F-F"
                mainhand = str(itm.Item.incrementGlobalItemId()) + "-25-25-F-F-F"
                offhand = str(itm.Item.incrementGlobalItemId()) + "-26-26-F-F-F"
                stamina = "13"
                stat = "11"
                health = "130"
        dictionary = {
            #Independant values for user
            "id":ID,
            "name":Name,
            "race":Race,
            "class":Class,
            "inventory":"",
            "resources":resources,
            "exp":"0",
            "gold":"0",
            "level":"1",
            "lockouts":"0X>DMVC-AAAAAAAAAAAAA, 0X>KARA-AAAAAAAAAAAAAAAA",
            "remainder":"0",
            "updated":res.calendar.timegm(res.time.gmtime()),

            #Equipment that is independant of class/race
            "helmet":"F-F-F-F-F-F",
            "shoulders":"F-F-F-F-F-F",
            "gloves":"F-F-F-F-F-F",
            "waist":"F-F-F-F-F-F",
            "trinket":"F-F-F-F-F-F",
            "chest":chest,
            "legs":legs,
            "feet":feet,
            "mainhand":mainhand,
            "offhand":offhand,
            "stamina":stamina,
            "armor":armor,
            "stat":stat,
            "health":health
        }
        return dictionary