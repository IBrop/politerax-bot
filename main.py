import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name="PoliteraX",
        details="🌍 Военно-политический сервер с модами",
        state="mc.politerax.ru | 1.20.1"
    )

    await bot.change_presence(
        status=discord.Status.online,
        activity=activity
    )

    print(f"Bot is online as {bot.user}")

bot.run(os.getenv("TOKEN"))
