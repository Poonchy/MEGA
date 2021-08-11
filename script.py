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
    embed = pyd.res.discord.Embed(title="Head over to my website to see a full list of my commands!", description="https://megapy.netlify.com/commands") #,color=Hex code
    await ctx.send(embed=embed)

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

@pyd.res.bot.command()
async def report(ctx):
    authortoken = str(ctx.author.id)
    await pyd.report(authortoken, ctx)

@pyd.res.bot.command()
async def duel(ctx):
    authortoken = str(ctx.author.id)
    await pyd.duel(authortoken, ctx)

@pyd.res.bot.command()
async def roll(ctx):
    authortoken = str(ctx.author.id)
    await pyd.roll(authortoken, ctx)

@pyd.res.bot.command()
async def trade(ctx):
    authortoken = str(ctx.author.id)
    await pyd.trade(authortoken, ctx)


@pyd.res.bot.event
async def on_ready():
    pyd.res.DiscordComponents(pyd.res.bot)
    print(f"Logged in as {pyd.res.bot.user}!")


@pyd.res.bot.listen()
async def on_message(ctx):
    if ctx.author.id == 207665962915332099 and isinstance(ctx.channel, pyd.res.discord.channel.DMChannel):
        split = ctx.content.split(" ")
        recipID = split[0]
        msg = " ".join(split[1:])
        recip = await pyd.res.bot.fetch_user(recipID)
        await recip.send(msg)
        await ctx.add_reaction(emoji="👍")
    elif isinstance(ctx.channel, pyd.res.discord.channel.DMChannel) and ctx.author.id != pyd.res.bot.user.id:
        owner = await pyd.res.bot.fetch_user(207665962915332099)
        await owner.send(ctx.author.name + " - " + str(ctx.author.id) + " - " + ctx.content)
        await ctx.add_reaction(emoji="👍")
        

pyd.res.bot.run(pyd.con.TOKEN)