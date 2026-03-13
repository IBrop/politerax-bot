import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio

# ===== INTENTS =====
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ===== ON READY =====
@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")

    await bot.change_presence(status=discord.Status.online)

    synced = await tree.sync()
    print(f"Synced {len(synced)} commands")

    bot.loop.create_task(update_voice_channel())


# ===== SLASH /stat =====
@tree.command(name="stat", description="Статистика сервера")
async def stat(interaction: discord.Interaction):
    guild = interaction.guild

    embed = discord.Embed(
        title="🌍 PoliteraX Статистика",
        color=0x2ecc71
    )

    embed.add_field(name="👥 Участников", value=guild.member_count)
    embed.add_field(name="🚀 Бустов", value=guild.premium_subscription_count)
    embed.add_field(name="📅 Создан", value=guild.created_at.strftime("%d.%m.%Y"))

    embed.set_footer(text="PoliteraX • Политический Minecraft сервер")

    await interaction.response.send_message(embed=embed)


# ===== ПРИВЕТСТВИЕ =====
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"👋 Добро пожаловать, {member.mention}!")


# ===== ПРОЩАНИЕ =====
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"😢 {member.name} покинул сервер...")


# ===== БУСТ =====
@bot.event
async def on_member_update(before, after):
    if not before.premium_since and after.premium_since:
        channel = discord.utils.get(after.guild.text_channels, name="general")
        if channel:
            await channel.send(f"🚀 {after.mention} забустил сервер! Спасибо!")


# ===== ОБНОВЛЕНИЕ ГОЛОСОВОГО КАНАЛА =====
async def update_voice_channel():
    await bot.wait_until_ready()

    while not bot.is_closed():
        for guild in bot.guilds:
            for channel in guild.voice_channels:
                if "Онлайн:" in channel.name:
                    await channel.edit(name=f"🟢 Онлайн: {guild.member_count}")
        await asyncio.sleep(60)


# ===== ЗАПУСК =====
bot.run(os.getenv("TOKEN"))
