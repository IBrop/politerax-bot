import discord
from discord.ext import commands
from mcstatus import JavaServer
import asyncio

bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())

SERVER_IP = "pepla4.minerent.io"
SERVER_PORT = 31012


def get_status_emoji(status):
    if status == "online":
        return "🟢 Онлайн"
    elif status == "restart":
        return "🟡 Рестарт"
    else:
        return "🔴 Оффлайн"


@bot.command()
async def stat(ctx):
    try:
        server = JavaServer.lookup(f"{SERVER_IP}:{SERVER_PORT}")

        status = server.status()

        state = "online"
        status_text = get_status_emoji(state)

        embed = discord.Embed(
            title="📊 Статус сервера",
            color=0x00ff00
        )

        embed.add_field(name="Статус", value=status_text, inline=False)
        embed.add_field(
            name="Игроки",
            value=f"{status.players.online}/{status.players.max}"
        )
        embed.add_field(
            name="Пинг",
            value=f"{round(status.latency)} ms"
        )
        embed.add_field(
            name="Версия",
            value=status.version.name
        )

        await ctx.send(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title="📊 Статус сервера",
            color=0xff0000
        )

        embed.add_field(
            name="Статус",
            value=get_status_emoji("offline"),
            inline=False
        )
        embed.add_field(
            name="Инфо",
            value="Сервер не отвечает или перезапускается",
            inline=False
        )

        await ctx.send(embed=embed)


bot.run(os.getenv("TOKEN"))
