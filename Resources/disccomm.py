from discord.enums import ButtonStyle
import Resources.imports as res
import Resources.character as char
import Resources.connection as con
import Resources.item as itm
import Resources.spells as spl
import Resources.shop as shp

#Importing dungeons
from Resources.dungeons.deadmines import Deadmines
def randomString(stringLength):
    letters = res.string.ascii_lowercase
    return ''.join(res.random.choice(letters) for i in range(stringLength))
def filterSpecialChars(string, keepSpace, removeNumbers):
    if keepSpace:
        for k in string.split("\n"):
            string = res.re.sub(r"[^a-zA-Z0-9]+", ' ', k)
    else:
        for k in string.split("\n"):
            string = res.re.sub(r'[^A-Za-z0-9]+', '', k)
    if removeNumbers:
        string = ''.join([i for i in string if not i.isdigit()])
    return string
def subStringAfter(keyword, message):
    try:
        regexp = res.re.compile(keyword + " (.*)$")
        name = regexp.search(message).group(1)
        name = " ".join(name.split()).lower()
        return name
    except Exception as e:
        print (e)

def pasteModel(modelID, subfolder, canvas, offset, delete):
    if modelID == "0" or modelID.upper == "F":
        temp = res.Image.open("Art/0.png").convert("RGBA")
    else:
        temp = res.Image.open("Art/" + subfolder + modelID + ".png").convert("RGBA")
    canvas.paste(temp, offset, mask = temp)
    if delete and modelID != "0" and modelID.upper != "F":
        res.os.remove("Art/" + subfolder + modelID + ".png")
async def createMessageCanvas(userID, message, printUser):
    #Creat the canvas
    canvas = res.Image.new('RGBA', (300,1200), (0, 0, 0, 0))
    draw = res.ImageDraw.Draw(canvas)
    heightCheck = 5
    pasteModel("messageBack", "", canvas, (0,0), False)
    if printUser:
        heightCheck = await pasteUser(userID, message, canvas, draw)
    return canvas, heightCheck, draw
async def pasteUser(userID, message, canvas, d):
    discordUser = await message.guild.query_members(user_ids=[userID])
    discordUser = discordUser[0]
    pfp = str(discordUser.avatar).replace("webp", "png")
    r = res.requests.get(pfp, allow_redirects=True)
    pfpsString = randomString(8)
    pfpString = pfpsString + ".png"
    open(pfpString, 'wb').write(r.content)
    profilePic = res.Image.open(pfpString)
    newPFP = profilePic.resize((35,35))
    canvas.paste(newPFP, (5, 5))
    res.os.remove(pfpString)

    #Gets user's discord name and pastes it to canvas
    author = discordUser.name
    Morpheus = res.ImageFont.truetype("Art/Fonts/Cthulhumbus.ttf", 24)
    d.text((45, 10), author, fill=(255,255,255), font = Morpheus)
    heightCheck = 45
    return heightCheck
async def pasteLongText(userID, d, font, offset, msg, canvas, message, toSplit, defaultColor = (255,255,255)):
    color = defaultColor
    coloring = ""
    width, height = offset[0], font.size
    currentWidth = offset[0]
    currentHeight = offset[1]
    cumulativeHeight = 0
    for i in msg.split(" "):
        if "%NPC" in i: #If npc name is showing up
            color = (255,255,0)
            coloring = "NPC"
            if "\n" in i:
                width, height = d.textsize(i + " ", font = font)
                currentHeight += height
                cumulativeHeight += height
                currentWidth = offset[0]
        elif "%ITEM" in i: #If item name is showing up
            i = i.replace("%ITEM", "").replace("\n","").replace(" ", "")
            newcolors = ()
            for y in i.split(","):
                newcolors = newcolors + (int(y),)
            color = newcolors
            coloring = "ITEM"
            if "\n" in i:
                width, height = d.textsize(i + " ", font = font)
                currentHeight += height
                cumulativeHeight += height
                currentWidth = offset[0]
        elif "%PLAYER" in i: #If player name is showing up
            color = (0,200,0)
            coloring = "PLAYER"
            if "\n" in i:
                width, height = d.textsize(i + " ", font = font)
                currentHeight += height
                cumulativeHeight += height
                currentWidth = offset[0]
        elif "%BOSS" in i:
            color = (255,0,0)
            coloring = "NPC"
            if "\n" in i:
                width, height = d.textsize(i + " ", font = font)
                currentHeight += height
                cumulativeHeight += height
                currentWidth = offset[0]
        else:
            #Get width of word and check if width is too large or if newspace began
            width, height = d.textsize(i + " ", font = font)
            height = font.size + 5
            if (width + currentWidth > 300 or "\n" in i) and toSplit: #Check if text is too big
                if "\n" in i:
                    i = i.replace("\n","")
                currentHeight += height
                cumulativeHeight += height
                currentWidth = offset[0]
                if currentHeight >= 250 and toSplit: #If message file it too large
                    #Send the current file as is
                    newMessage = canvas.crop((0,0,300,currentHeight + 10))
                    msgString = randomString(8)
                    imgString = msgString + ".png"
                    newMessage.save(imgString, format="png")
                    await message.channel.send(file=res.discord.File((imgString))), res.os.remove(imgString)

                    canvas, heightCheck, d = await createMessageCanvas(userID, message, False)
                    currentHeight = heightCheck + 5
            if ")" in i and coloring == "NPC": #If end of NPC name is detected
                #Paste last of npc name
                isSemicolon = False
                if ":" in i:
                    i = i.replace(":","")
                    isSemicolon = True
                i = i.replace(")","")
                width, height = d.textsize(i, font = font)
                d.text((currentWidth, currentHeight), i, fill=color, font = font)
                currentWidth += width
                color = defaultColor

                if isSemicolon:
                    #Paste semicolon and space
                    width, height = d.textsize(": ", font = font)
                    d.text((currentWidth, currentHeight), ":", fill=color, font = font)
                    currentWidth += width
                coloring = False
            elif "]" in i and coloring == "ITEM": #if end of item is detected
                #paste the item itself
                i = i.split("]")
                width, height = d.textsize(i[0] + "]", font = font)
                d.text((currentWidth, currentHeight), i[0] + "]", fill=color, font = font)
                currentWidth += width
                color = defaultColor

                #Paste substring after
                width, height = d.textsize(i[1] + " ", font = font)
                d.text((currentWidth, currentHeight), i[1], fill=color, font = font)
                currentWidth += width
                coloring = False
            elif coloring == "PLAYER": #If player colors were detected
                i = i.split(")")
                #Paste the name of the character
                width, height = d.textsize(i[0], font = font)
                d.text((currentWidth, currentHeight), i[0], fill=color, font = font)
                currentWidth += width
                color = defaultColor

                #Paste any substring after with normal color
                width, height = d.textsize(i[1] + " ", font = font)
                d.text((currentWidth, currentHeight), i[1], fill=color, font = font)
                currentWidth += width
                coloring = False
            else: #If it's just normal text
                d.text((currentWidth, currentHeight), i, fill=color, font = font)
                currentWidth += width
            height = font.size + 5
    return currentHeight + height + 5, canvas
def fetchColoredModel(modelID, race, subfolder):
    #Check if item exists or is real
    if modelID == "0" or modelID == "F":
        return "0"
    
    #Filter the name of the item and find it's properties
    realitem = res.re.sub(r"\D", "", modelID)
    item = itm.Item.returnItem(None, realitem)

    #Find the untextured image correlating to item and get it's properties.
    im = res.Image.open('Art/' + subfolder + race + item.ModelID + '.png')
    im = im.convert('RGBA')
    data = res.np.array(im)
    red, green, blue, alpha = data.T
    del alpha
    currentred = 255
    colors = item.Colors.split(",")

    #Repaint the item based on indicated colors
    for i in colors:
        currentlayer = (red == currentred) & (blue == 0) & (green == 0)
        newlayer = ()
        for y in i.split():
            newlayer = newlayer + (y,)
        data[..., :-1][currentlayer.T] = newlayer
        currentred -= 10

    #Save the image and return the name of the image
    im2 = res.Image.fromarray(data)
    im2.save("Art/" + subfolder + item.Name + ".png", "PNG")
    return item.Name

async def sendMessage(userID, message, textToSend, pasteUser):
    #Create the canvas
    canvas, heightCheck, draw = await createMessageCanvas(userID, message, pasteUser)

    #Paste text
    Morpheus = res.ImageFont.truetype("Art/Fonts/Cthulhumbus.ttf", 17)
    heightCheck, canvas = await pasteLongText(userID, draw, Morpheus, [5, heightCheck], textToSend, canvas, message, True)

    #Crop the image nicely and send it to Discord, then delete picture
    newMessage = canvas.crop((0,0,300,heightCheck))
    msgString = randomString(8)
    imgString = msgString + ".png"
    newMessage.save(imgString, format="png")

    return await message.channel.send(file=res.discord.File((imgString))), res.os.remove(imgString)


async def createCharacter(userID, message):
    User = char.Character(con.select("*","characters","ID",userID))
    if User.exists():
        return await sendMessage(userID, message, "You already have a character.", True)
    if User.isRunning(userID):
        return await sendMessage(userID, message, "You are doing something else.", True)
    User.toggleRun(userID)

    #Ask user to input their character's name, and wait for response.
    crudeName = await waitForMessages(userID, message, "Enter the name for your hero: \n \nThis name cannot contain special characters or spaces.", 30, whom = userID)
    if not crudeName:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message,"Character creation timed out.", True)
    #Filter name and make sure it's okay
    characterName = filterSpecialChars(crudeName[userID], False, True).title()
    if len(characterName) < 2:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "That name is too short.", True)
    if len(characterName) > 18:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "That name is too long.", True)
    #Checks if name is already taken
    anyOther = char.Character(con.select("*","characters","name",characterName))
    if anyOther.exists():
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "That name is already taken.", True)

    #Ask user to choose their race and wair for the resonse.
    raceChosen, cpumsg = await addReactionsAndWaitFor(userID, message, "You chose the name %PLAYER " + characterName + "). \n \nNext, choose your race: \n1: Orc \n2: Human", 30, whom=userID, orc='1⃣', human='2⃣')
    if not raceChosen:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "Character creation timed out.", True)

    #Ask user to choose their class and wair for the resonse.
    if raceChosen[userID] == "orc":
        displayRace = "n orc"
    else:
        displayRace = " human"
    classChosen, cpumsg = await addReactionsAndWaitFor(userID, message, "You chose a" + displayRace + ". \n \nLastly, choose your class: \n1: Warrior \n2: Mage \n3: Rogue", 30, whom=userID, warrior='1⃣', mage='2⃣', rogue = '3⃣')
    if not classChosen:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message,"Character creation timed out.", True)
    await sendMessage(userID, message, "You chose a" + displayRace + " " + classChosen[userID] + " named %PLAYER " + characterName + ").", True)
    char.Character.insertNewCharacter(char.Character.createDictionary(userID,characterName,raceChosen[userID],classChosen[userID]))
    res.activeUsers.remove(userID)
    return True
async def deleteCharacter(userID, message):
    if not await UserExists(userID, message, True, True):
        return
    User = char.Character(con.select("*","characters","ID",userID))
    User.toggleRun(userID)
    #Asks user if they're sure they want to delete their account.
    userReaction, cpumsg = await addReactionsAndWaitFor(userID, message, "Are you sure you want to delete your account, %PLAYER " + User.Name + ")? \nThis action cannot be reversed.", 20, whom = userID, yes='✅', no='❌')

    #Check if it timed out or they declined.
    if not userReaction[userID]:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "Character deletion timed out.", True)
    if userReaction[userID] == "no":
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "Character deletion cancelled.", True)

    #Delete the account.
    con.delete("Characters","ID", userID)
    res.activeUsers.remove(userID)
    await sendMessage(userID, message, "You have deleted your character.", True)
async def showCharacter(userID, message):
    #check if user is trying to show his character or someone elses,
    if len(message.content.split(" ")) == 3:
        recip = filterSpecialChars(subStringAfter("hero", message.content), False, False)
        User = char.Character(con.select("*","characters","ID",recip))
        if not await UserExists(userID, message, True, False):
            return await sendMessage(userID, message, "Player does not have a character.", True)
    else:
        User = char.Character(con.select("*","characters","ID",userID))
        if not await UserExists(userID, message, False, True):
            return

    User.updateHealth()
    #Set some initial variables and create canvas
    heroOffSet = (37,16)
    canvas = res.Image.new('RGBA', (300,300), (0, 0, 0, 0))
    d = res.ImageDraw.Draw(canvas)
    Morpheusbig = res.ImageFont.truetype("Art/Fonts/Morpheus.ttf", 24)
    Morpheussmall = res.ImageFont.truetype("Art/Fonts/Morpheus.ttf", 19)
    BitPotion = res.ImageFont.truetype("Art/Fonts/BitPotion.ttf", 28)

    #Paste backround and race
    pasteModel("white", "", canvas, (0,0), False)
    pasteModel(User.Race, "", canvas, heroOffSet, False)

    #Start pasting equipment
    pasteModel(fetchColoredModel(User.Feet.split("-")[2], User.Race, "Feet/"), "Feet/", canvas, heroOffSet, True)
    pasteModel(fetchColoredModel(User.Legs.split("-")[2], User.Race, "Legs/"), "Legs/", canvas, heroOffSet, True)
    pasteModel(fetchColoredModel(User.Gloves.split("-")[2], User.Race, "Gloves/"), "Gloves/", canvas, heroOffSet, True)
    pasteModel(fetchColoredModel(User.Chest.split("-")[2], User.Race, "Chest/"), "Chest/", canvas, heroOffSet, True)
    pasteModel(fetchColoredModel(User.Waist.split("-")[2], User.Race, "Waist/"), "Waist/", canvas, heroOffSet, True)
    pasteModel(fetchColoredModel(User.Shoulders.split("-")[2], User.Race, "Shoulders/"), "Shoulders/", canvas, heroOffSet, True)

    #Try to see if helmet shows hair, paste hair if it does
    item = itm.Item.returnItem(None, User.Helmet.split("-")[2])
    if item.exists():
        pasteModel(fetchColoredModel(User.Helmet.split("-")[2], User.Race, "Helmet/"), "Helmet/", canvas, heroOffSet, True)
    if not item.ShowHair == "no":
        pasteModel(User.Race + "hair", "", canvas, heroOffSet, False)
    
    #Paste weapons
    pasteModel(fetchColoredModel(User.Mainhand.split("-")[2], "", "Mainhand/"), "Mainhand/", canvas, heroOffSet, True)
    pasteModel(fetchColoredModel(User.Offhand.split("-")[2], User.Race, "Offhand/"), "Offhand/", canvas, heroOffSet, True)

    #Retrieve pictures of gold, bars, and frames.
    healthbar = res.Image.open("Art/healthbar.png").convert("RGBA")
    expbar = res.Image.open("Art/expbar.png").convert("RGBA")
    healthbarFrame = res.Image.open("Art/healthBarFrame.png").convert("RGBA")

    #Calculate the health and exp to display, and crop healthbar and exp bar accordingly.
    remainingHealth = int((int(User.Health)/(int(User.Stamina) * 10)) * 300)
    ActualHealthBar = healthbar.crop((0,0,remainingHealth,26))

    expneeded = 10 * res.math.floor((round((0.04*(int(User.Level)**3))+(0.8*(int(User.Level)**2))+(2*int(User.Level)))))
    remainingExp = int((int(User.Exp) / int(expneeded)) * 300)
    ActualExpBar = expbar.crop((0,0,remainingExp,26))

    #Paste the healthbar and expbar and their frames
    canvas.paste(ActualHealthBar, (0, 276), mask=ActualHealthBar)
    canvas.paste(healthbarFrame, (0, 276), mask=healthbarFrame)
    canvas.paste(ActualExpBar, (0, 256), mask=ActualExpBar)
    canvas.paste(healthbarFrame, (0, 256), mask=healthbarFrame)

    #Paste the numerical values of exp and health
    w, h = d.textsize(User.Health + " / " + str((int(User.Stamina) * 10)), font = BitPotion)
    await pasteLongText(userID, d, BitPotion, (((300-w)/2),(300- h - 5)), User.Health + " / " + str((int(User.Stamina) * 10)), canvas, message, False, (0,0,0))
    w, h = d.textsize(User.Exp + " / " + str(expneeded), font = BitPotion)
    await pasteLongText(userID, d, BitPotion, (((300-w)/2),(280- h - 5)), User.Exp + " / " + str(expneeded), canvas, message, False, (0,0,0))

    #Paste the name and race at the top of the screen
    w, h = d.textsize(User.Name, font = Morpheusbig)
    await pasteLongText(userID, d, Morpheusbig, (150 - (w/2),-4), "%PLAYER " + User.Name + ")", canvas, message, False, (0,0,0))
    w, h = d.textsize(User.Race.title() + " " + User.Class.title(), font = Morpheussmall)
    await pasteLongText(userID, d, Morpheussmall, (150 - (w/2), 20), User.Race.title() + " " + User.Class.title(), canvas, message, False, (0,0,0))

    #Paste the armor value and depending on class paste mainstat value
    await pasteLongText(userID, d, Morpheussmall, (2, 210), "Armor: " + User.Armor, canvas, message, False, (0,0,0))
    if User.Class == "warrior":
        await pasteLongText(userID, d, Morpheussmall, (2, 230), "Strength: " + User.Stat, canvas, message, False, (0,0,0))
    elif User.Class == "mage":
        await pasteLongText(userID, d, Morpheussmall, (2, 230), "Intellect: " + User.Stat, canvas, message, False, (0,0,0))
    elif User.Class == "rogue":
        await pasteLongText(userID, d, Morpheussmall, (2, 230), "Agility: " + User.Stat, canvas, message, False, (0,0,0))

    #Paste character level and gold amount in bottom right corner.
    w, h = d.textsize("Level: " + User.Level, font = Morpheussmall)
    await pasteLongText(userID, d, Morpheussmall, (300 - w - 2, 210), "Level: " + User.Level, canvas, message, False, (0,0,0))

    #Paste golden coin and golden numerical value in bottom right corner
    w, h = d.textsize(User.Gold + " gold", font = Morpheussmall)
    await pasteLongText(userID, d, Morpheussmall, (300 - w - 2, 230), User.Gold + " gold", canvas, message, False, (0,0,0))
    pasteModel("goldcoin", "", canvas, (300 - 22 - w - 2,235), False)

    #Create a random string, save image, send image and delete image
    msgString = randomString(8)
    imgString = msgString + ".png"
    canvas.save(imgString, format="png")
    await message.channel.send(file=res.discord.File((imgString))), res.os.remove(imgString)

async def UserExists(userID, message, checkRunning, sendmsg):
    User = char.Character(con.select("*","characters","ID",userID))
    if checkRunning and User.isRunning(userID):
        if sendmsg:
            await sendMessage(userID, message,"You are doing something else.", True)
        res.activeUsers.remove(userID)
        return False
    if not User.exists():
        if sendmsg:
            await sendMessage(userID, message, "You do not have a character.", True)
        res.activeUsers.remove(userID)
        return False
    return True

async def equip(userID, message):
    if not await UserExists(userID, message, True, True):
        return
    User = char.Character(con.select("*","characters","ID",userID))
    User.toggleRun(userID)
    if not len(message.content.split(" ")) >= 3:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "Type which item you'd like to equip.", True)
    itemName = filterSpecialChars(subStringAfter("equip", message.content), True, False)
    item = await showAllUniqueInInventory(userID, message, itemName, "Which one would you like to equip?")
    if item == None:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "Equipping timed out.", True)
    equipped, msg = User.equip(item)
    if equipped:
        await showCharacter(userID, message)
    res.activeUsers.remove(userID)
    await sendMessage(userID, message, msg, True)
async def unequip(userID, message):
    if not await UserExists(userID, message, True):
        return
    User = char.Character(con.select("*","characters","ID",userID))
    User.toggleRun(userID)
    if not len(message.content.split(" ")) >= 3:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "Type which item you'd like to unequip.", True)
    itemName = filterSpecialChars(subStringAfter("unequip", message.content), True, False)
    item = itm.Item.returnItem(itemName)
    itemString = item.returnItemString()
    unequipped, msg = User.unequip(itemString.split("-"))
    if unequipped:
        await showCharacter(userID, message)
    res.activeUsers.remove(userID)
    await sendMessage(userID, message, msg, True)
async def sell(userID, message):
    if not await UserExists(userID, message, True, True):
        res.activeUsers.remove(userID)
        return
    User = char.Character(con.select("*","characters","ID",userID))
    User.toggleRun(userID)
    if not len(message.content.split(" ")) >= 3:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "Type which item you'd like to sell.", True)
    itemName = filterSpecialChars(subStringAfter("sell", message.content), True, False)
    item = await showAllUniqueInInventory(userID, message, itemName, "Which one would you like to sell?")
    if item == None:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "Selling timed out.", True)
    sold, msg = User.sell(item)

    res.activeUsers.remove(userID)
    await sendMessage(userID, message, msg, True)
async def use(userID, message):
    if not await UserExists(userID, message, True, True):
        res.activeUsers.remove(userID)
        return
    User = char.Character(con.select("*","characters","ID",userID))
    User.toggleRun(userID)
    if not len(message.content.split(" ")) >= 3:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "Type which item you'd like to use.", True)
    itemName = filterSpecialChars(subStringAfter("use", message.content), True, False)
    item = await showAllUniqueInInventory(userID, message, itemName, "Which one would you like to use?")
    if item == None:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "Using timed out.", True)
    used, msg = User.use(item)
    res.activeUsers.remove(userID)
    await sendMessage(userID, message, msg, True)
async def train(userID, message):
    if not await UserExists(userID, message, True, True):
        res.activeUsers.remove(userID)
        return
    cont = True
    User = char.Character(con.select("*","characters","ID",userID))
    User.toggleRun(userID)
    while cont:
        cont, msg = User.train()
        if cont:
            reaction, cpumsg = await addReactionsAndWaitFor(userID, message, msg, 30, whom = userID, yes='✅', no='❌')
            if not reaction[userID] or reaction[userID] == "no":
                cont = False
                res.activeUsers.remove(userID)
                return await sendMessage(userID, message, "You chose to rest and train another day.", True)
            else:
                await cpumsg.delete()
        else:
            res.activeUsers.remove(userID)
            return await sendMessage(userID, message, msg, True)
async def inspect(userID, message):
    userid = None
    if len(message.content.split(" ")) >= 3:
        userid = filterSpecialChars(subStringAfter("inspect", message.content), False, False)
    else:
        userid = userID
    if not await UserExists(userid, message, False, False):
        if len(message.content.split(" ")) >= 3:
            return await sendMessage(userID, message, "That user does not have a character.", True)
        else:
            return await sendMessage(userID, message, "You do not have a character.", True)
    User = char.Character(con.select("*","characters","ID",userid))
    msg = User.Name + " is wearing: \n"
    msg += User.inspect()
    return await sendMessage(userID, message, msg, True)

async def getResources(userID, message):
    if not await UserExists(userID, message, True, True):
        return
    res.activeUsers.append(userID)
    if not len(message.content.split(" ")) >= 3:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "Type which resource you'd like to gather.", True)
    User = char.Character(con.select("*","characters","ID",userID))
    resource = filterSpecialChars(subStringAfter("gather", message.content), True, False).lower()
    if resource not in User.Resources:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "You cannot gather that resource.", True)
    cont = True
    while cont:
        listOfResources = User.Resources.split(",")
        healthLost = 10
        for i in range(len(listOfResources)):
            if resource in listOfResources[i]:
                healthLost *= (i+1)
                healthLost /= 10
                x = listOfResources[i]
                x = x.split("-")
                x[1] = str(int(x[1]) + 1)
                listOfResources[i] = "-".join(x)
        resources = ",".join(listOfResources)
        healthLostNum = int(User.Stamina) * healthLost
        newHealth = int(User.Health) - int(healthLostNum)
        if newHealth <= 0:
            res.activeUsers.remove(userID)
            newHealth = "1"
            User.updateSelf("health", newHealth)
            return await sendMessage(userID, message, "You were too weary when you started and collapsed before being able to gather " + resource + ". \n \nRest up and try again.", True)
        User.updateSelf("resources", resources)
        User.updateSelf("health", str(int(float(newHealth))))
        reaction, cpumsg = await addReactionsAndWaitFor(userID, message, "You succesfully gathered 1 " + resource + ", but were attacked and lost " + str(int(float(healthLostNum))) + " health in the process. \n \nWould you like to gather another or rest?", 30, whom = userID, yes='✅', no='❌')
        if not reaction[userID] or reaction[userID] == "no":
            cont = False
            res.activeUsers.remove(userID)
            await sendMessage(userID, message, "You chose to rest and gather another day another day.", True)
        else:
            await cpumsg.delete()
async def showResources(userID, message):
    if not await UserExists(userID, message, True, True):
        return
    msg = "Your resources: \n "
    User = char.Character(con.select("*","characters","ID",userID))
    listOfResources = User.Resources.split(",")
    if User.Resources.count("0") == 4:
        return await sendMessage(userID, message, "You do not have any resources. Go ahead and gather some!", True)
    for i in listOfResources:
        x = i.split("-")
        if x[1] != "0":
            msg += " \n" + x[0].title() + ": " + x[1]
    await sendMessage(userID, message, msg, True)





async def queryItem(userID, message):
    if not len(message.content.split(" ")) >= 3:
        return await sendMessage(userID, message, "Type which item you'd like to see.", True)
    if UserExists(userID, message, False, False):
        User = char.Character(con.select("*","characters","ID",userID))
        race = User.Race
    else:
        race = "orc"
    itemName = filterSpecialChars(subStringAfter("item", message.content), True, False)
    item = itm.Item.returnItem(itemName)
    if not item.exists():
        return await sendMessage(userID, message, "Item does not exist.", True)
    itemString = item.returnItemString()
    await showItemData(userID, message, itemString)
    itemStringSplit = itemString.split("-")
    if itemStringSplit[2] != "F" and item.Slot:
        canvas = res.Image.new('RGBA', (300,300), (0, 0, 0, 0))
        #Paste backround and race
        pasteModel("white", "", canvas, (0,0), False)
        pasteModel(race, "", canvas, (37, 16), False)
        if item.ShowHair != "no":
            pasteModel(race + "Hair", "", canvas, (37, 16), False)
        #Start pasting equipment
        pasteModel(fetchColoredModel(itemStringSplit[2], race, item.Slot.capitalize() + "/"), item.Slot.capitalize() + "/", canvas, (37, 16), True)
        msgString = randomString(8)
        imgString = msgString + ".png"
        canvas.save(imgString, format="png")
        await message.channel.send(file=res.discord.File((imgString))), res.os.remove(imgString)

async def showItemData(userID, message, itemString):
    #Check if the item exists.
    itemSegments = itemString.split("-")
    item = itm.Item.returnItem(None, itemSegments[1])
    Morpheusbig = res.ImageFont.truetype("Art/Fonts/Morpheus.ttf", 24)
    Morpheussmall = res.ImageFont.truetype("Art/Fonts/Morpheus.ttf", 19)
    canvas = res.Image.new('RGBA', (300,1200), (0, 0, 0, 0))
    d = res.ImageDraw.Draw(canvas)
    heightCheck = 0
    pasteModel("black", "", canvas, (0,0), False)
    pasteModel("topandbot", "", canvas, (0,0), False)
    name = item.returnFullItemName()
    w, h = d.textsize("[" + item.Name + "]", Morpheusbig)
    del h
    #Name of the item:
    if w >= 286:
        heightCheck, canvas = await pasteLongText(userID, d, Morpheusbig, (10, heightCheck), name, canvas, message, True)
    else:
        heightCheck, canvas = await pasteLongText(userID, d, Morpheusbig, (150 - (w/2), heightCheck), name, canvas, message, False)
    
    #Binding properties of item and transmog:
    if itemSegments[1] != itemSegments[2] and item.Slot:
        itemsApperance = itm.Item.returnItem(None, itemSegments[2])
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Transmogrified to: [" + itemsApperance.Name + "]", canvas, message, True, (231, 43, 237))
        del itemsApperance
    if itemSegments[3] != "F":
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), itemSegments[3], canvas, message, True, (255,255,255))

    #Slot item goes into (if armor):
    if item.Slot and item.Type:
        noVal, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Slot, canvas, message, True, (255,255,255))
        w, h = d.textsize(item.Type, font = Morpheussmall)
        del noVal
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (300 - 7 - w, heightCheck), item.Type, canvas, message, True, (255,255,255))
    elif item.Slot and item.Type.lower() == None:
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Slot, canvas, message, True, (255,255,255))
    if item.Damage:
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Damage + " Damage", canvas, message, True, (255,255,255))
    if item.Armor != "0":
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Armor + " Armor", canvas, message, True, (255,255,255))
    if item.Stamina != "0":
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stamina + " Stamina", canvas, message, True, (20, 255, 20))
    if item.Stat != "0":
        if item.Type.lower() == "mail" or item.Type.lower() == "sword" or item.Type.lower() == "shield" or item.Type.lower() == "axe" or item.Type.lower() == "mace":
            heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stat + " Strength", canvas, message, True, (20, 255, 20))
        if item.Type.lower() == "cloth" or item.Type.lower() == "staff":
            heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stat + " Intellect", canvas, message, True, (20, 255, 20))
        if item.Type.lower() == "leather" or item.Type.lower() == "dagger":
            heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stat + " Agility", canvas, message, True, (20, 255, 20))
    
    if item.Level and item.Level != "F":
        color = (255,255,255)
        User = char.Character(con.select("*","characters","ID",userID))
        if User.exists():
            color = (255,255,255)
            if item.Level > User.Level:
                color = (255,30,30)
        else:
            color = (255,255,255)
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Requires level: " + item.Level, canvas, message, False, color)
    
    if itemSegments[4] != "F":
        spellSplit = itemSegments[4].split("&")
        spellSplit.pop()
        for i in spellSplit:
            heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Use: " + spl.Spell.findByID(i).Description, canvas, message, True, (30,255,0))

    if itemSegments[5] != "F":
        if int(itemSegments[5]) > 1:
            heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), itemSegments[5] + " Charges", canvas, message, True, (255,255,255))
        else:
            heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), itemSegments[5] + " Charge", canvas, message, True, (255,255,255))
    if item.Flavor:
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Flavor, canvas, message, True, (251, 203, 2))
    if item.Value:
        w, h = d.textsize("Sell value: " + item.Value, Morpheussmall)
        pasteModel("goldcoin", "", canvas, (10+w, heightCheck+7), False)
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Sell value: " + item.Value, canvas, message, True, (255,255,255))
    pasteModel("topandbot", "", canvas, (0, heightCheck + 2), False)
    newItem = canvas.crop((0,0,300,heightCheck + 7))
    msgString = randomString(8)
    itemString = msgString + ".png"
    newItem.save(itemString, format="png")
    await message.channel.send(file=res.discord.File((itemString))), res.os.remove(itemString)
    return itemSegments[0]
    

def returnAllInstancesOfItem(User, itemName):
    item = itm.Item.returnItem(itemName)
    allItemsFound = []
    inBag = User.checkIfHasItem(item)
    if inBag:
        for i in inBag:
            allItemsFound.append(i)
    return allItemsFound
    
async def showAllUniqueInInventory(userID, message, itemName, msgToSend):
    User = char.Character(con.select("*","characters","ID",userID))
    ifExists = itm.Item.returnItem(itemName)
    if not ifExists.exists():
        return await sendMessage(userID, message, "Item does not exist.", True)
    itemsFound = returnAllInstancesOfItem(User, itemName)
    for i in itemsFound[:]:
        for ii in itemsFound[:]:
            if ii in itemsFound and i in itemsFound:
                if i[1:] == ii[1:] and itemsFound.index(i) < itemsFound.index(ii):
                    itemsFound.remove(ii)
    if itemsFound == []:
        return [ifExists.ID,ifExists.ID,ifExists.ID]
    if len(itemsFound) == 1:
        return itemsFound[0]
    #Case when more than one item is chosen
    itemAndEmoji = {}
    count = ["ONE","TWO","THREE","FOUR","FIVE","SIX","SEVEN","EIGHT","NINE"]
    emojis = ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(1, 10)]
    for i in range(len(itemsFound)):
        Morpheus = res.ImageFont.truetype("Art/Fonts/Cthulhumbus.ttf", 17)
        canvas = res.Image.new('RGBA', (1,1), (0, 0, 0, 0))
        d = res.ImageDraw.Draw(canvas)
        word = count[i]
        pad = " "
        wordWidth, wordHeight = d.textsize(word, font = Morpheus)
        padWidth, padHeight = d.textsize(pad, font = Morpheus)
        del padHeight, wordHeight
        while padWidth + (wordWidth/2) < 140:
            pad += " "
            padWidth, padHeight = d.textsize(pad, font = Morpheus)
        await sendMessage(userID, message, pad + count[i], False)
        await showItemData(userID, message, "-".join(itemsFound[i]))
        itemAndEmoji[itemsFound[i][0]] = emojis[i]
    reaction, cpumsg = await addReactionsAndWaitFor(userID, message, msgToSend, 10, whom = userID, **itemAndEmoji)
    if not reaction[userID]:
        return None
    for i in itemsFound:
        if i[0] == reaction[userID]:
            return i
    






async def craftItem(userID, message):
    if not await UserExists(userID, message, True, True):
        return
    User = char.Character(con.select("*","characters","ID",userID))
    if not len(message.content.split(" ")) >= 3:
        return await sendMessage(userID, message, "Type which item you'd like to craft.", True)
    itemName = filterSpecialChars(subStringAfter("craft", message.content), True, False)
    item = itm.Item.returnItem(itemName)
    if not item.exists():
        return await sendMessage(userID, message, "Item does not exist.", True)
    if item.Reagents == None:
        return await sendMessage(userID, message, "That item cannot be crafted.", True)
    for i in item.Reagents.split(","):
        if "" != i:
            ii = i.split("-")
            if ii[1] not in User.Resources:
                return await sendMessage(userID, message, "That item cannot be crafted by your class.", True)
            else:
                for x in User.Resources.split(","):
                    xx = x.split("-")
                    if xx[0] == ii[1]:
                        if ii[0] > xx[1]:
                            return await sendMessage(userID, message, "You do not have enough " + xx[0] + " to craft that.", True)
    #Code past here assumes user is able to craft item
    individualReagents = item.Reagents.split(",")
    userResources = User.Resources.split(",")
    for i in individualReagents:
        if "" != i:
            ii = i.split("-")
            for i, x in enumerate(userResources):
                if ii[1] in x:
                    xx = x.split("-")
                    newAmount = str(int(xx[1]) - int(ii[0]))
                    xx[1] = newAmount
                    final = "-".join(xx)
                    userResources[i] = final
    #add item to inventory
    itemString = item.ItemStringWithNewGlobalID()
    newInventory = User.Inventory + itemString + ","
    User.updateSelf("inventory", newInventory)
    User.updateSelf("resources", ",".join(userResources))
    return await sendMessage(userID, message, "You succesfully crafted: " + item.returnFullItemName() + ".", True)


async def showInventory(userID, message):
    if not await UserExists(userID, message, True, True):
        return
    User = char.Character(con.select("*","characters","ID",userID))
    if User.Inventory == "" or User.Inventory == ",":
        return await sendMessage(userID, message, "Your inventory is empty.", True)
    msg = "Your inventory:"
    for i in User.Inventory.split(","):
        if "" != i:
            x = i.split("-")
            item = itm.Item.returnItem(None, x[1])
            msg += " \n- " + item.returnFullItemName()
    return await sendMessage(userID, message, msg, True)


async def showFullInventory(userID, message):
    if not await UserExists(userID, message, True):
        return
    User = char.Character(con.select("*","characters","ID",userID))
    if User.Inventory == "" or User.Inventory == ",":
        return await sendMessage(userID, message, "Your inventory is empty.", True)

    totalHeight = 0
    bigCanvas = res.Image.new('RGBA', (300,100000), (0, 0, 0, 0))

    for i in User.Inventory.split(","):
        if "" != i:
            itemSegments = i.split("-")
            item = itm.Item.returnItem(None, itemSegments[1])
            Morpheusbig = res.ImageFont.truetype("Art/Fonts/Morpheus.ttf", 24)
            Morpheussmall = res.ImageFont.truetype("Art/Fonts/Morpheus.ttf", 19)
            canvas = res.Image.new('RGBA', (300,1200), (0, 0, 0, 0))
            d = res.ImageDraw.Draw(canvas)
            heightCheck = 0
            pasteModel("black", "", canvas, (0,0), False)
            pasteModel("topandbot", "", canvas, (0,0), False)
            name = item.returnFullItemName()
            w, h = d.textsize("[" + item.Name + "]", Morpheusbig)
            del h
            #Name of the item:
            if w >= 286:
                heightCheck, canvas = await pasteLongText(userID, d, Morpheusbig, (10, heightCheck), name, canvas, message, True)
            else:
                heightCheck, canvas = await pasteLongText(userID, d, Morpheusbig, (150 - (w/2), heightCheck), name, canvas, message, False)
            
            #Binding properties of item and transmog:
            if itemSegments[1] != itemSegments[2]:
                itemsApperance = itm.Item.returnItem(None, itemSegments[2])
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Transmogrified to: [" + itemsApperance.Name + "]", canvas, message, True, (231, 43, 237))
                del itemsApperance
            if itemSegments[3] != "F":
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), itemSegments[3], canvas, message, True, (255,255,255))

            #Slot item goes into (if armor):
            if item.Slot.lower() != None and item.Type.lower() != None:
                noVal, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Slot, canvas, message, True, (255,255,255))
                w, h = d.textsize(item.Type, font = Morpheussmall)
                del noVal
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (300 - 7 - w, heightCheck), item.Type, canvas, message, True, (255,255,255))
            elif item.Slot.lower() != None and item.Type.lower() == None:
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Slot, canvas, message, True, (255,255,255))
            if item.Damage.lower() != None:
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Damage + " Damage", canvas, message, True, (255,255,255))
            if item.Armor != "0":
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Armor + " Armor", canvas, message, True, (255,255,255))
            if item.Stamina != "0":
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stamina + " Stamina", canvas, message, True, (20, 255, 20))
            if item.Stat != "0":
                if item.Type.lower() == "mail" or item.Type.lower() == "sword" or item.Type.lower() == "shield" or item.Type.lower() == "axe" or item.Type.lower() == "mace":
                    heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stat + " Strength", canvas, message, True, (20, 255, 20))
                if item.Type.lower() == "cloth" or item.Type.lower() == "staff":
                    heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stat + " Intellect", canvas, message, True, (20, 255, 20))
                if item.Type.lower() == "leather" or item.Type.lower() == "dagger":
                    heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stat + " Agility", canvas, message, True, (20, 255, 20))
            
            if item.Level.lower() != None and item.Level != "F":
                color = (255,255,255)
                User = char.Character(con.select("*","characters","ID",userID))
                if User.exists():
                    color = (255,255,255)
                    if item.Level > User.Level:
                        color = (255,30,30)
                else:
                    color = (255,255,255)
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Requires level: " + item.Level, canvas, message, False, color)
            if item.Flavor.lower() != None:
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Flavor, canvas, message, True, (120,120,120))
            if itemSegments[5] != "F":
                if int(itemSegments[5]) > 1:
                    heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), itemSegments[6] + " Charges", canvas, message, True, (255,255,255))
                else:
                    heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), itemSegments[6] + " Charge", canvas, message, True, (255,255,255))
            if item.Value.lower() != None:
                w, h = d.textsize("Sell value: " + item.Value, Morpheussmall)
                pasteModel("goldcoin", "", canvas, (10+w, heightCheck+7), False)
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Sell value: " + item.Value, canvas, message, True, (255,255,255))
            pasteModel("topandbot", "", canvas, (0, heightCheck + 2), False)
            newItem = canvas.crop((0,0,300,heightCheck + 7))
            msgString = randomString(8)
            itemString = msgString + ".png"
            newItem.save(itemString, format="png")
            temp = res.Image.open(itemString).convert("RGBA")
            bigCanvas.paste(temp, (0, totalHeight), mask = temp)
            totalHeight += heightCheck + 3
            res.os.remove(itemString)
    
    newItem = bigCanvas.crop((0,0,300,totalHeight + 7))
    msgString = randomString(8)
    itemString = msgString + ".png"
    newItem.save(itemString, format="png")
    await message.channel.send(file=res.discord.File((itemString))), res.os.remove(itemString)
    return await sendMessage(userID, message, "If the picture seems too small, open it in your browser.", True)







#Define 2 specific functions for these 2 operation to work
def updateDict(dict, key, value):
    dict[key] = value
    return True
def checkAllVoted(dicts):
    for i in dicts.values():
        if i == None:
            return False
    return True
#Sends a message using sendMessage, adds specified emojis and waits for specified user(s) to respond. Returns a dict with user(s) and their reaction(s)
async def addReactionsAndWaitFor(userID, message, msgToSend, timeouts, **kwargs):
    cpumsg, throwaway = await sendMessage(userID, message, msgToSend, True)
    del throwaway
    users, reactions = [], []
    reactionvalues = {}
    usersreactions = {}
    for key, value in kwargs.items():
        if "whom" not in key:
            if "hashed" in key:
                for k,v in key:
                    await cpumsg.add_reaction(v)
                    reactions.append(v)
                    reactionvalues[value] = k
            else:
                await cpumsg.add_reaction(value)
                reactions.append(value)
                reactionvalues[value] = key
        else:
            if "hashed" in key:
                for k,v in key:
                    users.append(v)
                    usersreactions[v] = None
            else:
                users.append(value)
                usersreactions[value] = None
    try:
        await res.client.wait_for('reaction_add', timeout=timeouts, check=lambda reaction, user: reaction.emoji in reactions and str(user.id) in users and updateDict(usersreactions, str(user.id), reactionvalues[reaction.emoji]) and checkAllVoted(usersreactions))
    except Exception as e:
        print(e)
    return usersreactions, cpumsg
#Sends a message using sendMessage and waits for specified user(s) to respond.
async def waitForMessages(userID, message, msgToSend, timeouts, **kwargs):
    await sendMessage(userID, message, msgToSend, True)
    users = []
    usersreactions = {}
    for key, value in kwargs.items():
        if "whom" in key:
            users.append(value)
            usersreactions[value] = None
    await res.client.wait_for('message', timeout=timeouts, check=lambda user: str(user.author.id) in users and updateDict(usersreactions, str(user.author.id), str(user.content)) and checkAllVoted(usersreactions))
    return usersreactions

async def shop(userID, message):
    if not await UserExists(userID, message, True, True):
        return
    if not len(message.content.split(" ")) >= 3:
        return await sendMessage(userID, message, "Type which shop you'd like to browse.", True)
    User = char.Character(con.select("*","characters","ID",userID))
    shopName = filterSpecialChars(subStringAfter("shop", message.content), True, False)
    Shop = shp.Shop.findShop(shopName)
    if not Shop:
        return await sendMessage(userID, message, "That shop does not exist", True)
    User.toggleRun(userID)
    await sendMessage(userID, message, Shop.Dialogue, True)


    #Shop display
    itemAndEmoji = {}
    count = ["1","2","3","4","5","6","7","8","9"]
    emojis = ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(1, 10)]
    msg = ""
    itemAndEmoji = {}
    for i in range(len(Shop.Items)):
        item = itm.Item.returnItem(None, str(Shop.Items[i]))
        word = count[i]
        itemAndEmoji[str(i)] = emojis[i]
        msg += word + ": " + item.returnFullItemName() + " \nCost: " + str(Shop.Prices[i]) + " \n \n"
    msg = msg[:-4]
    reaction, cpumsg = await addReactionsAndWaitFor(userID, message, msg, 40, whom = userID, **itemAndEmoji)
    if not reaction[userID]:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, Shop.Bye, True)
    index = int(reaction[userID])

    item = itm.Item.returnItem(None, str(Shop.Items[index]))
    price = Shop.Prices[index]
    if int(User.Gold) < price:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, Shop.Poor, True)
    User.modifyGold(-price, -price)
    User.addToInventory(item.ItemStringWithNewGlobalID())
    res.activeUsers.remove(userID)
    return await sendMessage(userID, message, Shop.Thank + " \n \nYou bought: " + item.returnFullItemName(), True)

#Dungeon Stuff
async def runDungeon(userID, message):
    if not await UserExists(userID, message, True, True):
        return
    if not len(message.content.split(" ")) >= 3:
        return await sendMessage(userID, message, "Type which dungeon you'd like to run.", True)
    cont = True
    User = char.Character(con.select("*","characters","ID",userID))
    dungeon = []
    curLockout = ""
    nameOfDungeon = filterSpecialChars(subStringAfter("run", message.content), True, False)
    if nameOfDungeon == "deadmines":
        dungeon = Deadmines
        lister = User.Lockouts.split(",")
        for i in lister:
            if "DMVC" in i:
                curLockout = i
    else:
        return await sendMessage(userID, message, "That dungeon doesn't exist.", True)
    User.toggleRun(userID)
    userReaction, cpumsg = await addReactionsAndWaitFor(userID, message, dungeon.intro, 60, whom = userID, fight='⚔', flee='🏃')
    if not userReaction[userID] or userReaction[userID] == "no":
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, "After contemplating for awhile, you choose to flee and live another day.", True)
    if curLockout[0:3] != "0=>":
        res.activeUsers.remove(userID)
        return await sendMessage(userID, message, dungeon.attunefail, True)
    #Now the fun begins
    while cont:
        curLetter = curLockout[int(dungeon.cPoS.ID) + 7]
        turns = {"forward":"🔼", "back":"🔽", "left":"◀", "right":"▶"}
        emojis = {"flee":'🏃'}
        msg = ""
        if curLetter != "A" and dungeon.cPoS.clear:
            msg = dungeon.cPoS.clear
        else:
            msg = dungeon.cPoS.description
        validMoves = dungeon.returnValidMoves()
        #Check for exit
        if not validMoves:
            cont = False
            msg = dungeon.cPoS.description
            res.activeUsers.remove(userID)
            return await sendMessage(userID, message, dungeon.cPoS.name + " \n \n" + msg, True)
        
        for k in validMoves:
            if dungeon.cPoS.boss:
                if str(k) == "forward":
                    if curLetter != "A":
                        emojis[k] = turns[k]
                elif str(k) == "right" or str(k) == 'left':
                    if dungeon.cPoS.boss.type != "boss":
                        emojis[k] = turns[k]
                    elif dungeon.cPoS.boss.type == "boss" and curLetter != "A":
                        emojis[k] = turns[k]
                else:
                    emojis[str(k)] = turns[k]
            else:
                emojis[k] = turns[k]
        
        #Checks for boss
        if dungeon.cPoS.boss and dungeon.cPoS.boss.type != "rare" and curLetter == "A":
            if dungeon.cPoS.boss.cmodecheck and dungeon.cPoS.boss.cmodecheck(User):
                emojis["cmode"] = dungeon.cPoS.boss.cmode
            else:
                emojis["fight"] ='⚔'
        elif dungeon.cPoS.boss and dungeon.cPoS.boss.type == "rare" and curLetter == "A" or curLetter == "E" and (curLetter != 'D' or curLetter != 'B' or curLetter != 'F'):
            roll = res.random.randint(0, 100)
            if roll <= int(dungeon.cPoS.boss.chance) or curLetter == "E":
                msg += dungeon.cPoS.boss.suprise
                emojis["fight"] ='⚔'
                curLockout = User.updateLockout("E", curLockout, int(dungeon.cPoS.ID))
                curLetter = "E"
            else:
                curLockout = User.updateLockout("D", curLockout, int(dungeon.cPoS.ID))
                curLetter = "D"
        else:
            #checks for other stuff
            if dungeon.cPoS.treasure and (curLetter != "T" and curLetter != 'F'):
                emojis["treasure"] = '🎁'
            if dungeon.cPoS.interactable and (curLetter != "I" and curLetter != "B"):
                if dungeon.cPoS.interactable.restriction:
                    for i in dungeon.cPoS.interactable.restriction:
                        emojis.pop(i, None)
                emojis["interact"] = '🧩'
        userReaction, cpumsg = await addReactionsAndWaitFor(userID, message, dungeon.cPoS.name + " \n \n" + msg, 120, whom = userID, **emojis)
        if not userReaction[userID] or userReaction[userID] == "flee":
            cont = False
        elif userReaction[userID] == "fight" or userReaction[userID] == "cmode":
            if userReaction[userID] == "cmode":
                User.combat(dungeon.cPoS.boss, True)
            else:
                User.combat(dungeon.cPoS.boss, False)
            if int(User.Health) <= 0:
                cont = False
                dungeon.cPoS = dungeon.rooms[0]
                User.updateSelf("health",1)
                res.activeUsers.remove(userID)
                if userReaction[userID] == "cmode":
                    return await sendMessage(userID, message, dungeon.cPoS.boss.cmkill, True)
                else:
                    return await sendMessage(userID, message, dungeon.cPoS.boss.killquote, True)
            else:
                User.updateSelf("health",User.Health)
                expCalc = round(res.math.sqrt(int(dungeon.cPoS.boss.level)) * 5)
                expGained = User.modifyExp(expCalc,expCalc)
                goldGained = User.modifyGold(2 + int(dungeon.cPoS.boss.level), 5 + int(dungeon.cPoS.boss.level))
                cmodeloot = True if userReaction[userID] == "cmode" else False
                itemLooted = itm.Item.returnItem(None, str(dungeon.cPoS.boss.rollLoot(cmodeloot)))
                itemGained = itemLooted.ItemStringWithNewGlobalID()
                User.addToInventory(itemGained)
                if userReaction[userID] == "cmode" and dungeon.cPoS.boss.hardmodecheck(User):
                    curLockout = User.updateLockout("S", curLockout, int(dungeon.cPoS.ID))
                elif userReaction[userID] == "cmode" and not dungeon.cPoS.boss.hardmodecheck(User):
                    curLockout = User.updateLockout("C", curLockout, int(dungeon.cPoS.ID))
                elif not userReaction[userID] == "cmode" and dungeon.cPoS.boss.hardmodecheck(User):
                    curLockout = User.updateLockout("H", curLockout, int(dungeon.cPoS.ID))
                else:
                    curLockout = User.updateLockout("X", curLockout, int(dungeon.cPoS.ID))
                msg = " \n \nYou gained " + str(goldGained) + " gold and " + str(expGained) + " exp. \nYou recieved an item: " + itemLooted.returnFullItemName() + User.checkLevelUp(True)
                if userReaction[userID] == "cmode":
                    await sendMessage(userID, message, dungeon.cPoS.boss.cmdie + msg, True)
                else:
                    await sendMessage(userID, message, dungeon.cPoS.boss.diequote + msg, True)
        elif userReaction[userID] == "interact":
            if dungeon.cPoS.interactable.req(User):
                if not dungeon.cPoS.boss:
                    curLockout = User.updateLockout("I", curLockout, int(dungeon.cPoS.ID))
                else:
                    curLockout = User.updateLockout("B", curLockout, int(dungeon.cPoS.ID))
                await sendMessage(userID, message, dungeon.cPoS.interactable.success, True)
            else:
                await sendMessage(userID, message, dungeon.cPoS.interactable.failure, True)
        elif userReaction[userID] == "treasure":
            if dungeon.cPoS.treasure.req(User):
                if not dungeon.cPoS.boss:
                    curLockout = User.updateLockout("T", curLockout, int(dungeon.cPoS.ID))
                else:
                    curLockout = User.updateLockout("F", curLockout, int(dungeon.cPoS.ID))
                itemLooted = itm.Item.returnItem(None, str(dungeon.cPoS.treasure.rollLoot()))
                itemGained = itemLooted.ItemStringWithNewGlobalID()
                User.addToInventory(itemGained)
                await sendMessage(userID, message, dungeon.cPoS.treasure.success + " \nYou recieved an item: " + itemLooted.returnFullItemName(), True)
            else:
                await sendMessage(userID, message, dungeon.cPoS.treasure.failure, True)
        
        else:
            dungeon.move(userReaction[userID])
    dungeon.cPoS = dungeon.rooms[0]
    res.activeUsers.remove(userID)
    return await sendMessage(userID, message, "After contemplating for awhile, you choose to flee and live another day.", True)

def toggleUser(userID):
    User = char.Character(con.select("*","characters","ID",userID))
    User.toggleRun(userID)  