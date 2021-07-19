import discord
from discord.ext.commands import Bot
from discord_components import DiscordComponents, Button, Select, SelectOption
from decouple import config
TOKEN = config("TOKEN")
from discord.ext.commands import Bot

from discord_components import DiscordComponents, Button, Select, SelectOption, ActionRow



bot = Bot(command_prefix = "")





@bot.event

async def on_ready():

    DiscordComponents(bot)
    print (DiscordComponents)

    print(f"Logged in as {bot.user}!")

orc = discord.File("orc.png")
opts = []
i = 0
while i < 24:
    opts.append(SelectOption(label=i, value=i))
    i+=1
@bot.command()
async def dungeon(ctx):
    await ctx.send(
        file = orc,
        components = [
            [
                Button(label = "🧩", style = 3, disabled=True, id = "interactable"),
                Button(label = "🔼", style = 1),
                Button(label = "🎁", style = 3, disabled=True, id = "treasure")
            ],
            [
                Button(label = "◀️", style = 1,),
                Button(label = "🏃", style = 2, id = "flee"),
                Button(label = "▶️", style = 1,)
            ],
            [
                Button(label = "⚔", style = 4, disabled=True, id = "fight"),
                Button(label = "🔽", style = 1),
                Button(label = "👊", style = 4, disabled=True, id = "cmode")
            ]
        ]

    )



    interaction = await bot.wait_for("button_click", check = lambda i: i.component.label.startswith("WOW"))

    await interaction.respond(content = "Button clicked!")

@bot.command()
async def combat(ctx):
    await ctx.send(
        file = orc,
        components = [
            [
                Select(options = opts, placeholder='Skills')
            ],
            [
                Select(options = opts, placeholder='Spells')
            ],
            [
                Select(options = opts, placeholder='Items')
            ],
            [
                Button(label = "Attack", style = 4, id = "fight"),
                Button(label = "Flee", style = 1, id = "flee"),
            ]
        ]

    )




@bot.command()

async def select(ctx):

    await ctx.send(

        "Hello, World!",

        components = [

            Select(placeholder="select something!", options=[SelectOption(label="a", value="A"), SelectOption(label="b", value="B")])

        ]

    )



    interaction = await bot.wait_for("select_option", check = lambda i: i.component[0].value == "A")

    await interaction.respond(content = f"{interaction.component[0].label} selected!")





bot.run(TOKEN)
