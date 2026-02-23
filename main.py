import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

bot.run(os.environ["MTQ3NTU5MjYzNjEwNTQ5MDU1Mg.Gim3Xt.WO2x4-B5HzSJvDk5m_t5zwiELxFa0xkJYA4bSw"])
