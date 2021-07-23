import Resources.imports as res
import Resources.character as char
import Resources.connection as con
import Resources.item as itm
import Resources.spells as spl
import Resources.shop as shp
import Resources.npcnames as nms
import copy

#Importing dungeons
import Resources.dungeon as dng
import Resources.dungeons.deadmines as dmvc
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
def subStringAfter(keyword, ctx):
    try:
        regexp = res.re.compile(keyword + " (.*)$")
        name = regexp.search(ctx).group(1)
        name = " ".join(name.split()).lower()
        return name
    except Exception as e:
        print (e)

def pasteModel(modelID, subfolder, canvas, offset, delete):
    if modelID == "0" or modelID.upper == "F":
        temp = res.Image.open("./Art/0.png").convert("RGBA")
    else:
        temp = res.Image.open("./Art/" + subfolder + modelID + ".png").convert("RGBA")
    canvas.paste(temp, offset, mask = temp)
    if delete and modelID != "0" and modelID.upper != "F":
        res.os.remove("./Art/" + subfolder + modelID + ".png")
async def createMessageCanvas(userID, ctx, printUser):
    #Creat the canvas
    canvas = res.Image.new('RGBA', (300,1200), (0, 0, 0, 0))
    draw = res.ImageDraw.Draw(canvas)
    heightCheck = 5
    pasteModel("messageBack", "", canvas, (0,0), False)
    if printUser:
        heightCheck = await pasteUser(userID, ctx, canvas, draw)
    return canvas, heightCheck, draw
async def pasteUser(userID, ctx, canvas, d):
    discordUser = await ctx.guild.query_members(user_ids=[userID])
    discordUser = discordUser[0]
    pfp = str(discordUser.avatar_url).replace("webp", "png")
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
    Morpheus = res.ImageFont.truetype("./Art/fonts/Cthulhumbus.ttf", 24)
    d.text((45, 10), author, fill=(255,255,255), font = Morpheus)
    heightCheck = 45
    return heightCheck
async def pasteLongText(userID, d, font, offset, msg, canvas, ctx, toSplit, defaultColor = (255,255,255)):
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
            if (width + currentWidth > 300 or "\n" in i): #Check if text is too big
                if "\n" in i:
                    i = i.replace("\n","").strip()
                    currentHeight += height
                    cumulativeHeight += height
                    currentWidth = offset[0]
                else:
                    currentHeight += height
                    cumulativeHeight += height
                    currentWidth = offset[0]
                if currentHeight >= 250 and toSplit: #If ctx file it too large
                    #Send the current file as is
                    newctx = canvas.crop((0,0,300,currentHeight + 10))
                    msgString = randomString(8)
                    imgString = msgString + ".png"
                    newctx.save(imgString, format="png")
                    await ctx.send(file=res.discord.File((imgString))), res.os.remove(imgString)

                    canvas, heightCheck, d = await createMessageCanvas(userID, ctx, False)
                    currentHeight = heightCheck + 5
            if i != "" and i != " ":
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
    im = res.Image.open('./Art/' + subfolder + race + item.ModelID + '.png')
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
    im2.save("./Art/" + subfolder + item.Name + ".png", "PNG")
    return item.Name

async def sendMessage(userID, ctx, textToSend, pasteUser, components = None):
    #Create the canvas
    canvas, heightCheck, draw = await createMessageCanvas(userID, ctx, pasteUser)

    #Paste text
    Morpheus = res.ImageFont.truetype("./Art/fonts/Cthulhumbus.ttf", 17)
    heightCheck, canvas = await pasteLongText(userID, draw, Morpheus, [5, heightCheck], textToSend, canvas, ctx, True)

    #Crop the image nicely and send it to Discord, then delete picture
    newctx = canvas.crop((0,0,300,heightCheck))
    msgString = randomString(8)
    imgString = msgString + ".png"
    newctx.save(imgString, format="png")
    if components:
        return await ctx.send(file=res.discord.File((imgString)), components = components), res.os.remove(imgString)
    else:
        return await ctx.send(file=res.discord.File((imgString))), res.os.remove(imgString)


async def createCharacter(userID, ctx):
    User = fetchUser(userID, False)
    if User.exists():
        return await sendMessage(userID, ctx, "You already have a character.", True)
    if User.isRunning(userID):
        return await sendMessage(userID, ctx, "You are doing something else.", True)
    User.toggleRun(userID)

    #Ask user to input their character's name, and wait for response.
    crudeName = await waitForMessage(userID, ctx, "Enter the name for your hero: \n \nThis name cannot contain special characters or spaces.", 30, whom = userID)
    if not crudeName[userID]:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx,"Character creation timed out.", True)
    #Filter name and make sure it's okay
    characterName = filterSpecialChars(crudeName[userID], False, True).title()
    if len(characterName) < 2:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "That name is too short.", True)
    if len(characterName) > 18:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "That name is too long.", True)
    #Checks if name is already taken
    anyOther = char.Character(con.select("*","characters","name",characterName))
    if anyOther.exists():
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "That name is already taken.", True)

    #Ask user to choose their race and wair for the resonse.
    raceChosen = await addComponentsAndWaitFor(userID, ctx, "You chose the name %PLAYER " + characterName + "). \n \nNext, choose your race: \n1: Orc \n2: Human", 30, whom=userID, comps = [
        [
            res.Button(label = "Orc", style = 4, id = "orc"),
            res.Button(label = "Human", style = 1, id = "human")
        ]
        ]
    )
    if not raceChosen[userID]:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Character creation timed out.", True)

    #Ask user to choose their class and wair for the resonse.
    if raceChosen[userID] == "orc":
        displayRace = "n orc"
    else:
        displayRace = " human"
    classChosen = await addComponentsAndWaitFor(userID, ctx, "You chose a" + displayRace + ". \n \nLastly, choose your class: \n1: Warrior \n2: Mage \n3: Rogue", 30, whom=userID, comps = [
        [
            res.Button(label = "Warrior", style = 4, id = "warrior"),
            res.Button(label = "Mage", style = 1, id = "mage"),
            res.Button(label = "Rogue", style = 2, id = "rogue")
        ]
        ])
    if not classChosen[userID]:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx,"Character creation timed out.", True)
    await sendMessage(userID, ctx, "You chose a" + displayRace + " " + classChosen[userID] + " named %PLAYER " + characterName + ").", True)
    char.Character.insertNewCharacter(char.Character.createDictionary(userID,characterName,raceChosen[userID],classChosen[userID]))
    res.activeUsers.remove(userID)
    return True
async def deleteCharacter(userID, ctx):
    if not await UserExists(userID, ctx, True, True):
        return
    User = fetchUser(userID, False)
    User.toggleRun(userID)
    #Asks user if they're sure they want to delete their account.
    #userReaction, interaction = await addComponentsAndWaitFor(userID, ctx, "Are you sure you want to delete your account, %PLAYER " + User.Name + ")? \nThis action cannot be reversed.", 5, whom = userID, comps = [res.Button(label = "I'm sure", style = 3, id = "yes"), res.Button(label = "Cancel", style = 4, id = "no")])
    userReaction = await addComponentsAndWaitFor(userID, ctx, "Are you sure you want to delete your account, %PLAYER " + User.Name + ")? \nThis action cannot be reversed.", 20, whom = userID, comps = [
        res.Select(options=[res.SelectOption(label="yes", value="yes"), res.SelectOption(label="no", value="no")]),
        [
            res.Button(label = "I'm sure", style = 3, id = "yes"),
            res.Button(label = "Cancel", style = 4, id = "no")
        ]
    ])
    #Check if it timed out or they declined
    if not userReaction[userID]:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Character deletion timed out.", True)
    if userReaction[userID] == "no":
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Character deletion cancelled.", True)

    #Delete the account.
    con.delete("Characters","ID", userID)
    res.activeUsers.remove(userID)
    await sendMessage(userID, ctx, "You have deleted your character.", True)
async def showCharacter(userID, ctx):
    #check if user is trying to show his character or someone elses,
    if len(ctx.message.content.split(" ")) == 3:
        recip = filterSpecialChars(subStringAfter("hero", ctx.message.content), False, False)
        User = char.Character(con.select("*","characters","ID",recip))
        if not await UserExists(userID, ctx, True, False):
            return await sendMessage(userID, ctx, "Player does not have a character.", True)
    else:
        User = fetchUser(userID, False)
        if not await UserExists(userID, ctx, False, True):
            return

    User.updateHealth()
    #Set some initial variables and create canvas
    heroOffSet = (37,16)
    canvas = res.Image.new('RGBA', (300,300), (0, 0, 0, 0))
    d = res.ImageDraw.Draw(canvas)
    Morpheusbig = res.ImageFont.truetype("./Art/fonts/Morpheus.ttf", 24)
    Morpheussmall = res.ImageFont.truetype("./Art/fonts/Morpheus.ttf", 19)
    BitPotion = res.ImageFont.truetype("./Art/fonts/BitPotion.ttf", 28)

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
    healthbar = res.Image.open("./Art/healthbar.png").convert("RGBA")
    expbar = res.Image.open("./Art/expbar.png").convert("RGBA")
    healthbarFrame = res.Image.open("./Art/healthBarFrame.png").convert("RGBA")

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
    await pasteLongText(userID, d, BitPotion, (((300-w)/2),(300- h - 5)), User.Health + " / " + str((int(User.Stamina) * 10)), canvas, ctx.message, False, (0,0,0))
    w, h = d.textsize(User.Exp + " / " + str(expneeded), font = BitPotion)
    await pasteLongText(userID, d, BitPotion, (((300-w)/2),(280- h - 5)), User.Exp + " / " + str(expneeded), canvas, ctx.message, False, (0,0,0))

    #Paste the name and race at the top of the screen
    w, h = d.textsize(User.Name, font = Morpheusbig)
    await pasteLongText(userID, d, Morpheusbig, (150 - (w/2),-4), "%PLAYER " + User.Name + ")", canvas, ctx.message, False, (0,0,0))
    w, h = d.textsize(User.Race.title() + " " + User.Class.title(), font = Morpheussmall)
    await pasteLongText(userID, d, Morpheussmall, (150 - (w/2), 20), User.Race.title() + " " + User.Class.title(), canvas, ctx.message, False, (0,0,0))

    #Paste the armor value and depending on class paste mainstat value
    await pasteLongText(userID, d, Morpheussmall, (2, 210), "Armor: " + User.Armor, canvas, ctx.message, False, (0,0,0))
    if User.Class == "warrior":
        await pasteLongText(userID, d, Morpheussmall, (2, 230), "Strength: " + User.Stat, canvas, ctx.message, False, (0,0,0))
    elif User.Class == "mage":
        await pasteLongText(userID, d, Morpheussmall, (2, 230), "Intellect: " + User.Stat, canvas, ctx.message, False, (0,0,0))
    elif User.Class == "rogue":
        await pasteLongText(userID, d, Morpheussmall, (2, 230), "Agility: " + User.Stat, canvas, ctx.message, False, (0,0,0))

    #Paste character level and gold amount in bottom right corner.
    w, h = d.textsize("Level: " + User.Level, font = Morpheussmall)
    await pasteLongText(userID, d, Morpheussmall, (300 - w - 5, 210), "Level: " + User.Level, canvas, ctx.message, False, (0,0,0))

    #Paste golden coin and golden numerical value in bottom right corner
    w, h = d.textsize(User.Gold + " gold", font = Morpheussmall)
    await pasteLongText(userID, d, Morpheussmall, (300 - w - 5, 230), User.Gold + " gold", canvas, ctx.message, False, (0,0,0))
    pasteModel("goldcoin", "", canvas, (300 - 29 - w,235), False)

    #Create a random string, save image, send image and delete image
    msgString = randomString(8)
    imgString = msgString + ".png"
    canvas.save(imgString, format="png")
    await ctx.send(file=res.discord.File(imgString)), res.os.remove(imgString)

async def UserExists(userID, ctx, checkRunning, sendmsg):
    User = fetchUser(userID, False)
    if checkRunning and User.isRunning(userID):
        if sendmsg:
            await sendMessage(userID, ctx,"You are doing something else.", True)
        return False
    if not User.exists():
        if sendmsg:
            await sendMessage(userID, ctx, "You do not have a character.", True)
        res.activeUsers.remove(userID)
        return False
    return True

async def equip(userID, ctx):
    if not await UserExists(userID, ctx, True, True):
        return
    User = fetchUser(userID, False)
    User.toggleRun(userID)
    if not len(ctx.message.content.split(" ")) >= 3:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Type which item you'd like to equip.", True)
    itemName = filterSpecialChars(subStringAfter("equip", ctx.message.content), True, False)
    checkItem = itm.Item.returnItem(itemName)
    if not checkItem.ID:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Item does not exist.", True)
    item = await showAllUniqueInInventory(userID, ctx, itemName, "Which one would you like to equip?")
    if item == None:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Equipping timed out.", True)
    print(item)
    equipped, msg = User.equip(item)
    if equipped:
        await showCharacter(userID, ctx)
    res.activeUsers.remove(userID)
    await sendMessage(userID, ctx, msg, True)
async def unequip(userID, ctx):
    if not await UserExists(userID, ctx, True, True):
        return
    User = fetchUser(userID, False)
    User.toggleRun(userID)
    if not len(ctx.message.content.split(" ")) >= 3:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Type which item you'd like to unequip.", True)
    itemName = filterSpecialChars(subStringAfter("unequip", ctx.message.content), True, False)
    checkItem = itm.Item.returnItem(itemName)
    if not checkItem.ID:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Item does not exist.", True)
    item = itm.Item.returnItem(itemName)
    itemString = item.returnItemString()
    unequipped, msg = User.unequip(itemString.split("-"))
    if unequipped:
        await showCharacter(userID, ctx)
    res.activeUsers.remove(userID)
    await sendMessage(userID, ctx, msg, True)
async def sell(userID, ctx):
    if not await UserExists(userID, ctx, True, True):
        res.activeUsers.remove(userID)
        return
    User = fetchUser(userID, False)
    User.toggleRun(userID)
    if not len(ctx.message.content.split(" ")) >= 3:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Type which item you'd like to sell.", True)
    itemName = filterSpecialChars(subStringAfter("sell", ctx.message.content), True, False)
    checkItem = itm.Item.returnItem(itemName)
    if not checkItem.ID:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Item does not exist.", True)
    item = await showAllUniqueInInventory(userID, ctx, itemName, "Which one would you like to sell?")
    if item == None:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Selling timed out.", True)
    sold, msg = User.sell(item)

    res.activeUsers.remove(userID)
    await sendMessage(userID, ctx, msg, True)
async def use(userID, ctx):
    if not await UserExists(userID, ctx, True, True):
        res.activeUsers.remove(userID)
        return
    User = fetchUser(userID, False)
    User.toggleRun(userID)
    if not len(ctx.message.content.split(" ")) >= 3:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Type which item you'd like to use.", True)
    itemName = filterSpecialChars(subStringAfter("use", ctx.message.content), True, False)
    itemQueried = itm.Item.returnItem(itemName)
    if not itemQueried.ID:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Item does not exist.", True)
    if itemQueried.Slot:
        item = User.checkIfWearingItem(itemQueried)
        if not item:
            res.activeUsers.remove(userID)
            return await sendMessage(userID, ctx, "Item not found equipped.", True)
        item = item.split("-")
    else:
        item = await showAllUniqueInInventory(userID, ctx, itemName, "Which one would you like to use?")
    if not item:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Using timed out.", True)
    used, msg = User.use(item)
    res.activeUsers.remove(userID)
    await sendMessage(userID, ctx, msg, True)


async def train(userID, ctx):
    if not await UserExists(userID, ctx, True, True):
        res.activeUsers.remove(userID)
        return
    User = fetchUser(userID, True)
    class Mobs:
        ()
    Mob = Mobs
    response = {}
    response = await addComponentsAndWaitFor(userID, ctx, "Would you like to begin combat?", 30, components=[
        [
            res.Button(label = "Begin combat", style = 3, id = "yes"),
            res.Button(label = "Rest", style = 4, id = "no")
        ]
    ])
    while response[userID] == "yes":
        if response[userID] != "yes":
            res.activeUsers.remove(userID)
            return await sendMessage(userID, ctx, "You choose to rest and train another day.", True)
        Mob.name = nms.randomNPCName()
        Mob.level = max(1, res.random.randint(int(User.Level) - 1, int(User.Level) + 1))
        Mob.health = 40 + (10 * int(Mob.level)) * ((.1 * Mob.level) + 1)
        Mob.maxHealth = Mob.health
        Mob.damage = [round(((.1 * Mob.level) + 1) * (9 + (9 * .1 * res.math.sqrt(Mob.level)))),round(((.1 * Mob.level) + 1)*(14 + (14 * .1 * res.math.sqrt(Mob.level))))]
        success, Mob = await combat(userID, ctx, Mob)
        User = fetchUser(userID, False)
        if not success and int(User.Health) <= 1:
            res.activeUsers.remove(userID)
            return await sendMessage(userID, ctx, "Try as you might, you were no match for " + Mob.name + ". \n \nRest up and train again!", True)
        elif not success:
            cont = False
            break
        exp, gold, dinged = User.trainRewards(Mob)
        response = await addComponentsAndWaitFor(userID, ctx, "You succesfully killed " + Mob.name + ", gaining " + gold + " gold and " + exp + "exp." + dinged + " \nNow standing at " + User.Health + " health, would you like to train some more?", 30, components=[
            [
                res.Button(label = "Continue", style = 3, id = "yes"),
                res.Button(label = "Rest", style = 4, id = "no")
            ]
        ])
    res.activeUsers.remove(userID)
    return await sendMessage(userID, ctx, "You choose to rest and train another day.", True)

async def combatMessage(userID, ctx, Mob, combattext, components):
    canvas, heightCheck, draw = await createMessageCanvas(userID, ctx, False)
    User = fetchUser(userID, False)
    #Paste text
    Morpheus = res.ImageFont.truetype("./Art/fonts/Cthulhumbus.ttf", 17)
    healthbar = res.Image.open("./Art/healthbar.png").convert("RGBA")
    healthbarFrame = res.Image.open("./Art/whitehealthBarFrame.png").convert("RGBA")
    BitPotion = res.ImageFont.truetype("./Art/fonts/BitPotion.ttf", 28)
    w, h = draw.textsize(User.Name, font = Morpheus)
    heightCheck, canvas = await pasteLongText(userID, draw, Morpheus, [150-(w/2), heightCheck], "%PLAYER " + User.Name + ")", canvas, ctx, True)
    remainingHealth = int((int(User.Health)/(int(User.Stamina) * 10)) * 300)
    ActualHealthBar = healthbar.crop((0,0,remainingHealth,26))
    canvas.paste(ActualHealthBar, (0, heightCheck), mask=ActualHealthBar)
    canvas.paste(healthbarFrame, (0, heightCheck), mask=healthbarFrame)
    w, h = draw.textsize(User.Health + " / " + str((int(User.Stamina) * 10)), font = BitPotion)
    await pasteLongText(userID, draw, BitPotion, (150 - (w/2),heightCheck - 1), User.Health + " / " + str((int(User.Stamina) * 10)), canvas, ctx.message, False, (255,255,255))
    heightCheck += 30
    w, h = draw.textsize("VS.", font = Morpheus)
    heightCheck, canvas = await pasteLongText(userID, draw, Morpheus, [150-(w/2), heightCheck], "VS.", canvas, ctx, True)
    w, h = draw.textsize(Mob.name.split("%BOSS")[1].split(" )")[0], font = Morpheus)
    heightCheck, canvas = await pasteLongText(userID, draw, Morpheus, [150-(w/2), heightCheck], Mob.name, canvas, ctx, True)
    remainingHealth = int((int(Mob.health)/(int(Mob.maxHealth))) * 300)
    ActualHealthBar = healthbar.crop((0,0,remainingHealth,26))
    canvas.paste(ActualHealthBar, (0, heightCheck), mask=ActualHealthBar)
    canvas.paste(healthbarFrame, (0, heightCheck), mask=healthbarFrame)
    w, h = draw.textsize(str(int(Mob.health)) + " / " + str(int(Mob.maxHealth)), font = BitPotion)
    await pasteLongText(userID, draw, BitPotion, (150 - (w/2),heightCheck - 1), str(int(Mob.health)) + " / " + str(int(Mob.maxHealth)), canvas, ctx.message, False, (255,255,255))
    heightCheck += 30
    

    

    
    heightCheck, canvas = await pasteLongText(userID, draw, Morpheus, [5, heightCheck], combattext, canvas, ctx, True)

    #Crop the image nicely and send it to Discord, then delete picture
    newctx = canvas.crop((0,0,300,heightCheck))
    msgString = randomString(8)
    imgString = msgString + ".png"
    newctx.save(imgString, format="png")
    if components:
        return await ctx.send(file=res.discord.File((imgString)), components = components), res.os.remove(imgString)
    else:
        return await ctx.send(file=res.discord.File((imgString))), res.os.remove(imgString)
async def addCombatComponentsAndWaitFor(userID, ctx, Mob, msgtosend, timeouts, **kwargs):
    labelToHold = {}
    components = []
    def Check(userID, response, label):
        usersReactions[userID] = response
        labelToHold["label"] = label.label
        if hasattr(label, "id"):
            labelToHold["label"] = ""
        for k in usersReactions:
            if not usersReactions[k]:
                return False
        return True
    usersReactions = {}
    for key, value in kwargs.items():
        if "whom" in key:
            usersReactions[value] = None
        else:
            components.append(value)
    msg, _ = await combatMessage(userID, ctx, Mob, msgtosend, components[0])
    try:
        done, pending = await res.asyncio.wait([
            res.bot.wait_for('select_option', check = lambda i: Check(str(i.user.id), i.component[0].value, i.component[0])),
            res.bot.wait_for('button_click', check = lambda i: Check(str(i.user.id), i.component.id, i.component))
        ], return_when=res.asyncio.FIRST_COMPLETED, timeout=timeouts)
        for task in done:
            interaction = task.result()
        for i in components[0]:
            for x in i:
                x.disabled = True
                if labelToHold["label"]:
                    x.placeholder = labelToHold["label"]
        await interaction.respond(type=7, components = components[0])
    except:
        for i in components[0]:
            for x in i:
                x.disabled = True
                x.placeholder = ""
        await msg.edit(components = components[0])

    return usersReactions

async def combat(userID, ctx, Mob):
    User = fetchUser(userID, False)
    cont = True
    User.procs = []
    User.onhits = []
    User.stunned = True
    User.toggleRun(userID)
    Mob = Mob
    mesg = ""
    while cont:
        mesg += " \nPick your action."
        opts = []
        i = 0
        while i < 24:
            opts.append(res.SelectOption(label=i, value=i))
            i+=1
        #Create items options:
        itemsList = []
        for i in User.returnEquipment():
            if i.split("-")[4] != "F":
                for x in i.split("-")[4].split("&"):
                    spell = spl.Spell.findByID(x)
                    if spell and spell.Type == "active":
                        item = itm.Item.returnItem(None, i.split("-")[1])
                        itemsList.append(res.SelectOption(label=item.Name, value = "item-" + i.split("-")[0].strip(), description=spell.Name))
                    elif spell and spell.Type == "proc":
                        User.procs.append(spell)
                    elif spell and spell.Type == "onhit":
                        User.onhits.append(spell)
        for i in User.Inventory.split(","):
            split = i.split("-")
            if len(split) > 1:
                item = itm.Item.returnItem(None, split[1])
                if not item.Slot and split[4] != "F":
                    msg = ""
                    for x in split[4].split("&"):
                        spell = spl.Spell.findByID(x)
                        if spell:
                            if spell.Type == "active":
                                msg += spell.Name + ", "
                    if msg:
                        itemsList.append(res.SelectOption(label=item.Name, value = "item-" + split[0].strip(), description=msg[0:-2]))
        noItems = [res.SelectOption(label = "No items found", value = "doesntmatter")]
        response = await addCombatComponentsAndWaitFor(userID, ctx, Mob, mesg, 30, whom = userID, comps = [
            [
                res.Select(options = itemsList if itemsList else noItems, placeholder='Items' if itemsList else "No items found", disabled = False if itemsList else True)
            ],
            [
                res.Button(label = "Attack", style = 4, id = "attack"),
                res.Button(label = "Flee", style = 1, id = "flee"),
            ]
        ])
        if response[userID] == "attack":
            dmgDealt = User.calculateDamagedealt(Mob)
            mesg = " \nYou dealt " + str(dmgDealt) + " damage."
            Mob.health -= dmgDealt
        elif response[userID] == "flee":
            return False, Mob
        elif response[userID]:
            splitR = response[userID].split("-")
            if "item" in splitR:
                itemString = User.findByGlobalID(splitR[1])
                success, typemsg = User.use(itemString.split("-"))
                mesg = typemsg + " \n"
        else:
            cont = False
        if Mob.health < 0:
            cont = False
            break
        dmgTaken, onhits = User.calculateDamageTaken(Mob)
        User.modifyHealth(-dmgTaken, -dmgTaken)
        if int(User.Health) <= 0:
            cont = False
        mesg += " \n \nYou get hit for " + str(dmgTaken) + " damage."
        mesg += onhits
    if int(User.Health) <= 0:
        User.updateHealth()
        User.updateSelf("Health", "1")
        return False, Mob
    else:
        return True, Mob


async def inspect(userID, ctx):
    userid = None
    if len(ctx.message.content.split(" ")) >= 3:
        userid = filterSpecialChars(subStringAfter("inspect", ctx.message.content), False, False)
    else:
        userid = userID
    if not await UserExists(userid, ctx, False, False):
        if len(ctx.message.content.split(" ")) >= 3:
            return await sendMessage(userID, ctx, "That user does not have a character.", True)
        else:
            return await sendMessage(userID, ctx, "You do not have a character.", True)
    User = fetchUser(userID, False)
    msg = User.Name + " is wearing: \n"
    msg += User.inspect()
    return await sendMessage(userID, ctx, msg, True)

async def getResources(userID, ctx):
    if not await UserExists(userID, ctx, True, True):
        return
    if not len(ctx.message.content.split(" ")) >= 3:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "Type which resource you'd like to gather.", True)
    User = fetchUser(userID, True)
    type = "ore"
    if User.Class == "mage":
        type = "cloth"
    elif User.Class == "rogue":
        type = "leather"
    fullresource = filterSpecialChars(subStringAfter("gather", ctx.message.content), True, False).lower()
    splitresource = fullresource.split(" ")
    resource = splitresource[0]
    intendedType = splitresource[1]
    if not type == intendedType:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "You cannot gather that resource type.", True)
    cont = False
    for i in User.Resources.split(","):
        split = i.split("-")
        if split[0] == resource:
            cont = True
    if not cont:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "You cannot gather that resource.", True)
    while cont:
        listOfResources = User.Resources.split(",")
        healthLost = 10
        for i in range(len(listOfResources)):
            if resource in listOfResources[i]:
                healthLost *= (i+1)
                healthLost /= 10
                x = listOfResources[i]
                x = x.split("-")
                resource = x[0]
                x[1] = str(int(x[1]) + 1)
                listOfResources[i] = "-".join(x)
        resources = ",".join(listOfResources)
        healthLostNum = int(User.Stamina) * healthLost
        newHealth = int(User.Health) - int(healthLostNum)
        if newHealth <= 0:
            res.activeUsers.remove(userID)
            newHealth = "1"
            User.updateSelf("health", newHealth)
            return await sendMessage(userID, ctx, "You were too weary when you started and collapsed before being able to gather " + resource + ". \n \nRest up and try again.", True)
        User.updateSelf("resources", resources)
        User.updateSelf("health", str(int(float(newHealth))))
        
        reaction, cpumsg = await addComponentsAndWaitFor(userID, ctx, "You succesfully gathered 1 " + resource + " " + type + ", but were attacked and lost " + str(int(float(healthLostNum))) + " health in the process. \n \nWould you like to gather another or rest?", 30, whom = userID, comps = [
            [
                res.Button(label = "Keep Gathering!", style = 1, id = "yes"),
                res.Button(label = "Rest.", style = 1, id = "no")
            ]
        ])
        if not reaction[userID] or reaction[userID] == "no":
            cont = False
            res.activeUsers.remove(userID)
            await sendMessage(userID, ctx, "You chose to rest and gather another day another day.", True)
        else:
            await cpumsg.delete()
async def showResources(userID, ctx):
    if not await UserExists(userID, ctx, True, True):
        return
    msg = "Your resources: \n "
    User = fetchUser(userID, False)
    listOfResources = User.Resources.split(",")
    if User.Resources.count("0") == 4:
        return await sendMessage(userID, ctx, "You do not have any resources. Go ahead and gather some!", True)
    for i in listOfResources:
        x = i.split("-")
        if x[1] != "0":
            msg += " \n" + x[0].title() + ": " + x[1]
    await sendMessage(userID, ctx, msg, True)





async def queryItem(userID, ctx):
    if not len(ctx.message.content.split(" ")) >= 3:
        return await sendMessage(userID, ctx, "Type which item you'd like to see.", True)
    if await UserExists(userID, ctx, False, False):
        User = fetchUser(userID, False)
        race = User.Race
    else:
        race = "orc"
    itemName = filterSpecialChars(subStringAfter("item", ctx.message.content), True, False)
    item = itm.Item.returnItem(itemName)
    if not item.exists():
        return await sendMessage(userID, ctx, "Item does not exist.", True)
    #Check if user has it in bag
    itemString = ""
    if await UserExists(userID, ctx, False, False):
        User = fetchUser(userID, False)
        if item.Slot:
            if User.checkIfWearingItem(item):
                itemString = getattr(User, item.Slot)
            elif User.checkIfHasItem(item):
                itemString = User.checkIfHasItem()[0]
            else:
                itemString = item.returnItemString()
        else:
            itemString = item.returnItemString()
    else:
        itemString = item.returnItemString()
    await showItemData(userID, ctx, itemString)
    itemStringSplit = itemString.split("-")
    if itemStringSplit[2] != "F" and item.Slot and item.Type:
        canvas = res.Image.new('RGBA', (300,300), (0, 0, 0, 0))
        #Paste backround and race
        pasteModel("white", "", canvas, (0,0), False)
        pasteModel(race, "", canvas, (37, 16), False)
        if item.ShowHair != "no":
            pasteModel(race + "Hair", "", canvas, (37, 16), False)
        #Start pasting equipment
        if item.Slot and item.Slot.lower() == "mainhand":
            pasteModel(fetchColoredModel(itemStringSplit[2], "", item.Slot.capitalize() + "/"), item.Slot.capitalize() + "/", canvas, (37, 16), True)
        else:
            pasteModel(fetchColoredModel(itemStringSplit[2], race, item.Slot.capitalize() + "/"), item.Slot.capitalize() + "/", canvas, (37, 16), True)
        msgString = randomString(8)
        imgString = msgString + ".png"
        canvas.save(imgString, format="png")
        await ctx.channel.send(file=res.discord.File((imgString))), res.os.remove(imgString)

async def showItemData(userID, ctx, itemString):
    #Check if the item exists.
    itemSegments = itemString.split("-")
    item = itm.Item.returnItem(None, itemSegments[1])
    Morpheusbig = res.ImageFont.truetype("./Art/fonts/Morpheus.ttf", 24)
    Morpheussmall = res.ImageFont.truetype("./Art/fonts/Morpheus.ttf", 19)
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
        heightCheck, canvas = await pasteLongText(userID, d, Morpheusbig, (10, heightCheck), name, canvas, ctx, True)
    else:
        heightCheck, canvas = await pasteLongText(userID, d, Morpheusbig, (150 - (w/2), heightCheck), name, canvas, ctx, False)
    
    #Binding properties of item and transmog:
    if itemSegments[1] != itemSegments[2] and item.Slot and itemSegments[2] != "F":
        itemsApperance = itm.Item.returnItem(None, itemSegments[2])
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Transmogrified to: [" + itemsApperance.Name + "]", canvas, ctx, True, (231, 43, 237))
        del itemsApperance
    if itemSegments[3] != "F":
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), itemSegments[3], canvas, ctx, True, (255,255,255))

    #Slot item goes into (if armor):
    if item.Slot and item.Type:
        noVal, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Slot, canvas, ctx, True, (255,255,255))
        w, h = d.textsize(item.Type, font = Morpheussmall)
        del noVal
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (300 - 7 - w, heightCheck), item.Type, canvas, ctx, True, (255,255,255))
    elif item.Slot and item.Type == None:
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Slot, canvas, ctx, True, (255,255,255))
    if item.Damage:
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Damage + " Damage", canvas, ctx, True, (255,255,255))
    if item.Armor != "0":
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Armor + " Armor", canvas, ctx, True, (255,255,255))
    if item.Stamina != "0":
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stamina + " Stamina", canvas, ctx, True, (20, 255, 20))
    if item.Stat != "0":
        if item.Type.lower() == "mail" or item.Type.lower() == "sword" or item.Type.lower() == "shield" or item.Type.lower() == "axe" or item.Type.lower() == "mace":
            heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stat + " Strength", canvas, ctx, True, (20, 255, 20))
        if item.Type.lower() == "cloth" or item.Type.lower() == "staff":
            heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stat + " Intellect", canvas, ctx, True, (20, 255, 20))
        if item.Type.lower() == "leather" or item.Type.lower() == "dagger":
            heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stat + " Agility", canvas, ctx, True, (20, 255, 20))
    
    if item.Level and item.Level != "F":
        color = (255,255,255)
        User = fetchUser(userID, False)
        if User.exists():
            color = (255,255,255)
            if item.Level > User.Level:
                color = (255,30,30)
        else:
            color = (255,255,255)
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Requires level: " + item.Level, canvas, ctx, False, color)
    
    if itemSegments[4] != "F":
        spellSplit = itemSegments[4].split("&")
        if "" in spellSplit:
            spellSplit.remove("")
        for i in spellSplit:
            spell = spl.Spell.findByID(i)
            if spell.Type == "active":
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Use: " + spell.Description + " %ITEM255,255,255 " + spell.Name, canvas, ctx, False, (30,255,0))
            elif spell.Type == "proc":
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "On Hit: " + spell.Description + " %ITEM255,255,255 " + spell.Name, canvas, ctx, False, (30,255,0))
            else:
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Equipped: " + spell.Description + " %ITEM255,255,255 " + spell.Name, canvas, ctx, False, (30,255,0))

    """ if itemSegments[4] != "F":
        spellSplit = itemSegments[4].split("&")
        if "" in spellSplit:
            spellSplit.remove("")
        for i in spellSplit:
            spell = spl.Spell.findByID(i)
            if spell.Type == "active":
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), spell.Name, canvas, ctx, False, (255,255,255))
            elif spell.Type == "proc":
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), spell.Name, canvas, ctx, False, (255,255,255))
            else:
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), spell.Name, canvas, ctx, False, (255,255,255)) """



    if itemSegments[5] != "F":
        if int(itemSegments[5]) > 1:
            heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), itemSegments[5] + " Charges", canvas, ctx, False, (255,255,255))
        else:
            heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), itemSegments[5] + " Charge", canvas, ctx, False, (255,255,255))
    
    
    if item.Flavor:
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Flavor, canvas, ctx, False, (251, 203, 2))
    if item.Value:
        w, h = d.textsize("Sell value: " + item.Value, Morpheussmall)
        pasteModel("goldcoin", "", canvas, (10+w, heightCheck+7), False)
        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Sell value: " + item.Value, canvas, ctx, False, (255,255,255))
    pasteModel("topandbot", "", canvas, (0, heightCheck + 2), False)
    newItem = canvas.crop((0,0,300,heightCheck + 7))
    msgString = randomString(8)
    itemString = msgString + ".png"
    newItem.save(itemString, format="png")
    await ctx.channel.send(file=res.discord.File((itemString))), res.os.remove(itemString)
    return itemSegments[0]
    

def returnAllInstancesOfItem(User, itemName):
    item = itm.Item.returnItem(itemName)
    allItemsFound = []
    inBag = User.checkIfHasItem(item)
    if inBag:
        for i in inBag:
            allItemsFound.append(i)
    return allItemsFound
    
async def showAllUniqueInInventory(userID, ctx, itemName, msgToSend):
    User = fetchUser(userID, False)
    ifExists = itm.Item.returnItem(itemName)
    if not ifExists.exists():
        return await sendMessage(userID, ctx, "Item does not exist.", True)
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
    compss = []
    for i in itemsFound:
        item = itm.Item.returnItem(None, i[1])
        print (item.Name)
        desc = ""
        for x in i[4].split("&"):
            spell = spl.Spell.findByID(x)
            desc += spell.Name + ", "
        desc = desc[0:-2]
        compss.append(res.SelectOption(label = item.Name, value = i[0], description=desc))
        print (compss)
        await showItemData(userID, ctx, "-".join(i))
    reaction = await addComponentsAndWaitFor(userID, ctx, msgToSend, 10, whom = userID, comps = [res.Select(options=compss)])
    if not reaction[userID]:
        return None
    for i in itemsFound:
        if i[0] == reaction[userID]:
            return i
    






async def craftItem(userID, ctx):
    if not await UserExists(userID, ctx, True, True):
        return
    User = fetchUser(userID, False)
    if not len(ctx.message.content.split(" ")) >= 3:
        return await sendMessage(userID, ctx, "Type which item you'd like to craft.", True)
    itemName = filterSpecialChars(subStringAfter("craft", ctx.message.content), True, False)
    item = itm.Item.returnItem(itemName)
    if not item.exists():
        return await sendMessage(userID, ctx, "Item does not exist.", True)
    if item.Reagents == None:
        return await sendMessage(userID, ctx, "That item cannot be crafted.", True)
    for i in item.Reagents.split(","):
        if "" != i:
            ii = i.split("-")
            if ii[1] not in User.Resources:
                return await sendMessage(userID, ctx, "That item cannot be crafted by your class.", True)
            else:
                for x in User.Resources.split(","):
                    xx = x.split("-")

                    if xx[0] == ii[1]:
                        if int(ii[0]) > int(xx[1]):
                            return await sendMessage(userID, ctx, "You do not have enough " + xx[0] + " to craft that.", True)
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
    return await sendMessage(userID, ctx, "You succesfully crafted: " + item.returnFullItemName() + ".", True)


async def showInventory(userID, ctx):
    if not await UserExists(userID, ctx, True, True):
        return
    User = fetchUser(userID, False)
    if User.Inventory == "" or User.Inventory == ",":
        return await sendMessage(userID, ctx, "Your inventory is empty.", True)
    msg = "Your inventory:"
    for i in User.Inventory.split(","):
        if "" != i:
            x = i.split("-")
            item = itm.Item.returnItem(None, x[1])
            msg += " \n- " + item.returnFullItemName()
    return await sendMessage(userID, ctx, msg, True)


async def showFullInventory(userID, ctx):
    if not await UserExists(userID, ctx, True, True):
        return
    User = fetchUser(userID, False)
    if User.Inventory == "" or User.Inventory == ",":
        return await sendMessage(userID, ctx, "Your inventory is empty.", True)

    totalHeight = 0
    bigCanvas = res.Image.new('RGBA', (300,100000), (0, 0, 0, 0))

    for i in User.Inventory.split(","):
        if "" != i:
            itemSegments = i.split("-")
            item = itm.Item.returnItem(None, itemSegments[1])
            Morpheusbig = res.ImageFont.truetype("./Art/fonts/Morpheus.ttf", 24)
            Morpheussmall = res.ImageFont.truetype("./Art/fonts/Morpheus.ttf", 19)
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
                heightCheck, canvas = await pasteLongText(userID, d, Morpheusbig, (10, heightCheck), name, canvas, ctx, True)
            else:
                heightCheck, canvas = await pasteLongText(userID, d, Morpheusbig, (150 - (w/2), heightCheck), name, canvas, ctx, False)
            
            #Binding properties of item and transmog:
            if itemSegments[1] != itemSegments[2]:
                itemsApperance = itm.Item.returnItem(None, itemSegments[2])
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Transmogrified to: [" + itemsApperance.Name + "]", canvas, ctx, True, (231, 43, 237))
                del itemsApperance
            if itemSegments[3] != "F":
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), itemSegments[3], canvas, ctx, True, (255,255,255))

            #Slot item goes into (if armor):
            if item.Slot and item.Type:
                noVal, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Slot, canvas, ctx, True, (255,255,255))
                w, h = d.textsize(item.Type, font = Morpheussmall)
                del noVal
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (300 - 7 - w, heightCheck), item.Type, canvas, ctx, True, (255,255,255))
            elif item.Slot and not item.Type:
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Slot, canvas, ctx, True, (255,255,255))
            if item.Damage:
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Damage + " Damage", canvas, ctx, True, (255,255,255))
            if item.Armor != "0":
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Armor + " Armor", canvas, ctx, True, (255,255,255))
            if item.Stamina != "0":
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stamina + " Stamina", canvas, ctx, True, (20, 255, 20))
            if item.Stat != "0":
                if item.Type.lower() == "mail" or item.Type.lower() == "sword" or item.Type.lower() == "shield" or item.Type.lower() == "axe" or item.Type.lower() == "mace":
                    heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stat + " Strength", canvas, ctx, True, (20, 255, 20))
                if item.Type.lower() == "cloth" or item.Type.lower() == "staff":
                    heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stat + " Intellect", canvas, ctx, True, (20, 255, 20))
                if item.Type.lower() == "leather" or item.Type.lower() == "dagger":
                    heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "+ " + item.Stat + " Agility", canvas, ctx, True, (20, 255, 20))
            
            if item.Level and item.Level != "F":
                color = (255,255,255)
                User = fetchUser(userID, False)
                if User.exists():
                    color = (255,255,255)
                    if item.Level > User.Level:
                        color = (255,30,30)
                else:
                    color = (255,255,255)
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Requires level: " + item.Level, canvas, ctx, False, color)
            
            if itemSegments[4] != "F":
                spellSplit = itemSegments[4].split("&")
                if "" in spellSplit:
                    spellSplit.remove("")
                for i in spellSplit:
                    spell = spl.Spell.findByID(i)
                    if spell.Type == "active":
                        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Use: " + spell.Description, canvas, ctx, True, (30,255,0))
                    elif spell.Type == "proc":
                        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "On Hit: " + spell.Description, canvas, ctx, True, (30,255,0))
                    else:
                        heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Equipped: " + spell.Description, canvas, ctx, True, (30,255,0))

            if itemSegments[5] != "F":
                if int(itemSegments[5]) > 1:
                    heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), itemSegments[6] + " Charges", canvas, ctx, True, (255,255,255))
                else:
                    heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), itemSegments[6] + " Charge", canvas, ctx, True, (255,255,255))
            if item.Flavor:
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), item.Flavor, canvas, ctx, True, (120,120,120))
            if item.Value:
                w, h = d.textsize("Sell value: " + item.Value, Morpheussmall)
                pasteModel("goldcoin", "", canvas, (10+w, heightCheck+7), False)
                heightCheck, canvas = await pasteLongText(userID, d, Morpheussmall, (7, heightCheck), "Sell value: " + item.Value, canvas, ctx, True, (255,255,255))
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
    await ctx.channel.send(file=res.discord.File((itemString))), res.os.remove(itemString)
    return await sendMessage(userID, ctx, "If the picture seems too small, open it in your browser.", True)


def fetchUser(userID, toggleRun):
    User = char.Character(con.select("*","characters","ID",userID))
    if User.Health:
        User.updateHealth()
    if toggleRun:
        User.toggleRun(userID)
    return User




#Define 2 specific functions for these 2 operation to work
def updateDict(dict, key, value):
    dict[key] = value
    return True
def checkAllVoted(dicts):
    for i in dicts.values():
        if i == None:
            return False
    return True
#Sends a ctx using sendMessage, adds specified emojis and waits for specified user(s) to respond. Returns a dict with user(s) and their reaction(s)
async def addComponentsAndWaitFor(userID, ctx, msgToSend, timeouts, **kwargs):
    labelToHold = {}
    components = []
    def Check(userID, response, label):
        usersReactions[userID] = response
        labelToHold["label"] = label.label
        if hasattr(label, "id"):
            labelToHold["label"] = ""
        for k in usersReactions:
            if not usersReactions[k]:
                return False
        return True
    usersReactions = {}
    for key, value in kwargs.items():
        if "whom" in key:
            usersReactions[value] = None
        else:
            components.append(value)
    msg, _ = await sendMessage(userID, ctx, msgToSend, True, components[0])
    try:
        done, pending = await res.asyncio.wait([
            res.bot.wait_for('select_option', check = lambda i: Check(str(i.user.id), i.component[0].value, i.component[0])),
            res.bot.wait_for('button_click', check = lambda i: Check(str(i.user.id), i.component.id, i.component))
        ], return_when=res.asyncio.FIRST_COMPLETED, timeout=timeouts)
        for task in done:
            interaction = task.result()
        for i in components[0]:
            for x in i:
                x.disabled = True
                if labelToHold["label"]:
                    x.placeholder = labelToHold["label"]
        await interaction.respond(type=7, components = components[0])
    except:
        for i in components[0]:
            for x in i:
                x.disabled = True
                x.placeholder = ""
        await msg.edit(components = components[0])

    return usersReactions
    


#Sends a ctx using sendMessage and waits for specified user(s) to respond.
async def waitForMessage(userID, ctx, msgToSend, timeouts, **kwargs):
    await sendMessage(userID, ctx, msgToSend, True)
    users = []
    usersreactions = {}
    for key, value in kwargs.items():
        if "whom" in key:
            users.append(value)
            usersreactions[value] = None
    try:
        await res.bot.wait_for('message', timeout=timeouts, check=lambda user: str(user.author.id) in users and updateDict(usersreactions, str(user.author.id), str(user.content)) and checkAllVoted(usersreactions))
    except:
        pass
    return usersreactions

async def shop(userID, ctx):
    if not await UserExists(userID, ctx, True, True):
        return
    if not len(ctx.message.content.split(" ")) >= 3:
        return await sendMessage(userID, ctx, "Type which shop you'd like to browse.", True)
    User = fetchUser(userID, False)
    shopName = filterSpecialChars(subStringAfter("shop", ctx.message.content), True, False)
    Shop = shp.Shop.findShop(shopName)
    if not Shop:
        return await sendMessage(userID, ctx, "That shop does not exist", True)
    User.toggleRun(userID)
    await sendMessage(userID, ctx, Shop.Dialogue, True)

    comps = []
    #Shop display
    msg = ""
    itemAndEmoji = {}
    for i in range(len(Shop.Items)):
        item = itm.Item.returnItem(None, str(Shop.Items[i]))
        comps.append(res.Button(label = item.Name, id = str(i), style = 3))
        msg += item.returnFullItemName() + " \nCost: " + str(Shop.Prices[i]) + " \n \n"
    comps.append(res.Button(label = "Leave", id = "exit", style = 4))
    msg = msg[:-4]
    reaction = await addComponentsAndWaitFor(userID, ctx, msg, 40, whom = userID, comps = comps)
    if not reaction[userID] or reaction[userID] == "exit":
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, Shop.Bye, True)
    index = int(reaction[userID])

    item = itm.Item.returnItem(None, str(Shop.Items[index]))
    price = Shop.Prices[index]
    if int(User.Gold) < price:
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, Shop.Poor, True)
    User.modifyGold(-price, -price)
    User.addToInventory(item.ItemStringWithNewGlobalID())
    res.activeUsers.remove(userID)
    return await sendMessage(userID, ctx, Shop.Thank + " \n \nYou bought: " + item.returnFullItemName(), True)

#Dungeon Stuff
async def runDungeon(userID, ctx):
    if not await UserExists(userID, ctx, True, True):
        return
    if not len(ctx.message.content.split(" ")) >= 3:
        return await sendMessage(userID, ctx, "Type which dungeon you'd like to run.", True) 
    cont = True
    User = fetchUser(userID, True)
    dungeon = []
    curLockout = ""
    nameOfDungeon = filterSpecialChars(subStringAfter("run", ctx.message.content), True, False)
    if nameOfDungeon == "deadmines":
        dungeon = dng.Dungeon([
            dmvc.room1, dmvc.room2, dmvc.room3, dmvc.room4, dmvc.room5, dmvc.room6, dmvc.room7, dmvc.room8, dmvc.room9, dmvc.room10, dmvc.room11, dmvc.room12
        ],{
            "intro":"You\'ve reached the entrance to The Deadmines, do you wish to enter or flee?",
            "attunefail":"You try to open the door, but no matter how hard you try, the door will not budge. It\'s locked, and the key is nowhere in sight. \n \nOut of the corner of your eye, you catch a glimpse of a merchant, skulking around. \n%NPC Defias Profiteer): ‘Trying to get in there, are we? Not without this here key. You want it? Pay up.’ \n \nYou can view what the merchant sells by typing \'Mega Shop Deadmines\'.",
            "hardmodecheck": dmvc.hardMode
        })
        lister = User.Lockouts.split(",")
        for i in lister:
            if "DMVC" in i:
                curLockout = i
    else:
        return await sendMessage(userID, ctx, "That dungeon doesn't exist.", True)
    User.toggleRun(userID)

    userReaction = await addComponentsAndWaitFor(userID, ctx, dungeon.intro, 60, whom = userID, comps=[
        [
            res.Button(label = "Enter dungeon", id = "fight", style = 4),
            res.Button(label = "Flee", id = "flee", style = 1),
        ]
    ])
    if not userReaction[userID] or userReaction[userID] == "flee":
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, "After contemplating for awhile, you choose to flee and live another day.", True)
    if curLockout[0:3] != "0=>":
        res.activeUsers.remove(userID)
        return await sendMessage(userID, ctx, dungeon.attunefail, True)
    #Now the fun begins
    while cont:
        curLetter = curLockout[int(dungeon.cPoS.ID) + 7]
        possibleMoves = [
            [
                res.Button(label = "🧩", style = 2, disabled=True, id = "interact"),
                res.Button(label = "🔼", style = 2, disabled=True, id = "forward"),
                res.Button(label = "🎁", style = 2, disabled=True, id = "treasure"),
            ],
            [
                res.Button(label = "◀️", style = 2, disabled=True, id = "left"),
                res.Button(label = "🏃", style = 1, id = "flee"),
                res.Button(label = "▶️", style = 2, disabled=True, id = "right"),
            ],
            [
                res.Button(label = "⚔️", style = 2, disabled=True, id = "fight"),
                res.Button(label = "🔽", style = 2, disabled=True, id = "back"),
                res.Button(label = "❓", style = 2, disabled=True, id = "cmode")
            ]
        ]
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
            return await sendMessage(userID, ctx, dungeon.cPoS.name + " \n \n" + msg, True)
        
        def toggleStatus(k, status):
            if str(k) == "forward":
                possibleMoves[0][1].disabled = status
                if not status:
                    possibleMoves[0][1].style = 1
                else:
                    possibleMoves[0][1].style = 4
            elif str(k) == "right":
                possibleMoves[1][2].disabled = status
                if not status:
                    possibleMoves[1][2].style = 1
                else:
                    possibleMoves[1][2].style = 4
            elif str(k) == "left":
                possibleMoves[1][0].disabled = status
                if not status:
                    possibleMoves[1][0].style = 1
                else:
                    possibleMoves[1][0].style = 4
            else:
                possibleMoves[2][1].disabled = status
                if not status:
                    possibleMoves[2][1].style = 1
                else:
                    possibleMoves[2][1].style = 4

        for k in validMoves:
            if dungeon.cPoS.boss:
                if str(k) == "forward":
                    if curLetter != "A":
                        toggleStatus(k, False)
                elif str(k) == "right" or str(k) == 'left':
                    if dungeon.cPoS.boss.type != "boss":
                        toggleStatus(k, False)
                    elif dungeon.cPoS.boss.type == "boss" and curLetter != "A":
                        toggleStatus(k, False)
                else:
                    toggleStatus(str(k), False)
            else:
                toggleStatus(str(k), False)
        
        #Checks for boss
        if dungeon.cPoS.boss and dungeon.cPoS.boss.type != "rare" and curLetter == "A":
            if dungeon.cPoS.boss.cmodecheck and dungeon.cPoS.boss.cmodecheck(User):
                possibleMoves[2][2].disabled = False
                possibleMoves[2][2].label = dungeon.cPoS.boss.cmode
                possibleMoves[2][2].style = 4
            possibleMoves[2][0].disabled = False
            possibleMoves[2][0].style = 4
        elif dungeon.cPoS.boss and dungeon.cPoS.boss.type == "rare" and curLetter == "A" or curLetter == "E" and (curLetter != 'D' or curLetter != 'B' or curLetter != 'F'):
            roll = res.random.randint(0, 100)
            if roll <= int(dungeon.cPoS.boss.chance) or curLetter == "E":
                msg += dungeon.cPoS.boss.suprise
                possibleMoves[2][0].disabled = False
                curLockout = User.updateLockout("E", curLockout, int(dungeon.cPoS.ID))
                curLetter = "E"
            else:
                curLockout = User.updateLockout("D", curLockout, int(dungeon.cPoS.ID))
                if dungeon.cPoS.treasure:
                    possibleMoves[0][2].disabled = False 
                    possibleMoves[0][2].style = 3
                    curLetter = 'F'
                elif dungeon.cPoS.interactable:
                    possibleMoves[0][0].disabled = False
                    possibleMoves[0][0].style = 3
                    curLetter = 'B'
                else:
                    curLetter = "D"
        else:
            #checks for other stuff
            if dungeon.cPoS.treasure and (curLetter != "T" and curLetter != 'F'):
                possibleMoves[0][2].disabled = False 
                possibleMoves[0][2].style = 3
            if dungeon.cPoS.interactable and (curLetter != "I" and curLetter != "B"):
                possibleMoves[0][0].disabled = False
                possibleMoves[0][0].style = 3
                if dungeon.cPoS.interactable.restriction:
                    for i in dungeon.cPoS.interactable.restriction:
                        toggleStatus(str(i), True)
        userReaction = await addComponentsAndWaitFor(userID, ctx, dungeon.cPoS.name + " \n \n" + msg, 120, whom = userID, comps=possibleMoves)
        if not userReaction[userID] or userReaction[userID] == "flee":
            cont = False
        elif userReaction[userID] == "fight" or userReaction[userID] == "cmode":
            Mob = copy.deepcopy(dungeon.cPoS.boss)
            if userReaction[userID] == "cmode":
                Mob.health = round(int(Mob.health) * 1.10)
                temp = Mob.damage.split("-")
                Mob.damage = [round(int(temp[0])) * 1.10, round(int(temp[1])) * 1.10]
            else:
                temp = Mob.damage.split("-")
                Mob.damage = [round(int(temp[0])), round(int(temp[1]))]
            Mob.health = int(Mob.health)
            Mob.maxHealth = Mob.health
            Mob.name = "%BOSS " + Mob.name + ") "
            success, _ = await combat(userID, ctx, Mob)
            User = fetchUser(userID, False)
            if not success and int(User.Health) <= 1:
                cont = False
                User.updateSelf("health",1)
                res.activeUsers.remove(userID)
                if userReaction[userID] == "cmode":
                    return await sendMessage(userID, ctx, dungeon.cPoS.boss.cmkill, True)
                else:
                    return await sendMessage(userID, ctx, dungeon.cPoS.boss.killquote, True)
            elif success:
                User.updateSelf("health",User.Health)
                expCalc = round((res.math.sqrt(int(dungeon.cPoS.boss.level)) * 8) * ((.5 * int(dungeon.cPoS.boss.level)) + 1))
                expGained = User.modifyExp(expCalc, expCalc)
                goldGained = User.modifyGold(int(dungeon.cPoS.boss.level), int(dungeon.cPoS.boss.level) * 2)
                cmodeloot = True if userReaction[userID] == "cmode" else False
                lootallowed = dungeon.cPoS.boss.cmlootamount if userReaction[userID] == "cmode" else dungeon.cPoS.boss.lootamount
                itemsDropped = dungeon.cPoS.boss.rollLoot(cmodeloot, User.Class, lootallowed)
                itemsLooted = []
                itemsGained = []
                itemmsg = ""
                for i in itemsDropped:
                    itemLooted = itm.Item.returnItem(None, str(i))
                    itemsLooted.append(itemLooted)
                    itemGained = itemLooted.ItemStringWithNewGlobalID()
                    itemsGained.append(itemGained)
                    User.addToInventory(itemGained)
                    itemmsg += " \nYou recieved item: " + itemLooted.returnFullItemName()
                if userReaction[userID] == "cmode" and dungeon.cPoS.boss.hardmodecheck(User):
                    curLockout = User.updateLockout("S", curLockout, int(dungeon.cPoS.ID))
                elif userReaction[userID] == "cmode" and not dungeon.cPoS.boss.hardmodecheck(User):
                    curLockout = User.updateLockout("C", curLockout, int(dungeon.cPoS.ID))
                elif not userReaction[userID] == "cmode" and dungeon.cPoS.boss.hardmodecheck(User):
                    curLockout = User.updateLockout("H", curLockout, int(dungeon.cPoS.ID))
                else:
                    curLockout = User.updateLockout("X", curLockout, int(dungeon.cPoS.ID))
                msg = " \n \nYou gained " + str(goldGained) + " gold and " + str(expGained) + " exp." + itemmsg + User.checkLevelUp(True)
                if userReaction[userID] == "cmode":
                    await sendMessage(userID, ctx, dungeon.cPoS.boss.cmdie + msg, True)
                else:
                    await sendMessage(userID, ctx, dungeon.cPoS.boss.diequote + msg, True)
            else:
                cont = False
                break
        elif userReaction[userID] == "interact":
            if dungeon.cPoS.interactable.req(User):
                if not dungeon.cPoS.boss:
                    curLockout = User.updateLockout("I", curLockout, int(dungeon.cPoS.ID))
                else:
                    curLockout = User.updateLockout("B", curLockout, int(dungeon.cPoS.ID))
                await sendMessage(userID, ctx, dungeon.cPoS.interactable.success, True)
            else:
                await sendMessage(userID, ctx, dungeon.cPoS.interactable.failure, True)
        elif userReaction[userID] == "treasure":
            if dungeon.cPoS.treasure.req(User):
                if not dungeon.cPoS.boss:
                    curLockout = User.updateLockout("T", curLockout, int(dungeon.cPoS.ID))
                else:
                    curLockout = User.updateLockout("F", curLockout, int(dungeon.cPoS.ID))
                itemsDropped = dungeon.cPoS.treasure.rollLoot(User.Class, dungeon.cPoS.treasure.lootamount)
                itemsLooted = []
                itemsGained = []
                itemmsg = ""
                for i in itemsDropped:
                    itemLooted = itm.Item.returnItem(None, str(i))
                    itemsLooted.append(itemLooted)
                    itemGained = itemLooted.ItemStringWithNewGlobalID()
                    itemsGained.append(itemGained)
                    User.addToInventory(itemGained)
                    itemmsg += " \nYou recieved item: " + itemLooted.returnFullItemName()
                await sendMessage(userID, ctx, dungeon.cPoS.treasure.success + itemmsg, True)
            else:
                await sendMessage(userID, ctx, dungeon.cPoS.treasure.failure, True)   
        else:
            dungeon.move(userReaction[userID])
    dungeon.cPoS = dungeon.rooms[0]
    res.activeUsers.remove(userID)
    return await sendMessage(userID, ctx, "After contemplating for awhile, you choose to flee and live another day.", True)

def toggleUser(userID):
    User = fetchUser(userID, False)
    User.toggleRun(userID)  