import os
import random
import time

import hikari
import lightbulb

import psycopg2

from dotenv import load_dotenv

SECRETS_FILE = os.getenv("DISCORD_SECRETS_FILE") or ".env"
load_dotenv(SECRETS_FILE)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_ALLOWED_GUILDS = [int(guild_id) for guild_id in os.getenv("ALLOWED_SERVERS").split(",")]

while True:
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="postgres",
            host="db",
            port="5432",
            database="postgres"
        )
    except:
        time.sleep(1)
        continue
    break


bot = lightbulb.BotApp(
    token=DISCORD_TOKEN,
    default_enabled_guilds=DISCORD_ALLOWED_GUILDS,
)

@bot.command
@lightbulb.command("snek", "Sneks a user")
@lightbulb.implements(lightbulb.UserCommand)
async def snek(ctx: lightbulb.UserContext) -> None:
    """Sneks a user"""
    target_id = ctx.options.target.id
    author_id = ctx.author.id
    emoji = random.choice([
        ":goblin:",
        ":nose:",
        ":snake:",
        ":sparkles:",
        ":two_hearts:",
        ":yarn:",
    ])

    cur = conn.cursor()
    cur.execute("INSERT INTO sneks(user_id_snekker, user_id_snekked) VALUES (%s, %s)", (author_id, target_id))
    conn.commit()

    embed = hikari.Embed(description=f"{emoji} <@{author_id}> sneks <@{target_id}>! {emoji}")
    await ctx.respond(embed=embed)

@bot.command
@lightbulb.option("snekker", "The user who sneks", type=hikari.Member)
@lightbulb.option("snekked", "The user who is snekked", type=hikari.Member)
@lightbulb.command("snek-counter", "Check how many times a user has snekked another user")
@lightbulb.implements(lightbulb.SlashCommand)
async def snek_counter(ctx: lightbulb.SlashContext) -> None:
    """Check how many times a user has snekked another user"""
    user_snekker: hikari.Member = ctx.options.snekker
    user_snekked: hikari.Member = ctx.options.snekked
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sneks WHERE user_id_snekker = %s AND user_id_snekked = %s", (user_snekker.id, user_snekked.id))
    count = cur.fetchall()[0][0]
    await ctx.respond(f"<@{user_snekker.id}> has snekked <@{user_snekked.id}> {count} times!")
    

@bot.command
@lightbulb.command("party", "throw a party!")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    """Ping the bot"""
    await ctx.respond("Why hello there")

bot.run()
