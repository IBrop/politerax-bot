import discord
from discord.ext import commands
from mcstatus import JavaServer
import asyncio
import os
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

SERVER_IP = "pepla4.minerent.io"
SERVER_PORT = 31012

@bot.event
async def on_ready():
    print("БОТ ЗАПУЩЕН")

def get_status_data(state):
    if state == "online":
        return "🟢 Онлайн", 0x00ff00
    elif state == "restart":
        return "🟡 Рестарт", 0xffcc00
    else:
        return "🔴 Оффлайн", 0xff0000


@bot.command()
async def stat(ctx):
    server = JavaServer.lookup(f"{SERVER_IP}:{SERVER_PORT}")

    try:
        status = server.status()
        state = "online"

    except:
        # пробуем ещё раз → возможно рестарт
        await asyncio.sleep(2)
        try:
            status = server.status()
            state = "restart"
        except:
            state = "offline"
            status = None

    status_text, color = get_status_data(state)

    embed = discord.Embed(
        title="📊 LA4 • Статус сервера",
        color=color
    )

    embed.add_field(name="Статус", value=status_text, inline=False)

    if status:
        embed.add_field(
            name="Игроки",
            value=f"{status.players.online}/{status.players.max}",
            inline=True
        )

        embed.add_field(
            name="Пинг",
            value=f"{round(status.latency)} ms",
            inline=True
        )

        embed.add_field(
            name="Версия",
            value=status.version.name,
            inline=True
        )

        # список игроков (если есть)
        if status.players.sample:
            players = ", ".join([p.name for p in status.players.sample])
            embed.add_field(
                name="Онлайн игроки",
                value=players[:1000],
                inline=False
            )

    else:
        embed.add_field(
            name="Инфо",
            value="Сервер не отвечает или перезапускается",
            inline=False
        )

    # время обновления
    embed.set_footer(text=f"Обновлено: {datetime.now().strftime('%H:%M:%S')}")

    await ctx.send(embed=embed)


TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("❌ TOKEN НЕ НАЙДЕН")
