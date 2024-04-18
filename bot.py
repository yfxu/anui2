import os
import random

import hikari
import lightbulb

from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PERMISSIONS = 414464657472
ALLOWED_GUILDS = (
    int(os.getenv("ALLOWED_SERVER_1")),
    int(os.getenv("ALLOWED_SERVER_2")),    
)

bot = lightbulb.BotApp(
    token=DISCORD_TOKEN,
    default_enabled_guilds=ALLOWED_GUILDS,
)

@bot.command
@lightbulb.command("snek", "Sneks a user")
@lightbulb.implements(lightbulb.UserCommand)
async def snek(ctx: lightbulb.UserContext) -> None:
    """Sneks a user"""
    target_id = ctx.options.target.id
    author_id = ctx.author.id
    emoji = random.choice([
        ":nose",
        ":golbin:",
        ":snake:",
        ":sparkles:",
        ":yarn:",
    ])
    embed = hikari.Embed(description=f"{emoji} <@{author_id}> sneks <@{target_id}>! {emoji}")
    await ctx.respond(embed=embed)

@bot.command
@lightbulb.command("party", "throw a party!")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    """Ping the bot"""
    await ctx.respond("Why hello there")

bot.run()
