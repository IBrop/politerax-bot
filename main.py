import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    activity = discord.Game(name="Politerax | Minecraft 🌍")
    await bot.change_presence(
        status=discord.Status.online,
        activity=activity
    )
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

bot.run(os.environ["TOKEN"])
