# Work with Python 3.6
import Resources.disccomm as pyd
import traceback

@pyd.res.client.event
async def on_message(message):
    authortoken = str(message.author.id)
    if message.author == pyd.res.client.user:
        return
    elif message.content.lower().startswith('mega help'):
        await message.author.send("https://mega-frontend.herokuapp.com")
        await pyd.sendMessage(authortoken, message, "Head over to my website to see a full list of my commands!", False)
    elif message.content.lower().startswith('mega create'):
        try:
            await pyd.createCharacter(authortoken, message)
        except Exception as e:
            print(e)
            pyd.res.activeUsers.remove(authortoken)
    elif message.content.lower().startswith('mega delete'):
        try:
            await pyd.deleteCharacter(authortoken, message)
        except Exception as e:
            print(e)
            pyd.res.activeUsers.remove(authortoken)
    elif message.content.lower().startswith('mega hero'):
        await pyd.showCharacter(authortoken, message)
    elif message.content.lower().startswith('mega equip'):
        try:
            await pyd.equip(authortoken, message)
        except Exception as e:
            print(e)
            pyd.res.activeUsers.remove(authortoken)
    elif message.content.lower().startswith('mega unequip'):
        try:
            await pyd.unequip(authortoken, message)
        except Exception as e:
            print(e)
            pyd.res.activeUsers.remove(authortoken)
    elif message.content.lower().startswith('mega sell'):
        try:
            await pyd.sell(authortoken, message)
        except Exception as e:
            print(e)
            pyd.res.activeUsers.remove(authortoken)
    elif message.content.lower().startswith('mega use'):
        try:
            await pyd.use(authortoken, message)
        except Exception as e:
            traceback.print_exc()
            print(e)
            pyd.res.activeUsers.remove(authortoken)
    elif message.content.lower().startswith('mega inspect'):
        try:
            await pyd.inspect(authortoken, message)
        except Exception as e:
            traceback.print_exc()
            print(e)
            pyd.res.activeUsers.remove(authortoken)
    elif message.content.lower().startswith('mega shop'):
        try:
            await pyd.shop(authortoken, message)
        except Exception as e:
            traceback.print_exc()
            print(e)
            pyd.res.activeUsers.remove(authortoken)
    elif message.content.lower().startswith('mega train'):
        try:
            await pyd.train(authortoken, message)
        except Exception as e:
            print(e)
            pyd.res.activeUsers.remove(authortoken)
    elif message.content.lower().startswith('mega item'):
        await pyd.queryItem(authortoken, message)
    elif message.content.lower().startswith('mega gather'):
        await pyd.getResources(authortoken, message)
    elif message.content.lower().startswith('mega resources'):
        await pyd.showResources(authortoken, message)
    elif message.content.lower().startswith('mega craft'):
        await pyd.craftItem(authortoken, message)
    elif message.content.lower().startswith('mega inventory'):
        await pyd.showInventory(authortoken, message)
    elif message.content.lower().startswith('mega full inventory'):
        await pyd.showFullInventory(authortoken, message)
    
    #God have mercy on my soul
    elif message.content.lower().startswith('mega run'):
        try:
            await pyd.runDungeon(authortoken, message)
        except Exception as e:
            traceback.print_exc()
            print(e)
            pyd.res.activeUsers.remove(authortoken)
    
    
    elif message.content.lower().startswith('reset'):
        pyd.res.activeUsers.remove(authortoken)
    elif message.content.lower().startswith('stop'):
        await pyd.res.client.logout()

@pyd.res.client.event
async def on_ready():
    print('Succesfull bootup')
    game = pyd.res.discord.Activity(type = pyd.res.discord.ActivityType.listening, name = "Mega Help")
    await pyd.res.client.change_presence(status=pyd.res.discord.Status.online, activity=game)
pyd.res.client.run(pyd.con.TOKEN)