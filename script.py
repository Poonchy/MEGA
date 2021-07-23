# Work with Python 3.6
import Resources.disccomm as pyd
import traceback


@pyd.res.bot.command()
async def hero(ctx):
    authortoken = str(ctx.author.id)
    await pyd.showCharacter(authortoken, ctx)

@pyd.res.bot.command()
async def help(ctx):
    authortoken = str(ctx.author.id)
    await ctx.message.author.send("https://megapy.netlify.com")
    await pyd.sendMessage(authortoken, ctx, "Head over to my website to see a full list of my commands!", False)

@pyd.res.bot.command()
async def create(ctx):
    authortoken = str(ctx.author.id)
    await pyd.createCharacter(authortoken, ctx)

@pyd.res.bot.command()
async def delete(ctx):
    authortoken = str(ctx.author.id)
    await pyd.deleteCharacter(authortoken, ctx)


@pyd.res.bot.command()
async def equip(ctx):
    authortoken = str(ctx.author.id)
    await pyd.equip(authortoken, ctx)

@pyd.res.bot.command()
async def unequip(ctx):
    authortoken = str(ctx.author.id)
    await pyd.unequip(authortoken, ctx)

@pyd.res.bot.command()
async def use(ctx):
    authortoken = str(ctx.author.id)
    await pyd.use(authortoken, ctx)

@pyd.res.bot.command()
async def sell(ctx):
    authortoken = str(ctx.author.id)
    await pyd.sell(authortoken, ctx)

@pyd.res.bot.command()
async def inspect(ctx):
    authortoken = str(ctx.author.id)
    await pyd.inspect(authortoken, ctx)

@pyd.res.bot.command()
async def shop(ctx):
    authortoken = str(ctx.author.id)
    await pyd.shop(authortoken, ctx)

@pyd.res.bot.command()
async def train(ctx):
    authortoken = str(ctx.author.id)
    await pyd.train(authortoken, ctx)

@pyd.res.bot.command()
async def item(ctx):
    print (ctx)
    authortoken = str(ctx.author.id)
    await pyd.queryItem(authortoken, ctx)

@pyd.res.bot.command()
async def gather(ctx):
    authortoken = str(ctx.author.id)
    await pyd.getResources(authortoken, ctx)

@pyd.res.bot.command()
async def craft(ctx):
    authortoken = str(ctx.author.id)
    await pyd.craftItem(authortoken, ctx)

@pyd.res.bot.command()
async def resources(ctx):
    authortoken = str(ctx.author.id)
    await pyd.showResources(authortoken, ctx)

@pyd.res.bot.command()
async def inventory(ctx):
    authortoken = str(ctx.author.id)
    await pyd.showInventory(authortoken, ctx)

@pyd.res.bot.command()
async def full(ctx, inventory = None):
    if inventory != "inventory":
        return
    authortoken = str(ctx.author.id)
    await pyd.showFullInventory(authortoken, ctx)

@pyd.res.bot.command()
async def run(ctx):
    authortoken = str(ctx.author.id)
    await pyd.runDungeon(authortoken, ctx)

@pyd.res.bot.event
async def on_ready():
    pyd.res.DiscordComponents(pyd.res.bot)
    print(f"Logged in as {pyd.res.bot.user}!")

pyd.res.bot.run(pyd.con.TOKEN)